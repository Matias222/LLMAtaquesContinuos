"""
Control "centroide": en vez de un vector al azar con la norma del parche Shared,
un vector que apunta hacia donde viven los tokens del idioma en la capa 0.

    cA = mu_L             (centroide absoluto de los tokens de las preguntas en L)
    cB = mu_L - mu_en     (diferencia de medias contra las MISMAS preguntas en ingles)

ambos reescalados a ||v_L|| (la norma del parche Shared) y guardados como
[1, 1, d], o sea goal_all: se suman igual a cada token de la pregunta, como v_L.

mu se calcula sobre los ids del tramo goal_all (la pregunta dentro del template,
sin system ni headers: exactamente lo que el parche toca), ponderado por
frecuencia, SOLO con las filas de entrenamiento (antes del split). Nada del
held-out entra en los centroides.

Pregunta: el parche entrenado es solo "mover los tokens hacia el idioma"? Si cB
cambia el idioma de la respuesta como v_L, el idioma sale por aritmetica simple
en la capa 0 y la optimizacion no aporta direccion. Si no, v_L codifica algo que
no es la geometria lexica del vocabulario.

cA se espera dominado por la anisotropia (la media global del vocabulario /
de los tokens de pregunta en cualquier idioma); por eso se imprime tambien
cos(mu_L, mu_vocab) y cos(mu_L, mu_en).

Solo CPU: lee la matriz de embeddings de los safetensors y el tokenizer.

    python3 make_centroid_patch.py --model $MODEL --lang fr \\
        --like algebra/runs/v10/alg_fr/lang_patch_best_train.pt \\
        --targets attributes/v10/targets_v8_fr.csv --train_test_split 0.84 \\
        --out_dir algebra/runs/centroide/fr
"""

import argparse
import json
import os

import pandas as pd
import torch
from transformers import AutoTokenizer

from lm import DEFAULT_MODEL
from nearest_token_patch import goal_ids
from transfer_patch import load_embeddings


def cos(a, b):
    a, b = a.double().reshape(-1), b.double().reshape(-1)
    return float(a @ b / (a.norm() * b.norm()))


def centroid(W, ids_lists):
    """Media de W[t] sobre todas las ocurrencias (ponderada por frecuencia) y
    la version por token unico, para ver si las repeticiones (puntuacion,
    articulos) dominan."""
    flat = torch.tensor([t for ids in ids_lists for t in ids])
    uniq = torch.unique(flat)
    return W[flat].mean(0), W[uniq].mean(0), len(flat), len(uniq)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--lang", default="fr", help="idioma del centroide (columna prompt_<lang>)")
    ap.add_argument("--base_col", default="prompt", help="columna contra la que se resta en cB")
    ap.add_argument("--like", required=True, help="parche Shared del que copiar forma, norma y dtype")
    ap.add_argument("--targets", default="attributes/v10/targets_v8_fr.csv")
    ap.add_argument("--train_test_split", type=float, default=0.84)
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=False)
    W = load_embeddings(args.model, "cpu").float()
    W = W[:len(tok)]   # Qwen rellena filas que no son tokens (ver nearest_token_patch)
    like = torch.load(args.like, map_location="cpu")
    v = like.float().reshape(-1)
    if like.shape[1] != 1:
        raise SystemExit(f"--like tiene que ser un parche Shared [1, 1, d]; llego {tuple(like.shape)}")
    target_norm = v.norm().item()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    n_train = int(len(df) * args.train_test_split)
    train = df.iloc[:n_train]
    col_l = f"prompt_{args.lang}"
    for c in (col_l, args.base_col):
        if c not in train.columns:
            raise SystemExit(f"falta la columna {c} en {args.targets}")
    pares = [(str(a), str(b)) for a, b in zip(train[col_l], train[args.base_col])
             if str(a).strip() and str(b).strip()]
    ids_l = [goal_ids(tok, a) for a, _ in pares]
    ids_b = [goal_ids(tok, b) for _, b in pares]

    mu_l, mu_l_u, n_l, u_l = centroid(W, ids_l)
    mu_b, mu_b_u, n_b, u_b = centroid(W, ids_b)
    mu_vocab = W.mean(0)

    raw = {"cA": mu_l, "cB": mu_l - mu_b}
    out = {}
    for name, vec in raw.items():
        p = (vec / vec.norm() * target_norm).reshape(like.shape).to(like.dtype)
        path = os.path.join(args.out_dir, f"{name}.pt")
        torch.save(p, path)
        out[name] = {"path": path, "norma_cruda": vec.norm().item(), "norma": p.float().norm().item(),
                     "cos_shared": cos(vec, v), "cos_mu_vocab": cos(vec, mu_vocab)}

    d = v.numel()
    rep = {
        "lang": args.lang, "base_col": args.base_col, "like": args.like, "targets": args.targets,
        "n_train_filas": len(pares), "norma_shared": target_norm, "d": d,
        "cos_azar_esperado": 1 / d ** 0.5,
        "tokens": {col_l: {"ocurrencias": n_l, "unicos": u_l},
                   args.base_col: {"ocurrencias": n_b, "unicos": u_b}},
        "vectores": out,
        "diagnostico": {
            "cos(mu_L, mu_en)": cos(mu_l, mu_b),
            "cos(mu_L, mu_vocab)": cos(mu_l, mu_vocab),
            "cos(mu_en, mu_vocab)": cos(mu_b, mu_vocab),
            "cos(shared, mu_vocab)": cos(v, mu_vocab),
            "norma mu_vocab": mu_vocab.norm().item(),
            # misma cuenta con tokens unicos: si cambia mucho, las repeticiones dominan
            "unicos: cos(cA, shared)": cos(mu_l_u, v),
            "unicos: cos(cB, shared)": cos(mu_l_u - mu_b_u, v),
            "unicos: cos(cB, cB_frecuencia)": cos(mu_l_u - mu_b_u, mu_l - mu_b),
        },
    }

    print(f"Shared {args.like}  ||v|| {target_norm:.4f}  d {d}  (cos al azar ~ {1 / d ** 0.5:.4f})")
    print(f"train: {len(pares)} filas  |  {col_l}: {n_l} tokens ({u_l} unicos)  "
          f"|  {args.base_col}: {n_b} tokens ({u_b} unicos)")
    print("-" * 70)
    for name, o in out.items():
        print(f"{name}: norma cruda {o['norma_cruda']:.4f} -> {o['norma']:.4f}  "
              f"cos(shared) {o['cos_shared']:+.4f}  cos(mu_vocab) {o['cos_mu_vocab']:+.4f}  -> {o['path']}")
    print("-" * 70)
    for k, val in rep["diagnostico"].items():
        print(f"  {k:32s} {val:+.4f}")

    with open(os.path.join(args.out_dir, "centroide.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)
    print(f"\nreporte: {os.path.join(args.out_dir, 'centroide.json')}")


if __name__ == "__main__":
    main()
