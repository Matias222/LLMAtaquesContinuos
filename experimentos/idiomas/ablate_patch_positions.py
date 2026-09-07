"""
Experimento 4a de mecanismo: que aporta cada una de las 3 posiciones, y si el
parche depende de estar al INICIO de la pregunta.

Todo sobre el parche YA ENTRENADO (v4_250), sin reentrenar. Cada variante es una
transformacion del tensor [1, 3, d] o de donde se suma:

    full       el parche tal cual                              (= eval)
    zeroK      posicion K a cero, las otras dos intactas       necesidad de K
    onlyK      solo la posicion K, las otras dos a cero        suficiencia de K
    permABC    las 3 direcciones reordenadas (p.ej. perm201)  especificidad posicional
    shiftK     el parche entero movido a goal_start + K        dependencia del inicio

Lecturas:

    zero/only   si ninguna posicion sola alcanza y quitar cualquiera rompe, las
                tres actuan en conjunto; si una sola alcanza, el "3 tokens" es
                holgura y k=1 seria el numero a reportar.
    perm        si permutar rompe, cada vector es especifico de SU posicion (lo
                que espera un modelo con posiciones rotatorias); si no rompe,
                el parche es una perturbacion casi intercambiable.
    shift       si el parche entrenado en 1-3 deja de funcionar en 4-6, hay dos
                lecturas posibles que este script NO separa: (a) las
                direcciones son especificas de la posicion (RoPE) o (b) el
                inicio del goal es especial (attention sink). Lo que las separa
                es REENTRENAR con --patch_offset K (train_lang_patch.py) y
                evaluar con el mismo offset: si el parche reentrenado en 4-6
                funciona, era (a); si tampoco, era (b).

Las preguntas mas cortas que offset + 3 tokens reciben un parche recortado; se
cuentan en `truncados` y conviene mirar la tasa excluyendolas.

    python3 -u ablate_patch_positions.py --model $M \\
        --patch runs/v4_250/lang_patch_best_train.pt --out_dir runs/ablate_v4
"""

import argparse
import json
import os
import re

import pandas as pd
import torch
import tqdm

from attn_utils import add_metrics, aggregate
from checkers import truncate_at_role_leak
from lm import DEFAULT_MODEL, build_suffix_manager, generate_one, load_model_and_tokenizer

DEFAULT_VARIANTS = "full,zero0,zero1,zero2,only0,only1,only2,perm201,perm120,shift1,shift2,shift3,shift4"


def make_variant(patch, name):
    """-> (tensor [1, N, d], offset)."""
    n = patch.shape[1]
    if name == "full":
        return patch.clone(), 0
    m = re.fullmatch(r"zero(\d+)", name)
    if m:
        k = int(m.group(1))
        p = patch.clone()
        p[:, k, :] = 0
        return p, 0
    m = re.fullmatch(r"only(\d+)", name)
    if m:
        k = int(m.group(1))
        p = torch.zeros_like(patch)
        p[:, k, :] = patch[:, k, :]
        return p, 0
    m = re.fullmatch(r"perm(\d+)", name)
    if m:
        orden = [int(c) for c in m.group(1)]
        if sorted(orden) != list(range(n)):
            raise ValueError(f"{name}: la permutacion tiene que usar cada posicion 0..{n - 1} una vez")
        return patch[:, orden, :].clone(), 0
    m = re.fullmatch(r"shift(\d+)", name)
    if m:
        return patch.clone(), int(m.group(1))
    raise ValueError(f"variante desconocida: {name}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", default="runs/v4_250/lang_patch_best_train.pt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--variants", default=DEFAULT_VARIANTS)
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--n", type=int, default=0, help="limitar filas (0 = todo el held-out)")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    heldout = df.iloc[int(len(df) * args.train_test_split):]
    if args.n > 0:
        heldout = heldout.head(args.n)

    patch = torch.load(args.patch, map_location=args.device).to(args.device)
    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    for v in variants:
        make_variant(patch, v)     # valida los nombres antes de cargar el modelo

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    os.makedirs(args.out_dir, exist_ok=True)

    print(f"parche {args.patch}  norma total {patch.norm(2).item():.4f}")
    for k in range(patch.shape[1]):
        print(f"  posicion {k}: norma {patch[0, k, :].norm(2).item():.4f}")
    print(f"held-out {len(heldout)}  |  variantes: {variants}\n")

    # largo del goal por prompt, para contar parches recortados en los shift
    goal_len = {}
    for i, r in heldout.iterrows():
        sm = build_suffix_manager(tokenizer, r["prompt"], target="")
        goal_len[int(i)] = sm._goal_slice.stop - sm._goal_slice.start

    resumen = []
    for name in variants:
        p, off = make_variant(patch, name)
        rows = []
        for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc=name):
            raw = generate_one(model, tokenizer, r["prompt"], args.device, args.num_tokens, 0.0,
                               patch=p, num_patch_positions=args.num_patch_positions,
                               clean=False, patch_offset=off)
            txt = truncate_at_role_leak(raw)
            aplicadas = max(0, min(args.num_patch_positions, goal_len[int(i)] - off))
            rec = {"idx": int(i), "prompt": r["prompt"], "answer": r["answer"],
                   "baseline": r["baseline_en"], "reference": r["output"],
                   "patched": txt, "patched_role_leak": bool(txt != raw.strip()),
                   "goal_len": goal_len[int(i)], "posiciones_aplicadas": aplicadas,
                   "truncado": aplicadas < args.num_patch_positions,
                   "patched_igual_baseline": txt.strip() == str(r["baseline_en"]).strip()}
            add_metrics(rec, "patched", txt, r["answer"], r["aliases"])
            rows.append(rec)

        agg = aggregate(rows, "patched")
        agg["igual_baseline"] = sum(r["patched_igual_baseline"] for r in rows) / len(rows)
        agg["truncados"] = sum(r["truncado"] for r in rows)
        completos = [r for r in rows if not r["truncado"]]
        agg["is_french_sin_truncados"] = (sum(r["patched_is_french"] for r in completos) / len(completos)
                                          if completos else float("nan"))
        rep = {"objetivo": "ablacion por posicion del parche", "variante": name, "offset": off,
               "patch": os.path.abspath(args.patch), "norma_variante": p.norm(2).item(),
               "config": vars(args), "n_heldout": len(rows), "metrics": agg, "rows": rows}
        with open(os.path.join(args.out_dir, f"ablate_{name}.json"), "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2, ensure_ascii=False)
        resumen.append({"variante": name, "offset": off, "norma": p.norm(2).item(), **agg})

    print("\n" + "=" * 104)
    print(f"{'variante':<10}{'off':>4}{'norma':>8}{'is_french':>10}{'sin_trunc':>10}{'starts_fr':>10}"
          f"{'accuracy':>10}{'largo':>7}{'<25ch':>6}{'=base':>7}{'trunc':>6}")
    for r in resumen:
        print(f"{r['variante']:<10}{r['offset']:>4}{r['norma']:>8.3f}{r['is_french']:>10.2f}"
              f"{r['is_french_sin_truncados']:>10.2f}{r['starts_fr']:>10.2f}{r['answer_correct']:>10.2f}"
              f"{r['len_media']:>7.1f}{r['cortas_lt25']:>6d}{r['igual_baseline']:>7.2f}{r['truncados']:>6d}")
    print("=" * 104)
    print("zero/only: necesidad y suficiencia de cada posicion.  perm: especificidad posicional.")
    print("shift: si cae, reentrenar con --patch_offset K separa RoPE de attention sink.")

    with open(os.path.join(args.out_dir, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"patch": os.path.abspath(args.patch), "resumen": resumen}, f, indent=2,
                  ensure_ascii=False)
    print(f"\nGuardado en {args.out_dir}/")


if __name__ == "__main__":
    main()
