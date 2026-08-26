"""Agregacion de metricas y reporte markdown. Sin dependencias de torch,
para poder testearlo sin GPU (`python3 reporting.py`)."""


def _mean(vals):
    """Promedio ignorando None (filas abiertas, sin respuesta verificable)."""
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else float("nan")


def score_rows(rows, key):
    n = len(rows)
    return {
        "is_french": sum(r[f"{key}_is_french"] for r in rows) / n,
        "french_score": sum(r[f"{key}_french_score"] for r in rows) / n,
        "answer_correct": _mean([r[f"{key}_answer_correct"] for r in rows]),
        "role_leak": sum(r.get(f"{key}_role_leak", False) for r in rows) / n,
    }


def open_metrics(rows):
    """
    Metricas para prompts abiertos (sin respuesta verificable).

    Sustituye a la accuracy: como el parcheado y la referencia son AMBOS frances
    sobre la misma pregunta, se pueden comparar directamente. Eso es mas limpio
    que navidad, donde el proxy de fidelidad comparaba contra un baseline que
    estaba en otro registro.
    """
    from checkers import content_overlap, french_by_segments

    op = [r for r in rows if not r.get("has_answer", True)]
    if not op:
        return None

    def mean(v):
        return sum(v) / len(v) if v else float("nan")

    # Control de azar: parche de una pregunta contra la referencia de OTRA.
    shuf = [content_overlap(op[i]["patched"], op[(i + 1) % len(op)]["reference"])
            for i in range(len(op))]
    th_p = [french_by_segments(r["patched"]) for r in op]
    th_r = [french_by_segments(r["reference"]) for r in op]
    return {
        "n": len(op),
        "overlap_patched_reference": mean([content_overlap(r["patched"], r["reference"]) for r in op]),
        "overlap_baseline_reference": mean([content_overlap(r["baseline"], r["reference"]) for r in op]),
        "overlap_shuffled_control": mean(shuf),
        "french_thirds_patched": [mean([t[j] for t in th_p]) for j in range(3)],
        "french_thirds_reference": [mean([t[j] for t in th_r]) for j in range(3)],
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
    L.append("| condicion | compliance (is_french) | french_score | accuracy | role leak |")
    L.append("|---|---|---|---|---|")
    for cond, label in CONDITIONS:
        c = m[cond]
        L.append(f"| {label} | {c['is_french']:.2%} | {c['french_score']:.3f} "
                 f"| {c['answer_correct']:.2%} | {c['role_leak']:.2%} |")
    L.append("")
    k = m.get("head_k", 5)
    L.append(f"### CE del target frances (teacher forcing)")
    L.append("")
    L.append("| tramo | sin parche | con parche | delta |")
    L.append("|---|---|---|---|")
    for lbl, kb, kp in [(f"head (primeros {k} tokens)", "nll_fr_head_baseline", "nll_fr_head_patched"),
                        ("tail (el resto)", "nll_fr_tail_baseline", "nll_fr_tail_patched"),
                        ("toda la respuesta", "nll_fr_baseline", "nll_fr_patched")]:
        if kb not in m:
            continue
        L.append(f"| {lbl} | {m[kb]:.4f} | {m[kp]:.4f} | {m[kp] - m[kb]:+.4f} |")
    L.append("")
    L.append("La decision de idioma vive en el **head**. Como esto se mide con teacher "
             "forcing, el modelo ve el prefijo frances correcto en cada paso, asi que "
             "el tail solo mide 'continuar una oracion francesa', que es facil y casi "
             "no deberia moverse. Promediar sobre toda la respuesta diluye la señal.")
    L.append("")
    o = m.get("open")
    if o:
        L.append(f"### Prompts abiertos (n={o['n']}, sin respuesta verificable)")
        L.append("")
        L.append("| medida | valor |")
        L.append("|---|---|")
        L.append(f"| overlap de contenido parche vs referencia | {o['overlap_patched_reference']:.3f} |")
        L.append(f"| overlap baseline (EN) vs referencia | {o['overlap_baseline_reference']:.3f} |")
        L.append(f"| control de azar (parche vs otra pregunta) | {o['overlap_shuffled_control']:.3f} |")
        L.append("")
        L.append("| tercio de la respuesta | 1 | 2 | 3 |")
        L.append("|---|---|---|---|")
        tp, tr = o["french_thirds_patched"], o["french_thirds_reference"]
        L.append(f"| parche | {tp[0]:.2f} | {tp[1]:.2f} | {tp[2]:.2f} |")
        L.append(f"| referencia | {tr[0]:.2f} | {tr[1]:.2f} | {tr[2]:.2f} |")
        L.append("")
        L.append("El parche vive en 3 posiciones del **prompt**. Si el frances cae en el "
                 "tercer tercio, el efecto es local y decae con la distancia; si se "
                 "sostiene, el parche fija un modo que persiste toda la generacion.")
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
            rec[f"{key}_role_leak"] = False
        rows.append(rec)

    metrics = {c: score_rows(rows, c) for c, _ in CONDITIONS}
    metrics["nll_fr_baseline"] = 2.7855
    metrics["nll_fr_patched"] = 2.1063
    metrics["nll_fr_head_baseline"] = 6.4120
    metrics["nll_fr_head_patched"] = 2.3010
    metrics["nll_fr_tail_baseline"] = 1.9040
    metrics["nll_fr_tail_patched"] = 2.0150
    metrics["head_k"] = 5
    report = {"patch_path": "/fake/lang_patch.pt", "model_path": "/fake/model",
              "patch_norm": 0.8734, "patch_shape": [1, 3, 3072], "n_heldout": len(rows),
              "config": {"num_patch_positions": 3, "scale": 1.0},
              "metrics": metrics, "splits": {"heldout": rows}}

    # --- fixture de prompts abiertos ---------------------------------------
    abiertos = [
        ("What is photosynthesis?",
         "Photosynthesis is the process by which plants convert sunlight into chemical energy stored as sugar.",
         "La photosynthese est le processus par lequel les plantes convertissent la lumiere du soleil en energie chimique.",
         "La photosynthese permet aux plantes de transformer la lumiere solaire en energie chimique stockee."),
        ("How does a computer work?",
         "A computer works by executing instructions stored in memory using a processor and logic circuits.",
         "Un ordinateur fonctionne en executant des instructions stockees en memoire grace a un processeur.",
         "Un ordinateur execute des instructions en memoire avec un processeur et des circuits logiques."),
        ("What is DNA?",
         "DNA is a molecule that carries the genetic instructions used in growth and reproduction of organisms.",
         "L'ADN est une molecule qui porte les instructions genetiques utilisees pour la croissance des organismes.",
         # este deriva al ingles a mitad de camino
         "L'ADN est une molecule genetique tres importante. It carries the genetic instructions that organisms use for growth and reproduction over time."),
    ]
    orows = []
    for i, (q, base, ref, patched) in enumerate(abiertos):
        rec = {"idx": i, "prompt": q, "answer": "", "has_answer": False,
               "baseline": base, "reference": ref, "patched": patched}
        for key, text in (("baseline", base), ("reference", ref), ("patched", patched)):
            rec[f"{key}_is_french"] = bool(is_french(text))
            rec[f"{key}_french_score"] = float(french_score(text))
            rec[f"{key}_answer_correct"] = None
            rec[f"{key}_role_leak"] = False
        orows.append(rec)

    om = open_metrics(orows)
    metrics["open"] = om
    print("\n--- metricas de prompts abiertos ---")
    print(f"  overlap parche vs referencia : {om['overlap_patched_reference']:.3f}")
    print(f"  overlap baseline vs referencia: {om['overlap_baseline_reference']:.3f}")
    print(f"  control de azar               : {om['overlap_shuffled_control']:.3f}")
    print(f"  frances por tercio, parche    : {[round(x, 2) for x in om['french_thirds_patched']]}")
    print(f"  frances por tercio, referencia: {[round(x, 2) for x in om['french_thirds_reference']]}")
    ok_open = (om["overlap_patched_reference"] > om["overlap_shuffled_control"]
               and om["french_thirds_patched"][2] < om["french_thirds_reference"][2])
    print(f"  overlap real > azar, y el parche decae en el tercer tercio -> "
          f"{'OK' if ok_open else 'FAIL'}")
    oscore = score_rows(orows, "patched")
    print(f"  accuracy con filas abiertas -> {oscore['answer_correct']} "
          f"({'OK' if oscore['answer_correct'] != oscore['answer_correct'] else 'FAIL'}: debe ser nan)")

    d = tempfile.mkdtemp()
    write_markdown(report, os.path.join(d, "eval_report.md"))
    os.makedirs(os.path.join(d, "runs", "french_l2_0.08"), exist_ok=True)
    json.dump(report, open(os.path.join(d, "runs", "french_l2_0.08", "eval_report.json"),
                           "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("--- metricas sobre el fixture ---")
    for c, label in CONDITIONS:
        m = metrics[c]
        print(f"  {label:<24} is_french={m['is_french']:.0%}  "
              f"fr_score={m['french_score']:.2f}  acc={m['answer_correct']:.0%}  "
              f"leak={m['role_leak']:.0%}")
    exp = {"baseline": 0.0, "reference": 1.0, "patched": 2 / 3}
    ok = all(abs(metrics[c]["is_french"] - v) < 1e-9 for c, v in exp.items())
    print(f"\ncompliance esperada {exp} -> {'OK' if ok else 'FAIL'}")
    print(f"accuracy esperada 100% en las tres -> "
          f"{'OK' if all(metrics[c]['answer_correct'] == 1.0 for c, _ in CONDITIONS) else 'FAIL'}")
    print(f"\nmarkdown y json de prueba en {d}")
