"""
Inyeccion de una direccion en el residual stream. El test CAUSAL.

Es el trasplante que ANALISIS_CAPAS.md seccion 11 dejo pendiente desde el
principio (y P5 de HALLAZGOS.md seccion 9), ahora con una descomposicion
concreta que inyectar en vez de un barrido a ciegas.

---------------------------------------------------------------------------
QUE PREGUNTA CONTESTA
---------------------------------------------------------------------------
La serie de activaciones establecio que cos(delta, d_frq) NO es la variable
causal: ocho parches reproducen d_frq al 94-100% del techo de ruido y ninguno
pasa del 60% de frances, mientras que v_CE esta al 81% y llega al 90%.

Descomponiendo el delta de v_CE respecto de d_frq (capa 16, ||d|| = 7.29):

    parche        paralelo   ortogonal
    v_CE              5.48        8.12
    act_l16           5.26        3.64
    band 12-16        5.83        3.65

Los componentes PARALELOS son casi identicos. Lo unico que distingue a v_CE es
el ortogonal, mas del doble. Y la loss de MSE, escrita como

    rel = (par - 1)^2 + ort^2

tiene un segundo termino cuyo minimo es ||delta_ort|| = 0: esta suprimiendo por
diseno exactamente eso.

Este script inyecta cada componente por separado y mide si produce frances.

    solo delta_ort  produce frances  -> el ingrediente causal vive FUERA de
                                        d_frq, y el marco de diferencia de
                                        medias mide el subespacio equivocado
    solo delta_par  produce frances  -> el problema es de magnitud a lo largo
                                        de d, y el barrido de escala alcanza
    ninguno, y las dos juntas si     -> hace falta la combinacion; ninguna
                                        direccion lineal sola explica el efecto

---------------------------------------------------------------------------
EL CONTROL DE NORMA NO ES OPCIONAL
---------------------------------------------------------------------------
||delta_ort|| = 8.12 es MAS GRANDE que ||delta_par|| = 5.48. Sin una condicion
aleatoria de norma igualada, un resultado positivo para el ortogonal se
confunde con "empujar fuerte en cualquier direccion". Es el mismo rol que
make_random_patch.py cumple en el espacio de embeddings.

---------------------------------------------------------------------------
DOS DECISIONES DE DISENO QUE CAMBIAN EL RESULTADO
---------------------------------------------------------------------------
--positions   donde sumar el vector dentro de la secuencia.
              `last` solo en la ultima posicion del prompt, que es donde se
              midio todo y donde se decide el primer token.
              `all` en todas, que es la convencion de ActAdd.

--during      `prompt` solo en el forward del prompt; `all` tambien en cada
              paso de generacion.
              El idioma se decide en el primer token, pero si el efecto no
              persiste la respuesta puede volver al ingles a mitad de camino.
              Con `prompt` se mide "fijar el estado inicial alcanza?"; con
              `all`, "sostener el estado alcanza?". Son preguntas distintas y
              las dos importan: el hallazgo de HALLAZGOS.md seccion 5.4 es que
              el parche de embeddings FIJA UN MODO que sobrevive 100 tokens.

Default `all`/`all`, con las otras como control.

---------------------------------------------------------------------------
    # las cinco condiciones sobre el delta de v_CE en la capa 16
    python3 -u inject_direction.py --model $M --layer 16 \\
        --deltas runs/v4_250/profile_deltas.pt --split par,ort,total,random,d \\
        --out_dir runs/inject_v4_l16
"""

import argparse
import json
import os

import pandas as pd
import torch
import tqdm

from checkers import answer_correct, french_score, is_french, language_verdict, truncate_at_role_leak
from lm import (DEFAULT_MODEL, build_suffix_manager, get_embedding_matrix,
                get_embeddings, load_model_and_tokenizer, stop_token_ids)

SPLITS = ("total", "par", "ort", "random", "d", "none")


def descomponer(mean_delta, d, seed=0):
    """
    delta = delta_par + delta_ort, proyeccion ortogonal sobre d.

    `random` iguala la norma de delta_ort, que es el control que hace falta
    porque delta_ort es el vector mas largo de los tres.
    `d` es la direccion media cruda, en su norma natural.
    `none` es el vector cero: control de que el hook no hace nada por si mismo.
    """
    dn2 = (d * d).sum()
    par_coef = (mean_delta * d).sum() / dn2
    par = par_coef * d
    ort = mean_delta - par
    g = torch.Generator(device="cpu").manual_seed(seed)
    r = torch.randn(d.shape, generator=g).to(d.device)
    rnd = r / r.norm() * ort.norm()

    # Auto-verificacion: si la descomposicion esta mal, todo lo que sigue no
    # significa nada. Barato y se corre una vez.
    orto = (par * ort).sum().abs().item()
    pit = (par.norm() ** 2 + ort.norm() ** 2 - mean_delta.norm() ** 2).abs().item()
    esc = mean_delta.norm().item() ** 2
    assert orto < 1e-3 * esc, f"par y ort no son ortogonales: <par,ort> = {orto:.3e}"
    assert pit < 1e-3 * esc, f"no se cumple Pitagoras: error {pit:.3e}"
    assert abs(rnd.norm().item() - ort.norm().item()) < 1e-4 * ort.norm().item(), \
        "el control aleatorio no tiene la norma de ort"

    return {"total": mean_delta, "par": par, "ort": ort, "random": rnd,
            "d": d.clone(), "none": torch.zeros_like(d)}


class _Inyector:
    """Suma `vec` a la salida del bloque `layer-1` en las posiciones pedidas."""

    def __init__(self, model, layer, vec, positions="all"):
        self.mod = model.model.layers[layer - 1]
        self.vec = vec
        self.positions = positions
        self.h = None
        self.activo = False

    def _hook(self, _m, _i, out):
        if not self.activo:
            return out
        tup = isinstance(out, tuple)
        h = out[0] if tup else out
        v = self.vec.to(h.dtype).to(h.device)
        if self.positions == "last":
            h = h.clone()
            h[:, -1, :] = h[:, -1, :] + v
        else:
            h = h + v
        return (h,) + out[1:] if tup else h

    def __enter__(self):
        self.h = self.mod.register_forward_hook(self._hook)
        return self

    def __exit__(self, *a):
        if self.h is not None:
            self.h.remove()


@torch.no_grad()
def generar_inyectado(model, tokenizer, instruction, device, inyector,
                      num_tokens=100, during="all"):
    """
    Generacion greedy desde embeddings, con la inyeccion activa.

    Espeja lm.generate_one: corta en <|eot_id|> y trunca en la fuga de rol.
    La diferencia es `during`: con "prompt" la inyeccion se apaga despues del
    primer forward, asi que mide si FIJAR el estado inicial alcanza.
    """
    sm = build_suffix_manager(tokenizer, instruction, target="")
    tokens = sm.get_input_ids().to(device)
    embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()
    embeds = embeds[:, : sm._assistant_role_slice.stop, :]

    emb_matrix = get_embedding_matrix(model)
    stop = stop_token_ids(tokenizer)
    out = []
    for paso in range(num_tokens):
        inyector.activo = (during == "all") or (paso == 0)
        logits = model(inputs_embeds=embeds).logits
        tok = torch.argmax(logits[:, -1, :])
        if int(tok) in stop:
            break
        out.append(int(tok))
        embeds = torch.hstack([embeds, emb_matrix[tok][None, None, :]])
    inyector.activo = False
    txt = tokenizer.decode(out, skip_special_tokens=True)
    return truncate_at_role_leak(txt), txt


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--deltas", required=True,
                    help="profile_deltas.pt de train_act_patch.py --profile_only")
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--split", default="total,par,ort,random,d,none",
                    help="condiciones a inyectar, separadas por coma: " + ", ".join(SPLITS))
    ap.add_argument("--scales", default="1.0",
                    help="escalas sobre el vector inyectado, separadas por coma")
    ap.add_argument("--positions", default="all", choices=["last", "all"])
    ap.add_argument("--during", default="all", choices=["prompt", "all"])
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    blob = torch.load(args.deltas, map_location="cpu")
    L = args.layer
    if L not in blob["mean_delta"]:
        raise SystemExit(f"el archivo no tiene la capa {L}")
    md, d = blob["mean_delta"][L].float(), blob["d"][L].float()
    vecs = descomponer(md, d)

    print(f"delta de: {blob['patch']}")
    print(f"capa {L}   ||d|| = {d.norm():.3f}   ||delta medio|| = {md.norm():.3f}")
    print(f"{'condicion':<10}{'norma':>10}{'cos con d':>12}")
    for k in SPLITS:
        v = vecs[k]
        c = torch.nn.functional.cosine_similarity(v, d, dim=0).item() if v.norm() > 0 else float("nan")
        print(f"{k:<10}{v.norm():>10.3f}{c:>12.3f}")

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    n_train = int(len(df) * args.train_test_split)
    heldout = df.iloc[n_train:]
    print(f"\nHeld-out: {len(heldout)}  |  posiciones: {args.positions}  |  durante: {args.during}")

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    conds = [c.strip() for c in args.split.split(",") if c.strip()]
    escalas = [float(a) for a in args.scales.split(",") if a.strip()]
    os.makedirs(args.out_dir, exist_ok=True)

    resumen = []
    for cond in conds:
        if cond not in SPLITS:
            raise SystemExit(f"condicion desconocida: {cond}")
        for a in escalas:
            vec = (vecs[cond] * a).to(args.device)
            iny = _Inyector(model, L, vec, args.positions)
            rows = []
            with iny:
                for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout),
                                      desc=f"{cond} a={a}"):
                    txt, raw = generar_inyectado(model, tokenizer, r["prompt"],
                                                 args.device, iny, args.num_tokens,
                                                 args.during)
                    has = str(r["answer"]).strip() != ""
                    rows.append({
                        "idx": int(i), "prompt": r["prompt"], "answer": r["answer"],
                        "injected": txt,
                        "injected_is_french": bool(is_french(txt)),
                        "injected_french_score": float(french_score(txt)),
                        "injected_lang": language_verdict(txt),
                        "injected_answer_correct": bool(answer_correct(txt, r["answer"], r["aliases"])) if has else None,
                        "identico_al_baseline": txt.strip() == str(r["baseline_en"]).strip(),
                        "role_leak": bool(txt != raw.strip()),
                    })

            def frac(k):
                v = [x[k] for x in rows if x[k] is not None]
                return sum(v) / len(v) if v else float("nan")
            m = {
                "is_french": frac("injected_is_french"),
                "french_score": sum(x["injected_french_score"] for x in rows) / len(rows),
                "answer_correct": frac("injected_answer_correct"),
                "identico_al_baseline": frac("identico_al_baseline"),
                "role_leak": frac("role_leak"),
            }
            cuenta = {}
            for x in rows:
                cuenta[x["injected_lang"]] = cuenta.get(x["injected_lang"], 0) + 1

            rep = {
                "objetivo": "inyeccion causal",
                "deltas": os.path.abspath(args.deltas),
                "patch_origen": blob["patch"], "layer": L,
                "condicion": cond, "escala": a,
                "positions": args.positions, "during": args.during,
                "norma_inyectada": float(vec.norm().item()),
                "cos_con_d": float(torch.nn.functional.cosine_similarity(
                    vec.cpu(), d, dim=0).item()) if vec.norm() > 0 else None,
                "n_heldout": len(rows), "metrics": m, "veredictos": cuenta,
                "rows": rows,
            }
            nom = f"inject_{cond}_a{a}.json"
            with open(os.path.join(args.out_dir, nom), "w", encoding="utf-8") as f:
                json.dump(rep, f, indent=2, ensure_ascii=False)
            resumen.append({"cond": cond, "a": a, "norma": vec.norm().item(),
                            **m, "veredictos": cuenta})
            print(f"  -> {nom}   is_french={m['is_french']:.2f}  "
                  f"acc={m['answer_correct']:.2f}  inerte={m['identico_al_baseline']:.2f}")

    print("\n" + "=" * 84)
    print(f"CAPA {L}  ·  posiciones={args.positions}  ·  durante={args.during}")
    print(f"{'condicion':<10}{'escala':>8}{'norma':>9}{'is_french':>11}{'accuracy':>10}"
          f"{'inerte':>9}   veredictos")
    for r in resumen:
        print(f"{r['cond']:<10}{r['a']:>8.2f}{r['norma']:>9.2f}{r['is_french']:>11.2f}"
              f"{r['answer_correct']:>10.2f}{r['identico_al_baseline']:>9.2f}   {r['veredictos']}")
    with open(os.path.join(args.out_dir, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"layer": L, "positions": args.positions, "during": args.during,
                   "resumen": resumen}, f, indent=2, ensure_ascii=False)
    print(f"\nGuardado en {args.out_dir}/")
    print("\nLectura: si 'ort' produce frances y 'par' no, el ingrediente causal vive")
    print("fuera de d_frq. 'random' tiene la MISMA norma que 'ort' -- si tambien")
    print("produce frances, lo que importa es empujar fuerte, no la direccion.")


if __name__ == "__main__":
    main()
