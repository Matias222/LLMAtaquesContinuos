"""
Etapa base del run v9: todo lo que va SIN parche, generado una sola vez.

    held-out v8  M(q_L)  L = en, es, de, fr, it, pt   (6 x 112)
    open1        M(q_L)  L = en, es, de, fr           (4 x 99)
    open2        M(q_L)  L = en, es, de, fr           (4 x 50)

Con GEN_CACHE=<dir> (lo exporta run_train_v9.sh) cada salida queda en el cache
de lm.generate, y las etapas A, C y E la reusan en vez de regenerarla: el
baseline en ingles, el control nativo M(q_X) de cada celda y las condiciones
a=0. No depende de ningun parche, asi que es la misma para las tres celdas.

Escribe <out_dir>/base.json (filas con idioma GlotLID y accuracy) y base.md
(% por idioma detectado y accuracy, por set y por idioma de entrada).

    GEN_CACHE=algebra/runs/v9/gen_cache python3 base_v9.py --model $M \
        --heldout attributes/v8/targets_v8_fr.csv --split 0.84 \
        --open1 attributes/v9/open1_fr.csv --open2 attributes/v9/open2_fr.csv \
        --num_tokens 150 --out_dir algebra/runs/v9/base
"""

import argparse
import json
import os
from collections import Counter

import pandas as pd
import tqdm

import lang_id
from checkers import answer_correct, lang_detail
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

COLS = {"heldout": ["prompt", "prompt_es", "prompt_de", "prompt_fr", "prompt_it", "prompt_pt"],
        "open1": ["prompt", "prompt_es", "prompt_de", "prompt_fr"],
        "open2": ["prompt", "prompt_es", "prompt_de", "prompt_fr"]}


def idioma_col(col):
    return "en" if col == "prompt" else col.split("_", 1)[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--heldout", required=True)
    ap.add_argument("--split", type=float, default=0.84)
    ap.add_argument("--open1", required=True)
    ap.add_argument("--open2", required=True)
    ap.add_argument("--num_tokens", type=int, default=150)
    ap.add_argument("--n", type=int, default=0, help="limitar filas por set (0 = todas; humo)")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()
    if not os.environ.get("GEN_CACHE"):
        print("AVISO: sin GEN_CACHE las salidas no se reusan en las etapas siguientes")

    sets = {}
    df = pd.read_csv(args.heldout, sep=";", keep_default_na=False, dtype=str)
    sets["heldout"] = df.iloc[int(len(df) * args.split):]
    sets["open1"] = pd.read_csv(args.open1, sep=";", keep_default_na=False, dtype=str)
    sets["open2"] = pd.read_csv(args.open2, sep=";", keep_default_na=False, dtype=str)
    if args.n > 0:
        sets = {k: v.head(args.n) for k, v in sets.items()}

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    os.makedirs(args.out_dir, exist_ok=True)
    filas = []
    for nombre, d in sets.items():
        for col in COLS[nombre]:
            if col not in d.columns:
                raise SystemExit(f"{nombre}: falta la columna {col}")
            for i, r in tqdm.tqdm(d.iterrows(), total=len(d), desc=f"{nombre} {col}"):
                q = str(r[col]).strip()
                if not q:
                    continue
                out = generate_one(model, tokenizer, q, args.device, args.num_tokens, 0.0)
                ans = str(r.get("answer", "")).strip()
                filas.append({"set": nombre, "idx": int(i), "col": col, "idioma_entrada": idioma_col(col),
                              "prompt_en": r["prompt"], "prompt_usado": q, "answer": ans, "out": out,
                              "out_lang": lang_detail(out)["lang"],
                              "out_answer_correct": (bool(answer_correct(out, ans, r.get("aliases", "")))
                                                     if ans else None)})

    with open(os.path.join(args.out_dir, "base.json"), "w", encoding="utf-8") as f:
        json.dump({"config": vars(args), "lang_id": lang_id.descripcion(), "filas": filas},
                  f, indent=2, ensure_ascii=False)

    L = ["# Base v9: salidas sin parche", "",
         f"Generacion greedy de {args.num_tokens} tokens. Idioma: GlotLID. Estas salidas son el "
         "baseline, el control nativo M(q_X) y las condiciones a=0 de todas las celdas.", ""]
    for nombre in sets:
        L += [f"## {nombre}", "", "| entrada | n | idioma de la salida (%) | acc |", "|---|---|---|---|"]
        for col in COLS[nombre]:
            rs = [r for r in filas if r["set"] == nombre and r["col"] == col]
            if not rs:
                continue
            c = Counter(r["out_lang"] for r in rs)
            dist = ", ".join(f"{k} {100 * v / len(rs):.0f}" for k, v in c.most_common(4))
            accs = [r["out_answer_correct"] for r in rs if r["out_answer_correct"] is not None]
            acc = f"{100 * sum(accs) / len(accs):.0f}" if accs else "-"
            L.append(f"| {idioma_col(col)} | {len(rs)} | {dist} | {acc} |")
        L.append("")
    with open(os.path.join(args.out_dir, "base.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
