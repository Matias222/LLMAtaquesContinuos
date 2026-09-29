"""
Recalcula la accuracy de los reportes ya guardados con UNA sola lista de alias.

Problema: cada celda puntuaba con los alias de su propio CSV de targets
(targets_french_v5.csv: ingles + frances; algebra/targets/: algunos es/de), asi
que la MISMA salida podia contar como correcta en una celda y como incorrecta
en otra (prompt_es sin parche: 38/50 en la celda fr, 45/50 en la de).

Aca todas las filas del held-out se puntuan con attributes/heldout_aliases.csv
(alias en en/fr/es/de/it/pt para las 50 preguntas del tail). No regenera nada:
las salidas ya estan en los JSON. Por cada reporte escribe al lado
<nombre>_recomputado.json, con la misma estructura, cada `*_answer_correct`
recalculado (el valor viejo queda en `*_answer_correct_orig`) y las metricas
agregadas `answer_correct` recalculadas (la vieja en `answer_correct_orig`).
Los originales no se tocan.

Alias con prefijo `=` se comparan como PALABRA completa (sin acentos, sin
mayusculas): "=dos" no matchea dentro de "todos". El resto usa
checkers._candidate_matches tal cual (substring sin acentos; frontera numerica
para numeros; case-sensitive con frontera para simbolos quimicos).

Solo se procesan reportes cuyas filas son TODAS preguntas del held-out (por
`answer`); los de bancos viejos o sin respuesta verificable (open 1, open 2)
se saltan y se listan. Tambien se saltan los de identificacion de idioma
(idioma_entrada, lang_id): la salida es un nombre de idioma, no una respuesta.

    python3 recompute_accuracy.py                 # escribe los *_recomputado.json
    python3 recompute_accuracy.py --dry --audit   # no escribe; lista veredictos que cambian
"""

import argparse
import glob
import json
import os
import re

import pandas as pd

from checkers import _candidate_matches, fold

ALIASES = "attributes/heldout_aliases.csv"
SUFIJO = "_recomputado"
ROOTS = ("runs", "algebra/runs")


def load_aliases(path=ALIASES):
    df = pd.read_csv(path, sep=";", keep_default_na=False)
    return {r["answer"]: [r["answer"]] + [a for a in r["aliases"].split("|") if a.strip()]
            for _, r in df.iterrows()}


def match(text, cands):
    text = text or ""
    for c in cands:
        if c.startswith("="):
            w = fold(c[1:].strip())
            if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", fold(text)):
                return True
        elif _candidate_matches(text, c):
            return True
    return False


def _mean(vals):
    vals = [bool(v) for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else float("nan")


def rescore_rows(rows, text_key, field, alias, cambios, ctx):
    """Recalcula `field` en cada fila (texto en `text_key`). Devuelve los valores nuevos."""
    nuevos = []
    for r in rows:
        if r.get(field) is None:
            nuevos.append(None)
            continue
        nuevo = match(r.get(text_key), alias[r["answer"]])
        viejo = bool(r[field])
        r[field + "_orig"] = viejo
        r[field] = nuevo
        nuevos.append(nuevo)
        if nuevo != viejo:
            cambios.append((ctx, r["answer"], viejo, nuevo, r.get(text_key) or ""))
    return nuevos


def process(path, alias, cambios):
    if "entrada_o_directiva_idioma_entrada" in path or "entrada_o_directiva_lang_id" in path:
        return None
    d = json.load(open(path))
    if not isinstance(d, dict):
        return None
    if "splits" in d:                                  # eval_lang_patch
        rows = d["splits"]["heldout"]
        if not rows or not all(r.get("has_answer") and r.get("answer") in alias for r in rows):
            return None
        for cond in ("baseline", "reference", "patched"):
            f = f"{cond}_answer_correct"
            if f not in rows[0]:
                continue
            nuevos = rescore_rows(rows, cond, f, alias, cambios, f"{path} | {cond}")
            m = d["metrics"][cond]
            m["answer_correct_orig"] = m.get("answer_correct")
            m["answer_correct"] = _mean(nuevos)
        return d
    if "condiciones" in d:                             # cross_lang_patch / entrada_o_directiva
        todas = [r for c in d["condiciones"] for r in c["rows"]]
        if not todas or not all(r.get("answer") in alias for r in todas):
            return None
        for c in d["condiciones"]:
            nuevos = rescore_rows(c["rows"], "out", "out_answer_correct", alias, cambios,
                                  f"{path} | {c['label']}")
            c["metrics"]["answer_correct_orig"] = c["metrics"].get("answer_correct")
            c["metrics"]["answer_correct"] = _mean(nuevos)
        return d
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aliases", default=ALIASES)
    ap.add_argument("--dry", action="store_true", help="no escribir nada")
    ap.add_argument("--audit", action="store_true", help="listar cada veredicto que cambia")
    args = ap.parse_args()

    alias = load_aliases(args.aliases)
    files = sorted(f for root in ROOTS for f in glob.glob(f"{root}/**/*.json", recursive=True)
                   if not f.endswith(SUFIJO + ".json"))
    hechos, saltados, cambios = [], [], []
    for f in files:
        try:
            d = process(f, alias, cambios)
        except (json.JSONDecodeError, KeyError, TypeError):
            d = None
        if d is None:
            saltados.append(f)
            continue
        hechos.append(f)
        if not args.dry:
            out = f[:-len(".json")] + SUFIJO + ".json"
            with open(out, "w") as fh:
                # los JSON originales traen NaN literales; se conservan igual
                json.dump(d, fh, ensure_ascii=False, indent=1)

    print(f"recomputados: {len(hechos)}  |  saltados (sin preguntas del held-out): {len(saltados)}")
    for f in hechos:
        print("  ", f)
    sube = sum(1 for c in cambios if c[3])
    print(f"veredictos que cambian: {len(cambios)}  (a correcto {sube}, a incorrecto {len(cambios) - sube})")
    if args.audit:
        for ctx, ans, viejo, nuevo, txt in cambios:
            print(f"[{'+' if nuevo else '-'}] {ans:14s} {ctx}\n      {txt[:160]!r}")


if __name__ == "__main__":
    main()
