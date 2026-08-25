"""
Paso 2: evaluar el parche sobre el HELD-OUT, en tres condiciones.

    baseline    M(q)              -> deberia ser ingles y correcto
    referencia  M([FR ; q])       -> TECHO: la instruccion en texto
    parche      M(q + v)          -> lo que queremos medir

Metricas, ninguna basada en lexicon tematico:
    compliance  = is_french(output)          + french_score continuo
    accuracy    = answer_correct(output)     (invariante al idioma)
    nll_fr      = CE por token del target frances de referencia

La referencia es lo que le faltaba al trabajo de navidad: sin ella no se puede
decir si una caida de accuracy la causa el parche o la instruccion misma.

Solo se reporta el held-out. El train no se mira.
"""

import argparse
import json
import os

import pandas as pd
import torch
import tqdm

from checkers import answer_correct, french_score, is_french
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer, nll_of_target
from reporting import CONDITIONS, score_rows, write_markdown


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="targets_french.csv")
    ap.add_argument("--train_test_split", type=float, default=0.8)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--scale", type=float, default=1.0,
                    help="escala alfa aplicada al parche (dose-response)")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_json", default="eval_report.json")
    ap.add_argument("--out_md", default="eval_report.md")
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    heldout = df.iloc[int(len(df) * args.train_test_split):].reset_index(drop=True)

    patch = torch.load(args.patch, map_location=args.device).to(args.device)
    if args.scale != 1.0:
        patch = patch * args.scale

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    print(f"Held-out: {len(heldout)}  |  parche: {args.patch}  |  escala: {args.scale}")
    print("=" * 70)

    rows, nll_b, nll_p = [], [], []
    for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc="eval"):
        q, ans, al = r["prompt"], r["answer"], r["aliases"]

        # baseline y referencia ya fueron generadas de forma determinista
        # (greedy) en generate_targets.py; reusarlas es identico y mas barato.
        base = r["baseline_en"]
        ref = r["output"]
        patched = generate_one(model, tokenizer, q, args.device, args.num_tokens,
                               args.temperature, patch=patch,
                               num_patch_positions=args.num_patch_positions)

        rec = {"idx": int(i), "prompt": q, "answer": ans,
               "baseline": base, "reference": ref, "patched": patched}
        for key, text in (("baseline", base), ("reference", ref), ("patched", patched)):
            rec[f"{key}_is_french"] = bool(is_french(text))
            rec[f"{key}_french_score"] = float(french_score(text))
            rec[f"{key}_answer_correct"] = bool(answer_correct(text, ans, al))
        rows.append(rec)

        nll_b.append(nll_of_target(model, tokenizer, q, ref, args.device, patch=None))
        nll_p.append(nll_of_target(model, tokenizer, q, ref, args.device, patch=patch,
                                   num_patch_positions=args.num_patch_positions))

    metrics = {c: score_rows(rows, c) for c, _ in CONDITIONS}
    metrics.update({
        "nll_fr_baseline": sum(nll_b) / len(nll_b),
        "nll_fr_patched": sum(nll_p) / len(nll_p),
    })

    report = {
        "patch_path": os.path.abspath(args.patch),
        "model_path": args.model,
        "patch_norm": float(patch.norm(2).item()),
        "patch_shape": list(patch.shape),
        "n_heldout": len(rows),
        "config": {
            "num_patch_positions": args.num_patch_positions,
            "scale": args.scale,
            "num_tokens": args.num_tokens,
            "temperature": args.temperature,
            "train_test_split": args.train_test_split,
        },
        "metrics": metrics,
        "splits": {"heldout": rows},
    }

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    write_markdown(report, args.out_md)

    print("\n" + "=" * 70)
    print(f"{'condicion':<26}{'is_french':>11}{'fr_score':>11}{'accuracy':>11}")
    print("-" * 70)
    for cond, label in CONDITIONS:
        c = metrics[cond]
        print(f"{label:<26}{c['is_french']:>10.1%}{c['french_score']:>11.3f}{c['answer_correct']:>10.1%}")
    print("-" * 70)
    print(f"CE target FR   sin parche={metrics['nll_fr_baseline']:.4f}  "
          f"con parche={metrics['nll_fr_patched']:.4f}  "
          f"delta={metrics['nll_fr_patched'] - metrics['nll_fr_baseline']:+.4f}")
    print("=" * 70)
    print(f"\nReportes: {args.out_json}\n          {args.out_md}")


if __name__ == "__main__":
    main()
