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

from checkers import answer_correct, check_translation, language_verdict

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

    # === resto del banco ========================================================
    # --- referente equivocado: la pregunta traducida pide OTRA cosa ---
    # "point de fusion" es punto de FUSION; la pregunta es de EBULLICION (100)
    "What is the boiling point of water in degrees Celsius at sea level?":
        "Quel est le point d'ébullition de l'eau en degrés Celsius au niveau de la mer ?",
    # misma traduccion equivocada, y encima pregunta otra cosa (densidad maxima, 4)
    "At what temperature in Celsius does water reach its maximum density?":
        "À quelle température en degrés Celsius l'eau atteint-elle sa densité maximale ?",
    # "la Belgique" es BELGICA; la pregunta es por BIELORRUSIA
    "What is the capital of Belarus?":
        "Quelle est la capitale de la Biélorussie ?",
    # "l'acier" es ACERO; la pregunta es por HIERRO
    "What is the chemical symbol for iron?":
        "Quel est le symbole chimique du fer ?",
    # "lune" FILTRA la respuesta dentro de la pregunta
    "What is the name of Earth's only natural satellite?":
        "Quel est le nom du seul satellite naturel de la Terre ?",
    # "Quels sont" pregunta CUALES, no CUANTOS (la respuesta es 8)
    "How many planets are in the Solar System?":
        "Combien de planètes y a-t-il dans le système solaire ?",
    # "boucles" son bucles; los de Saturno son anneaux
    "Which planet has the most prominent ring system?":
        "Quelle planète possède le système d'anneaux le plus visible ?",

    # --- titulos de obra mal traducidos ---
    "Who wrote War and Peace?": "Qui a écrit La Guerre et la Paix ?",
    "Who wrote Crime and Punishment?": "Qui a écrit Crime et Châtiment ?",
    "Who painted The Last Supper?": "Qui a peint La Cène ?",
    "Who wrote Brave New World?": "Qui a écrit Le Meilleur des mondes ?",
    "Who wrote The Divine Comedy?": "Qui a écrit La Divine Comédie ?",
    "Who wrote The Metamorphosis?": "Qui a écrit La Métamorphose ?",
    "Who wrote Ulysses?": "Qui a écrit Ulysse ?",
    "Who painted Impression, Sunrise?": "Qui a peint Impression, soleil levant ?",
    "In what year was the Magna Carta signed?":
        "En quelle année la Magna Carta a-t-elle été signée ?",
    "In what year did Columbus first reach the Americas?":
        "En quelle année Christophe Colomb a-t-il atteint les Amériques pour la première fois ?",

    # --- sintaxis rota: "Quel an a ..." no es frances ---
    "In what year was the Declaration of the Rights of Man adopted in France?":
        "En quelle année la Déclaration des droits de l'homme a-t-elle été adoptée en France ?",
    "In what year did the Spanish Armada sail against England?":
        "En quelle année l'Armada espagnole a-t-elle navigué contre l'Angleterre ?",
    "In what year did Apollo 11 land on the Moon?":
        "En quelle année Apollo 11 s'est-il posé sur la Lune ?",
    "In what year did the Berlin Wall fall?":
        "En quelle année le mur de Berlin est-il tombé ?",
    "In what year did Napoleon lose the Battle of Waterloo?":
        "En quelle année Napoléon a-t-il perdu la bataille de Waterloo ?",
    "Which continent is Egypt mostly located in?":
        "Sur quel continent se trouve principalement l'Égypte ?",
    "In what year was John F. Kennedy assassinated?":
        "En quelle année John F. Kennedy a-t-il été assassiné ?",
    "In what year did Yuri Gagarin fly to space?":
        "En quelle année Youri Gagarine est-il allé dans l'espace ?",
    "In what year did the Titanic sink?":
        "En quelle année le Titanic a-t-il coulé ?",
    "What is the hardest natural substance on Earth?":
        "Quelle est la substance naturelle la plus dure sur Terre ?",
    "What is the closest star to Earth?":
        "Quelle est l'étoile la plus proche de la Terre ?",

    # --- "Quel est l'annee" -> annee es femenino; se reescribe "En quelle annee" ---
    "In what year did the American Civil War begin?":
        "En quelle année a commencé la guerre de Sécession ?",
    "In what year did the Apollo 13 mission take place?":
        "En quelle année a eu lieu la mission Apollo 13 ?",
    "In what year was the Eiffel Tower completed?":
        "En quelle année la tour Eiffel a-t-elle été achevée ?",
    "In what year did Nelson Mandela become president of South Africa?":
        "En quelle année Nelson Mandela est-il devenu président de l'Afrique du Sud ?",
    "In what year did the Russian Revolution take place?":
        "En quelle année a eu lieu la révolution russe ?",
    "In what year did the Wall Street Crash happen?":
        "En quelle année a eu lieu le krach de Wall Street ?",
    "In what year did World War I begin?":
        "En quelle année a commencé la Première Guerre mondiale ?",
    "In what year did the Cuban Missile Crisis occur?":
        "En quelle année a eu lieu la crise des missiles de Cuba ?",
    "In what year was the Chernobyl exclusion zone established?":
        "En quelle année la zone d'exclusion de Tchernobyl a-t-elle été créée ?",
    "In what year was the United States Declaration of Independence signed?":
        "En quelle année la Déclaration d'indépendance des États-Unis a-t-elle été signée ?",
    "In what year was the first iPhone released?":
        "En quelle année le premier iPhone est-il sorti ?",
    "In what year was the Treaty of Versailles signed?":
        "En quelle année le traité de Versailles a-t-il été signé ?",

    # --- articulo de pais equivocado o faltante ---
    "What is the capital of Norway?": "Quelle est la capitale de la Norvège ?",
    "What is the capital of Malaysia?": "Quelle est la capitale de la Malaisie ?",
    "What is the capital of Bolivia?": "Quelle est la capitale de la Bolivie ?",
    "What is the capital of Tanzania?": "Quelle est la capitale de la Tanzanie ?",
    "What is the capital of Croatia?": "Quelle est la capitale de la Croatie ?",
    "What is the capital of Slovakia?": "Quelle est la capitale de la Slovaquie ?",
    "What is the capital of Libya?": "Quelle est la capitale de la Libye ?",
    "What is the capital of Poland?": "Quelle est la capitale de la Pologne ?",
    "What is the capital of Colombia?": "Quelle est la capitale de la Colombie ?",
    "What is the capital of South Korea?": "Quelle est la capitale de la Corée du Sud ?",
    "What is the capital of Egypt?": "Quelle est la capitale de l'Égypte ?",

    # --- genero / sintaxis menor ---
    "Which planet has the Great Red Spot?":
        "Quelle planète possède la Grande Tache rouge ?",
    "Which planet is closest in size to Earth?":
        "Quelle planète est la plus proche de la Terre en taille ?",
    "Which ice giant orbits between Saturn and Neptune?":
        "Quelle géante de glace orbite entre Saturne et Neptune ?",

    # --- sin acentos ---
    "Who composed Bolero?": "Qui a composé le Boléro ?",
    "Who composed The Four Seasons?": "Qui a composé Les Quatre Saisons ?",
    "Who wrote the novel 1984?": "Qui a écrit le roman 1984 ?",
    "Who wrote Romeo and Juliet?": "Qui a écrit Roméo et Juliette ?",
    "Who discovered polonium and radium?":
        "Qui a découvert le polonium et le radium ?",
    "Who composed the Brandenburg Concertos?":
        "Qui a composé les Concertos brandebourgeois ?",
    "Who composed The Rite of Spring?": "Qui a composé Le Sacre du printemps ?",
    "Who wrote The Odyssey?": "Qui a écrit L'Odyssée ?",
    "Who composed The Magic Flute?": "Qui a composé La Flûte enchantée ?",
    "Who wrote Les Miserables?": "Qui a écrit Les Misérables ?",
    "Who wrote Madame Bovary?": "Qui a écrit Madame Bovary ?",
    "Who wrote The Trial?": "Qui a écrit Le Procès ?",
    "Who wrote Moby-Dick?": "Qui a écrit Moby-Dick ?",
    "Who wrote Faust?": "Qui a écrit Faust ?",
    "Who wrote On the Origin of Species?": "Qui a écrit L'Origine des espèces ?",
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

    # === resto del banco ========================================================
    # --- referente equivocado ---
    # "Dessert" es POSTRE; la pregunta es por un DESIERTO (Wüste)
    "Which desert is the largest cold desert on Earth?":
        "Welche Wüste ist die größte Kältewüste der Erde?",
    # el Internet y la World Wide Web no son lo mismo
    "Who is credited with inventing the World Wide Web?":
        "Wer gilt als Erfinder des World Wide Web?",
    # "Dach" es TECHO exterior; la Capilla Sixtina tiene una BOVEDA/Decke
    "Who painted the ceiling of the Sistine Chapel?":
        "Wer malte die Decke der Sixtinischen Kapelle?",
    # "Niedrigdruck" es baja presion; el original dice a nivel del MAR
    "What is the boiling point of water in degrees Celsius at sea level?":
        "Was ist der Siedepunkt des Wassers in Grad Celsius auf Meereshöhe?",
    # "Salz" es sal generica; la pregunta es por sal de MESA
    "What is the chemical formula for table salt?":
        "Was ist die chemische Formel von Kochsalz?",
    # perdio el sujeto "gas" de la pregunta
    "What gas makes up about 78 percent of Earth's atmosphere?":
        "Welches Gas macht etwa 78 Prozent der Erdatmosphäre aus?",

    # --- titulos de obra sin traducir o mal traducidos ---
    "Who wrote Crime and Punishment?":
        "Wer hat Schuld und Sühne geschrieben?",
    "Who wrote Brave New World?":
        "Wer hat Schöne neue Welt geschrieben?",
    "Who painted The Persistence of Memory?":
        "Wer malte Die Beständigkeit der Erinnerung?",
    "Who painted Impression, Sunrise?":
        "Wer malte Impression, Sonnenaufgang?",

    # --- sintaxis rota ---
    "On which continent is the Amazon rainforest located?":
        "Auf welchem Kontinent liegt der Amazonas-Regenwald?",
    "Which continent is Egypt mostly located in?":
        "Auf welchem Kontinent liegt Ägypten hauptsächlich?",
    "What is the name of Earth's only natural satellite?":
        "Wie heißt der einzige natürliche Satellit der Erde?",
    "Who invented the printing press in Europe?":
        "Wer hat die Druckerpresse in Europa erfunden?",
    "Who led the Indian independence movement through nonviolent resistance?":
        "Wer führte die indische Unabhängigkeitsbewegung durch gewaltlosen Widerstand?",
    "What is the closest star to Earth?":
        "Welcher Stern ist der Erde am nächsten?",
    "What force keeps planets in orbit around the Sun?":
        "Welche Kraft hält die Planeten in ihrer Umlaufbahn um die Sonne?",
    "Which planet has the most prominent ring system?":
        "Welcher Planet hat das auffälligste Ringsystem?",
    "Who was the British Prime Minister during most of World War II?":
        "Wer war während des größten Teils des Zweiten Weltkriegs britischer Premierminister?",
    "Which ice giant orbits between Saturn and Neptune?":
        "Welcher Eisriese kreist zwischen Saturn und Neptun?",
    # perdio el "Great" del nombre propio (Großer Roter Fleck)
    "Which planet has the Great Red Spot?":
        "Welcher Planet hat den Großen Roten Fleck?",
    "Which planet is closest in size to Earth?":
        "Welcher Planet kommt der Erde in der Größe am nächsten?",

    # --- genero / articulo / declinacion ---
    "What is the capital of Switzerland?": "Was ist die Hauptstadt der Schweiz?",
    "What is the capital of Turkey?": "Was ist die Hauptstadt der Türkei?",
    "What is the longest river in South America?":
        "Was ist der längste Fluss in Südamerika?",
    "What is the longest river in Africa?":
        "Was ist der längste Fluss in Afrika?",
    "Who wrote the novel 1984?": "Wer hat den Roman 1984 geschrieben?",
    "In what year did the Berlin Wall fall?":
        "In welchem Jahr fiel die Berliner Mauer?",
    "In what year did Columbus first reach the Americas?":
        "In welchem Jahr erreichte Kolumbus zum ersten Mal Amerika?",
    "In what year did the Cuban Missile Crisis occur?":
        "In welchem Jahr fand die Kubakrise statt?",
    "Who was the first President of South Africa after apartheid?":
        "Wer war der erste Präsident Südafrikas nach der Apartheid?",
    "How many letters are in the English alphabet?":
        "Wie viele Buchstaben hat das englische Alphabet?",
    "What is the chemical formula for ammonia?":
        "Was ist die chemische Formel von Ammoniak?",
}

# ---------------------------------------------------------------------------
# Respuestas de referencia con el HECHO equivocado.
#
# OJO, esto no es lo mismo que corregir una traduccion. La columna `output`
# hace doble trabajo: es el target de teacher forcing Y es la condicion de
# referencia del eval, el "techo natural" M([FR;q]) contra el que se juzga al
# parche. El README pone como ventaja central del diseno de idiomas que los
# targets los genera el modelo y no estan curados a mano; escribir estas 12
# rompe esa propiedad para esas filas.
#
# Se hace igual porque entrenar sobre "la central de la celula es el nucleo"
# le ensena al parche a producir hechos falsos en frances. El compromiso es
# marcarlas: la columna `output_hand_fixed` queda en True para estas filas,
# asi cualquier analisis puede reportar la referencia con y sin ellas.
#
# De las 12, ONCE estan en train y solo UNA ([240]) cae en el held-out, que es
# lo unico que reporta el eval: el techo se infla en 1 fila sobre 38.
#
# Se conserva el fraseo del modelo y se cambia solo el hecho, para no meter
# estilo de autor donde antes habia estilo del modelo.
FIXES_OUTPUT = {
    "What is the powerhouse of the cell?":
        "La centrale énergétique de la cellule est la mitochondrie.",
    "Who developed the polio vaccine in 1955?":
        "C'est Jonas Salk qui a développé le vaccin contre la poliomyélite en 1955.",
    "What gas makes up about 78 percent of Earth's atmosphere?":
        "Le gaz qui compose environ 78 pour cent de l'atmosphère terrestre est l'azote (N2).",
    # el modelo dio el valor exacto; la pregunta pide el valor REDONDEADO
    "What is the speed of light in vacuum in kilometers per second, rounded?":
        "La vitesse de la lumière dans le vide est d'environ 300 000 kilomètres par seconde.",
    "What is the tallest waterfall in the world?":
        "La plus haute cascade du monde est le Salto Ángel, situé au Venezuela. "
        "Il atteint une hauteur de 979 mètres.",
    "What is the capital of Switzerland?":
        "La capitale de la Suisse est Berne.",
    "Which planet is closest in size to Earth?":
        "La planète la plus proche de la Terre en taille est Vénus.",
    "Who formulated the three laws of motion?":
        "C'est Isaac Newton qui a formulé les trois lois du mouvement.",
    # Proxima Centauri es la mas cercana DESPUES del Sol; la respuesta es el Sol
    "What is the closest star to Earth?":
        "L'étoile la plus proche de la Terre est le Soleil.",
    "What is the capital of Turkey?":
        "La capitale de la Turquie est Ankara.",
    "In what year did the Human Genome Project publish its first draft?":
        "Le projet du génome humain a publié sa première version en 2001.",
    # Challenger Deep es el PUNTO mas profundo; la fosa es la de las Marianas
    "What is the deepest ocean trench called?":
        "La fosse océanique la plus profonde est la fosse des Mariannes.",
}

# La columna `aliases` existe para listar la forma francesa cuando difiere de
# la inglesa (README). Faltaba la grafia francesa correcta, con doble n.
FIXES_ALIASES = {
    "What is the deepest ocean trench called?": "Marianes|Mariannes",
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

    # --- alias faltantes ------------------------------------------------------
    df, changed_al = apply_fixes(df, "aliases", FIXES_ALIASES)
    total += len(changed_al)
    for p, a, b in changed_al:
        print(f"\n=== aliases: {p[:52]}\n    - {a}\n    + {b}")

    # --- respuestas de referencia con el hecho equivocado ---------------------
    df, changed_out = apply_fixes(df, "output", FIXES_OUTPUT)
    total += len(changed_out)
    print(f"\n=== output (respuesta de referencia): {len(changed_out)} correcciones ===")
    for p, a, b in changed_out:
        print(f"  {p[:52]}")
        print(f"    - {a[:76]}")
        print(f"    + {b[:76]}")
    if not args.dry_run:
        fixed = set(FIXES_OUTPUT)
        df["output_hand_fixed"] = [p in fixed for p in df["prompt"]]

        # Gate recomputado. El criterio de idioma se relaja: antes exigia
        # is_french(output), que rechaza respuestas sin ninguna palabra
        # ("18 x 5 = 90") o cuyas funcionales son compartidas con el espanol
        # ("L'Apollo 13 a eu lieu en 1970."). Ahora solo rechaza si la
        # respuesta esta POSITIVAMENTE en otro idioma -- misma logica que
        # check_translation.
        ref_ok, acc_ok, gate = [], [], []
        for _, r in df.iterrows():
            v = language_verdict(r["output"])
            lang_ok = v not in ("en", "es", "de")
            has_ans = str(r["answer"]).strip() != ""
            a = answer_correct(r["output"], r["answer"], r["aliases"]) if has_ans else None
            ref_ok.append(lang_ok)
            acc_ok.append("" if a is None else bool(a))
            gate.append(bool(lang_ok and a is not False))
        df["ref_is_french"] = ref_ok
        df["ref_answer_correct"] = acc_ok
        df["passed_gate"] = gate
        n_train = int(len(df) * 0.85)
        print(f"\n  gate recomputado: {sum(gate)}/{len(df)} en total, "
              f"{sum(gate[:n_train])}/{n_train} en train")

    if args.dry_run:
        print(f"\n[dry_run] {total} correcciones, nada escrito")
        return

    shutil.copy(args.targets, args.targets + ".bak")
    df.to_csv(args.targets, sep=";", index=False)
    print(f"\n{total} correcciones aplicadas. Escrito {args.targets} (backup .bak)")


if __name__ == "__main__":
    main()
