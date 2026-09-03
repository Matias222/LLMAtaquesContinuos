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

from checkers import answer_correct, french_score, is_french, truncate_at_role_leak
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer, nll_of_target
from reporting import CONDITIONS, open_metrics, score_rows, write_markdown


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--train_test_split", type=float, default=0.8)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--head_k", type=int, default=5,
                    help="cuantos tokens iniciales cuentan como 'head' (decision de idioma)")
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
        patched_raw = generate_one(model, tokenizer, q, args.device, args.num_tokens,
                                   args.temperature, patch=patch,
                                   num_patch_positions=args.num_patch_positions,
                                   clean=False)
        patched = truncate_at_role_leak(patched_raw)

        has_answer = str(ans).strip() != ""
        rec = {"idx": int(i), "prompt": q, "answer": ans, "has_answer": has_answer,
               "baseline": base, "reference": ref, "patched": patched}
        for key, text in (("baseline", base), ("reference", ref), ("patched", patched)):
            rec[f"{key}_is_french"] = bool(is_french(text))
            rec[f"{key}_french_score"] = float(french_score(text))
            # None en prompts abiertos: no hay respuesta verificable que medir
            rec[f"{key}_answer_correct"] = bool(answer_correct(text, ans, al)) if has_answer else None
        rec["baseline_role_leak"] = str(r.get("baseline_role_leak", False)).lower() == "true"
        rec["reference_role_leak"] = str(r.get("ref_role_leak", False)).lower() == "true"
        rec["patched_role_leak"] = bool(patched != patched_raw.strip())
        rows.append(rec)

        nll_b.append(nll_of_target(model, tokenizer, q, ref, args.device, patch=None,
                                   head_k=args.head_k))
        nll_p.append(nll_of_target(model, tokenizer, q, ref, args.device, patch=patch,
                                   num_patch_positions=args.num_patch_positions,
                                   head_k=args.head_k))
        rec["nll_baseline"] = nll_b[-1]
        rec["nll_patched"] = nll_p[-1]

    def avg(dicts, key):
        vals = [d[key] for d in dicts if d[key] == d[key]]   # descarta nan
        return sum(vals) / len(vals) if vals else float("nan")

    metrics = {c: score_rows(rows, c) for c, _ in CONDITIONS}
    metrics.update({
        "nll_fr_baseline": avg(nll_b, "all"),
        "nll_fr_patched": avg(nll_p, "all"),
        "nll_fr_head_baseline": avg(nll_b, "head"),
        "nll_fr_head_patched": avg(nll_p, "head"),
        "nll_fr_tail_baseline": avg(nll_b, "tail"),
        "nll_fr_tail_patched": avg(nll_p, "tail"),
        "head_k": args.head_k,
    })

    om = open_metrics(rows)
    if om:
        metrics["open"] = om

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
    print(f"{'condicion':<26}{'is_french':>11}{'fr_score':>11}{'accuracy':>11}{'leak':>8}")
    print("-" * 70)
    for cond, label in CONDITIONS:
        c = metrics[cond]
        print(f"{label:<26}{c['is_french']:>10.1%}{c['french_score']:>11.3f}"
              f"{c['answer_correct']:>10.1%}{c['role_leak']:>8.0%}")
    print("-" * 70)
    print(f"{'CE target FR':<26}{'sin parche':>12}{'con parche':>12}{'delta':>10}")
    for lbl, kb, kp in [(f"head (primeros {args.head_k})", "nll_fr_head_baseline", "nll_fr_head_patched"),
                        ("tail (el resto)", "nll_fr_tail_baseline", "nll_fr_tail_patched"),
                        ("toda la respuesta", "nll_fr_baseline", "nll_fr_patched")]:
        print(f"{lbl:<26}{metrics[kb]:>12.4f}{metrics[kp]:>12.4f}"
              f"{metrics[kp] - metrics[kb]:>+10.4f}")
    print("  el head es donde vive la decision de idioma; el tail casi no deberia moverse")

    if "open" in metrics:
        o = metrics["open"]
        print("\n" + "=" * 70)
        print(f"PROMPTS ABIERTOS  (n={o['n']}, sin respuesta verificable)")
        print(f"  overlap de contenido parche vs referencia : {o['overlap_patched_reference']:.3f}")
        print(f"  overlap baseline(EN) vs referencia        : {o['overlap_baseline_reference']:.3f}")
        print(f"  control de azar (parche vs otra pregunta) : {o['overlap_shuffled_control']:.3f}")
        print(f"  frances por tercio, parche     : {[round(x, 2) for x in o['french_thirds_patched']]}")
        print(f"  frances por tercio, referencia : {[round(x, 2) for x in o['french_thirds_reference']]}")
        print("  si el parche cae en el tercer tercio, el efecto es local y decae")
    print("=" * 70)
    print(f"\nReportes: {args.out_json}\n          {args.out_md}")


if __name__ == "__main__":
    main()
