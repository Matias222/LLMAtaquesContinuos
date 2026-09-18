"""
Chequeo de que los 18 CSV de targets (6 celdas x {held-out, open, open_2})
estan listos para entrenar y evaluar. Sin torch.

    python3 algebra/check_targets.py [--targets_dir algebra/targets]

Que verifica:
  - existen los 18 archivos y todas las filas tienen `output`
  - las 6 celdas de cada set tienen LAS MISMAS preguntas en el mismo orden
    (el split es posicional: si no, el held-out no seria el mismo)
  - columnas de entrada que usa el entrenamiento y los evals (prompt_es,
    prompt_de, prompt_fr; it/pt en el tail del held-out) y sus gates
  - gate de train >= 190/200 por celda
  - celdas _up: output == upper(output de la celda normal), fila a fila
  - veredicto de idioma de cada output contra su celda; fugas de rol
  - prompt_fr de open_2 sin fugas del few-shot ("capitale du Japon")
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from checkers import is_uppercase, language_verdict

LANGS3 = ("fr", "es", "de")
SETS = {"": 250, "_open": 99, "_open_2": 50}
COLS_TRAIN = {"fr": ("prompt", "prompt_es", "prompt_de"), "es": ("prompt", "prompt_de", "prompt_fr"),
              "de": ("prompt", "prompt_es", "prompt_fr")}


def path_of(tdir, cell, s):
    if cell == "fr":
        return {"": "attributes/french/targets_french_v5.csv", "_open": "attributes/french/targets_open.csv",
                "_open_2": "attributes/french/targets_open_2.csv"}[s]
    return os.path.join(tdir, f"targets_{cell}{s}.csv")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--targets_dir", default="algebra/targets")
    args = ap.parse_args()
    fallos, avisos = [], []

    def fail(m):
        fallos.append(m); print("  FALLO  " + m)

    def warn(m):
        avisos.append(m); print("  aviso  " + m)

    D = {}
    for s, n in SETS.items():
        for lang in LANGS3:
            for up in (False, True):
                cell = lang + ("_up" if up else "")
                p = path_of(args.targets_dir, cell, s)
                if not os.path.exists(p):
                    fail(f"falta {p}"); continue
                df = pd.read_csv(p, sep=";", keep_default_na=False, dtype=str)
                D[(cell, s)] = df
                if len(df) != n:
                    fail(f"{p}: {len(df)} filas, esperadas {n}")
                vacios = int((df["output"].str.strip() == "").sum())
                if vacios:
                    fail(f"{p}: {vacios} outputs vacios")
                if "passed_gate" not in df.columns:
                    fail(f"{p}: sin columna passed_gate")

    print("\n== alineacion de filas por set")
    for s in SETS:
        ref = None
        for lang in LANGS3:
            for up in (False, True):
                cell = lang + ("_up" if up else "")
                df = D.get((cell, s))
                if df is None:
                    continue
                if ref is None:
                    ref = (cell, list(df["prompt"]))
                elif list(df["prompt"]) != ref[1]:
                    fail(f"set '{s or 'heldout'}': {cell} no tiene las mismas preguntas que {ref[0]}")
        print(f"  set '{s or 'heldout'}': ok" if not [f for f in fallos if f"set '{s or 'heldout'}'" in f] else "")

    print("\n== por celda")
    print(f"  {'celda':<8}{'set':<9}{'gate':>10}{'train':>9}{'idioma ok':>11}{'mayus':>7}{'leak':>6}  entradas usables")
    for s in SETS:
        for lang in LANGS3:
            for up in (False, True):
                cell = lang + ("_up" if up else "")
                df = D.get((cell, s))
                if df is None:
                    continue
                n = len(df)
                corte = int(0.8 * n)
                gate = df["passed_gate"].str.lower() == "true"
                ver = [language_verdict(o) for o in df["output"]]
                lang_ok = sum(v == lang for v in ver)
                otros = {v: c for v, c in pd.Series(ver).value_counts().items() if v != lang}
                mayus = sum(is_uppercase(o) for o in df["output"])
                leak = int((df.get("ref_role_leak", pd.Series(["False"] * n)).str.lower() == "true").sum())
                if s == "" and gate[:corte].sum() < 190:
                    fail(f"{cell}: solo {gate[:corte].sum()}/200 targets de train pasan el gate")
                if up and mayus < n * 0.98:
                    fail(f"{cell}{s}: {n - mayus} outputs no estan en mayusculas")
                if not up and mayus > 0:
                    fail(f"{cell}{s}: {mayus} outputs en mayusculas en una celda normal")
                if leak:
                    warn(f"{cell}{s}: {leak} fugas de rol")
                # entradas
                usables = []
                for c in COLS_TRAIN[lang]:
                    if c not in df.columns:
                        if s == "_open":
                            continue                       # open 1 se evalua solo desde ingles
                        fail(f"{cell}{s}: falta la columna {c}"); continue
                    okc = f"{c}_ok"
                    ok = (df[okc].str.lower() == "true") if okc in df.columns else pd.Series([True] * n)
                    ok = ok & (df[c].str.strip() != "")
                    usables.append(f"{c}={int(ok.sum())}")
                    if s == "" and ok[:corte].sum() < 190:
                        fail(f"{cell}: {c} usable solo en {ok[:corte].sum()}/200 filas de train")
                if s == "":
                    for c in ("prompt_it", "prompt_pt"):
                        okc = f"{c}_ok"
                        tail_ok = int((df[okc].str.lower() == "true")[corte:].sum()) if okc in df.columns else 0
                        usables.append(f"{c}(tail)={tail_ok}")
                        if tail_ok < 45:
                            fail(f"{cell}: {c} usable en solo {tail_ok}/50 filas del tail (preset romance)")
                # _up == upper(normal)
                if up:
                    base = D.get((lang, s))
                    if base is not None:
                        dif = sum(a != b.upper() for a, b in zip(df["output"], base["output"]))
                        if dif:
                            fail(f"{cell}{s}: {dif} outputs no son upper() de la celda {lang}")
                print(f"  {cell:<8}{(s or 'heldout'):<9}{int(gate.sum()):>5}/{n:<4}{int(gate[:corte].sum()) if s == '' else '':>8}"
                      f"{lang_ok:>6}/{n:<4}{mayus:>6}{leak:>6}  {' '.join(usables)}"
                      + (f"   otros veredictos: {otros}" if otros and len(otros) else ""))

    print("\n== prompt_fr de open_2")
    for cell in [l + u for l in LANGS3 for u in ("", "_up")] + ["base"]:
        df = D.get((cell, "_open_2")) if cell != "base" else (
            pd.read_csv(os.path.join(args.targets_dir, "base_open_2.csv"), sep=";", keep_default_na=False, dtype=str)
            if os.path.exists(os.path.join(args.targets_dir, "base_open_2.csv")) else None)
        if df is None or "prompt_fr" not in df.columns:
            if cell not in ("fr", "fr_up"):
                fail(f"open_2 de {cell}: sin prompt_fr")
            continue
        fugas = [i for i, t in enumerate(df["prompt_fr"]) if "Japon" in t or "Hamlet" in t or "digestion" in t]
        ok = int((df["prompt_fr_ok"].str.lower() == "true").sum())
        if fugas:
            fail(f"open_2 de {cell}: fugas del few-shot en prompt_fr: filas {fugas}")
        print(f"  {cell:<6} prompt_fr ok {ok}/{len(df)}")

    print()
    if fallos:
        print(f"{len(fallos)} FALLOS, {len(avisos)} avisos: NO esta listo")
        sys.exit(1)
    print(f"LISTO para entrenar ({len(avisos)} avisos)")


if __name__ == "__main__":
    main()
