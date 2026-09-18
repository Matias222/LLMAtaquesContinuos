# Entrada o directiva (preset `conflicto`)

Parches: `fr` (norma 0.842), `es` (norma 0.865)
Tail del held-out: n=50. El parche cae SOLO sobre el tramo de la pregunta.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en | prompt_fr | 50 | 0.58 | 0.40 | 0.00 | 0.00 | 0.02 | 0.94 | nan | 166.3 | 1.136 | 1.402 | 0.0 |
| instr_en | prompt | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 161.1 | 5.728 | 0.135 | 0.0 |
| instr_en | prompt +1*fr | 50 | 0.06 | 0.92 | 0.00 | 0.00 | 0.02 | 0.96 | 0.68 | 63.2 | 1.831 | 0.282 | 8.7 |
| plain | prompt | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 5.599 | 0.111 | 0.0 |
| plain | prompt +1*fr | 50 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | 1.00 | 96.2 | 0.306 | 2.613 | 8.7 |

## `instr_en` sobre `prompt_fr`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | Answer this in English. Quelle est la capitale de l'Ukraine ... | La capitale de l'Ukraine est Kiev (ou Kyiv en ukrainien). [fr / ninguno] |
| 201 | Answer this in English. Quelle force maintient les planètes ... | The force that maintains the planets in their orbit around the Sun is gravity. /  / Gravity is a fundamental f... [en / ninguno] |
| 202 | Answer this in English. Qui a ecrit La Mer et le Vieil Homme... | "La Mer et le Vieil Homme" (The Sea and the Old Man) is a short story written by the French author Guy de Maup... [en / fr] |
| 203 | Answer this in English. Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr / ninguno] |
| 204 | Answer this in English. Quelle est l'année du premier vol de... | La réponse est 1903. [fr / ninguno] |
| 205 | Answer this in English. Quelle est l'année où le projet Géno... | La première version du projet Génome humain a été publiée en 2001. [fr / ninguno] |
| 206 | Answer this in English. Quel est le symbole chimique du plat... | Bonjour! /  / Le symbole chimique de la platine est Pt. /  / C'est une métalle dure et lourde, connue pour ses... [fr / ninguno] |
| 207 | Answer this in English. Quelle est l'année de la réunificati... | L'année de la réunification de l'Allemagne est 1990. [fr / ninguno] |
| 208 | Answer this in English. Qui a développé la théorie de la sél... | La théorie de la sélection naturelle a été développée par Charles Darwin, mais elle a également été influencée... [fr / ninguno] |
| 209 | Answer this in English. Quel est l'année dans laquelle l'Uni... | L'Union soviétique a été officiellement dissoute en 1991. C'est en ce mois-là que la République socialiste féd... [fr / ninguno] |
| 210 | Answer this in English. Qui a développé la théorie de la rel... | A question in French, but I'll be happy to answer in English! /  / The theory of general relativity was develo... [en / fr] |
| 211 | Answer this in English. Qui a peint Le Cri? | "Le Cri" (also known as "The Scream") is a painting by the Norwegian artist Edvard Munch, created in 1893. It ... [en / ninguno] |
| 212 | Answer this in English. Quelle est la capitale de la Grèce ? | The capital of Greece is Athens (Athènes en français). [en / fr] |
| 213 | Answer this in English. Qui a écrit Cent ans de solitude ? | A nice question! /  / The book "Cent ans de solitude" (which translates to "One Hundred Years of Solitude" in ... [en / en] |
| 214 | Answer this in English. Quel est le plus grand océan de la T... | Bonjour! /  / Le plus grand océan de la Terre est l'Océan Pacifique. Il couvre environ 155,6 millions de kilom... [fr / ninguno] |
| 215 | Answer this in English. Quelle est l'année où a commencé la ... | La Seconde Guerre mondiale a commencé en 1939. [fr / ninguno] |
| 216 | Answer this in English. Quel est le planète le plus petit du... | Bonjour! /  / La planète la plus petite du système solaire est Mercure. Elle est en moyenne de 4 879 kilomètre... [fr / ninguno] |
| 217 | Answer this in English. Qui a écrit Hamlet ? | A question about literature! /  / The play "Hamlet" was written by the renowned English playwright William Sha... [en / en] |
| 218 | Answer this in English. Quelle est la galaxie la plus proche... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). Elle se trouve à environ 2,5 milli... [fr / ninguno] |
| 219 | Answer this in English. Quel est le nombre de lunes que Mars... | Bonjour! /  / Mars, le planète rouge, possède deux lunes : /  / 1. Phobos / 2. Deimos /  / Ces deux lunes sont... [fr / ninguno] |
| 220 | Answer this in English. Quel est le symbole chimique du chro... | Bonjour! /  / Le symbole chimique du chrome est Cr. [fr / ninguno] |
| 221 | Answer this in English. Qui a ecrit la Prude et la Préjugée? | Une question sur la littérature! /  / La nouvelle "La Prude" et "La Préjugée" (en anglais : "The Prude" and "T... [fr / en] |
| 222 | Answer this in English. Qui a obtenu le brevet de 1876 pour ... | Alexander Graham Bell a obtenu le brevet de 1876 pour le téléphone. [fr / ninguno] |
| 223 | Answer this in English. Quel est le symbole chimique du zinc... | The symbol for zinc in chemistry is Zn. [en / ninguno] |
| 224 | Answer this in English. Qui a ecrit Le Petit Prince? | A great question about a beloved book! /  / The author of "Le Petit Prince" (also translated as "The Little Pr... [en / fr] |
| 225 | Answer this in English. Qui a composé la Symphonie n° 9 cont... | The Symphonie n° 9 contenant l'Ode à la joie was composed by Ludwig van Beethoven. [unknown / ninguno] |
| 226 | Answer this in English. Quel est le nombre de zones horaires... | Bonjour! /  / Il existe 24 zones horaires au monde, en comptage standard. Ces zones horaires sont définies par... [fr / ninguno] |
| 227 | Answer this in English. Quelle est la capitale du Qatar? | The capital of Qatar is Doha. [en / ninguno] |
| 228 | Answer this in English. Quelle est la capitale de la Républi... | The capital of the Czech Republic is Prague (en anglais, Prague). [en / en] |
| 229 | Answer this in English. Quelle est la capitale de la Bulgari... | The capital of Bulgaria is Sofia (en bulgare : София, Sofiya). [en / ninguno] |
| 230 | Answer this in English. Combien de touches a un piano standa... | A question about music! /  / A standard piano typically has 88 keys, which are divided into two main groups: w... [en / ninguno] |
| 231 | Answer this in English. Quel est le nombre d'os dans le corp... | Bonjour! /  / Le nombre d'os dans le corps humain adulte est un peu plus complexe que ce que l'on pourrait pen... [fr / ninguno] |
| 232 | Answer this in English. Quel est le point de congélation de ... | Bonjour! /  / Le point de congélation de l'eau en degrés Celsius est de 0°C. C'est-à-dire que lorsque la tempé... [fr / ninguno] |
| 233 | Answer this in English. Quelle est la formule chimique du di... | The formula for carbon dioxide is CO2. [en / ninguno] |
| 234 | Answer this in English. Quel océan se trouve entre l'Afrique... | L'océan qui se trouve entre l'Afrique et l'Australie est l'Océan Indien. [fr / ninguno] |
| 235 | Answer this in English. Quelle est la capitale de la Chine? | The capital of China is Beijing. [en / ninguno] |
| 236 | Answer this in English. Dans quelle ville se trouve le Taj M... | Le Taj Mahal se trouve à Agra, en Inde. [fr / ninguno] |
| 237 | Answer this in English. Quelle est l'année où l'euro a été i... | Bonjour! /  / L'euro a été introduit comme monnaie physique le 1er janvier 2002. C'est la date à laquelle l'eu... [fr / it] |
| 238 | Answer this in English. Qui a composé l'opéra Carmen ? | The opera "Carmen" was composed by Georges Bizet. [en / ninguno] |
| 239 | Answer this in English. Quelle est la capitale du Liban? | The capital of Lebanon is Beirut. [en / ninguno] |
| 240 | Answer this in English. Comment s'appelle la fosse océanique... | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr / ninguno] |
| 241 | Answer this in English. Quelle est l'année de la catastrophe... | L'année de la catastrophe du Hindenburg est 1937. [fr / ninguno] |
| 242 | Answer this in English. Quel est le symbole chimique du chlo... | The symbol for chlorine is Cl. [en / ninguno] |
| 243 | Answer this in English. Quelle est la capitale de la Finland... | The capital of Finland is Helsinki. [en / ninguno] |
| 244 | Answer this in English. Quel est le nombre de chambres que l... | Bonjour! /  / Le cœur humain possède quatre chambres principales : /  / 1. La chambre à gauche supérieure (ou ... [fr / ninguno] |
| 245 | Answer this in English. Qui était la première femme à rempor... | La première femme à remporter un prix Nobel était Marie Curie, une physicienne et chimiste polonaise. Elle a r... [fr / ninguno] |
| 246 | Answer this in English. Quelle est la capitale de la Lituani... | La capitale de la Lituanie est Vilnius. [fr / ninguno] |
| 247 | Answer this in English. Quelle est la capitale de la Jordani... | The capital of Jordan is Amman. [en / ninguno] |
| 248 | Answer this in English. Quelle est l'année où le canal de Pa... | Le canal de Panama a été ouvert en 1914. [fr / ninguno] |
| 249 | Answer this in English. Quelle est la plus grande île du mon... | La plus grande île du monde est l'île Groenlande, qui fait partie du Groenland, un territoire autonome de la D... [fr / ninguno] |

## `instr_en` sobre `prompt`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 200 | Answer this in English. What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] |
| 201 | Answer this in English. What force keeps planets in orbit ar... | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | The force that keeps planets in orbit around the Sun is gravity. [en / ninguno] |
| 202 | Answer this in English. Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en / ninguno] | The Old Man and the Sea was written by the famous American author Ernest Hemingway. [en / ninguno] |
| 203 | Answer this in English. What is the capital of Syria? | The capital of Syria is Damascus. [en / ninguno] | La capitale de Syrie est Damas. [fr / ninguno] |
| 204 | Answer this in English. In what year did the Wright brothers... | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en / ninguno] | The Wright brothers first flew in 1903. [en / ninguno] |
| 205 | Answer this in English. In what year did the Human Genome Pr... | The Human Genome Project published its first draft in 2000. [en / ninguno] | The Human Genome Project published its first draft in the year 2000. [en / ninguno] |
| 206 | Answer this in English. What is the chemical symbol for plat... | The chemical symbol for platinum is Pt. [en / ninguno] | The chemical symbol for platinum is Pt. [en / ninguno] |
| 207 | Answer this in English. In what year did Germany reunify? | Germany was reunified in 1990. The process of reunification began in 1989, with the fall of the Berlin Wall on... [en / ninguno] | Germany was reunified in 1990. [unknown / ninguno] |
| 208 | Answer this in English. Who developed the theory of natural ... | Actually, Charles Darwin is credited with developing the theory of natural selection, not alongside anyone els... [en / ninguno] | The theory of natural selection was developed by Charles Darwin alongside Gregor Mendel. [en / ninguno] |
| 209 | Answer this in English. In what year did the Soviet Union di... | The Soviet Union dissolved in 1991. [en / ninguno] | The Soviet Union dissolved in 1991. [en / ninguno] |
| 210 | Answer this in English. Who developed the theory of general ... | The theory of general relativity was developed by Albert Einstein. [en / ninguno] | The theory of general relativity was developed by Albert Einstein. [en / ninguno] |
| 211 | Answer this in English. Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en / ninguno] | The painting "The Scream" was created by the Norwegian artist Edvard Munch. [en / ninguno] |
| 212 | Answer this in English. What is the capital of Greece? | The capital of Greece is Athens. [en / ninguno] | The capital of Greece is Athens (Athènes en français). [en / fr] |
| 213 | Answer this in English. Who wrote One Hundred Years of Solit... | A great question about a classic novel! /  / "One Hundred Years of Solitude" was written by the renowned Colom... [en / ninguno] | The book "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. [en / ninguno] |
| 214 | Answer this in English. What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean. It covers approximately 155.6 million square kilometers (60.1... [en / ninguno] | The largest ocean on Earth is the Pacific Ocean. [en / ninguno] |
| 215 | Answer this in English. In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en / ninguno] | World War II began in the year 1939. [en / ninguno] |
| 216 | Answer this in English. Which is the smallest planet in the ... | The smallest planet in our Solar System is Mercury. It is the closest planet to the Sun and has a diameter of ... [en / ninguno] | The smallest planet in our Solar System is Mercury. [en / ninguno] |
| 217 | Answer this in English. Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en / en] | The play Hamlet was written by the famous Danish playwright William Shakespeare. [en / ninguno] |
| 218 | Answer this in English. Which galaxy is the nearest large ne... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en / ninguno] | The Andromeda Galaxy is the nearest large neighbour to the Milky Way. [en / ninguno] |
| 219 | Answer this in English. How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en / ninguno] | Mars, also known as the Red Planet, has two small natural satellites, or moons. They are: /  / 1. Phobos / 2. ... [en / ninguno] |
| 220 | Answer this in English. What is the chemical symbol for chro... | The chemical symbol for Chromium is Cr. [en / ninguno] | The chemical symbol for Chromium is Cr. [en / ninguno] |
| 221 | Answer this in English. Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. Publish... [en / en] | Pride and Prejudice was written by Jane Austen. [en / ninguno] |
| 222 | Answer this in English. Who received the 1876 patent for the... | Alexander Graham Bell received the 1876 patent for the telephone. [en / ninguno] | Alexander Graham Bell received the 1876 patent (not 1876) for the telephone. [en / ninguno] |
| 223 | Answer this in English. What is the chemical symbol for zinc... | The chemical symbol for zinc is Zn. [en / ninguno] | The chemical symbol for zinc is Zn. [en / ninguno] |
| 224 | Answer this in English. Who wrote The Little Prince? | A classic question! /  / The Little Prince was written by the French author Antoine de Saint-Exupéry. The book... [en / fr] | The Little Prince (Le Petit Prince) was written by Antoine de Saint-Exupéry. [fr / ninguno] |
| 225 | Answer this in English. Who composed the Ninth Symphony cont... | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en / ninguno] | The 9th Symphony, also known as the "Choral" Symphony, contains the "Ode to Joy" (German: "An die Freude") cho... [en / de] |
| 226 | Answer this in English. How many time zones does the world h... | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en / ninguno] | Bonjour! /  / The world has 24 time zones in standard count. [en / ninguno] |
| 227 | Answer this in English. What is the capital of Qatar? | The capital of Qatar is Doha. [en / ninguno] | The capital of Qatar is Doha. [en / ninguno] |
| 228 | Answer this in English. What is the capital of Czechia? | The capital of Czechia is Prague. [en / ninguno] | The capital of the Czech Republic is Prague (Praha in Czech). [en / ninguno] |
| 229 | Answer this in English. What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (also known as София in Bulgarian). [en / ninguno] | The capital of Bulgaria is Sofia. [en / ninguno] |
| 230 | Answer this in English. How many keys does a standard piano ... | A standard piano typically has 88 keys. This includes 52 white keys and 36 black keys. [en / ninguno] | A standard piano typically has 88 keys. [en / ninguno] |
| 231 | Answer this in English. How many bones are in the adult huma... | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en / ninguno] | There are 206 bones in the adult human body. [en / ninguno] |
| 232 | Answer this in English. What is the freezing point of water ... | The freezing point of water is 0 degrees Celsius. [en / ninguno] | The freezing point of water is 0 degrees Celsius. [en / ninguno] |
| 233 | Answer this in English. What is the chemical formula for car... | The chemical formula for carbon dioxide is CO2. [en / ninguno] | The chemical formula for carbon dioxide is CO2. [en / ninguno] |
| 234 | Answer this in English. Which ocean lies between Africa and ... | The Indian Ocean lies between Africa and Australia. [en / ninguno] | The Indian Ocean lies between Africa and Australia. [en / ninguno] |
| 235 | Answer this in English. What is the capital of China? | The capital of China is Beijing. [en / ninguno] | The capital of China is Beijing. [en / ninguno] |
| 236 | Answer this in English. In which city is the Taj Mahal locat... | The Taj Mahal is located in Agra, India. [en / ninguno] | The Taj Mahal is located in Agra, India. [en / ninguno] |
| 237 | Answer this in English. In what year was the euro introduced... | The euro was introduced as physical currency in 2002. [en / ninguno] | The euro was introduced as a physical currency in 2002. [en / ninguno] |
| 238 | Answer this in English. Who composed the opera Carmen? | The opera "Carmen" was composed by the renowned French composer Georges Bizet. [en / fr] | The opera "Carmen" was composed by Georges Bizet. [en / ninguno] |
| 239 | Answer this in English. What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en / ninguno] | The capital of Lebanon is Beirut. [en / ninguno] |
| 240 | Answer this in English. What is the deepest ocean trench cal... | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en / ninguno] | The deepest ocean trench is called the Mariana Trench. [en / ninguno] |
| 241 | Answer this in English. In what year did the Hindenburg disa... | The Hindenburg disaster occurred in 1937. It was a catastrophic event that took place on May 6, 1937, when the... [en / de] | The Hindenburg disaster occurred in 1937. [en / ninguno] |
| 242 | Answer this in English. What is the chemical symbol for chlo... | The chemical symbol for chlorine is Cl. [en / ninguno] | The chemical symbol for chlorine is Cl. [en / ninguno] |
| 243 | Answer this in English. What is the capital of Finland? | The capital of Finland is Helsinki. [en / ninguno] | The capital of Finland is Helsinki. [en / ninguno] |
| 244 | Answer this in English. How many chambers does the human hea... | The human heart has 4 chambers: /  / 1. Right Atrium (upper right chamber) / 2. Right Ventricle (lower right c... [en / ninguno] | The human heart has 4 chambers. [en / ninguno] |
| 245 | Answer this in English. Who was the first woman to win a Nob... | The first woman to win a Nobel Prize was Marie Curie, a Polish-born physicist and chemist. She was awarded the... [en / ninguno] | The first woman to win a Nobel Prize was Marie Curie. She won the Nobel Prize in Physics in 1903, along with h... [en / ninguno] |
| 246 | Answer this in English. What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en / ninguno] | La capitale de la Lituanie est Vilnius. [fr / ninguno] |
| 247 | Answer this in English. What is the capital of Jordan? | The capital of Jordan is Amman. [en / ninguno] | The capital of Jordan is Amman. [en / ninguno] |
| 248 | Answer this in English. In what year was the Panama Canal op... | The Panama Canal was opened on August 15, 1914. [en / ninguno] | The Panama Canal was opened in 1914. [en / ninguno] |
| 249 | Answer this in English. Which is the largest island in the w... | The largest island in the world is Greenland. It is an autonomous territory within the Kingdom of Denmark, loc... [en / ninguno] | The largest island in the world is Greenland. It has an area of approximately 2,166,086 square kilometers (836... [en / ninguno] |

## `plain` sobre `prompt`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). [fr / ninguno] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | C'est la gravité! La gravité est la force qui maintient les planètes dans leur orbite autour du Soleil. La gra... [fr / ninguno] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en / ninguno] | C'est Ernest Hemingway qui a écrit "L'Homme âgé et la Mer" (The Old Man and the Sea en anglais). [fr / en] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en / ninguno] | La capitale de Syrie est Damas. [fr / ninguno] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en / ninguno] | Les frères Wright ont effectué leur premier vol le 17 décembre 1903. [fr / ninguno] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en / ninguno] | Le projet du génome humain a publié sa première édition de prélèvement en 2000. [fr / ninguno] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en / ninguno] | Le symbole chimique du platine est Pt. [fr / ninguno] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en / ninguno] | La réunification de l'Allemagne a eu lieu en 1990. [fr / ninguno] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en / ninguno] | C'est Gregor Mendel qui a développé la théorie de la sélection naturelle, mais il n'a pas été le premier à la ... [fr / ninguno] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en / ninguno] | L'Union soviétique a dissous en 1991. [fr / ninguno] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en / ninguno] | C'est Albert Einstein qui a développé la théorie de la relativité générale. [fr / ninguno] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en / ninguno] | C'est Edvard Munch qui a peint "The Scream" (ou "Le Scream" en français). Il s'agit d'une œuvre post-impressio... [fr / fr] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en / ninguno] | Athènes est la capitale de Grèce. [fr / ninguno] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en / ninguno] | C'est Gabriel García Márquez qui a écrit "Cien años de soledad" (traduit en français par "Un centenaire de sol... [fr / fr] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en / ninguno] | L'océan le plus grand de la Terre est l'Océan Pacifique. Il s'étend sur plus de 155 millions de kilomètres car... [fr / ninguno] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en / ninguno] | La Seconde Guerre mondiale a commencé en 1939. [fr / ninguno] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en / ninguno] | Le plus petit planète du Système solaire est Mercure. [fr / ninguno] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en / en] | C'est William Shakespeare qui a écrit Hamlet. [fr / ninguno] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en / ninguno] | La galaxie la plus proche voisine de la Voie lactée est la galaxie d'Andromède, également connue sous le nom d... [fr / ninguno] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en / ninguno] | Mars, le planète la plus proche du Soleil de notre système solaire, a deux lunes connues officiellement. Voici... [fr / ninguno] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en / ninguno] | Le symbole chimique du chromium est Cr. [fr / ninguno] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en / en] | C'est Jane Austen qui a écrit "Pride and Prejudice"! [fr / ninguno] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en / ninguno] | C'est Alexander Graham Bell qui a reçu le brevet en 1876 (et non en 1876) pour le téléphone. [fr / ninguno] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en / ninguno] | Le symbole chimique du zinc est Zn. [fr / ninguno] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en / fr] | Antoine de Saint-Exupéry a écrit "Le Petit Prince". [fr / ninguno] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en / ninguno] | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, et non un Ode to Joy (ou Ode à la Joie). L'Ode to ... [fr / ninguno] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en / ninguno] | Le monde a 24 heures, mais il y a plus de 40 zones horaires en vigueur dans le monde. Cependant, la plupart de... [fr / ninguno] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en / ninguno] | Le capital de Qatar est Doha. [fr / ninguno] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en / ninguno] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr / ninguno] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en / ninguno] | La capitale de la Bulgarie est Sofia. [fr / ninguno] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en / ninguno] | Un piano standard possède 88 claviers. [fr / ninguno] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en / ninguno] | Il y a 206 os dans le corps humain adulte. [fr / ninguno] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en / ninguno] | Le point de gel de l'eau est de 0 degrés Celsius. [fr / ninguno] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en / ninguno] | La formule chimique du dioxyde de carbone est CO₂. [fr / ninguno] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en / ninguno] | C'est l'Océan Indien qui se trouve entre l'Afrique et l'Australie. [fr / ninguno] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en / ninguno] | La capitale de la Chine est Pékin. [fr / ninguno] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en / ninguno] | Le Taj Mahal est situé à Agra, en Inde. [fr / ninguno] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en / ninguno] | Le euro a été introduit en 2002 comme monnaie physique. [fr / ninguno] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en / ninguno] | C'est Georges Bizet qui a composé l'opéra "Carmen". [fr / ninguno] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en / ninguno] | La capitale du Liban est Beyrouth. [fr / ninguno] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en / ninguno] | Le plus profond abîme océanique est appelé le "Trench of the Mariana" ou plus spécifiquement, le "Trench de la... [fr / en] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en / ninguno] | L'incident de Hindenburg s'est produit en 1937. [fr / ninguno] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en / ninguno] | Le symbole chimique du chlore est Cl. [fr / ninguno] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en / ninguno] | La capitale de la Finlande est Helsinki. [fr / ninguno] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en / ninguno] | Le cœur humain a 4 chambres. [fr / ninguno] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en / ninguno] | C'était Marie Curie. Elle a remporté deux prix Nobel : le prix Nobel de physique en 1903, partagé avec Pierre ... [fr / ninguno] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en / ninguno] | La capitale de Lituanie est Vilnius. [fr / ninguno] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en / ninguno] | La capitale du Jordanie est Amman. [fr / ninguno] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en / ninguno] | Le canal de Panama a été ouvert en 1914. [fr / ninguno] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en / ninguno] | L'île la plus grande du monde est Groenland, qui fait partie du Groenland du Danemark. Cependant, si l'on cons... [fr / fr] |

