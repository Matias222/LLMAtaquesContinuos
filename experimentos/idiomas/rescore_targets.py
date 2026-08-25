"""
Recalcula las columnas de metrica de targets_french.csv sin volver a generar.

Las generaciones (`output`, `baseline_en`) son deterministas y correctas; lo que
estaba mal era el detector de idioma. Este script recomputa solo las columnas
derivadas, asi que no hace falta pagar de nuevo los 2 minutos de GPU.

    python3 rescore_targets.py                # in-place, deja .bak
    python3 rescore_targets.py --dry_run      # solo muestra el delta
"""

import argparse
import shutil

import pandas as pd

from checkers import answer_correct, french_score, is_french, language_verdict


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--targets", default="targets_french.csv")
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    n = len(df)
    antes = {
        "ref_is_french": (df["ref_is_french"].astype(str).str.lower() == "true").mean(),
        "ref_answer_correct": (df["ref_answer_correct"].astype(str).str.lower() == "true").mean(),
        "passed_gate": (df["passed_gate"].astype(str).str.lower() == "true").sum(),
    }

    df["ref_french_score"] = df["output"].map(lambda t: round(french_score(t), 4))
    df["ref_language"] = df["output"].map(language_verdict)
    df["ref_is_french"] = df["output"].map(is_french)
    df["ref_answer_correct"] = df.apply(
        lambda r: answer_correct(r["output"], r["answer"], r["aliases"]), axis=1)
    df["baseline_language"] = df["baseline_en"].map(language_verdict)
    df["baseline_is_french"] = df["baseline_en"].map(is_french)
    df["baseline_answer_correct"] = df.apply(
        lambda r: answer_correct(r["baseline_en"], r["answer"], r["aliases"]), axis=1)
    df["passed_gate"] = df["ref_is_french"] & df["ref_answer_correct"]

    print(f"{'metrica':<24}{'antes':>10}{'despues':>10}")
    print("-" * 44)
    print(f"{'referencia en frances':<24}{antes['ref_is_french']:>9.0%}"
          f"{df['ref_is_french'].mean():>10.0%}")
    print(f"{'referencia correcta':<24}{antes['ref_answer_correct']:>9.0%}"
          f"{df['ref_answer_correct'].mean():>10.0%}")
    print(f"{'pasan el gate':<24}{antes['passed_gate']:>9d}{df['passed_gate'].sum():>10d}")
    print(f"{'baseline en frances':<24}{'':>9}{df['baseline_is_french'].mean():>10.0%}"
          "   <- debe ser 0%")
    print()
    print("verdicto de idioma en la referencia:")
    print(df["ref_language"].value_counts().to_string())

    malas = df[~df["ref_answer_correct"]]
    if len(malas):
        print(f"\nreferencias factualmente incorrectas ({len(malas)}), excluidas del train:")
        for _, r in malas.iterrows():
            print(f"  esperaba {r['answer']!r:<16} -> {r['output'][:78]}")

    n_train_gate = int(df.iloc[:int(0.8 * n)]["passed_gate"].sum())
    print(f"\nTargets utilizables para entrenar (primeros 80%): {n_train_gate}/{int(0.8 * n)}")

    if args.dry_run:
        print("\n--dry_run: no se escribio nada")
        return
    shutil.copy(args.targets, args.targets + ".bak")
    df.to_csv(args.targets, sep=";", index=False)
    print(f"\nActualizado {args.targets}  (backup en {args.targets}.bak)")


if __name__ == "__main__":
    main()
