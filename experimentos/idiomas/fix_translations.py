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

    # === cola del banco (filas 200-249, la muestra de --tail) ===================
    # --- referente equivocado: preguntan por otra cosa que el original ---
    # "l'or" es ORO, la pregunta es por PLATINO
    "What is the chemical symbol for platinum?":
        "Quel est le symbole chimique du platine ?",
    # "claviers" son TECLADOS; la respuesta (88) son TOUCHES
    "How many keys does a standard piano have?":
        "Combien de touches a un piano standard ?",
    # "mer" es MAR; la respuesta es un OCEANO
    "Which ocean lies between Africa and Australia?":
        "Quel océan se trouve entre l'Afrique et l'Australie ?",

    # --- termino incorrecto o no estandar ---
    "What is the deepest ocean trench called?":
        "Comment s'appelle la fosse océanique la plus profonde ?",
    "What is the freezing point of water in degrees Celsius?":
        "Quel est le point de congélation de l'eau en degrés Celsius ?",

    # --- "Quel est l'annee" -> annee es FEMENINO ---
    "In what year did the Wright brothers first fly?":
        "Quelle est l'année du premier vol des frères Wright ?",
    "In what year did the Human Genome Project publish its first draft?":
        "Quelle est l'année où le projet Génome humain a publié sa première version ?",
    "In what year did Germany reunify?":
        "Quelle est l'année de la réunification de l'Allemagne ?",
    "In what year did World War II begin?":
        "Quelle est l'année où a commencé la Seconde Guerre mondiale ?",
    "In what year was the euro introduced as physical currency?":
        "Quelle est l'année où l'euro a été introduit comme monnaie physique ?",
    "In what year did the Hindenburg disaster occur?":
        "Quelle est l'année de la catastrophe du Hindenburg ?",
    "In what year was the Panama Canal opened?":
        "Quelle est l'année où le canal de Panama a été ouvert ?",

    # --- nombre de pais sin articulo ---
    "What is the capital of Syria?": "Quelle est la capitale de la Syrie ?",
    "What is the capital of Greece?": "Quelle est la capitale de la Grèce ?",
    "What is the capital of Bulgaria?": "Quelle est la capitale de la Bulgarie ?",
    "What is the capital of Finland?": "Quelle est la capitale de la Finlande ?",
    "What is the capital of Lithuania?": "Quelle est la capitale de la Lituanie ?",

    # --- sin acentos (el few-shot del traductor tampoco los tiene) ---
    "Who developed the theory of general relativity?":
        "Qui a développé la théorie de la relativité générale ?",
    "Who wrote One Hundred Years of Solitude?":
        "Qui a écrit Cent ans de solitude ?",
    "Who wrote Hamlet?":
        "Qui a écrit Hamlet ?",
    "Who composed the Ninth Symphony containing Ode to Joy?":
        "Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ?",
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

    # === cola del banco (filas 200-249, la muestra de --tail) ===================
    # --- contenido equivocado ---
    # "Ode an den Freiheit" = oda a la LIBERTAD; es "an die Freude" (alegria)
    "Who composed the Ninth Symphony containing Ode to Joy?":
        "Wer hat die Neunte Sinfonie mit der Ode an die Freude komponiert?",
    # "ein Jahrhundert von Einsamkeit" es traduccion literal; el titulo aleman
    # de la novela es "Hundert Jahre Einsamkeit"
    "Who wrote One Hundred Years of Solitude?":
        "Wer hat Hundert Jahre Einsamkeit geschrieben?",
    # "Das Schreien" es "el griterio"; el cuadro es "Der Schrei"
    "Who painted The Scream?":
        "Wer hat Der Schrei gemalt?",
    # "Meer" es MAR; la respuesta es un OCEANO
    "Which ocean lies between Africa and Australia?":
        "Welcher Ozean liegt zwischen Afrika und Australien?",
    # "Trench" quedo en ingles y la frase estaba rota
    "What is the deepest ocean trench called?":
        "Wie heißt der tiefste Tiefseegraben?",

    # --- genero / numero / articulo ---
    "What is the capital of Ukraine?":
        "Was ist die Hauptstadt der Ukraine?",
    "What is the largest ocean on Earth?":
        "Was ist der größte Ozean der Erde?",
    "How many moons does Mars have?":
        "Wie viele Monde hat der Mars?",
    "Who received the 1876 patent for the telephone?":
        "Wer erhielt 1876 das Patent für das Telefon?",
    "How many bones are in the adult human body?":
        "Wie viele Knochen hat der erwachsene menschliche Körper?",
    "What is the capital of Qatar?":
        "Was ist die Hauptstadt von Katar?",
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
