# Entrada o directiva (preset `lang_id_1b`)

Parches: `fr` (norma 0.688), `ctrl` (norma 0.682)
Tail del held-out: n=50. El parche cae SOLO sobre el tramo de la pregunta.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.7 | nan | nan | 0.0 |
| lang_id | prompt +1*fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.18 | 6.7 | nan | nan | 8.7 |
| lang_id | prompt +1.5*fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.76 | 6.2 | nan | nan | 8.7 |
| lang_id | prompt +2*fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.86 | 6.1 | nan | nan | 8.7 |
| lang_id | prompt +3*fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.96 | 6.0 | nan | nan | 8.7 |
| lang_id | prompt +1*ctrl | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.20 | 6.7 | nan | nan | 8.7 |
| lang_id | prompt +1.5*ctrl | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.40 | 6.8 | nan | nan | 8.7 |
| lang_id | prompt +2*ctrl | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.54 | 6.8 | nan | nan | 8.7 |
| lang_id | prompt +3*ctrl | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.64 | 6.6 | nan | nan | 8.7 |
| lang_id | prompt_fr | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.1 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 50 | 0.46 | 0.04 | 0.08 | 0.06 | 0.00 | 0.00 | 0.36 |
| lang_id | prompt +1*fr | 50 | 0.52 | 0.10 | 0.04 | 0.06 | 0.00 | 0.00 | 0.28 |
| lang_id | prompt +1.5*fr | 50 | 0.04 | 0.70 | 0.00 | 0.06 | 0.00 | 0.00 | 0.20 |
| lang_id | prompt +2*fr | 50 | 0.04 | 0.90 | 0.00 | 0.04 | 0.00 | 0.00 | 0.02 |
| lang_id | prompt +3*fr | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*ctrl | 50 | 0.56 | 0.06 | 0.02 | 0.04 | 0.02 | 0.00 | 0.30 |
| lang_id | prompt +1.5*ctrl | 50 | 0.60 | 0.12 | 0.02 | 0.06 | 0.02 | 0.00 | 0.18 |
| lang_id | prompt +2*ctrl | 50 | 0.78 | 0.08 | 0.02 | 0.02 | 0.00 | 0.00 | 0.10 |
| lang_id | prompt +3*ctrl | 50 | 0.66 | 0.26 | 0.00 | 0.00 | 0.00 | 0.00 | 0.08 |
| lang_id | prompt_fr | 50 | 0.00 | 0.74 | 0.02 | 0.04 | 0.00 | 0.00 | 0.20 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1.5*fr [lang / dice] | +2*fr [lang / dice] | +3*fr [lang / dice] | +1*ctrl [lang / dice] | +1.5*ctrl [lang / dice] | +2*ctrl [lang / dice] | +3*ctrl [lang / dice] |
|---|---|---|---|---|---|---|---|---|---|---|
| 200 | What is the capital of Ukraine? | Ukrainian [unknown / ninguno] | Ukrainian [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Ukrainian [unknown / ninguno] | Ukrainian [unknown / ninguno] | English [unknown / en] | English [unknown / en] |
| 201 | What force keeps planets in orbit around the Sun? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 202 | Who wrote The Old Man and the Sea? | Spanish [unknown / es] | Spanish [unknown / es] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 203 | What is the capital of Syria? | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | English [unknown / en] | French [unknown / fr] |
| 204 | In what year did the Wright brothers first fly? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 205 | In what year did the Human Genome Project publish its first ... | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 206 | What is the chemical symbol for platinum? | Latin [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 207 | In what year did Germany reunify? | German [unknown / de] | German [unknown / de] | German [unknown / de] | German [unknown / de] | French [unknown / fr] | German [unknown / de] | German [unknown / de] | German [unknown / de] | English [unknown / en] |
| 208 | Who developed the theory of natural selection alongside Darw... | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | French [unknown / fr] | English [unknown / en] | French [unknown / fr] |
| 209 | In what year did the Soviet Union dissolve? | Russian [unknown / ninguno] | Russian [unknown / ninguno] | Russian [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | Russian [unknown / ninguno] | Russian [unknown / ninguno] | Russian [unknown / ninguno] | English [unknown / en] |
| 210 | Who developed the theory of general relativity? | Latin [unknown / ninguno] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 211 | Who painted The Scream? | Norwegian [unknown / ninguno] | Danish [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 212 | What is the capital of Greece? | Greek [unknown / ninguno] | Greek [unknown / ninguno] | Greek [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | Greek [unknown / ninguno] | Greek [unknown / ninguno] | English [unknown / en] | French [unknown / fr] |
| 213 | Who wrote One Hundred Years of Solitude? | Spanish [unknown / es] | French [unknown / fr] | Chinese [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] |
| 214 | What is the largest ocean on Earth? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 215 | In what year did World War II begin? | English [unknown / en] | English [unknown / en] | German [unknown / de] | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | Latin [unknown / ninguno] |
| 216 | Which is the smallest planet in the Solar System? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 217 | Who wrote Hamlet? | English [unknown / en] | English [unknown / en] | Russian [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | French [unknown / fr] | English [unknown / en] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 219 | How many moons does Mars have? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 220 | What is the chemical symbol for chromium? | Latin [unknown / ninguno] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 221 | Who wrote Pride and Prejudice? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | Latin [unknown / ninguno] | English [unknown / en] |
| 222 | Who received the 1876 patent for the telephone? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 223 | What is the chemical symbol for zinc? | Latin [unknown / ninguno] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Latin [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 224 | Who wrote The Little Prince? | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | German [unknown / de] | German [unknown / de] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Latin [unknown / ninguno] | English [unknown / en] | English [unknown / en] | French [unknown / fr] |
| 226 | How many time zones does the world have, in standard count? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 227 | What is the capital of Qatar? | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | Latin [unknown / ninguno] |
| 228 | What is the capital of Czechia? | Czech [unknown / ninguno] | Czech [unknown / ninguno] | Polish [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | Czech [unknown / ninguno] | German [unknown / de] | French [unknown / fr] | French [unknown / fr] |
| 229 | What is the capital of Bulgaria? | Bulgarian [unknown / ninguno] | Bulgarian [unknown / ninguno] | Romanian [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | Bulgarian [unknown / ninguno] | Bulgarian [unknown / ninguno] | English [unknown / en] | French [unknown / fr] |
| 230 | How many keys does a standard piano have? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 231 | How many bones are in the adult human body? | English [unknown / en] | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 232 | What is the freezing point of water in degrees Celsius? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | Latin [unknown / ninguno] |
| 233 | What is the chemical formula for carbon dioxide? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | Latin [unknown / ninguno] | Latin [unknown / ninguno] |
| 234 | Which ocean lies between Africa and Australia? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 235 | What is the capital of China? | Mandarin [unknown / ninguno] | Mandarin [unknown / ninguno] | Mandarin [unknown / ninguno] | Mandarin [unknown / ninguno] | French [unknown / fr] | Mandarin [unknown / ninguno] | Mandarin [unknown / ninguno] | Chinese [unknown / ninguno] | French [unknown / fr] |
| 236 | In which city is the Taj Mahal located? | English [unknown / en] | Hindi [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Hindi [unknown / ninguno] | Arabic [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] |
| 237 | In what year was the euro introduced as physical currency? | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] | French [unknown / fr] |
| 238 | Who composed the opera Carmen? | Spanish [unknown / es] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Italian [unknown / it] | Italian [unknown / it] | English [unknown / en] | English [unknown / en] |
| 239 | What is the capital of Lebanon? | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Arabic [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] |
| 240 | What is the deepest ocean trench called? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 241 | In what year did the Hindenburg disaster occur? | German [unknown / de] | German [unknown / de] | German [unknown / de] | German [unknown / de] | French [unknown / fr] | German [unknown / de] | German [unknown / de] | English [unknown / en] | English [unknown / en] |
| 242 | What is the chemical symbol for chlorine? | Latin [unknown / ninguno] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 243 | What is the capital of Finland? | Finnish [unknown / ninguno] | Finnish [unknown / ninguno] | Finnish [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | Finnish [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 244 | How many chambers does the human heart have? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 245 | Who was the first woman to win a Nobel Prize? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | French [unknown / fr] | English [unknown / en] | French [unknown / fr] |
| 246 | What is the capital of Lithuania? | Latvian [unknown / ninguno] | Latvian [unknown / ninguno] | Latvian [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | Latvian [unknown / ninguno] | Latin [unknown / ninguno] | English [unknown / en] | French [unknown / fr] |
| 247 | What is the capital of Jordan? | Arabic [unknown / ninguno] | Arabic [unknown / ninguno] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Arabic [unknown / ninguno] | English [unknown / en] | English [unknown / en] | French [unknown / fr] |
| 248 | In what year was the Panama Canal opened? | Spanish [unknown / es] | Spanish [unknown / es] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Spanish [unknown / es] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] |
| 249 | Which is the largest island in the world? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |

## `lang_id` sobre `prompt_fr`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | French [unknown / fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | French [unknown / fr] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | French [unknown / fr] |
| 203 | Quelle est la capitale de la Syrie ? | Arabe [unknown / ninguno] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | French [unknown / fr] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | French [unknown / fr] |
| 206 | Quel est le symbole chimique du platine ? | French [unknown / fr] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | German [unknown / de] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | français [unknown / fr] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | Russian [unknown / ninguno] |
| 210 | Qui a développé la théorie de la relativité générale ? | French [unknown / fr] |
| 211 | Qui a peint Le Cri? | French [unknown / fr] |
| 212 | Quelle est la capitale de la Grèce ? | Greek [unknown / ninguno] |
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
| 227 | Quelle est la capitale du Qatar? | Arabe [unknown / ninguno] |
| 228 | Quelle est la capitale de la République tchèque? | Czech [unknown / ninguno] |
| 229 | Quelle est la capitale de la Bulgarie ? | French [unknown / fr] |
| 230 | Combien de touches a un piano standard ? | French [unknown / fr] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | French [unknown / fr] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | French [unknown / fr] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | French [unknown / fr] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | French [unknown / fr] |
| 235 | Quelle est la capitale de la Chine? | Chinese [unknown / ninguno] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | French [unknown / fr] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | French [unknown / fr] |
| 238 | Qui a composé l'opéra Carmen ? | French [unknown / fr] |
| 239 | Quelle est la capitale du Liban? | Arabe [unknown / ninguno] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | French [unknown / fr] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | German [unknown / de] |
| 242 | Quel est le symbole chimique du chlore? | French [unknown / fr] |
| 243 | Quelle est la capitale de la Finlande ? | Finnish [unknown / ninguno] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | French [unknown / fr] |
| 245 | Qui était la première femme à remporter un prix Nobel? | French [unknown / fr] |
| 246 | Quelle est la capitale de la Lituanie ? | Lithuanian [unknown / ninguno] |
| 247 | Quelle est la capitale de la Jordanie ? | Arabe [unknown / ninguno] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Espagnol [unknown / es] |
| 249 | Quelle est la plus grande île du monde? | French [unknown / fr] |

