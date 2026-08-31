"""
Vectores de diferencia de medias, metodo de Ball, Kreuter & Panickssery
(arXiv:2406.09289, EACL 2026), aplicado al parche de idioma.

    v^l = (1/|D|) * SUM_i  delta a_i^l

Diferencia de medias en el residual stream, en el ULTIMO TOKEN DE LA
INSTRUCCION, sobre un dataset de pares contrastivos. Despues coseno entre los
vectores medios. En el paper la capa es la del medio (16 para modelos de 7B,
20 para 13B/14B, o sea L/2); Llama-3.2-3B tiene 28 capas, asi que la del medio
es la 14. Aca se computan todas y se imprimen de --from_layer en adelante.

Tres condiciones, todas contra la MISMA linea de base (pregunta en ingles):

    d_patch = mean( h(q + v)            - h(q) )
    d_frq   = mean( h(q_fr)             - h(q) )
    d_instr = mean( h("Answer this in French. " + q) - h(q) )

y los tres cosenos entre ellos.

Escala de referencia del paper: entre tipos de jailbreak distintos que ellos
concluyeron que comparten mecanismo, el coseno cae entre 0.4 y 0.6. No esperar
0.9.

TECHO DE RUIDO: con 40 muestras en 3072 dimensiones la direccion media es
ruidosa, y el coseno entre dos medias ruidosas esta sesgado hacia abajo. Se
estima por split-half: se parte el dataset en dos mitades, se calcula el vector
en cada una y se saca el coseno de una condicion CONTRA SI MISMA. Ese es el
maximo observable. Sin el, un coseno bajo no se puede interpretar.
"""

import argparse
import json

import numpy as np
import pandas as pd
import torch
import tqdm

from layer_analysis import hidden_at_last
from lm import DEFAULT_MODEL, load_model_and_tokenizer

INSTRUCTION = "Answer this in French."

# Controles. Sin estos no se puede saber si un coseno de 0.78 significa
# "frances" o simplemente "el modelo responde distinto del baseline ingles".
# Las tres condiciones originales comparten ese componente trivial.
#   aleman  -> otro idioma. Si da lo mismo que el frances, el numero no mide idioma.
#   corto   -> cambio de modo SIN cambio de idioma. Es el piso generico.
CONTROLES = {
    "de": "Answer this in German.",
    "corto": "Answer this in one short sentence.",
}


def cos(a, b):
    """Coseno por capa entre dos matrices [L+1, d]."""
    return torch.nn.functional.cosine_similarity(a, b, dim=1).numpy()


def split_half_ceiling(deltas, n_splits=10, seed=0):
    """
    Techo de ruido: coseno de una condicion contra si misma, por split-half.

    Promedia sobre n_splits particiones aleatorias para que el techo no dependa
    de una particion afortunada.
    """
    rng = np.random.RandomState(seed)
    n = len(deltas)
    vals = []
    for _ in range(n_splits):
        idx = rng.permutation(n)
        a = torch.stack([deltas[i] for i in idx[: n // 2]]).mean(0)
        b = torch.stack([deltas[i] for i in idx[n // 2:]]).mean(0)
        vals.append(cos(a, b))
    return np.stack(vals).mean(0)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--from_layer", type=int, default=15)
    ap.add_argument("--instruction", default=INSTRUCTION)
    ap.add_argument("--no_controls", action="store_true",
                    help="saltear las condiciones de control (aleman, respuesta corta)")
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--scale", type=float, default=1.0,
                    help="escala alfa sobre el parche. El coseno es invariante a escala, "
                         "pero un delta mas grande cambia la relacion senal/ruido y empuja "
                         "mas adentro del estado de idioma: sirve para separar si la "
                         "alineacion depende de la magnitud o del comportamiento.")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out", default="mean_diff_vectors.json")
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    if "prompt_fr" not in df.columns:
        raise SystemExit("falta la columna prompt_fr; corre translate_questions.py")
    # Filtrar PRIMERO y despues tomar n, para que las tres condiciones usen
    # exactamente los mismos prompts.
    usables = df[df.get("prompt_fr_ok", True).astype(str).str.lower() == "true"]
    df = usables.head(args.n)
    print(f"prompts con traduccion usable: {len(usables)}  |  se usan: {len(df)}")
    if len(df) < 10:
        raise SystemExit("muy pocos prompts usables")

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    patch = torch.load(args.patch, map_location=args.device).to(args.device)
    if args.scale != 1.0:
        patch = patch * args.scale
        print(f"escala {args.scale} -> norma {patch.norm(2).item():.3f}")

    ctrl = {} if args.no_controls else CONTROLES
    D = {k: [] for k in ["patch", "frq", "instr"] + list(ctrl)}
    for _, r in tqdm.tqdm(df.iterrows(), total=len(df), desc="activaciones"):
        q = r["prompt"]
        h_en = hidden_at_last(model, tokenizer, q, args.device)
        D["patch"].append((hidden_at_last(model, tokenizer, q, args.device, patch,
                                          args.num_patch_positions) - h_en).cpu())
        D["frq"].append((hidden_at_last(model, tokenizer, r["prompt_fr"],
                                        args.device) - h_en).cpu())
        # Espacio, no salto de linea.
        D["instr"].append((hidden_at_last(model, tokenizer, f"{args.instruction} {q}",
                                          args.device) - h_en).cpu())
        for k, ins in ctrl.items():
            D[k].append((hidden_at_last(model, tokenizer, f"{ins} {q}",
                                        args.device) - h_en).cpu())

    V = {k: torch.stack(v).mean(0) for k, v in D.items()}
    ceil = {k: split_half_ceiling(v) for k, v in D.items()}

    c_pf = cos(V["patch"], V["frq"])
    c_pi = cos(V["patch"], V["instr"])
    c_fi = cos(V["frq"], V["instr"])
    # Correccion por atenuacion: cos / sqrt(techo_a * techo_b).
    # Verificado con datos sinteticos de coseno verdadero conocido:
    #
    #   techo 0.88 -> crudo 0.75 / corr 0.85  (verdadero 0.80)   sirve
    #   techo 0.39 -> crudo 0.46 / corr 1.14  (verdadero 0.80)   sobre-corrige
    #   techo 0.06 -> basura
    #
    # O sea: con techo alto el CRUDO ya es casi correcto y no hace falta
    # corregir; con techo bajo la correccion es peor que no corregir. Por eso
    # solo se muestra cuando los dos techos superan MIN_CEIL.
    MIN_CEIL = 0.5

    def corr(c, a, b, l):
        if min(ceil[a][l], ceil[b][l]) < MIN_CEIL:
            return None
        return c[l] / np.sqrt(ceil[a][l] * ceil[b][l])

    L = len(c_pf)
    lo = max(0, min(args.from_layer, L - 1))
    print(f"\ncapas {lo}..{L - 1}  (la del medio segun el paper seria {(L - 1) // 2})")
    print(f"\n{'capa':>5}{'patch~frq':>11}{'patch~instr':>13}{'frq~instr':>11}"
          f"{'|':>3}{'techo patch':>13}{'techo frq':>11}{'techo instr':>13}"
          f"{'|':>3}{'p~f corr':>10}{'p~i corr':>10}")
    print("-" * 106)
    for l in range(lo, L):
        f1, f2 = corr(c_pf, "patch", "frq", l), corr(c_pi, "patch", "instr", l)
        s1 = f"{f1:.3f}" if f1 is not None else "-"
        s2 = f"{f2:.3f}" if f2 is not None else "-"
        print(f"{l:>5}{c_pf[l]:>11.3f}{c_pi[l]:>13.3f}{c_fi[l]:>11.3f}{'|':>3}"
              f"{ceil['patch'][l]:>13.3f}{ceil['frq'][l]:>11.3f}{ceil['instr'][l]:>13.3f}{'|':>3}"
              f"{s1:>10}{s2:>10}")

    rng = slice(lo, L)
    print(f"\nPromedio de la capa {lo} en adelante:")
    print(f"  patch ~ frq    {c_pf[rng].mean():+.3f}   (techos {ceil['patch'][rng].mean():.3f} / "
          f"{ceil['frq'][rng].mean():.3f})")
    print(f"  patch ~ instr  {c_pi[rng].mean():+.3f}   (techos {ceil['patch'][rng].mean():.3f} / "
          f"{ceil['instr'][rng].mean():.3f})")
    print(f"  frq   ~ instr  {c_fi[rng].mean():+.3f}")
    gana = "PREGUNTA EN FRANCES" if c_pf[rng].mean() > c_pi[rng].mean() else "INSTRUCCION EN TEXTO"
    print(f"\n-> el parche se parece mas a: {gana} "
          f"(diferencia {abs(c_pf[rng].mean() - c_pi[rng].mean()):.3f})")
    if ctrl:
        keys = ["patch", "frq", "instr"] + list(ctrl)
        etiq = {"patch": "parche", "frq": "preg. FR", "instr": "instr. FR",
                "de": "instr. DE", "corto": "resp. corta"}
        print("\n" + "=" * 70)
        print(f"MATRIZ COMPLETA, promedio capas {lo}..{L - 1}")
        print("  de    = instruccion de responder en ALEMAN  (otro idioma)")
        print("  corto = responder en una oracion corta      (cambio de modo, mismo idioma)")
        print()
        print(" " * 13 + "".join(f"{etiq[k]:>13}" for k in keys))
        for a in keys:
            fila = "".join(f"{cos(V[a], V[b])[rng].mean():>13.3f}" for b in keys)
            print(f"{etiq[a]:<13}{fila}")
        print()
        print("Lectura decisiva:")
        pf = cos(V["patch"], V["frq"])[rng].mean()
        pd_ = cos(V["patch"], V["de"])[rng].mean()
        pc = cos(V["patch"], V["corto"])[rng].mean()
        print(f"  parche~preg.FR    {pf:.3f}")
        print(f"  parche~instr.DE   {pd_:.3f}   <- si es parecido, el numero NO mide idioma")
        print(f"  parche~resp.corta {pc:.3f}   <- piso generico de 'responder distinto'")
        margen = pf - max(pd_, pc)
        print(f"\n  margen del frances sobre el mejor control: {margen:+.3f}")
        if margen < 0.05:
            print("  -> el coseno esta dominado por un componente generico de cambio de")
            print("     modo, no por el idioma. La comparacion frances-vs-instruccion")
            print("     no significa nada hasta separar ese componente.")
        else:
            print("  -> hay un componente especifico de idioma por encima del piso.")

    print("\nComo leerlo:")
    print("  - Escala de referencia (Ball et al. 2406.09289): entre jailbreaks que")
    print("    ellos concluyeron que comparten mecanismo, el coseno da 0.4 a 0.6.")
    print("    No esperar 0.9.")
    print(f"  - El TECHO manda. Si esta por encima de ~0.7, el coseno crudo ya es")
    print("    casi correcto y la columna corregida sobra. Si esta por debajo de")
    print(f"    {MIN_CEIL}, la medicion de esa condicion no es confiable y la corregida")
    print("    ni se muestra: con techo bajo corregir es PEOR que no corregir.")
    print("  - Un techo bajo con n=40 significa que esa condicion es inconsistente")
    print("    entre prompts, no que el efecto sea chico. Se arregla subiendo --n.")

    json.dump({"layers_from": lo, "n_prompts": len(df),
               "cos_patch_frq": c_pf.tolist(), "cos_patch_instr": c_pi.tolist(),
               "cos_frq_instr": c_fi.tolist(),
               "ceiling_patch": ceil["patch"].tolist(),
               "ceiling_frq": ceil["frq"].tolist(),
               "ceiling_instr": ceil["instr"].tolist(),
               "instruction": args.instruction, "patch": args.patch,
               "scale": args.scale, "patch_norm": float(patch.norm(2).item()),
               "conditions": list(V),
               "cos_matrix": {a: {b: cos(V[a], V[b]).tolist() for b in V} for a in V},
               "ceilings": {k: v.tolist() for k, v in ceil.items()}},
              open(args.out, "w"), indent=2)
    print(f"\nGuardado en {args.out}")


if __name__ == "__main__":
    main()
