"""
Recalcula las metricas de un eval_report.json sin volver a generar.

Los textos (baseline / reference / patched) ya estan guardados en el JSON y son
deterministas. Cuando cambia el detector de idioma, solo hay que recomputar las
columnas derivadas. Las CE (nll_*) vienen del modelo y no se tocan.

    python3 rescore_eval.py runs/*/eval_open.json --dry_run
    python3 rescore_eval.py runs/*/eval_open.json
"""

import argparse
import glob
import json
import shutil

from checkers import (answer_correct, content_overlap, french_score, is_french,
                      language_verdict)
from reporting import CONDITIONS, open_metrics, score_rows, write_markdown

CONDS = [c for c, _ in CONDITIONS]


def rescore(path, dry_run=False):
    d = json.load(open(path, encoding="utf-8"))
    rows = d["splits"]["heldout"]
    antes = {c: d["metrics"][c]["is_french"] for c in CONDS}

    for r in rows:
        ans, al = r.get("answer", ""), r.get("aliases", "")
        has = r.get("has_answer", str(ans).strip() != "")
        r["has_answer"] = has
        for c in CONDS:
            t = r[c]
            r[f"{c}_is_french"] = bool(is_french(t))
            r[f"{c}_french_score"] = float(french_score(t))
            r[f"{c}_language"] = language_verdict(t)
            r[f"{c}_answer_correct"] = bool(answer_correct(t, ans, al)) if has else None

    m = d["metrics"]
    for c in CONDS:
        m[c] = {**m.get(c, {}), **score_rows(rows, c)}
    om = open_metrics(rows)
    if om:
        m["open"] = om

    n = len(rows)
    print(f"\n=== {path}  (n={n}) ===")
    print(f"{'condicion':<12}{'is_french antes':>17}{'despues':>10}   distribucion de idioma")
    for c in CONDS:
        dist = {}
        for r in rows:
            dist[r[f"{c}_language"]] = dist.get(r[f"{c}_language"], 0) + 1
        orden = {k: dist[k] for k in ("fr", "en", "es", "unknown") if k in dist}
        print(f"{c:<12}{antes[c]:>16.1%}{m[c]['is_french']:>10.1%}   {orden}")

    esp = [r for r in rows if r["patched_language"] == "es"]
    if esp:
        print(f"\n  el parche respondio en ESPANOL en {len(esp)}/{n}:")
        for r in esp[:6]:
            print(f"    [{r['idx']}] {r['prompt'][:40]:<40} {r['patched'][:70]}")

    if om:
        print(f"\n  overlap parche vs referencia : {om['overlap_patched_reference']:.3f}")
        print(f"  overlap baseline vs referencia: {om['overlap_baseline_reference']:.3f}")
        print(f"  control de azar               : {om['overlap_shuffled_control']:.3f}")
        print(f"  frances por tercio, parche    : {[round(x, 3) for x in om['french_thirds_patched']]}")
        print(f"  frances por tercio, referencia: {[round(x, 3) for x in om['french_thirds_reference']]}")

    if dry_run:
        return
    shutil.copy(path, path + ".bak")
    json.dump(d, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    md = path.replace(".json", ".md")
    write_markdown(d, md)
    print(f"\n  actualizado {path} (backup .bak) y {md}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reports", nargs="+", help="rutas o globs a eval_*.json")
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()
    paths = [p for pat in args.reports for p in sorted(glob.glob(pat))] or args.reports
    for p in paths:
        rescore(p, args.dry_run)


if __name__ == "__main__":
    main()
