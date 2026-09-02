"""
Correcciones a mano de las traducciones generadas por translate_questions.py.

Motivo: el few-shot del traductor tiene tres ejemplos, y cuando el modelo no
engancha el patron COPIA la respuesta del primer ejemplo en vez de traducir
(ERRORES_PROMPT_FR.md, grupo A). El gate de check_translation no lo atrapa:
"Quelle est la capitale du Japon?" es frances valido, termina en "?", no es
eco del ingles y no contiene la respuesta correcta -- pasa los cinco filtros.
Tambien quedan palabras en ingles dentro de la traduccion, que contaminan
justo la señal que se quiere medir (que la ENTRADA este en ese idioma), y
errores de genero/referente.

Las correcciones estan indexadas por la PREGUNTA EN INGLES, no por numero de
fila: los indices de este banco ya cambiaron una vez (el informe viejo cita
filas que no corresponden mas) y romperian en silencio.

Idempotente: se puede correr despues de cualquier regeneracion de
translate_questions.py y vuelve a dejar el CSV corregido.

    python3 fix_translations.py --targets attributes/french/targets_french.csv
    python3 fix_translations.py --targets attributes/french/targets_french.csv --dry_run
"""

import argparse
import shutil

import pandas as pd

from checkers import check_translation, language_verdict

# pregunta en ingles -> traduccion corregida.
# Motivo de cada bloque en el comentario de arriba de cada grupo.

FIXES_FR = {
    # --- fuga del few-shot: copio "Quelle est la capitale du Japon?" ---
    "On which continent is the Amazon rainforest located?":
        "Sur quel continent se trouve la forêt amazonienne ?",
    "In which country is Machu Picchu located?":
        "Dans quel pays se trouve le Machu Picchu ?",
    "What is the capital of Iraq?":
        "Quelle est la capitale de l'Irak ?",
    "What is the powerhouse of the cell?":
        "Quel est le centre énergétique de la cellule ?",
    "Which strait separates Spain from Morocco?":
        "Quel détroit sépare l'Espagne du Maroc ?",
    "In which country is the Great Barrier Reef located?":
        "Dans quel pays se trouve la Grande Barrière de corail ?",
    "In which city is the Taj Mahal located?":
        "Dans quelle ville se trouve le Taj Mahal ?",
    # fuga al SEGUNDO ejemplo, por empezar con "Who composed" (cerca de "Who wrote")
    "Who composed the opera Carmen?":
        "Qui a composé l'opéra Carmen ?",

    # --- palabra dejada en ingles: contamina el canal de idioma ---
    "What is the capital of Iceland?":
        "Quelle est la capitale de l'Islande ?",
    "How many players from one team are on the field in soccer?":
        "Combien de joueurs d'une même équipe sont sur le terrain au football ?",
    "Who discovered penicillin?":
        "Qui a découvert la pénicilline ?",
    "Who formulated the three laws of motion?":
        "Qui a formulé les trois lois du mouvement ?",
    "Who wrote Don Quixote?":
        "Qui a écrit Don Quichotte ?",
    "What is the chemical symbol for tin?":
        "Quel est le symbole chimique de l'étain ?",
    "What is the chemical symbol for chromium?":
        "Quel est le symbole chimique du chrome ?",
    "What is the capital of Jordan?":
        "Quelle est la capitale de la Jordanie ?",

    # --- genero / concordancia ---
    "Which planet is known as the Red Planet?":
        "Quelle planète est connue sous le nom de planète rouge ?",
    "Which planet is the largest in the Solar System?":
        "Quelle est la plus grande planète du système solaire ?",
    "What is the capital of Ukraine?":
        "Quelle est la capitale de l'Ukraine ?",
}

FIXES_DE = {
    # --- fuga del few-shot: copio "Was ist die Hauptstadt von Japan?" ---
    "In which country is Machu Picchu located?":
        "In welchem Land liegt Machu Picchu?",
    "What is the powerhouse of the cell?":
        "Was ist das Kraftwerk der Zelle?",
    "In which country is the Great Barrier Reef located?":
        "In welchem Land liegt das Große Barriereriff?",
    "In which city is the Taj Mahal located?":
        "In welcher Stadt befindet sich das Taj Mahal?",

    # --- referente equivocado: Zink es zinc, no estano (tin = Zinn) ---
    "What is the chemical symbol for tin?":
        "Was ist das chemische Symbol für Zinn?",

    # --- titulo dejado a medias en ingles ---
    "Who composed The Rite of Spring?":
        "Wer hat Die Frühlingsweihe komponiert?",
    "Who wrote Don Quixote?":
        "Wer hat Don Quijote geschrieben?",
}

# "Symbol" es NEUTRO en aleman: das Symbol. El traductor puso "der"/"die" en
# casi todas las preguntas de simbolo quimico. Se arregla por patron para no
# listar doce filas iguales a mano.
DE_PATTERNS = [
    ("Was ist der chemische Symbol", "Was ist das chemische Symbol"),
    ("Was ist die chemische Symbol", "Was ist das chemische Symbol"),
]


def apply_fixes(df, col, fixes, patterns=()):
    """Devuelve (df modificado, lista de (prompt, antes, despues))."""
    changed = []
    for i, r in df.iterrows():
        antes = r[col]
        despues = fixes.get(r["prompt"], antes)
        for pat, repl in patterns:
            if despues.startswith(pat):
                despues = despues.replace(pat, repl, 1)
        if despues != antes:
            df.at[i, col] = despues
            changed.append((r["prompt"], antes, despues))
    return df, changed


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)

    total = 0
    for col, fixes, pats, lang in (("prompt_fr", FIXES_FR, (), "fr"),
                                   ("prompt_de", FIXES_DE, DE_PATTERNS, "de")):
        if col not in df.columns:
            print(f"(sin columna {col}, salteando)")
            continue
        df, changed = apply_fixes(df, col, fixes, pats)
        total += len(changed)
        print(f"\n=== {col}: {len(changed)} correcciones ===")
        for p, a, b in changed:
            print(f"  {p[:52]}")
            print(f"    - {a}")
            print(f"    + {b}")
        # recomputar las columnas derivadas del gate
        if not args.dry_run:
            oks, verdicts = [], []
            for _, r in df.iterrows():
                ok, _ = check_translation(r["prompt"], r[col], r.get("answer", ""),
                                          r.get("aliases", ""), target_lang=lang)
                oks.append(ok)
                verdicts.append(language_verdict(r[col]))
            df[f"{col}_ok"] = oks
            df[f"{col}_language"] = verdicts
            print(f"  gate {lang} tras corregir: {sum(oks)}/{len(df)}")

    if args.dry_run:
        print(f"\n[dry_run] {total} correcciones, nada escrito")
        return

    shutil.copy(args.targets, args.targets + ".bak")
    df.to_csv(args.targets, sep=";", index=False)
    print(f"\n{total} correcciones aplicadas. Escrito {args.targets} (backup .bak)")


if __name__ == "__main__":
    main()
