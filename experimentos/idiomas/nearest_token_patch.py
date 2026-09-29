"""
¿El parche goal_all mueve los embeddings de la pregunta a OTRO token?

Para cada token t de la pregunta (el mismo tramo goal_all que ve el parche en
train: la pregunta del usuario dentro del template, sin system ni headers) se
toma e' = W[t] + a*v y se busca el token del vocabulario mas cercano. Si el
vecino sigue siendo t, el parche no "reescribe" la pregunta en el espacio de
tokens: el modelo ve el mismo token corrido en una direccion. Si cambia, se
lista a que tokens va (¿palabras francesas? ¿siempre el mismo token?).

Dos metricas de vecino:
  l2    argmin ||W_j - e'||
  cos   argmax cos(W_j, e')

Controles:
  a      barrido de escala (el parche real es a=1)
  rand   vector al azar con la MISMA norma que v (misma escala, sin direccion)
  gap    distancia de cada token a su vecino mas cercano (sin parche), contra
         ||v||: si ||v|| < gap/2 el vecino l2 no puede cambiar

Solo CPU: lee la matriz de embeddings de los safetensors y el tokenizer, no
instancia el modelo.

    python3 nearest_token_patch.py --model $MODEL \\
        --patch runs/v5_goalall_head_multi/lang_patch_best_train.pt \\
        --out_dir runs/v5_goalall_head_multi/nearest_token
"""

import argparse
import collections
import json
import os

import pandas as pd
import torch
from transformers import AutoTokenizer

from lm import DEFAULT_MODEL, build_suffix_manager, patch_positions
from transfer_patch import load_embeddings


def goal_ids(tokenizer, question):
    """Los ids del tramo goal_all, tal cual caen dentro del template."""
    sm = build_suffix_manager(tokenizer, question, target="")
    ids = sm.get_input_ids()
    start, n = patch_positions(sm, anchor="goal_all")
    return ids[start:start + n].tolist()


@torch.no_grad()
def nearest(W, W_sq, W_unit, X, chunk=256):
    """Vecino l2 y cos (top-2) de cada fila de X contra el vocabulario."""
    l2_idx, l2_d, cos_idx, cos_s = [], [], [], []
    for i in range(0, len(X), chunk):
        x = X[i:i + chunk]
        dot = x @ W.T
        d2 = (W_sq[None, :] - 2 * dot + (x * x).sum(1, keepdim=True)).clamp_min(0)
        d, j = d2.topk(2, dim=1, largest=False)
        l2_idx.append(j); l2_d.append(d.sqrt())
        s, k = ((x / x.norm(dim=1, keepdim=True)) @ W_unit.T).topk(2, dim=1)
        cos_idx.append(k); cos_s.append(s)
    return (torch.cat(l2_idx), torch.cat(l2_d), torch.cat(cos_idx), torch.cat(cos_s))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--patch", default="runs/v5_goalall_head_multi/lang_patch_best_train.pt")
    ap.add_argument("--targets", default="attributes/french/targets_french_v5.csv")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--cols", default="prompt,prompt_es,prompt_de")
    ap.add_argument("--alphas", default="0.5,1,2,4,8")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n_show", type=int, default=10, help="preguntas a mostrar token por token")
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=False)
    W = load_embeddings(args.model, "cpu")
    W_sq = (W * W).sum(1)
    W_unit = W / W.norm(dim=1, keepdim=True)
    v = torch.load(args.patch, map_location="cpu").float().reshape(-1)
    g = torch.Generator().manual_seed(args.seed)
    r = torch.randn(v.shape, generator=g)
    r = r * (v.norm() / r.norm())
    alphas = [float(a) for a in args.alphas.split(",")]
    vocab_norm = W.norm(dim=1).mean().item()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    heldout = df.iloc[int(len(df) * args.train_test_split):]
    cols = [c for c in args.cols.split(",") if c in heldout.columns]
    preguntas = {c: [(int(i), goal_ids(tok, q)) for i, q in heldout[c].items() if str(q).strip()]
                 for c in cols}

    # El vecino depende solo del id del token, asi que se calcula por id unico.
    uniq = sorted({t for c in cols for _, ids in preguntas[c] for t in ids})
    U = torch.tensor(uniq)
    pos = {t: k for k, t in enumerate(uniq)}
    dec = lambda t: tok.decode([t])

    print(f"parche {args.patch}  ||v|| {v.norm():.4f}  ||e|| medio del vocab {vocab_norm:.4f}  "
          f"(ratio {v.norm().item() / vocab_norm:.3f})")
    # Percentil de ||v|| entre las normas de los embeddings: sobre todo el
    # vocabulario y sobre los tokens que de verdad aparecen en las preguntas.
    vn = v.norm().item()
    norms_vocab = W.norm(dim=1)
    norms_preg = norms_vocab[U]
    pct_vocab = (norms_vocab < vn).float().mean().item()
    pct_preg = (norms_preg < vn).float().mean().item()
    print(f"||v|| supera la norma de {pct_vocab:.1%} de los tokens del vocabulario y de "
          f"{pct_preg:.1%} de los tokens de las preguntas (mediana preguntas {norms_preg.median():.4f})")
    print(f"held-out {len(heldout)} filas (idx {heldout.index[0]}..{heldout.index[-1]})  |  "
          f"entradas {cols}  |  tokens unicos {len(uniq)}")

    # Sanity + gap: sin parche el vecino de W[t] es t (distancia 0); el segundo
    # vecino da cuanto hay que mover el token para que cambie.
    base = nearest(W, W_sq, W_unit, W[U])
    self_ok = (base[0][:, 0] == U).float().mean().item()
    gap = base[1][:, 1]
    print(f"sanity: vecino l2 de W[t] sin parche == t en {self_ok:.1%}")
    print(f"gap (distancia al 2do vecino): mediana {gap.median():.3f}  p10 {gap.quantile(.1):.3f}  "
          f"p90 {gap.quantile(.9):.3f}  |  ||v|| < gap/2 en {(v.norm() < gap / 2).float().mean():.1%}")

    filas, rep = [], {"patch": args.patch, "v_norm": v.norm().item(), "vocab_norm_mean": vocab_norm,
                      "n_unique": len(uniq), "sanity_self": self_ok,
                      "gap_median": gap.median().item(),
                      "pct_norma_vocab": pct_vocab, "pct_norma_preguntas": pct_preg,
                      "norma_mediana_preguntas": norms_preg.median().item(), "conds": []}
    detalle = {}
    for nombre, vec in (("v", v), ("rand", r)):
        for a in alphas:
            l2_i, l2_d, cos_i, _ = nearest(W, W_sq, W_unit, W[U] + a * vec)
            l2_nn, cos_nn = l2_i[:, 0].tolist(), cos_i[:, 0].tolist()
            # rank del token original: ¿sigue entre los 2 primeros?
            for c in cols:
                n_tok = n_l2 = n_cos = 0
                dest = collections.Counter()
                for _, ids in preguntas[c]:
                    for t in ids:
                        k = pos[t]
                        n_tok += 1
                        if l2_nn[k] != t:
                            n_l2 += 1
                            dest[l2_nn[k]] += 1
                        n_cos += cos_nn[k] != t
                top = [(dec(t), n) for t, n in dest.most_common(8)]
                filas.append((nombre, a, c, n_tok, n_l2 / n_tok, n_cos / n_tok, top))
                rep["conds"].append({"vec": nombre, "alpha": a, "col": c, "n_tok": n_tok,
                                     "cambia_l2": n_l2 / n_tok, "cambia_cos": n_cos / n_tok,
                                     "destinos_l2": top})
            if a == 1.0:
                detalle[nombre] = (l2_nn, cos_nn)

    print()
    print(f"{'vec':<5} {'a':>5}  {'entrada':<10} {'n_tok':>6}  {'cambia l2':>9}  {'cambia cos':>10}  destinos l2 mas frecuentes")
    print("-" * 110)
    for nombre, a, c, n, fl2, fcos, top in filas:
        tops = ", ".join(f"{s!r}x{n_}" for s, n_ in top[:5])
        print(f"{nombre:<5} {a:>5g}  {c:<10} {n:>6}  {fl2:>9.1%}  {fcos:>10.1%}  {tops}")

    # Token por token, a=1, para leer que "ve" el modelo.
    lineas = []
    if "v" in detalle:
        l2_nn, cos_nn = detalle["v"]
        for c in cols:
            lineas.append(f"\n## {c}  (a=1, parche v)\n")
            lineas.append("| # | original | vecino l2 | vecino cos |")
            lineas.append("|---|---|---|---|")
            for i, ids in preguntas[c][: args.n_show]:
                orig = "".join(dec(t) for t in ids)
                nl2 = "".join(dec(l2_nn[pos[t]]) if l2_nn[pos[t]] != t else dec(t) for t in ids)
                ncos = "".join(dec(cos_nn[pos[t]]) for t in ids)
                cambios = " ".join(f"`{dec(t)}`→`{dec(cos_nn[pos[t]])}`"
                                   for t in ids if cos_nn[pos[t]] != t)
                lineas.append(f"| {i} | {orig} | {nl2} | {ncos} |")
                if cambios:
                    lineas.append(f"|  | cambios cos: {cambios} | | |")
        print("\n".join(lineas))

    with open(os.path.join(args.out_dir, "nearest_token.json"), "w") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    with open(os.path.join(args.out_dir, "nearest_token.md"), "w") as f:
        f.write(f"# Vecino mas cercano de e + a*v (`{args.patch}`)\n\n")
        f.write(f"||v|| {v.norm():.4f}, ||e|| medio {vocab_norm:.4f}, gap mediano {gap.median():.3f}\n\n")
        f.write(f"||v|| supera la norma de {pct_vocab:.1%} de los tokens del vocabulario y de "
                f"{pct_preg:.1%} de los tokens de las preguntas (mediana {norms_preg.median():.4f})\n\n")
        f.write("| vec | a | entrada | n_tok | cambia l2 | cambia cos | destinos l2 |\n|---|---|---|---|---|---|---|\n")
        for nombre, a, c, n, fl2, fcos, top in filas:
            tops = ", ".join(f"`{s}`×{n_}" for s, n_ in top[:5])
            f.write(f"| {nombre} | {a:g} | {c} | {n} | {fl2:.1%} | {fcos:.1%} | {tops} |\n")
        f.write("\n".join(lineas) + "\n")
    print(f"\nGuardado: {args.out_dir}/nearest_token.json  {args.out_dir}/nearest_token.md")


if __name__ == "__main__":
    main()
