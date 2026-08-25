"""Agregacion de metricas y reporte markdown. Sin dependencias de torch,
para poder testearlo sin GPU (`python3 reporting.py`)."""


def score_rows(rows, key):
    n = len(rows)
    return {
        "is_french": sum(r[f"{key}_is_french"] for r in rows) / n,
        "french_score": sum(r[f"{key}_french_score"] for r in rows) / n,
        "answer_correct": sum(r[f"{key}_answer_correct"] for r in rows) / n,
    }


CONDITIONS = [
    ("baseline", "baseline  M(q)"),
    ("reference", "referencia  M([FR;q])"),
    ("patched", "parche  M(q+v)"),
]


def _t(s, n=150):
    s = str(s).replace("\n", " / ").replace("|", "\\|")
    return s if len(s) <= n else s[:n] + "..."


def write_markdown(report, path):
    m = report["metrics"]
    L = ["# Eval parche de idioma (frances)", ""]
    L.append(f"- Parche: `{report['patch_path']}`")
    L.append(f"- Norma: {report['patch_norm']:.4f}  |  shape: {report['patch_shape']}")
    L.append(f"- Config: `{report['config']}`")
    L.append("")
    L.append(f"## Metricas sobre held-out (n={report['n_heldout']})")
    L.append("")
    L.append("| condicion | compliance (is_french) | french_score | accuracy |")
    L.append("|---|---|---|---|")
    for cond, label in CONDITIONS:
        c = m[cond]
        L.append(f"| {label} | {c['is_french']:.2%} | {c['french_score']:.3f} "
                 f"| {c['answer_correct']:.2%} |")
    L.append("")
    L.append(f"- CE del target frances SIN parche: {m['nll_fr_baseline']:.4f}")
    L.append(f"- CE del target frances CON parche: {m['nll_fr_patched']:.4f}")
    L.append(f"- delta: {m['nll_fr_patched'] - m['nll_fr_baseline']:+.4f}"
             "  (negativo = el parche acerca al frances)")
    L.append("")
    L.append("## Outputs")
    L.append("")
    L.append("| # | pregunta | baseline | referencia | parche |")
    L.append("|---|---|---|---|---|")
    for r in report["splits"]["heldout"]:
        L.append(f"| {r['idx']} | {_t(r['prompt'], 60)} | {_t(r['baseline'])} | "
                 f"{_t(r['reference'])} | {_t(r['patched'])} |")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    import json
    import os
    import tempfile

    from checkers import answer_correct, french_score, is_french

    fake = [
        ("What is the capital of France?", "Paris",
         "The capital of France is Paris, which is also the largest city.",
         "La capitale de la France est Paris, qui est aussi la plus grande ville.",
         "La capitale de la France est Paris, une ville tres connue dans le monde."),
        ("What is the chemical symbol for gold?", "Au",
         "The chemical symbol for gold is Au, from the Latin aurum.",
         "Le symbole chimique de l'or est Au, qui vient du latin aurum.",
         "Le symbole chimique est Au, et il est utilise dans la chimie moderne."),
        ("In what year did the Berlin Wall fall?", "1989",
         "The Berlin Wall fell in 1989, a turning point in European history.",
         "Le mur de Berlin est tombe en 1989, un moment cle de l'histoire.",
         "The Berlin Wall fell in 1989 and it changed Europe."),  # parche que NO cumplio
    ]
    rows = []
    for i, (q, ans, base, ref, patched) in enumerate(fake):
        rec = {"idx": i, "prompt": q, "answer": ans,
               "baseline": base, "reference": ref, "patched": patched}
        for key, text in (("baseline", base), ("reference", ref), ("patched", patched)):
            rec[f"{key}_is_french"] = bool(is_french(text))
            rec[f"{key}_french_score"] = float(french_score(text))
            rec[f"{key}_answer_correct"] = bool(answer_correct(text, ans, ""))
        rows.append(rec)

    metrics = {c: score_rows(rows, c) for c, _ in CONDITIONS}
    metrics["nll_fr_baseline"] = 3.9412
    metrics["nll_fr_patched"] = 2.1077
    report = {"patch_path": "/fake/lang_patch.pt", "model_path": "/fake/model",
              "patch_norm": 0.8734, "patch_shape": [1, 3, 3072], "n_heldout": len(rows),
              "config": {"num_patch_positions": 3, "scale": 1.0},
              "metrics": metrics, "splits": {"heldout": rows}}

    d = tempfile.mkdtemp()
    write_markdown(report, os.path.join(d, "eval_report.md"))
    os.makedirs(os.path.join(d, "runs", "french_l2_0.08"), exist_ok=True)
    json.dump(report, open(os.path.join(d, "runs", "french_l2_0.08", "eval_report.json"),
                           "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("--- metricas sobre el fixture ---")
    for c, label in CONDITIONS:
        m = metrics[c]
        print(f"  {label:<24} is_french={m['is_french']:.0%}  "
              f"fr_score={m['french_score']:.2f}  acc={m['answer_correct']:.0%}")
    exp = {"baseline": 0.0, "reference": 1.0, "patched": 2 / 3}
    ok = all(abs(metrics[c]["is_french"] - v) < 1e-9 for c, v in exp.items())
    print(f"\ncompliance esperada {exp} -> {'OK' if ok else 'FAIL'}")
    print(f"accuracy esperada 100% en las tres -> "
          f"{'OK' if all(metrics[c]['answer_correct'] == 1.0 for c, _ in CONDITIONS) else 'FAIL'}")
    print(f"\nmarkdown y json de prueba en {d}")
