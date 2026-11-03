"""
Direccion de idioma por DIFERENCIA DE MEDIAS en la capa 0 (DiffMean), sin optimizar.

    D_L = mu_L - (1/|S|) * SUM_{s in S} mu_s

mu_X = media (ponderada por frecuencia) de los embeddings de entrada de los ids del
tramo goal_all (la pregunta dentro del template, exactamente lo que el parche toca)
de las preguntas escritas en X. Las preguntas son las MISMAS filas en todos los
idiomas (corpus paralelo), asi que lo que queda en D es el idioma y no el tema.

    --src prompt                       D_en    = mu_L - mu_en
    --src prompt,prompt_es,prompt_de   D_multi = mu_L - promedio(mu_en, mu_es, mu_de)
                                       (mismo peso por idioma; las fuentes de Shared)

Se guarda con NORMA 1 ([1, 1, d], goal_all): la escala que se pasa despues
(eval_lang_patch.py --scale, o un .pt reescalado) ES la norma absoluta del vector.
Asi D no toma nada de Shared: ni direccion ni norma.

Filas: --rows a:b (indices del CSV, por defecto 0:528, el train sin las 60 filas de
validacion 528:588 que usa la seleccion de norma). --n_rows N --seed s toma N filas
al azar de ese rango (curva de eficiencia de datos). Nada del held-out (588:) entra,
salvo que se pida explicitamente (it/pt, con validacion cruzada por folds).

Solo CPU: lee la matriz de embeddings de los safetensors y el tokenizer.

    python3 make_diffmean.py --model $M --targets attributes/v10/targets_v8_fr.csv \\
        --lang fr --src prompt,prompt_es,prompt_de --rows 0:528 \\
        --like algebra/runs/v10/alg_fr/lang_patch_best_train.pt \\
        --compare shared=algebra/runs/v10/alg_fr/lang_patch_best_train.pt \\
        --out algebra/runs/diffmean_llama/vec/Dmulti_fr.pt
"""

import argparse
import json
import os
import random

import pandas as pd
import torch
from transformers import AutoTokenizer

from nearest_token_patch import goal_ids
from transfer_patch import load_embeddings


def cos(a, b):
    a, b = a.double().reshape(-1), b.double().reshape(-1)
    return float(a @ b / (a.norm() * b.norm()))


def mean_emb(W, ids_lists):
    flat = torch.tensor([t for ids in ids_lists for t in ids])
    return W[flat].mean(0), len(flat), len(torch.unique(flat))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--lang", required=True, help="idioma target (columna prompt_<lang>)")
    ap.add_argument("--src", required=True, help="columnas de origen, separadas por coma")
    ap.add_argument("--rows", default="0:528", help="rango a:b de filas del CSV para construir D")
    ap.add_argument("--n_rows", type=int, default=0, help="submuestra de N filas del rango (0 = todas)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--like", required=True, help="parche [1, 1, d] del que copiar forma y dtype")
    ap.add_argument("--compare", action="append", default=[], metavar="NOMBRE=RUTA",
                    help="vectores contra los que reportar coseno (Shared, otros D)")
    ap.add_argument("--out", required=True, help="ruta del .pt (norma 1); al lado queda <out>.json")
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=False)
    W = load_embeddings(args.model, "cpu").float()[:len(tok)]
    like = torch.load(args.like, map_location="cpu")
    if like.dim() != 3 or like.shape[:2] != (1, 1):
        raise SystemExit(f"--like tiene que ser [1, 1, d]; llego {tuple(like.shape)}")

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    a, b = (int(x) for x in args.rows.split(":"))
    idx = list(range(a, min(b, len(df))))
    if args.n_rows:
        if args.n_rows > len(idx):
            raise SystemExit(f"--n_rows {args.n_rows} > {len(idx)} filas en {args.rows}")
        idx = sorted(random.Random(args.seed).sample(idx, args.n_rows))
    sub = df.iloc[idx]
    col_l = f"prompt_{args.lang}"
    srcs = [c.strip() for c in args.src.split(",") if c.strip()]
    for c in [col_l] + srcs:
        if c not in sub.columns:
            raise SystemExit(f"falta la columna {c} en {args.targets}")
        vacias = int((sub[c].astype(str).str.strip() == "").sum())
        if vacias:
            raise SystemExit(f"{c}: {vacias} filas vacias en {args.rows} (¿rango fuera de las traducciones?)")

    mu_l, n_l, u_l = mean_emb(W, [goal_ids(tok, str(q)) for q in sub[col_l]])
    mus, info = {}, {col_l: {"ocurrencias": n_l, "unicos": u_l}}
    for c in srcs:
        mus[c], n_c, u_c = mean_emb(W, [goal_ids(tok, str(q)) for q in sub[c]])
        info[c] = {"ocurrencias": n_c, "unicos": u_c}
    raw = mu_l - torch.stack([mus[c] for c in srcs]).mean(0)
    unit = (raw / raw.norm()).reshape(like.shape).to(like.dtype)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    torch.save(unit, args.out)

    comp = {}
    for spec in args.compare:
        k, _, p = spec.partition("=")
        comp[k] = cos(raw, torch.load(p, map_location="cpu").float())
    rep = {"lang": args.lang, "src": srcs, "targets": args.targets, "rows": args.rows,
           "n_rows": len(idx), "seed": args.seed if args.n_rows else None,
           "norma_cruda": raw.norm().item(), "norma_emb_media": W.norm(dim=1).mean().item(),
           "d": raw.numel(), "cos_azar_esperado": raw.numel() ** -0.5,
           "cos": comp, "cos(mu_L, mu_vocab)": cos(mu_l, W.mean(0)),
           "cos(D, mu_vocab)": cos(raw, W.mean(0)), "tokens": info, "out": args.out}
    with open(os.path.splitext(args.out)[0] + ".json", "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)
    print(f"{os.path.basename(args.out)}: L={args.lang} src={srcs} filas={len(idx)} "
          f"||raw||={rep['norma_cruda']:.4f}  " + "  ".join(f"cos({k})={v:+.3f}" for k, v in comp.items()))


if __name__ == "__main__":
    main()
