"""
Parche por alineacion de activaciones sobre una BANDA de capas, con pesos
proporcionales al techo de realizabilidad de cada capa.

Variante de `train_act_patch.py`. La loss es la misma familia; lo unico que
cambia es que las capas de la banda no pesan igual:

    L(v) = SUM_{l in B}  w_l * ||delta_i[l] - d[l]||^2 / ||d[l]||^2
           + lambda*||v||^2

    w_l = c_l^p / SUM_{k in B} c_k^p            SUM_l w_l = 1

`c_l` es el MEJOR coseno por prompt que un parche de entrada logro alcanzar en
la capa l, tomado como el maximo sobre las corridas del barrido de una capa.

---------------------------------------------------------------------------
POR QUE PONDERAR, Y POR QUE POR EL COSENO
---------------------------------------------------------------------------
Con una banda ancha las capas no son igual de alcanzables desde el espacio de
entrada. El barrido de una capa lo midio: c_l va de 0.898 en la capa 12 a
~0.735 en la 23.

Como el optimo de magnitud es mag* = cos (ver train_act_patch.py), el termino
de cada capa tiene un piso IRREDUCIBLE:

    rel_l >= 1 - c_l^2

o sea 0.194 en la capa 12 y 0.460 en la 23. En una suma sin pesos las capas
profundas aportan un residuo grande que el parche no puede bajar, y su
gradiente -- que apunta a un target inalcanzable -- compite con el de las capas
que si se pueden resolver. El resultado es un compromiso peor para todas.

Ponderar por c_l^p atenua esa competencia. El exponente NO es arbitrario: la
relacion entre coseno y piso es cuadratica (`piso = 1 - c^2`), asi que p=2
castiga cada capa en proporcion a la varianza que no puede explicar. p=1 es la
version lineal y p=0 recupera el uniforme de train_act_patch.py.

OJO CON EL SIGNO. Existe el esquema opuesto, tambien defendible:

    rel_norm[l] = (rel[l] - piso_l) / (1 - piso_l)      ==  peso proporcional a 1/c_l^2

que pone a todas las capas en "fraccion del progreso alcanzable" y AMPLIFICA
las dificiles. Responde otra pregunta ("que todas avancen parejo") y no es la
que implementa este script ("que las dificiles no distorsionen").

---------------------------------------------------------------------------
LA NORMALIZACION A SUMA 1 NO ES COSMETICA
---------------------------------------------------------------------------
Como rel_i[l] = 1 para toda capa cuando delta = 0, con SUM w_l = 1 la loss
sigue arrancando en exactamente 1.000 y 0.0 sigue siendo reproduccion perfecta.
Esa escala es lo que hace legible el log. Con pesos que no suman 1 se pierde.

Se reportan DOS numeros por epoch:

    band_w    la loss ponderada, que es lo que se optimiza
    band_u    la media sin pesos sobre la misma banda

`band_u` es lo unico comparable con las corridas de una capa de
train_act_patch.py, que son uniformes por construccion.

---------------------------------------------------------------------------
DE DONDE SALEN LOS c_l, Y UN CAVEAT
---------------------------------------------------------------------------
`--layer_weights auto` los lee de los act_metadata.json del barrido y toma el
maximo por capa sobre las corridas disponibles. El maximo hace trabajo real:
en la capa 24 el mejor coseno (0.750) NO viene de la corrida entrenada en la
24 (0.671) sino de la entrenada en la 20. Matchear temprano propaga hacia
adelante mejor de lo que matchear profundo resuelve su propia capa.

CAVEAT: esos cosenos salen de `perfil_heldout`, asi que usarlos para fijar un
peso de entrenamiento es seleccion sobre test. Es leve -- la brecha train /
held-out en rel es ~0.02, o sea <1% sobre los pesos -- pero es real y queda
declarado en el metadata. Este script guarda TAMBIEN el perfil de train
(`perfil_train`), asi que una banda futura puede derivar los pesos de train y
la objecion desaparece.

No confundir este techo con el de `mean_diff_vectors.py`: aquel es el techo de
RUIDO DE ESTIMACION por split-half (0.96-0.99 en todas las capas) y ponderar
por el daria pesos practicamente uniformes. Este es el techo de
REALIZABILIDAD, que es el que tiene dispersion.

---------------------------------------------------------------------------
    python3 -u train_act_band.py --model $M --layers 12-24 --weight_power 2 \\
        --target frq --output_dir runs/act_band12_24_p2
"""

import argparse
import glob
import json
import math
import os

import pandas as pd
import torch

from lm import (DEFAULT_MODEL, get_embedding_matrix, load_model_and_tokenizer)
from train_act_patch import (DEFAULT_CACHE, TARGETS, cosine_step,
                             hidden_at_layers, mean_direction, parse_layers,
                             perfil, states_for, usable_mask)

DEFAULT_WEIGHTS_FROM = "runs/act_l*_frq/act_metadata.json"


def achieved_cosines(patterns, split="heldout"):
    """
    c_l = mejor coseno por prompt alcanzado en la capa l, sobre las corridas
    del barrido. Devuelve {l: (c_l, corrida_de_donde_salio)}.

    Lee el perfil de la ULTIMA epoch de cada corrida, que es el checkpoint que
    quedo guardado.
    """
    campo = f"perfil_{split}"
    out = {}
    for path in sorted(glob.glob(patterns)):
        meta = json.load(open(path, encoding="utf-8"))
        curva = meta.get("curva") or []
        if not curva or campo not in curva[-1]:
            print(f"  (salteado, sin {campo}: {path})")
            continue
        etiqueta = os.path.basename(os.path.dirname(path))
        for l_str, m in curva[-1][campo].items():
            l = int(l_str)
            if l not in out or m["cos"] > out[l][0]:
                out[l] = (m["cos"], etiqueta)
    if not out:
        raise SystemExit(f"no encontre cosenos en {patterns}; corre el barrido primero "
                         f"o pasa --layer_weights uniform")
    return out


def band_weights(layers, spec, power, patterns):
    """
    {l: w_l} con SUM w_l = 1. Devuelve tambien la procedencia para el metadata.

    spec: 'uniform' | 'auto' | lista separada por comas, en el orden de layers.
    """
    if spec == "uniform":
        w = {l: 1.0 / len(layers) for l in layers}
        return w, {"modo": "uniform"}

    if spec != "auto":
        vals = [float(x) for x in spec.split(",")]
        if len(vals) != len(layers):
            raise SystemExit(f"--layer_weights tiene {len(vals)} valores para "
                             f"{len(layers)} capas")
        tot = sum(vals)
        return {l: v / tot for l, v in zip(layers, vals)}, {"modo": "explicito"}

    C = achieved_cosines(patterns)
    faltan = [l for l in layers if l not in C]
    if faltan:
        raise SystemExit(f"sin coseno medido para las capas {faltan}")
    crudo = {l: C[l][0] ** power for l in layers}
    tot = sum(crudo.values())
    w = {l: v / tot for l, v in crudo.items()}
    info = {"modo": "auto", "power": power, "fuente": patterns,
            "c_l": {l: C[l][0] for l in layers},
            "c_l_origen": {l: C[l][1] for l in layers},
            "piso_1_menos_c2": {l: 1 - C[l][0] ** 2 for l in layers}}
    return w, info


def train_band(model_path, targets_csv, layers, target, output_dir, weights_spec,
               weight_power, weights_from, l2_weight=0.055, num_epochs=8,
               num_steps_per_prompt=20, num_patch_positions=3, step_size=0.00025,
               train_test_split=0.80, device="cuda:0", use_gate=True,
               batch_size=32, step_decay="cosine", val_n=20, truncate=True,
               cache_dir=DEFAULT_CACHE, refresh_cache=False):
    df = pd.read_csv(targets_csv, sep=";", keep_default_na=False)

    # Split POSICIONAL, identico a train_lang_patch.py y train_act_patch.py.
    n_train = int(len(df) * train_test_split)
    train_df, test_df = df.iloc[:n_train], df.iloc[n_train:]
    if use_gate and "passed_gate" in train_df.columns:
        antes = len(train_df)
        train_df = train_df[train_df["passed_gate"].astype(str).str.lower() == "true"]
        print(f"Gate de calidad sobre train: {len(train_df)}/{antes}")

    print(f"\nPesos de la banda ({weights_spec}):")
    W, W_info = band_weights(layers, weights_spec, weight_power, weights_from)
    if W_info["modo"] == "auto":
        print(f"  {'capa':>5}{'c_l':>8}{'1-c^2':>8}{'w_l':>9}{'vs unif':>9}  origen")
        u = 1.0 / len(layers)
        for l in layers:
            print(f"  {l:>5}{W_info['c_l'][l]:>8.3f}{W_info['piso_1_menos_c2'][l]:>8.3f}"
                  f"{W[l]:>9.4f}{W[l] / u:>8.2f}x  {W_info['c_l_origen'][l]}")
        print(f"  spread {max(W.values()) / min(W.values()):.2f}x   "
              f"suma {sum(W.values()):.6f}")
        print("  (c_l sale de perfil_heldout: seleccion leve sobre test, ver docstring)")

    model, tokenizer = load_model_and_tokenizer(model_path, device=device)
    dim = get_embedding_matrix(model).shape[1]
    n_layers = len(model.model.layers)
    all_layers = list(range(1, n_layers + 1))
    if max(layers) > n_layers:
        raise SystemExit(f"el modelo tiene {n_layers} capas, pediste {max(layers)}")
    if max(layers) == n_layers:
        print(f"AVISO: hidden_states[{n_layers}] de HF esta post-norm y no es "
              "comparable con mean_diff_vectors.py")

    val_rows, train_rows = test_df.head(val_n), train_df.head(val_n)
    print(f"\nTrain: {len(train_df)}  |  Held-out: {len(test_df)}  |  diagnostico: {len(val_rows)}")
    print(f"Objetivo: ACTIVACIONES (banda ponderada)  |  target: {target}  |  capas: {layers}")
    print(f"L2: {l2_weight}  |  step: {step_size} ({step_decay})  |  posiciones: {num_patch_positions}")

    print(f"\nActivaciones ({cache_dir}):")
    base = "frq" if target == "random" else target
    ST_CLEAN = states_for(model, tokenizer, df, "clean", device, all_layers,
                          model_path, cache_dir, refresh_cache)
    ST_REF = states_for(model, tokenizer, df, base, device, all_layers,
                        model_path, cache_dir, refresh_cache)

    usable = usable_mask(target, df)
    idxs = [i for i in train_df.index if usable.loc[i] and i in ST_CLEAN and i in ST_REF]
    if len(idxs) < 10:
        raise SystemExit(f"solo {len(idxs)} filas usables para estimar d")
    D = mean_direction(ST_REF, ST_CLEAN, idxs)

    if target == "random":
        g = torch.Generator(device="cpu").manual_seed(0)
        R = torch.randn(D.shape, generator=g).to(D.device)
        D = R / R.norm(dim=1, keepdim=True) * D.norm(dim=1, keepdim=True)

    D_sq = (D ** 2).sum(dim=1)
    LI = {l: j for j, l in enumerate(all_layers)}
    print(f"d estimada sobre {len(idxs)}/{len(train_df)} filas de train")

    patch = torch.zeros(1, num_patch_positions, dim, requires_grad=True, device=device)
    n_batches = math.ceil(len(train_df) / batch_size)
    total_steps = num_epochs * n_batches * num_steps_per_prompt
    print(f"Epochs: {num_epochs}  |  batch: {batch_size} ({n_batches} batches/epoch)  "
          f"|  steps/batch: {num_steps_per_prompt}")
    print("=" * 70)

    Wt = {l: torch.tensor(W[l], device=device) for l in layers}
    best = {"loss": float("inf"), "patch": None, "epoch": None}
    best_tr = {"loss": float("inf"), "patch": None, "epoch": None}
    curva, global_step = [], 0

    for epoch in range(num_epochs):
        print(f"\n{'#' * 70}\nEPOCH {epoch + 1}/{num_epochs}\n{'#' * 70}")
        epoch_loss = []

        for b in range(n_batches):
            batch = train_df.iloc[b * batch_size:(b + 1) * batch_size]
            paso = []
            for _ in range(num_steps_per_prompt):
                vals = []
                for idx, row in batch.iterrows():
                    h_p = hidden_at_layers(model, tokenizer, row["prompt"], device,
                                           layers, patch=patch,
                                           num_patch_positions=num_patch_positions,
                                           truncate=truncate)
                    # SUMA, no media: los pesos ya suman 1, asi que delta=0 sigue
                    # dando exactamente 1.0.
                    band = torch.stack([
                        Wt[l] * ((h_p[l] - ST_CLEAN[idx][LI[l]] - D[LI[l]]) ** 2).sum()
                        / D_sq[LI[l]] for l in layers]).sum()
                    total = band + l2_weight * patch.norm(2) ** 2
                    (total / len(batch)).backward()
                    vals.append(band.item())

                lr = cosine_step(step_size, global_step, total_steps) \
                    if step_decay == "cosine" else step_size
                patch.data -= torch.sign(patch.grad.data) * lr
                model.zero_grad()
                patch.grad.zero_()
                global_step += 1
                paso.append(sum(vals) / len(vals))

            epoch_loss.append(sum(paso) / len(paso))
            if (b + 1) % max(1, 10 // batch_size) == 0 or b + 1 == n_batches:
                print(f"  [batch {b + 1}/{n_batches}] band_w={epoch_loss[-1]:.4f}  "
                      f"norma={patch.norm(2).item():.6f}  lr={lr:.2e}")

        p_va = perfil(model, tokenizer, val_rows, patch, ST_CLEAN, D, device,
                      all_layers, num_patch_positions)
        p_tr = perfil(model, tokenizer, train_rows, patch, ST_CLEAN, D, device,
                      all_layers, num_patch_positions)
        # band_w = lo que se optimiza. band_u = media sin pesos, que es lo unico
        # comparable contra las corridas de una capa de train_act_patch.py.
        w_va = sum(W[l] * p_va[l]["rel"] for l in layers)
        w_tr = sum(W[l] * p_tr[l]["rel"] for l in layers)
        u_va = sum(p_va[l]["rel"] for l in layers) / len(layers)
        u_tr = sum(p_tr[l]["rel"] for l in layers) / len(layers)
        curva.append({"epoch": epoch + 1, "band_w_train": w_tr, "band_w_heldout": w_va,
                      "band_u_train": u_tr, "band_u_heldout": u_va,
                      "gap": w_va - w_tr, "norm": patch.norm(2).item(),
                      "perfil_heldout": p_va, "perfil_train": p_tr})

        print(f"\nEpoch {epoch + 1}: band_w (trayectoria)={sum(epoch_loss) / len(epoch_loss):.4f}"
              f"   norma={patch.norm(2).item():.6f}")
        print(f"  band_w:  train={w_tr:.4f}   held-out={w_va:.4f}   brecha={w_va - w_tr:+.4f}"
              f"   (1.0 = no hizo nada)")
        print(f"  band_u:  train={u_tr:.4f}   held-out={u_va:.4f}   <- sin pesos, comparable "
              f"con el barrido")
        print(f"  {'capa':>5}{'w_l':>8}{'rel':>9}{'cos':>9}{'mag':>9}   (held-out)")
        for l in all_layers:
            if l in layers or l % 6 == 0:
                m = p_va[l]
                wl = f"{W[l]:.4f}" if l in layers else "-"
                print(f"  {l:>5}{wl:>8}{m['rel']:>9.3f}{m['cos']:>9.3f}{m['mag']:>9.3f}"
                      f"{'   *' if l in layers else ''}")

        if w_va < best["loss"]:
            best = {"loss": w_va, "patch": patch.detach().clone(), "epoch": epoch + 1}
            print(f"  * mejor HELD-OUT hasta ahora ({w_va:.4f})")
        if w_tr < best_tr["loss"]:
            best_tr = {"loss": w_tr, "patch": patch.detach().clone(), "epoch": epoch + 1}
            print(f"  * mejor TRAIN hasta ahora ({w_tr:.4f})")

    os.makedirs(output_dir, exist_ok=True)
    final = best["patch"] if best["patch"] is not None else patch.detach()
    torch.save(final, os.path.join(output_dir, "lang_patch.pt"))
    torch.save(best["patch"], os.path.join(output_dir, "lang_patch_best_heldout.pt"))
    torch.save(best_tr["patch"], os.path.join(output_dir, "lang_patch_best_train.pt"))

    print("\n" + "=" * 70)
    print(f"{'epoch':>6}{'band_w tr':>11}{'band_w ho':>11}{'band_u ho':>11}{'brecha':>9}{'norma':>9}")
    for c in curva:
        marca = ("  <- mejor held-out" if c["epoch"] == best["epoch"] else "") + \
                ("  <- mejor train" if c["epoch"] == best_tr["epoch"] else "")
        print(f"{c['epoch']:>6}{c['band_w_train']:>11.4f}{c['band_w_heldout']:>11.4f}"
              f"{c['band_u_heldout']:>11.4f}{c['gap']:>+9.4f}{c['norm']:>9.4f}{marca}")

    meta = {
        "objetivo": "activaciones_banda_ponderada",
        "aviso_circularidad": "entrenado CONTRA la direccion; no usar para sostener P1/P3 "
                              "de HALLAZGOS.md, que valen solo para el parche de CE",
        "target": target, "layers": layers, "n_layers": n_layers,
        "layer_weights": {l: W[l] for l in layers}, "weights_info": W_info,
        "targets_csv": os.path.abspath(targets_csv),
        "filas_usables_para_d": len(idxs),
        "norma_d_por_capa": {l: D[LI[l]].norm().item() for l in all_layers},
        "patch_norm": final.norm(2).item(),
        "train_size": len(train_df), "test_size": len(test_df),
        "l2_weight": l2_weight, "step_size": step_size, "step_decay": step_decay,
        "batch_size": batch_size, "num_epochs": num_epochs,
        "num_steps_per_prompt": num_steps_per_prompt,
        "num_patch_positions": num_patch_positions,
        "train_test_split": train_test_split,
        "best_heldout_epoch": best["epoch"], "best_heldout_band_w": best["loss"],
        "best_train_epoch": best_tr["epoch"], "best_train_band_w": best_tr["loss"],
        "curva": curva,
    }
    with open(os.path.join(output_dir, "act_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"\nNorma final: {final.norm(2).item():.6f}  (v_CE de referencia: 0.8021)")
    for i in range(num_patch_positions):
        print(f"  posicion {i}: {final[0, i, :].norm(2).item():.6f}")
    print(f"\nGuardado en {output_dir}/")
    print(f"  python3 -u eval_lang_patch.py --model ... --patch {output_dir}/lang_patch.pt")
    return final


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--layers", default="12-24",
                    help="banda. '12-24' | '12,14,16'. Capa = hidden_states[l], 1..L")
    ap.add_argument("--target", default="frq", choices=TARGETS)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--layer_weights", default="auto",
                    help="auto (c_l^p normalizado) | uniform | lista separada por comas")
    ap.add_argument("--weight_power", type=float, default=2.0,
                    help="p en w_l ∝ c_l^p. 2 sigue la estructura cuadratica del piso "
                         "1-c^2; 1 es lineal; 0 equivale a uniform")
    ap.add_argument("--weights_from", default=DEFAULT_WEIGHTS_FROM,
                    help="glob de act_metadata.json del barrido, de donde salen los c_l")
    ap.add_argument("--l2_weight", type=float, default=0.055)
    ap.add_argument("--num_epochs", type=int, default=8)
    ap.add_argument("--num_steps_per_prompt", type=int, default=20)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--step_size", type=float, default=0.00025)
    ap.add_argument("--step_decay", default="cosine", choices=["none", "cosine"])
    ap.add_argument("--batch_size", type=int, default=32,
                    help="32 = el de v4_250, para no mezclar cambio de loss con "
                         "cambio de optimizador")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--val_n", type=int, default=20)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--cache_dir", default=DEFAULT_CACHE)
    ap.add_argument("--refresh_cache", action="store_true")
    ap.add_argument("--no_gate", action="store_true")
    ap.add_argument("--no_truncate", action="store_true")
    args = ap.parse_args()

    train_band(args.model, args.targets, parse_layers(args.layers), args.target,
               args.output_dir, args.layer_weights, args.weight_power,
               args.weights_from, args.l2_weight, args.num_epochs,
               args.num_steps_per_prompt, args.num_patch_positions, args.step_size,
               args.train_test_split, args.device, use_gate=not args.no_gate,
               batch_size=args.batch_size, step_decay=args.step_decay,
               val_n=args.val_n, truncate=not args.no_truncate,
               cache_dir=args.cache_dir, refresh_cache=args.refresh_cache)


if __name__ == "__main__":
    main()
