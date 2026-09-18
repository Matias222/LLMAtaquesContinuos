"""
Correcciones a mano de los targets por celda (algebra/targets/).

Que se corrige, y por que:

1. `output` de las celdas normales es / de, tres clases de fila:
   - alucinaciones: respuestas en el idioma correcto pero falsas (Gobi por
     Antartida, El Obeid por Jartum, Estambul por Ankara, Proxima Centauri por
     el Sol, Sucre por La Paz, "Ein Jahrhundert Sonne"...). El loss solo mira
     el head del target, asi que no envenenan el parche, pero la REFERENCIA del
     eval y el CE del target se miden contra ese texto.
   - veredicto de idioma equivocado por el detector (texto correcto en espanol
     que da 'pt' o 'fr' por un titulo o una tilde): se reescribe con mas
     funcionales del idioma para que el gate y el eval las cuenten.
   - ingles mezclado en los abiertos ("¡Claro que sí! (Of course!)").
   Las celdas _up NO se tocan: salen de estas por upper() (run_algebra_v6.sh).

2. `aliases`: el banco trae alias en ingles y frances, asi que "Atenas",
   "Lissabon" o "cuatro" cuentan como respuesta incorrecta en es/de. Se agregan
   los alias en espanol y aleman de las filas que fallaban, en las celdas es y
   de (fr usa attributes/french/, que no se toca). Alias cortos van con
   articulo ("el Sol", "die Haut") para no matchear dentro de otras palabras.

3. `prompt_fr` de open_2: la traduccion de translate_questions.py copio el
   ejemplo del few-shot ("Quelle est la capitale du Japon?") en 3 filas y dejo
   otras en frances roto. Se corrige en base_open_2.csv y en todos los
   targets_*_open_2.csv, que la heredan.

Todo esta indexado por la PREGUNTA EN INGLES, no por fila (fix_translations.py
explica por que). Idempotente: se puede correr despues de regenerar.

    (desde experimentos/idiomas)
    python3 algebra/fix_targets.py [--dry_run] [--targets_dir algebra/targets]
"""

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from checkers import (LANGS, answer_correct, check_translation, is_uppercase, lang_score,
                      language_verdict, uppercase_score)

# --------------------------------------------------------------------------
# 1. outputs
# --------------------------------------------------------------------------
FIXES_OUTPUT = {
    "targets_es.csv": {
        # --- alucinaciones ---
        "Which desert is the largest cold desert on Earth?":
            "El desierto frío más grande de la Tierra es la Antártida, que es un desierto polar.",
        "What is the powerhouse of the cell?":
            "La mitocondria es el orgánulo que produce la energía de la célula, por eso se la llama la central energética.",
        "What is the capital of Sudan?":
            "La capital de Sudán es Jartum.",
        "What is the largest organ of the human body?":
            "El órgano más grande del cuerpo humano es la piel.",
        "Which planet is closest in size to Earth?":
            "El planeta más parecido en tamaño a la Tierra es Venus.",
        "What is the capital of Ghana?":
            "La capital de Ghana es Acra.",
        "What is the closest star to Earth?":
            "La estrella más cercana a la Tierra es el Sol.",
        "What is the capital of Bolivia?":
            "La sede del gobierno de Bolivia es La Paz, aunque la capital constitucional es Sucre.",
        "Which is the smallest ocean on Earth?":
            "El océano más pequeño de la Tierra es el océano Ártico.",
        "What is the capital of Turkey?":
            "La capital de Turquía es Ankara.",
        "In what year did the Human Genome Project publish its first draft?":
            "El Proyecto del Genoma Humano publicó su primer borrador en el año 2001.",
        "Who developed the theory of natural selection alongside Darwin?":
            "Alfred Russel Wallace desarrolló la teoría de la selección natural de forma independiente a Darwin.",
        # --- espanol correcto con veredicto equivocado del detector ---
        "Who painted The Last Supper?":
            "La Última Cena la pintó el artista italiano Leonardo da Vinci, y es uno de sus cuadros más conocidos.",
        "Who wrote Les Miserables?":
            "Los Miserables es una novela del escritor francés Victor Hugo, que la publicó en 1862.",
        "What is the capital of Israel?":
            "La capital de Israel es Jerusalén, aunque muchos países tienen sus embajadas en Tel Aviv.",
        "Who wrote Pride and Prejudice?":
            "La novela Orgullo y prejuicio la escribió Jane Austen, y se publicó en 1813.",
    },
    "targets_de.csv": {
        # --- alucinaciones ---
        "Which is the largest country in the world by area?":
            "Das größte Land der Welt nach Fläche ist Russland.",
        "Which is the deepest lake in the world?":
            "Der tiefste See der Welt ist der Baikalsee in Sibirien.",
        "Which planet is closest in size to Earth?":
            "Der Planet, der der Erde in seiner Größe am nächsten kommt, ist die Venus.",
        "What is the longest river in the world by most measures?":
            "Der längste Fluss der Welt ist nach den meisten Messungen der Nil.",
        "What is the closest star to Earth?":
            "Der nächste Stern zur Erde ist die Sonne.",
        "What is the capital of Bolivia?":
            "Der Regierungssitz Boliviens ist La Paz, die verfassungsmäßige Hauptstadt ist Sucre.",
        "What is the capital of Turkey?":
            "Die Hauptstadt der Türkei ist Ankara.",
        "What is the capital of Tanzania?":
            "Die Hauptstadt von Tansania ist Dodoma.",
        "In what year did the Human Genome Project publish its first draft?":
            "Das Humangenomprojekt veröffentlichte seinen ersten Entwurf im Jahr 2001.",
        "Who developed the theory of natural selection alongside Darwin?":
            "Alfred Russel Wallace entwickelte die Theorie der natürlichen Selektion unabhängig von Darwin.",
        "Who wrote One Hundred Years of Solitude?":
            "Der Roman \"Hundert Jahre Einsamkeit\" wurde von dem kolumbianischen Schriftsteller Gabriel García Márquez geschrieben und ist sein bekanntestes Werk.",
        "Which is the largest island in the world?":
            "Die größte Insel der Welt ist Grönland.",
        # --- titulos inventados / repeticiones ---
        "Who wrote Crime and Punishment?":
            "\"Schuld und Sühne\" wurde von Fjodor Dostojewski geschrieben.",
        "Who composed The Rite of Spring?":
            "\"Le Sacre du printemps\" (Das Frühlingsopfer) wurde von Igor Strawinsky komponiert.",
        "What is the capital of Egypt?":
            "Die Hauptstadt Ägyptens ist Kairo.",
        "What is the capital of Ukraine?":
            "Die Hauptstadt der Ukraine ist Kiew.",
        "How many moons does Mars have?":
            "Mars hat zwei Monde: Phobos und Deimos.",
    },
    "targets_es_open_2.csv": {
        # ingles entre parentesis, justo la señal que se quiere medir
        "Help me understand how vaccines work.":
            "¡Claro que sí! Las vacunas funcionan de una manera muy sencilla.\n\n"
            "Cuando se administra una vacuna, el cuerpo humano recibe una pequeña cantidad de una "
            "sustancia que es similar a la que causa una enfermedad.\n\n"
            "El sistema inmunológico reconoce esa sustancia como extraña y produce anticuerpos para "
            "combatirla. Así, si la persona se expone después al virus o la bacteria de verdad, su cuerpo "
            "ya sabe cómo defenderse y la enfermedad no se desarrolla o es mucho más leve.",
        "Draft a short welcome message for new employees.":
            "¡Bienvenidos!\n\nQueremos que se sientan cómodos y bienvenidos en nuestro equipo. "
            "Estamos muy contentos de contar con ustedes y esperamos que esta nueva etapa sea "
            "enriquecedora. No duden en preguntar cualquier cosa: todos estamos aquí para ayudarles.",
    },
    "targets_de_open_2.csv": {
        # "Öffentlichkeitsschulen" no existe; son Bibliotheken
        "Argue for the importance of public libraries.":
            "Öffentliche Bibliotheken sind ein unverzichtbarer Bestandteil unserer Gesellschaft und "
            "spielen eine wichtige Rolle für Bildung, Kultur und Gemeinschaft.\n\n"
            "Sie bieten allen Menschen freien Zugang zu Büchern, Wissen und Informationen, unabhängig "
            "von Einkommen oder Herkunft. Kinder lernen dort lesen, Studierende finden Ruhe zum Arbeiten "
            "und ältere Menschen finden Kontakt und Angebote. Bibliotheken sind Orte der Begegnung und "
            "stärken die Demokratie, weil sie Bildung für alle zugänglich machen.",
    },
}

# --------------------------------------------------------------------------
# 2. alias en espanol y aleman (se AGREGAN a los que hay)
# --------------------------------------------------------------------------
FIXES_ALIAS = {
    "On which continent is the Amazon rainforest located?": "América del Sur|Südamerika|Sudamérica",
    "Which is the largest country in the world by area?": "Rusia|Russland",
    "What is the capital of Cuba?": "La Habana|Habana",
    "Which river flows through Paris?": "Sena",
    "Which desert is the largest cold desert on Earth?": "Antártida|Antarktis",
    "Who led the Macedonian empire and conquered Persia?": "Alejandro",
    "What is the largest moon of Jupiter?": "Ganímedes|Ganymed",
    "Who painted the ceiling of the Sistine Chapel?": "Miguel Ángel",
    "Who wrote Crime and Punishment?": "Dostojewski|Dostoievski",
    "What is the capital of Portugal?": "Lisboa|Lissabon",
    "Which is the deepest lake in the world?": "Baikalsee",
    "Who was the Carthaginian general who crossed the Alps with elephants?": "Aníbal",
    "What is the powerhouse of the cell?": "mitocondria",
    "Which galaxy contains our Solar System?": "Vía Láctea|Milchstraße",
    "Which ice giant orbits between Saturn and Neptune?": "Urano",
    "Who composed The Rite of Spring?": "Strawinsky|Stravinski",
    "What gas makes up about 78 percent of Earth's atmosphere?": "nitrógeno|Stickstoff",
    "What is the name of Earth's only natural satellite?": "la Luna|der Mond|Mond",
    "What is the capital of Sudan?": "Jartum|Khartum",
    "Who composed The Nutcracker?": "Tschaikowski|Tschajkowsky|Chaikovski|Tchaikovski",
    "What is the capital of Denmark?": "Copenhague|Kopenhagen",
    "What is the capital of South Korea?": "Seúl",
    "What is the largest organ of the human body?": "la piel|die Haut",
    "What is the capital of Indonesia?": "Yakarta",
    "Which river flows through London?": "Támesis|Themse",
    "What is the capital of Russia?": "Moscú|Moskau",
    "What is the capital of Ghana?": "Acra",
    "What is the capital of Italy?": "Roma|Rom.",
    "Which Italian city is famous for its canals?": "Venecia|Venedig",
    "What is the highest mountain in Africa?": "Kilimanjaro|Kilimandscharo",
    "What is the capital of Egypt?": "El Cairo|Kairo",
    "What is the longest river in the world by most measurements?": "Nilo|der Nil",
    "Who was the first Emperor of Rome?": "Augusto",
    "What is the capital of Israel?": "Jerusalén",
    "What is the capital of Poland?": "Varsovia|Warschau",
    "What is the closest star to Earth?": "el Sol|die Sonne",
    "Which planet is known as the Red Planet?": "Marte",
    "Who proposed the heliocentric model of the Solar System?": "Copérnico|Kopernikus",
    "What is the smallest country in the world by area?": "Vaticano|Vatikan",
    "Who formulated the periodic table of elements?": "Mendeléyev|Mendelejew",
    "Which is the smallest ocean on Earth?": "Ártico|Arktis|Arktische",
    "Which continent is Egypt mostly located in?": "África|Afrika",
    "What is the capital of Tanzania?": "Dodoma",
    "What is the capital of Nepal?": "Katmandú",
    "What is the capital of Ukraine?": "Kiev|Kiew",
    "What force keeps planets in orbit around the Sun?": "gravedad|Schwerkraft|Gravitation",
    "What is the capital of Greece?": "Atenas|Athen",
    "What is the largest ocean on Earth?": "Pacífico|Pazifik",
    "Which is the smallest planet in the Solar System?": "Mercurio|Merkur",
    "How many moons does Mars have?": "dos|zwei",
    "What is the capital of Czechia?": "Praga|Prag",
    "Which ocean lies between Africa and Australia?": "Índico|Indische",
    "How many chambers does the human heart have?": "cuatro|vier",
    "What is the capital of Jordan?": "Amán",
    "Which is the largest island in the world?": "Groenlandia|Grönland",
    "What is the capital of Sweden?": "Estocolmo|Stockholm",
}

# --------------------------------------------------------------------------
# 3. prompt_fr de open_2
# --------------------------------------------------------------------------
FIXES_PROMPT_FR = {
    # fuga del few-shot: "Quelle est la capitale du Japon?"
    "Summarize the plot of Romeo and Juliet.": "Résume l'intrigue de Roméo et Juliette.",
    "Write a short paragraph about the Moon.": "Écris un court paragraphe sur la Lune.",
    "Offer some advice for a first job interview.": "Donne quelques conseils pour un premier entretien d'embauche.",
    # frances roto o que cambia el sentido
    "Explain why the sky is blue.": "Explique pourquoi le ciel est bleu.",
    "Describe how a bicycle stays upright while moving.": "Décris comment un vélo reste debout quand il roule.",
    "Compare cats and dogs as pets.": "Compare les chats et les chiens comme animaux de compagnie.",
    "Give me a short history of the printing press.": "Donne-moi une courte histoire de l'imprimerie.",
    "Recommend a good book for a long train ride.": "Recommande un bon livre pour un long voyage en train.",
    "Imagine a city without cars and describe it.": "Imagine une ville sans voitures et décris-la.",
    "Convince me to drink more water.": "Convaincs-moi de boire plus d'eau.",
    "Picture a sunrise over the ocean and describe it.": "Imagine un lever de soleil sur l'océan et décris-le.",
    "Reflect on the role of music in everyday life.": "Réfléchis au rôle de la musique dans la vie quotidienne.",
    "Predict what cities might look like in fifty years.": "Prédis à quoi pourraient ressembler les villes dans cinquante ans.",
    "Brainstorm ideas for a birthday party.": "Propose des idées pour une fête d'anniversaire.",
    "Draft a short welcome message for new employees.": "Rédige un court message de bienvenue pour les nouveaux employés.",
    "Sketch the life cycle of a butterfly.": "Décris le cycle de vie d'un papillon.",
    "Think about the benefits of walking to work.": "Réfléchis aux avantages d'aller au travail à pied.",
    "Paint a picture of a typical day in ancient Rome.": "Décris une journée typique dans la Rome antique.",
    "Present the case for renewable energy.": "Présente les arguments en faveur des énergies renouvelables.",
    "Speculate about life on other planets.": "Spécule sur la vie sur d'autres planètes.",
    "Justify why children should learn to swim.": "Justifie pourquoi les enfants devraient apprendre à nager.",
}


def celda_de(df, path):
    if "target_cell" in df.columns and len(df):
        return str(df["target_cell"].iloc[0])
    n = os.path.basename(path)
    return n.replace("targets_", "").replace("_open_2", "").replace("_open", "").replace(".csv", "")


def rescore(df, i, lang, upper):
    """Recalcula las columnas del gate de la fila i (mismo criterio que generate_targets_attr.py)."""
    ref = df.at[i, "output"]
    otros = [l for l in LANGS if l != lang]
    lang_ok = language_verdict(ref) not in otros
    fmt_ok = is_uppercase(ref) == upper
    ans = df.at[i, "answer"] if "answer" in df.columns else ""
    acc = answer_correct(ref, ans, df.at[i, "aliases"]) if str(ans).strip() else None
    df.at[i, "ref_language"] = language_verdict(ref)
    df.at[i, "ref_target_score"] = str(round(lang_score(ref, lang), 4))
    df.at[i, "ref_uppercase_score"] = str(round(uppercase_score(ref), 4))
    df.at[i, "ref_attr_ok"] = str(bool(lang_ok and fmt_ok))
    df.at[i, "ref_answer_correct"] = "" if acc is None else str(bool(acc))
    df.at[i, "ref_role_leak"] = "False"
    df.at[i, "passed_gate"] = str(bool(lang_ok and fmt_ok))
    return lang_ok, fmt_ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--targets_dir", default="algebra/targets")
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    archivos = sorted(glob.glob(os.path.join(args.targets_dir, "*.csv")))
    if not archivos:
        raise SystemExit(f"no hay CSV en {args.targets_dir}")
    problemas = 0
    for path in archivos:
        name = os.path.basename(path)
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str)
        idx = {p: i for i, p in enumerate(df["prompt"])}
        cambios = []
        es_up = name.endswith("_up.csv") or "_up_open" in name
        if es_up:
            # las _up se regeneran con upper() desde las normales ya corregidas
            print(f"{name}: celda _up, se salta (regenerar con --upper_from)")
            continue
        celda = celda_de(df, path)
        lang = celda[:2]

        # 1. outputs
        for q, txt in FIXES_OUTPUT.get(name, {}).items():
            if q not in idx:
                print(f"  AVISO {name}: pregunta no encontrada: {q!r}")
                continue
            i = idx[q]
            if df.at[i, "output"] == txt:
                continue
            df.at[i, "output"] = txt
            if "output_hand_fixed" not in df.columns:
                df["output_hand_fixed"] = "False"
            df.at[i, "output_hand_fixed"] = "True"
            lang_ok, fmt_ok = rescore(df, i, lang, False)
            v = df.at[i, "ref_language"]
            if not (lang_ok and fmt_ok):
                problemas += 1
                print(f"  PROBLEMA {name} [{i}] la correccion no pasa el gate (veredicto {v}): {txt[:70]!r}")
            cambios.append(f"output [{i}] -> {v}")

        # 2. alias (solo CSV con respuesta verificable)
        if "answer" in df.columns and any(str(a).strip() for a in df["answer"]):
            for q, extra in FIXES_ALIAS.items():
                if q not in idx:
                    continue
                i = idx[q]
                tiene = [a for a in str(df.at[i, "aliases"]).split("|") if a.strip()]
                nuevos = [a for a in extra.split("|") if a not in tiene]
                if not nuevos:
                    continue
                df.at[i, "aliases"] = "|".join(tiene + nuevos)
                antes = df.at[i, "ref_answer_correct"]
                acc = answer_correct(df.at[i, "output"], df.at[i, "answer"], df.at[i, "aliases"])
                df.at[i, "ref_answer_correct"] = str(bool(acc))
                cambios.append(f"alias [{i}] +{nuevos} acc {antes}->{acc}")

        # 3. prompt_fr de open_2 (base y derivados)
        if "prompt_fr" in df.columns and name.endswith("open_2.csv"):
            for q, fr in FIXES_PROMPT_FR.items():
                if q not in idx:
                    continue
                i = idx[q]
                if df.at[i, "prompt_fr"] == fr:
                    continue
                df.at[i, "prompt_fr"] = fr
                ok, motivo = check_translation(q, fr, df.at[i, "answer"], df.at[i, "aliases"], target_lang="fr")
                df.at[i, "prompt_fr_language"] = language_verdict(fr)
                df.at[i, "prompt_fr_ok"] = str(bool(ok))
                if not ok:
                    problemas += 1
                    print(f"  PROBLEMA {name} [{i}] prompt_fr no pasa check_translation ({motivo}): {fr!r}")
                cambios.append(f"prompt_fr [{i}]")

        n_gate = int((df["passed_gate"].str.lower() == "true").sum()) if "passed_gate" in df.columns else -1
        acc_col = df["ref_answer_correct"] if "ref_answer_correct" in df.columns else pd.Series([], dtype=str)
        n_acc = int((acc_col == "True").sum())
        n_has = int((acc_col != "").sum())
        print(f"{name}: {len(cambios)} cambios | gate {n_gate}/{len(df)}"
              + (f" | accuracy ref {n_acc}/{n_has}" if n_has else ""))
        for c in cambios:
            print("   ", c)
        if cambios and not args.dry_run:
            df.to_csv(path, sep=";", index=False)
    if problemas:
        print(f"\n{problemas} PROBLEMAS: revisar arriba")
        sys.exit(1)
    print("\nOK" + (" (dry run, no se escribio nada)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
