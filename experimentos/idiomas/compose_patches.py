"""
Geometria de parches: componer dos parches entrenados INDEPENDIENTEMENTE.

Motivo (HALLAZGOS.md, seccion 9): la compuerta AND de navidad (pos0+pos1 ->
navidad, cada una sola -> nada) esta confundida con co-adaptacion, porque las
posiciones se co-entrenaron. El test limpio es componer vectores que nunca se
vieron entre si. Aca se entrena un segundo parche sobre un atributo NO
lingueistico (mayusculas, generate_targets_upper.py) y se suma al de frances
(runs/v3_250/lang_patch.pt) para ver si el modelo produce las dos cosas a la
vez: frances Y en mayusculas.

Ambos parches ocupan las mismas 3 posiciones del goal slice, asi que sumarlos
es literal:

    v = alpha_fr * v_fr + alpha_upper * v_upper
    e'_i = e_i + v_i        para i en {0, 1, 2}

Condiciones evaluadas sobre el held-out (mismas preguntas que v3_250, si se
usa el split y CSV por defecto -- los dos parches se entrenaron sobre el mismo
data/questions.csv con el mismo train_test_split, asi que comparten held-out):

    baseline          M(q)                          sin parche
    solo frances      M(q + v_fr)                   alpha=1.0 fijo
    solo mayusculas   M(q + v_upper)                alpha=1.0 fijo
    referencia conjunta   M([MAYUS+FR ; q])          techo natural: la instruccion
                                                     combinada en texto, sin parche
    compuesto         M(q + alpha_fr*v_fr + alpha_upper*v_upper)
                      barrido sobre --alphas_fr x --alphas_upper (default: 1.0 x 1.0)

Metricas por condicion: is_french/french_score, is_uppercase/uppercase_score,
answer_correct. Ninguna es teacher-forcing CE: esto es generacion libre, como
eval_lang_patch.py.

    python3 -u compose_patches.py --model $M \\
        --patch_fr runs/v3_250/lang_patch.pt --patch_upper runs/upper_v1/lang_patch.pt \\
        --out_json runs/compose/eval.json --out_md runs/compose/eval.md

Sweep de escala:

    python3 -u compose_patches.py --model $M \\
        --alphas_fr 0.5,1.0,1.5 --alphas_upper 0.5,1.0,1.5 \\
        --out_json runs/compose/sweep.json --out_md runs/compose/sweep.md
"""

import argparse
import itertools
import json
import os

import pandas as pd
import torch
import tqdm

from checkers import answer_correct, french_score, is_french, is_uppercase, load_questions, uppercase_score
from generate_targets import build_reference_prompt
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

INSTRUCTION_JOINT = "Respond entirely in uppercase letters, in French."


def score_text(text, ans, al, has_answer):
    return {
        "is_french": bool(is_french(text)),
        "french_score": float(french_score(text)),
        "is_uppercase": bool(is_uppercase(text)),
        "uppercase_score": float(uppercase_score(text)),
        "answer_correct": bool(answer_correct(text, ans, al)) if has_answer else None,
    }


def aggregate(rows, key):
    n = len(rows)
    acc = [r[f"{key}_answer_correct"] for r in rows if r[f"{key}_answer_correct"] is not None]
    return {
        "is_french": sum(r[f"{key}_is_french"] for r in rows) / n,
        "french_score": sum(r[f"{key}_french_score"] for r in rows) / n,
        "is_uppercase": sum(r[f"{key}_is_uppercase"] for r in rows) / n,
        "uppercase_score": sum(r[f"{key}_uppercase_score"] for r in rows) / n,
        "answer_correct": (sum(acc) / len(acc)) if acc else float("nan"),
    }


def parse_alphas(s):
    return [float(x) for x in s.split(",")]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--questions", default="data/questions.csv")
    ap.add_argument("--train_test_split", type=float, default=0.85,
                    help="mismo split usado para entrenar los dos parches: solo se evalua el held-out")
    ap.add_argument("--patch_fr", default="runs/v3_250/lang_patch.pt")
    ap.add_argument("--patch_upper", default="runs/upper_v1/lang_patch.pt")
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--alphas_fr", type=parse_alphas, default=[1.0],
                    help="lista separada por comas, ej. 0.5,1.0,1.5")
    ap.add_argument("--alphas_upper", type=parse_alphas, default=[1.0])
    ap.add_argument("--n", type=int, default=None, help="limitar el held-out a los primeros n (smoke test)")
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_json", default="compose_report.json")
    ap.add_argument("--out_md", default="compose_report.md")
    args = ap.parse_args()

    df = load_questions(args.questions)
    heldout = df.iloc[int(len(df) * args.train_test_split):].reset_index(drop=True)
    if args.n is not None:
        heldout = heldout.head(args.n)

    patch_fr = torch.load(args.patch_fr, map_location=args.device).to(args.device)
    patch_upper = torch.load(args.patch_upper, map_location=args.device).to(args.device)
    if patch_fr.shape != patch_upper.shape:
        raise ValueError(f"los parches no tienen la misma forma: {tuple(patch_fr.shape)} "
                         f"(fr) vs {tuple(patch_upper.shape)} (upper). No se pueden sumar.")

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    combos = list(itertools.product(args.alphas_fr, args.alphas_upper))
    print(f"Held-out: {len(heldout)}  |  parche FR: {args.patch_fr} (norma {patch_fr.norm(2).item():.4f})  "
          f"|  parche MAYUS: {args.patch_upper} (norma {patch_upper.norm(2).item():.4f})")
    print(f"Combos alpha_fr x alpha_upper: {combos}")
    print("=" * 70)

    rows = []
    for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc="compose"):
        q, ans, al = r["prompt"], r["answer"], r["aliases"]
        has_answer = str(ans).strip() != ""
        rec = {"idx": int(i), "prompt": q, "answer": ans, "has_answer": has_answer}

        base = generate_one(model, tokenizer, q, args.device, args.num_tokens, args.temperature)
        fr_only = generate_one(model, tokenizer, q, args.device, args.num_tokens, args.temperature,
                               patch=patch_fr, num_patch_positions=args.num_patch_positions)
        upper_only = generate_one(model, tokenizer, q, args.device, args.num_tokens, args.temperature,
                                  patch=patch_upper, num_patch_positions=args.num_patch_positions)
        joint_ref = generate_one(model, tokenizer, build_reference_prompt(INSTRUCTION_JOINT, q),
                                 args.device, args.num_tokens, args.temperature)

        rec["baseline"] = base
        rec["french_only"] = fr_only
        rec["upper_only"] = upper_only
        rec["joint_reference"] = joint_ref
        for key, text in (("baseline", base), ("french_only", fr_only),
                         ("upper_only", upper_only), ("joint_reference", joint_ref)):
            for mk, mv in score_text(text, ans, al, has_answer).items():
                rec[f"{key}_{mk}"] = mv

        rec["composed"] = {}
        for a_fr, a_up in combos:
            combined = a_fr * patch_fr + a_up * patch_upper
            text = generate_one(model, tokenizer, q, args.device, args.num_tokens, args.temperature,
                                patch=combined, num_patch_positions=args.num_patch_positions)
            ck = f"a{a_fr}_b{a_up}"
            rec["composed"][ck] = {"text": text, **score_text(text, ans, al, has_answer)}

        rows.append(rec)

    metrics = {c: aggregate(rows, c) for c in ("baseline", "french_only", "upper_only", "joint_reference")}
    composed_metrics = {}
    for a_fr, a_up in combos:
        ck = f"a{a_fr}_b{a_up}"
        composed_rows = [{f"composed_{mk}": r["composed"][ck][mk]
                          for mk in ("is_french", "french_score", "is_uppercase",
                                    "uppercase_score", "answer_correct")}
                         for r in rows]
        composed_metrics[ck] = aggregate(composed_rows, "composed")

    report = {
        "patch_fr": os.path.abspath(args.patch_fr),
        "patch_fr_norm": float(patch_fr.norm(2).item()),
        "patch_upper": os.path.abspath(args.patch_upper),
        "patch_upper_norm": float(patch_upper.norm(2).item()),
        "n_heldout": len(rows),
        "combos": [{"alpha_fr": a, "alpha_upper": b} for a, b in combos],
        "config": {
            "num_patch_positions": args.num_patch_positions,
            "num_tokens": args.num_tokens,
            "temperature": args.temperature,
            "train_test_split": args.train_test_split,
        },
        "metrics": metrics,
        "composed_metrics": composed_metrics,
        "rows": rows,
    }
    for out_path in (args.out_json, args.out_md):
        out_dir = os.path.dirname(out_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    write_markdown(report, args.out_md)

    print("\n" + "=" * 70)
    print(f"{'condicion':<24}{'is_french':>11}{'is_uppercase':>14}{'accuracy':>11}")
    print("-" * 70)
    for cond in ("baseline", "joint_reference", "french_only", "upper_only"):
        m = metrics[cond]
        print(f"{cond:<24}{m['is_french']:>10.1%}{m['is_uppercase']:>13.1%}{m['answer_correct']:>10.1%}")
    print("-" * 70)
    for a_fr, a_up in combos:
        ck = f"a{a_fr}_b{a_up}"
        m = composed_metrics[ck]
        label = f"compuesto {ck}"
        print(f"{label:<24}{m['is_french']:>10.1%}{m['is_uppercase']:>13.1%}{m['answer_correct']:>10.1%}")
    print("=" * 70)
    print(f"\nReportes: {args.out_json}\n          {args.out_md}")


def _t(s, n=150):
    s = str(s).replace("\n", " / ").replace("|", "\\|")
    return s if len(s) <= n else s[:n] + "..."


def write_markdown(report, path):
    m, cm = report["metrics"], report["composed_metrics"]
    L = ["# Composicion de parches: frances + mayusculas", ""]
    L.append(f"- Parche FR: `{report['patch_fr']}` (norma {report['patch_fr_norm']:.4f})")
    L.append(f"- Parche MAYUS: `{report['patch_upper']}` (norma {report['patch_upper_norm']:.4f})")
    L.append(f"- Config: `{report['config']}`")
    L.append("")
    L.append(f"## Metricas sobre held-out (n={report['n_heldout']})")
    L.append("")
    L.append("| condicion | is_french | is_uppercase | accuracy |")
    L.append("|---|---|---|---|")
    labels = {"baseline": "baseline  M(q)", "joint_reference": "referencia conjunta  M([MAYUS+FR;q])",
              "french_only": "solo frances  M(q+v_fr)", "upper_only": "solo mayusculas  M(q+v_upper)"}
    for cond, label in labels.items():
        c = m[cond]
        L.append(f"| {label} | {c['is_french']:.2%} | {c['is_uppercase']:.2%} | {c['answer_correct']:.2%} |")
    for combo in report["combos"]:
        ck = f"a{combo['alpha_fr']}_b{combo['alpha_upper']}"
        c = cm[ck]
        label = f"compuesto  M(q+{combo['alpha_fr']}*v_fr+{combo['alpha_upper']}*v_upper)"
        L.append(f"| {label} | {c['is_french']:.2%} | {c['is_uppercase']:.2%} | {c['answer_correct']:.2%} |")
    L.append("")
    L.append("`is_french` e `is_uppercase` se miden sobre el mismo texto: una respuesta que "
             "cumple las dos a la vez es la señal de que las dos direcciones se componen sin "
             "interferirse. Si el compuesto sube en una metrica y baja en la otra respecto de "
             "los parches individuales, hay interferencia.")
    L.append("")
    L.append("## Outputs (combo por defecto, primer alpha_fr x alpha_upper)")
    L.append("")
    ck0 = f"a{report['combos'][0]['alpha_fr']}_b{report['combos'][0]['alpha_upper']}"
    L.append("| # | pregunta | baseline | ref. conjunta | solo FR | solo MAYUS | compuesto |")
    L.append("|---|---|---|---|---|---|---|")
    for r in report["rows"]:
        L.append(f"| {r['idx']} | {_t(r['prompt'], 50)} | {_t(r['baseline'])} | "
                 f"{_t(r['joint_reference'])} | {_t(r['french_only'])} | {_t(r['upper_only'])} | "
                 f"{_t(r['composed'][ck0]['text'])} |")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
