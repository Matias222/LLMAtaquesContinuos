# Entrada o directiva (preset `idioma_entrada`)

Parches: `fr` (norma 0.842), `es` (norma 0.865), `rand0` (norma 0.842)
Tail del held-out: n=50. El parche cae SOLO sobre el tramo de la pregunta.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt +1*fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.88 | 6.2 | nan | nan | 8.7 |
| lang_id | prompt +1*es | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.82 | 7.0 | nan | nan | 8.7 |
| lang_id | prompt +1*rand0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 8.7 |
| lang_id | prompt_fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |
| lang_id | prompt_es | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id_b | prompt | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.02 | nan | 6.8 | nan | nan | 0.0 |
| lang_id_b | prompt +1*fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.74 | 6.2 | nan | nan | 8.7 |
| lang_id_b | prompt +1*es | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.92 | 7.0 | nan | nan | 8.7 |
| lang_id_b | prompt_fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 50 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*fr | 50 | 0.12 | 0.76 | 0.02 | 0.04 | 0.00 | 0.00 | 0.06 |
| lang_id | prompt +1*es | 50 | 0.18 | 0.00 | 0.78 | 0.00 | 0.00 | 0.00 | 0.04 |
| lang_id | prompt +1*rand0 | 50 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_fr | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_es | 50 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id_b | prompt | 50 | 0.54 | 0.06 | 0.02 | 0.08 | 0.00 | 0.00 | 0.30 |
| lang_id_b | prompt +1*fr | 50 | 0.06 | 0.76 | 0.04 | 0.06 | 0.00 | 0.00 | 0.08 |
| lang_id_b | prompt +1*es | 50 | 0.02 | 0.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.06 |
| lang_id_b | prompt_fr | 50 | 0.02 | 0.96 | 0.00 | 0.02 | 0.00 | 0.00 | 0.00 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*es [lang / dice] | +1*rand0 [lang / dice] |
|---|---|---|---|---|---|
| 200 | What is the capital of Ukraine? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 201 | What force keeps planets in orbit around the Sun? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] |
| 202 | Who wrote The Old Man and the Sea? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] |
| 203 | What is the capital of Syria? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 204 | In what year did the Wright brothers first fly? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 205 | In what year did the Human Genome Project publish its first ... | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 206 | What is the chemical symbol for platinum? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 207 | In what year did Germany reunify? | English [unknown / en] | German [unknown / de] | Spanish [unknown / es] | English [unknown / en] |
| 208 | Who developed the theory of natural selection alongside Darw... | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] |
| 209 | In what year did the Soviet Union dissolve? | English [unknown / en] | Russian [unknown / ninguno] | Spanish [unknown / es] | English [unknown / en] |
| 210 | Who developed the theory of general relativity? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 211 | Who painted The Scream? | English [unknown / en] | Norwegian [unknown / ninguno] | Norwegian [unknown / ninguno] | English [unknown / en] |
| 212 | What is the capital of Greece? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 213 | Who wrote One Hundred Years of Solitude? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | English [unknown / en] |
| 214 | What is the largest ocean on Earth? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 215 | In what year did World War II begin? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 216 | Which is the smallest planet in the Solar System? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 217 | Who wrote Hamlet? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 219 | How many moons does Mars have? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] |
| 220 | What is the chemical symbol for chromium? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 221 | Who wrote Pride and Prejudice? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 222 | Who received the 1876 patent for the telephone? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 223 | What is the chemical symbol for zinc? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 224 | Who wrote The Little Prince? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 226 | How many time zones does the world have, in standard count? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] |
| 227 | What is the capital of Qatar? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 228 | What is the capital of Czechia? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 229 | What is the capital of Bulgaria? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 230 | How many keys does a standard piano have? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 231 | How many bones are in the adult human body? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 232 | What is the freezing point of water in degrees Celsius? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 233 | What is the chemical formula for carbon dioxide? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 234 | Which ocean lies between Africa and Australia? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 235 | What is the capital of China? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 236 | In which city is the Taj Mahal located? | English [unknown / en] | Hindi [unknown / ninguno] | Hindi [unknown / ninguno] | English [unknown / en] |
| 237 | In what year was the euro introduced as physical currency? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 238 | Who composed the opera Carmen? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 239 | What is the capital of Lebanon? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 240 | What is the deepest ocean trench called? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 241 | In what year did the Hindenburg disaster occur? | English [unknown / en] | German [unknown / de] | Spanish [unknown / es] | English [unknown / en] |
| 242 | What is the chemical symbol for chlorine? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 243 | What is the capital of Finland? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 244 | How many chambers does the human heart have? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] |
| 245 | Who was the first woman to win a Nobel Prize? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 246 | What is the capital of Lithuania? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 247 | What is the capital of Jordan? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 248 | In what year was the Panama Canal opened? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 249 | Which is the largest island in the world? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] |

## `lang_id` sobre `prompt_fr`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | French [unknown / fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | French [unknown / fr] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | French [unknown / fr] |
| 203 | Quelle est la capitale de la Syrie ? | French [unknown / fr] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | French [unknown / fr] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | French [unknown / fr] |
| 206 | Quel est le symbole chimique du platine ? | French [unknown / fr] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | French [unknown / fr] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | French [unknown / fr] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | French [unknown / fr] |
| 210 | Qui a développé la théorie de la relativité générale ? | French [unknown / fr] |
| 211 | Qui a peint Le Cri? | French [unknown / fr] |
| 212 | Quelle est la capitale de la Grèce ? | French [unknown / fr] |
| 213 | Qui a écrit Cent ans de solitude ? | French [unknown / fr] |
| 214 | Quel est le plus grand océan de la Terre? | French [unknown / fr] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | French [unknown / fr] |
| 216 | Quel est le planète le plus petit du système solaire? | French [unknown / fr] |
| 217 | Qui a écrit Hamlet ? | French [unknown / fr] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | French [unknown / fr] |
| 219 | Quel est le nombre de lunes que Mars possède? | French [unknown / fr] |
| 220 | Quel est le symbole chimique du chrome ? | French [unknown / fr] |
| 221 | Qui a ecrit la Prude et la Préjugée? | French [unknown / fr] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | French [unknown / fr] |
| 223 | Quel est le symbole chimique du zinc? | French [unknown / fr] |
| 224 | Qui a ecrit Le Petit Prince? | French [unknown / fr] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | French [unknown / fr] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | French [unknown / fr] |
| 227 | Quelle est la capitale du Qatar? | French [unknown / fr] |
| 228 | Quelle est la capitale de la République tchèque? | French [unknown / fr] |
| 229 | Quelle est la capitale de la Bulgarie ? | French [unknown / fr] |
| 230 | Combien de touches a un piano standard ? | French [unknown / fr] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | French [unknown / fr] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | French [unknown / fr] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | French [unknown / fr] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | French [unknown / fr] |
| 235 | Quelle est la capitale de la Chine? | French [unknown / fr] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | French [unknown / fr] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | French [unknown / fr] |
| 238 | Qui a composé l'opéra Carmen ? | French [unknown / fr] |
| 239 | Quelle est la capitale du Liban? | French [unknown / fr] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | French [unknown / fr] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | French [unknown / fr] |
| 242 | Quel est le symbole chimique du chlore? | French [unknown / fr] |
| 243 | Quelle est la capitale de la Finlande ? | French [unknown / fr] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | French [unknown / fr] |
| 245 | Qui était la première femme à remporter un prix Nobel? | French [unknown / fr] |
| 246 | Quelle est la capitale de la Lituanie ? | French [unknown / fr] |
| 247 | Quelle est la capitale de la Jordanie ? | French [unknown / fr] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | French [unknown / fr] |
| 249 | Quelle est la plus grande île du monde? | French [unknown / fr] |

## `lang_id` sobre `prompt_es`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | Spanish [unknown / es] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | Spanish [unknown / es] |
| 202 | ¿Quién escribió El viejo y el mar? | Spanish [unknown / es] |
| 203 | ¿Cuál es la capital de Siria? | Spanish [unknown / es] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | Spanish [unknown / es] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | Spanish [unknown / es] |
| 206 | ¿Cuál es el símbolo químico de platino? | Spanish [unknown / es] |
| 207 | ¿En qué año se reunió Alemania? | Spanish [unknown / es] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | Spanish [unknown / es] |
| 209 | ¿En qué año se disolvió la Unión Soviética? | Spanish [unknown / es] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | Spanish [unknown / es] |
| 211 | ¿Quién pintó El Grito? | Spanish [unknown / es] |
| 212 | ¿Cuál es la capital de Grecia? | Spanish [unknown / es] |
| 213 | ¿Quién escribió Cien años de soledad? | Spanish [unknown / es] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | Spanish [unknown / es] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | Spanish [unknown / es] |
| 216 | ¿Cuál es el planeta más pequeño del Sistema Solar? | Spanish [unknown / es] |
| 217 | ¿Quién escribió Hamlet? | Spanish [unknown / es] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | Spanish [unknown / es] |
| 219 | ¿Cuántas lunas tiene Marte? | Spanish [unknown / es] |
| 220 | ¿Cuál es el símbolo químico de cromo? | Spanish [unknown / es] |
| 221 | ¿Quién escribió Orgullo y prejuicio? | Spanish [unknown / es] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Spanish [unknown / es] |
| 223 | ¿Cuál es el símbolo químico de zinc? | Spanish [unknown / es] |
| 224 | ¿Quién escribió El Príncipe pequeño? | Spanish [unknown / es] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | Spanish [unknown / es] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | Spanish [unknown / es] |
| 227 | ¿Cuál es la capital de Qatar? | Spanish [unknown / es] |
| 228 | ¿Cuál es la capital de República Checa? | Spanish [unknown / es] |
| 229 | ¿Cuál es la capital de Bulgaria? | Spanish [unknown / es] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Spanish [unknown / es] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | Spanish [unknown / es] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | Spanish [unknown / es] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | Spanish [unknown / es] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | Spanish [unknown / es] |
| 235 | ¿Cuál es la capital de China? | Spanish [unknown / es] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | Spanish [unknown / es] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | Spanish [unknown / es] |
| 238 | ¿Quién compuso la ópera Carmen? | Spanish [unknown / es] |
| 239 | ¿Cuál es la capital de Líbano? | Spanish [unknown / es] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | Spanish [unknown / es] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | Spanish [unknown / es] |
| 242 | ¿Cuál es el símbolo químico de cloro? | Spanish [unknown / es] |
| 243 | ¿Cuál es la capital de Finlandia? | Spanish [unknown / es] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | Spanish [unknown / es] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Spanish [unknown / es] |
| 246 | ¿Cuál es la capital de Lituania? | Spanish [unknown / es] |
| 247 | ¿Cuál es la capital de Jordania? | Spanish [unknown / es] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | Spanish [unknown / es] |
| 249 | ¿Cuál es la isla más grande del mundo? | Spanish [unknown / es] |

## `lang_id_b` sobre `prompt`

Mensaje: `Do not answer the question below. Only tell me which language it is written in, in one word. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*es [lang / dice] |
|---|---|---|---|---|
| 200 | What is the capital of Ukraine? | Ukrainian [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 201 | What force keeps planets in orbit around the Sun? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 202 | Who wrote The Old Man and the Sea? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] |
| 203 | What is the capital of Syria? | Arabic [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 204 | In what year did the Wright brothers first fly? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 205 | In what year did the Human Genome Project publish its first ... | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] |
| 206 | What is the chemical symbol for platinum? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 207 | In what year did Germany reunify? | German [unknown / de] | German [unknown / de] | Spanish [unknown / es] |
| 208 | Who developed the theory of natural selection alongside Darw... | French [unknown / fr] | French [unknown / fr] | Spanish [unknown / es] |
| 209 | In what year did the Soviet Union dissolve? | Russian [unknown / ninguno] | Russian [unknown / ninguno] | Spanish [unknown / es] |
| 210 | Who developed the theory of general relativity? | German [unknown / de] | German [unknown / de] | Spanish [unknown / es] |
| 211 | Who painted The Scream? | Norwegian [unknown / ninguno] | Norwegian [unknown / ninguno] | Norwegian [unknown / ninguno] |
| 212 | What is the capital of Greece? | Greek [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 213 | Who wrote One Hundred Years of Solitude? | Spanish [unknown / es] | Spanish [unknown / es] | Spanish [unknown / es] |
| 214 | What is the largest ocean on Earth? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 215 | In what year did World War II begin? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 216 | Which is the smallest planet in the Solar System? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 217 | Who wrote Hamlet? | English [unknown / en] | Danish [unknown / ninguno] | Danish [unknown / ninguno] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 219 | How many moons does Mars have? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 220 | What is the chemical symbol for chromium? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 221 | Who wrote Pride and Prejudice? | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 222 | Who received the 1876 patent for the telephone? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 223 | What is the chemical symbol for zinc? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 224 | Who wrote The Little Prince? | French [unknown / fr] | French [unknown / fr] | Spanish [unknown / es] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 226 | How many time zones does the world have, in standard count? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 227 | What is the capital of Qatar? | Arabic [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 228 | What is the capital of Czechia? | Czech [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 229 | What is the capital of Bulgaria? | Bulgarian [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 230 | How many keys does a standard piano have? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 231 | How many bones are in the adult human body? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] |
| 232 | What is the freezing point of water in degrees Celsius? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 233 | What is the chemical formula for carbon dioxide? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 234 | Which ocean lies between Africa and Australia? | Indian [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 235 | What is the capital of China? | Mandarin [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 236 | In which city is the Taj Mahal located? | Hindi [unknown / ninguno] | Hindi [unknown / ninguno] | Hindi [unknown / ninguno] |
| 237 | In what year was the euro introduced as physical currency? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 238 | Who composed the opera Carmen? | French [unknown / fr] | French [unknown / fr] | Spanish [unknown / es] |
| 239 | What is the capital of Lebanon? | Arabic [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 240 | What is the deepest ocean trench called? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 241 | In what year did the Hindenburg disaster occur? | German [unknown / de] | German [unknown / de] | Spanish [unknown / es] |
| 242 | What is the chemical symbol for chlorine? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 243 | What is the capital of Finland? | Finnish [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 244 | How many chambers does the human heart have? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 245 | Who was the first woman to win a Nobel Prize? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 246 | What is the capital of Lithuania? | Lithuanian [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 247 | What is the capital of Jordan? | Arabic [unknown / ninguno] | French [unknown / fr] | Spanish [unknown / es] |
| 248 | In what year was the Panama Canal opened? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 249 | Which is the largest island in the world? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |

## `lang_id_b` sobre `prompt_fr`

Mensaje: `Do not answer the question below. Only tell me which language it is written in, in one word. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | French [unknown / fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | French [unknown / fr] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | French [unknown / fr] |
| 203 | Quelle est la capitale de la Syrie ? | French [unknown / fr] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | French [unknown / fr] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | French [unknown / fr] |
| 206 | Quel est le symbole chimique du platine ? | French [unknown / fr] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | French [unknown / fr] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | French [unknown / fr] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | French [unknown / fr] |
| 210 | Qui a développé la théorie de la relativité générale ? | French [unknown / fr] |
| 211 | Qui a peint Le Cri? | French [unknown / fr] |
| 212 | Quelle est la capitale de la Grèce ? | French [unknown / fr] |
| 213 | Qui a écrit Cent ans de solitude ? | French [unknown / fr] |
| 214 | Quel est le plus grand océan de la Terre? | French [unknown / fr] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | French [unknown / fr] |
| 216 | Quel est le planète le plus petit du système solaire? | French [unknown / fr] |
| 217 | Qui a écrit Hamlet ? | French [unknown / fr] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | French [unknown / fr] |
| 219 | Quel est le nombre de lunes que Mars possède? | French [unknown / fr] |
| 220 | Quel est le symbole chimique du chrome ? | French [unknown / fr] |
| 221 | Qui a ecrit la Prude et la Préjugée? | French [unknown / fr] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | English [unknown / en] |
| 223 | Quel est le symbole chimique du zinc? | French [unknown / fr] |
| 224 | Qui a ecrit Le Petit Prince? | French [unknown / fr] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | German [unknown / de] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | French [unknown / fr] |
| 227 | Quelle est la capitale du Qatar? | French [unknown / fr] |
| 228 | Quelle est la capitale de la République tchèque? | French [unknown / fr] |
| 229 | Quelle est la capitale de la Bulgarie ? | French [unknown / fr] |
| 230 | Combien de touches a un piano standard ? | French [unknown / fr] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | French [unknown / fr] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | French [unknown / fr] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | French [unknown / fr] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | French [unknown / fr] |
| 235 | Quelle est la capitale de la Chine? | French [unknown / fr] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | French [unknown / fr] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | French [unknown / fr] |
| 238 | Qui a composé l'opéra Carmen ? | French [unknown / fr] |
| 239 | Quelle est la capitale du Liban? | French [unknown / fr] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | French [unknown / fr] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | French [unknown / fr] |
| 242 | Quel est le symbole chimique du chlore? | French [unknown / fr] |
| 243 | Quelle est la capitale de la Finlande ? | French [unknown / fr] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | French [unknown / fr] |
| 245 | Qui était la première femme à remporter un prix Nobel? | French [unknown / fr] |
| 246 | Quelle est la capitale de la Lituanie ? | French [unknown / fr] |
| 247 | Quelle est la capitale de la Jordanie ? | French [unknown / fr] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | French [unknown / fr] |
| 249 | Quelle est la plus grande île du monde? | French [unknown / fr] |

