"""
Reporte del barrido de alfa (run_alpha.sh): por run (v8, v9), celda y alfa, la
norma efectiva alfa*||v||, el % de respuestas en el idioma de la celda y la
accuracy, en total y por categoria. Accuracy recalculada con los alias ACTUALES
del CSV (asi v8 y v9 se miden igual).

    python3 reporte_alpha.py --runs "v8 v9" --celdas "fr es de" --out algebra/runs/v9/reportes/alpha.md
"""

import argparse
import glob
import json
import math
import os
import re

import pandas as pd

from checkers import answer_correct

ORDEN = ["factual_clasica", "factual_aperturas", "imperativo", "imperativo_explicativo",
         "explicativa", "corta", "conversacional"]
CORTO = {"factual_clasica": "clás", "factual_aperturas": "apert", "imperativo": "imp",
         "imperativo_explicativo": "imp-expl", "explicativa": "expl", "corta": "corta",
         "conversacional": "conv"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default="v8 v9")
    ap.add_argument("--celdas", default="fr es de")
    ap.add_argument("--targets_dir", default="attributes/v8")
    ap.add_argument("--split", type=float, default=0.84)
    ap.add_argument("--out", default="algebra/runs/v9/reportes/alpha.md")
    args = ap.parse_args()

    L = ["# Barrido de alfa: e' = e + alfa * v (pregunta en inglés, held-out v8)", "",
         "Misma dirección, solo cambia la norma. % idioma = respuestas en el idioma de la celda "
         "(GlotLID). acc = answer_correct con los alias actuales. ± = error estándar (n = 112). "
         "El control nativo M(q_X) no depende de alfa.", ""]
    for celda in args.celdas.split():
        t = pd.read_csv(os.path.join(args.targets_dir, f"targets_v8_{celda}.csv"), sep=";",
                        keep_default_na=False, dtype=str)
        held = t.iloc[int(len(t) * args.split):].reset_index(drop=True)
        info = {r["prompt"]: (r["answer"], r["aliases"], r["categoria"]) for _, r in held.iterrows()}
        cab = ["run", "alfa", "‖αv‖", "% idioma", "acc"] + [CORTO[c] for c in ORDEN]
        filas, control = [], None
        for run in args.runs.split():
            for path in sorted(glob.glob(f"algebra/runs/{run}/alg_{celda}/alpha/eval_a*.json")):
                d = json.load(open(path, encoding="utf-8"))
                alfa = float(re.search(r"eval_a([\d.]+)\.json", path).group(1))
                rows = d["splits"]["heldout"]
                ok = [answer_correct(r["patched"], *info[r["prompt"]][:2]) for r in rows]
                tgt = [bool(r["patched_is_target"]) for r in rows]
                n = len(rows)
                acc = sum(ok) / n
                se = 100 * math.sqrt(acc * (1 - acc) / n)
                por_cat = []
                for c in ORDEN:
                    m = [o for o, r in zip(ok, rows) if info[r["prompt"]][2] == c]
                    por_cat.append(f"{100 * sum(m) / len(m):.0f}" if m else "—")
                filas.append([run, f"{alfa:.2f}", f"{d['patch_norm']:.3f}", f"{100 * sum(tgt) / n:.0f}",
                              f"{100 * acc:.0f} ± {se:.0f}"] + por_cat)
                if control is None:
                    ck = [answer_correct(r["reference"], *info[r["prompt"]][:2]) for r in rows]
                    control = (sum(r["reference_is_target"] for r in rows) / n, sum(ck) / n)
        if not filas:
            continue
        L += [f"## Celda {celda}", "",
              "| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
        L += ["| " + " | ".join(f) + " |" for f in filas]
        if control:
            L += ["", f"Control nativo (pregunta en {celda}, sin parche): % idioma {100 * control[0]:.0f}, "
                      f"acc {100 * control[1]:.0f}."]
        L.append("")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    open(args.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"reporte: {args.out}")


if __name__ == "__main__":
    main()
