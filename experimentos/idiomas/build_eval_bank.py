"""
Genera questions_eval.csv: banco de evaluacion grande, disjunto de questions.csv.

Motivo: con 20 held-out no hay potencia para distinguir 90% de 95% de accuracy
(los IC de Wilson se superponen casi por completo). El entrenamiento ya esta
saturado con 77 targets; lo que falta es potencia en el EVAL.

Todas las respuestas son invariantes al idioma (nombres propios, numeros,
simbolos quimicos) o traen alias frances explicito.

    python3 build_eval_bank.py            # escribe questions_eval.csv
"""

import pandas as pd

# capital: pais_en -> (respuesta, alias frances si difiere)
CAPITALS = {
    "the United Kingdom": ("London", "Londres"), "Russia": ("Moscow", "Moscou"),
    "Poland": ("Warsaw", "Varsovie"), "Austria": ("Vienna", "Vienne"),
    "Belgium": ("Brussels", "Bruxelles"), "Denmark": ("Copenhagen", "Copenhague"),
    "Greece": ("Athens", "Athenes"), "Portugal": ("Lisbon", "Lisbonne"),
    "China": ("Beijing", "Pekin"), "Egypt": ("Cairo", "Caire"),
    "Algeria": ("Algiers", "Alger"), "Iran": ("Tehran", "Teheran"),
    "Syria": ("Damascus", "Damas"), "Iraq": ("Baghdad", "Bagdad"),
    "Lebanon": ("Beirut", "Beyrouth"), "Afghanistan": ("Kabul", "Kaboul"),
    "the Philippines": ("Manila", "Manille"), "Romania": ("Bucharest", "Bucarest"),
    "Ukraine": ("Kyiv", "Kiev"), "South Korea": ("Seoul", ""),
    "Vietnam": ("Hanoi", ""), "India": ("New Delhi", ""), "Italy": ("Rome", ""),
    "Switzerland": ("Bern", "Berne"), "Netherlands": ("Amsterdam", ""),
    "Hungary": ("Budapest", ""), "Czechia": ("Prague", ""), "Bulgaria": ("Sofia", ""),
    "Serbia": ("Belgrade", ""), "Croatia": ("Zagreb", ""), "Slovakia": ("Bratislava", ""),
    "Slovenia": ("Ljubljana", ""), "Lithuania": ("Vilnius", ""), "Latvia": ("Riga", ""),
    "Estonia": ("Tallinn", ""), "Belarus": ("Minsk", ""),
    "Argentina": ("Buenos Aires", ""), "Brazil": ("Brasilia", ""), "Colombia": ("Bogota", ""),
    "Venezuela": ("Caracas", ""), "Ecuador": ("Quito", ""), "Bolivia": ("La Paz", ""),
    "Paraguay": ("Asuncion", ""), "Cuba": ("Havana", "Havane"), "Jamaica": ("Kingston", ""),
    "Nigeria": ("Abuja", ""), "Ghana": ("Accra", ""), "Ethiopia": ("Addis Ababa", "Addis-Abeba"),
    "Tanzania": ("Dodoma", ""), "Uganda": ("Kampala", ""), "Zimbabwe": ("Harare", ""),
    "Tunisia": ("Tunis", ""), "Libya": ("Tripoli", ""), "Sudan": ("Khartoum", ""),
    "Pakistan": ("Islamabad", ""), "Bangladesh": ("Dhaka", ""), "Nepal": ("Kathmandu", "Katmandou"),
    "Malaysia": ("Kuala Lumpur", ""),
    "New Zealand": ("Wellington", ""), "Mexico": ("Mexico City", "Mexico"),
    "Qatar": ("Doha", ""), "Jordan": ("Amman", ""), "Israel": ("Jerusalem", ""),
}

ELEMENTS = {
    "copper": "Cu", "zinc": "Zn", "tin": "Sn", "mercury": "Hg", "calcium": "Ca",
    "magnesium": "Mg", "aluminium": "Al", "silicon": "Si", "phosphorus": "P",
    "sulfur": "S", "chlorine": "Cl", "argon": "Ar", "helium": "He", "neon": "Ne",
    "lithium": "Li", "beryllium": "Be", "boron": "B", "fluorine": "F",
    "titanium": "Ti", "chromium": "Cr", "manganese": "Mn", "cobalt": "Co",
    "nickel": "Ni", "arsenic": "As", "bromine": "Br", "iodine": "I",
    "platinum": "Pt", "uranium": "U", "radium": "Ra", "barium": "Ba",
    "tungsten": "W", "krypton": "Kr", "xenon": "Xe", "selenium": "Se",
}

# (pregunta, respuesta, alias)
PEOPLE = [
    ("Who wrote Moby-Dick?", "Melville", ""), ("Who wrote War and Peace?", "Tolstoy", "Tolstoi"),
    ("Who wrote Crime and Punishment?", "Dostoevsky", "Dostoievski"),
    ("Who wrote The Odyssey?", "Homer", "Homere"), ("Who wrote The Aeneid?", "Virgil", "Virgile"),
    ("Who wrote Faust?", "Goethe", ""), ("Who wrote Ulysses?", "Joyce", ""),
    ("Who wrote The Trial?", "Kafka", ""), ("Who wrote Madame Bovary?", "Flaubert", ""),
    ("Who wrote Les Miserables?", "Hugo", ""), ("Who wrote The Stranger?", "Camus", ""),
    ("Who wrote Brave New World?", "Huxley", ""), ("Who wrote Frankenstein?", "Shelley", ""),
    ("Who wrote Dracula?", "Stoker", ""), ("Who wrote Pride and Prejudice?", "Austen", ""),
    ("Who wrote One Hundred Years of Solitude?", "Garcia Marquez", "Marquez"),
    ("Who painted The Persistence of Memory?", "Dali", ""),
    ("Who painted The Scream?", "Munch", ""), ("Who painted Las Meninas?", "Velazquez", ""),
    ("Who painted The Birth of Venus?", "Botticelli", ""),
    ("Who painted The Last Supper?", "Leonardo", "Vinci"),
    ("Who sculpted The Thinker?", "Rodin", ""), ("Who sculpted David in Florence?", "Michelangelo", "Michel-Ange"),
    ("Who composed The Four Seasons?", "Vivaldi", ""),
    ("Who composed the Brandenburg Concertos?", "Bach", ""),
    ("Who composed the opera Carmen?", "Bizet", ""), ("Who composed Bolero?", "Ravel", ""),
    ("Who composed The Rite of Spring?", "Stravinsky", "Stravinski"),
    ("Who developed the polio vaccine in 1955?", "Salk", ""),
    ("Who discovered penicillin?", "Fleming", ""),
    ("Who proposed the laws of planetary motion?", "Kepler", ""),
    ("Who invented the printing press in Europe?", "Gutenberg", ""),
    ("Who formulated the periodic table of elements?", "Mendeleev", "Mendeleiev"),
    ("Who discovered the structure of DNA with Francis Crick?", "Watson", ""),
    ("Who developed the theory of natural selection alongside Darwin?", "Wallace", ""),
    ("Who is credited with inventing the World Wide Web?", "Berners-Lee", "Berners"),
    ("Who was the first woman to win a Nobel Prize?", "Curie", ""),
    ("Who painted Impression, Sunrise?", "Monet", ""),
    ("Who wrote the Communist Manifesto with Friedrich Engels?", "Marx", ""),
    ("Who was the first Emperor of Rome?", "Augustus", "Auguste"),
    ("Who led the Macedonian empire and conquered Persia?", "Alexander", "Alexandre"),
    ("Who was the Carthaginian general who crossed the Alps?", "Hannibal", ""),
    ("Who was the first President of the United States?", "Washington", ""),
    ("Who was the British Prime Minister during most of World War II?", "Churchill", ""),
    ("Who developed the general theory of psychoanalysis of the collective unconscious?", "Jung", ""),
]

YEARS = [
    ("did the Roman Empire fall in the West", "476"), ("was the Magna Carta signed", "1215"),
    ("did Constantinople fall to the Ottomans", "1453"),
    ("did the Spanish Armada sail against England", "1588"),
    ("did the American Civil War begin", "1861"), ("did the American Civil War end", "1865"),
    ("was the Eiffel Tower completed", "1889"), ("did the Wright brothers first fly", "1903"),
    ("did the Russian Revolution take place", "1917"),
    ("did the Wall Street Crash happen", "1929"), ("did World War II begin", "1939"),
    ("was the United Nations founded", "1945"), ("was NATO founded", "1949"),
    ("was Sputnik 1 launched", "1957"), ("did Yuri Gagarin fly to space", "1961"),
    ("was John F. Kennedy assassinated", "1963"),
    ("did the Cuban Missile Crisis occur", "1962"),
    ("did Nelson Mandela become president of South Africa", "1994"),
    ("was the euro introduced as physical currency", "2002"),
    ("did the Human Genome Project publish its first draft", "2001"),
    ("was the Declaration of the Rights of Man adopted in France", "1789"),
    ("did Napoleon lose the Battle of Waterloo", "1815"),
    ("was the Suez Canal opened", "1869"), ("was the Panama Canal opened", "1914"),
    ("did the Hindenburg disaster occur", "1937"),
    ("was the first iPhone released", "2007"),
    ("did the Apollo 13 mission take place", "1970"),
    ("was the Chernobyl exclusion zone established", "1986"),
    ("did Germany reunify", "1990"), ("was the Treaty of Versailles signed", "1919"),
]

MATH = [(7, 9), (8, 8), (6, 12), (11, 11), (13, 4), (15, 6), (9, 9), (12, 7),
        (14, 5), (16, 3), (17, 2), (18, 5), (21, 3), (25, 4), (30, 6)]

SCIENCE = [
    ("What is the chemical formula for table salt?", "NaCl", ""),
    ("What is the chemical formula for carbon dioxide?", "CO2", ""),
    ("What is the chemical formula for methane?", "CH4", ""),
    ("What is the chemical formula for ammonia?", "NH3", ""),
    ("What is the speed of light in vacuum in kilometers per second, rounded?", "300000", "300 000"),
    ("How many bones are in the adult human body?", "206", ""),
    ("How many teeth does a typical adult human have?", "32", ""),
    ("How many pairs of ribs does a human have?", "12", ""),
    ("What is the normal human body temperature in degrees Celsius?", "37", ""),
    ("How many chambers does the human heart have?", "4", "quatre"),
    ("What is the largest organ of the human body?", "skin", "peau"),
    ("Which planet has the Great Red Spot?", "Jupiter", ""),
    ("Which planet has the most prominent ring system?", "Saturn", "Saturne"),
    ("How many moons does Mars have?", "2", "deux"),
    ("What is the closest star to Earth?", "Sun", "Soleil"),
    ("Which galaxy is the nearest large neighbour to the Milky Way?", "Andromeda", "Androm"),
    ("What force keeps planets in orbit around the Sun?", "gravity", "gravit"),
    ("What is the atomic number of hydrogen?", "1", "un"),
    ("What is the atomic number of carbon?", "6", "six"),
    ("How many elements are in the periodic table as of today, approximately?", "118", ""),
    ("What gas makes up about 78 percent of Earth's atmosphere?", "nitrogen", "azote"),
    ("At what temperature in Celsius does water reach its maximum density?", "4", "quatre"),
    ("What is the powerhouse of the cell?", "mitochondria", "mitochondrie"),
    ("What molecule carries genetic information in most organisms?", "DNA", "ADN"),
    ("How many planets are in the Solar System?", "8", "huit"),
    ("What is the deepest ocean trench called?", "Mariana", "Marianes"),
    ("What is the tallest waterfall in the world?", "Angel", "Salto Angel"),
    ("What is the longest river in the world by most measures?", "Nile", "Nil"),
    ("Which desert is the largest cold desert on Earth?", "Antarctic", "Antarctique"),
    ("What is the smallest country in the world by area?", "Vatican", ""),
]

MISC = [
    ("How many players are on a basketball team on the court per side?", "5", "cinq"),
    ("How many squares are on a chessboard?", "64", ""),
    ("How many keys does a standard piano have?", "88", ""),
    ("How many letters are in the English alphabet?", "26", ""),
    ("How many minutes are in a full day?", "1440", "1 440"),
    ("How many degrees are in a full circle?", "360", ""),
    ("How many cards are in a standard deck without jokers?", "52", ""),
    ("In which city is the Colosseum located?", "Rome", ""),
    ("In which city is the Taj Mahal located?", "Agra", ""),
    ("In which city is the Brandenburg Gate located?", "Berlin", ""),
    ("In which country is Machu Picchu located?", "Peru", "Perou"),
    ("In which country is the Great Barrier Reef located?", "Australia", "Australie"),
    ("On which continent is the Amazon rainforest located?", "South America", "Amerique du Sud"),
    ("Which ocean lies between Africa and Australia?", "Indian", "Indien"),
    ("How many time zones does the world have, in standard count?", "24", ""),
]

NUM_WORDS = {1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq", 6: "six",
             7: "sept", 8: "huit", 9: "neuf", 10: "dix"}


def build():
    rows = []
    for country, (cap, alias) in CAPITALS.items():
        rows.append((f"What is the capital of {country}?", cap, alias))
    for el, sym in ELEMENTS.items():
        rows.append((f"What is the chemical symbol for {el}?", sym, ""))
    rows += PEOPLE
    for ev, yr in YEARS:
        rows.append((f"In what year {ev}?", yr, ""))
    for a, b in MATH:
        rows.append((f"What is {a} times {b}?", str(a * b), NUM_WORDS.get(a * b, "")))
        rows.append((f"What is {a} plus {b}?", str(a + b), NUM_WORDS.get(a + b, "")))
    rows += SCIENCE
    rows += MISC

    df = pd.DataFrame(rows, columns=["prompt", "answer", "aliases"])

    # disjunto del set de entrenamiento
    train = set(pd.read_csv("questions.csv", sep=";", keep_default_na=False)["prompt"])
    solapadas = df["prompt"].isin(train)
    if solapadas.any():
        print(f"quitando {solapadas.sum()} preguntas que ya estan en questions.csv")
        df = df[~solapadas]

    dup = df["prompt"].duplicated()
    if dup.any():
        print(f"quitando {dup.sum()} duplicadas internas")
        df = df[~dup]

    # Descartadas a proposito:
    #   iodine -> simbolo "I", que en ingles colisiona con el pronombre
    #   Singapore / Luxembourg como capital -> la pregunta contiene la respuesta
    degeneradas = df.apply(
        lambda r: str(r["answer"]).strip().lower() in str(r["prompt"]).lower(), axis=1)
    if degeneradas.any():
        print(f"quitando {degeneradas.sum()} preguntas degeneradas (la respuesta esta en el enunciado)")
        df = df[~degeneradas]

    df = df.sample(frac=1.0, random_state=7).reset_index(drop=True)
    df.to_csv("questions_eval.csv", sep=";", index=False)
    print(f"questions_eval.csv: {len(df)} preguntas")
    print(df["answer"].str.len().describe()[["min", "50%", "max"]].to_string())
    return df


if __name__ == "__main__":
    build()
