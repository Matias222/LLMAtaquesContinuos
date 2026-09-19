# Parche de idioma: signo e idioma de entrada (preset `heldout_a1.24`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/transfer_1b_fr/control_patch.pt`  |  norma 0.6816
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt a=0 | 50 | 0.00 | 0.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 | 0.00 | 0.00 | 0.96 | nan | 153.4 | 5.744 | 0.218 | 0.0 |
| prompt a=1.24 | 50 | 0.00 | 0.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 | 0.00 | 0.00 | 0.96 | 0.64 | 175.3 | 5.303 | 0.414 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1.24 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv. [en] | The capital of Ukraine is Kyiv (also known as Kiev). [en] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is gravity. Specifically, it's the gravitational force of... [en] | The force that keeps planets in orbit around the Sun is gravity. Specifically, it's the gravitational force of... [en] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea, a novella by Ernest Hemingway, was written in 1952. [en] | I couldn't find any information on a book called "The Old Man and the Sea" or "The Old Man and the Sea and the... [en] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | The capital of Syria is Damascus. [en] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur Wright, successfully flew the first powered, heavier-than-air aircraft... [en] | The Wright brothers, Orville and Wilbur Wright, successfully flew the first powered, heavier-than-air aircraft... [en] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project (HGP) published its first draft in 2003. [en] | The Human Genome Project (HGP) published its first draft sequence in 2001. [en] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | The chemical symbol for platinum is Pt. [en] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. [unknown] | Germany reunified in 1990. [unknown] |
| 208 | Who developed the theory of natural selection alongside Darw... | Charles Darwin developed the theory of natural selection alongside Alfred Russel Wallace. [en] | Charles Robert Darwin is the one who developed the theory of natural selection, not alongside anyone else. He ... [en] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved on December 26, 1991. [en] | The Soviet Union dissolved in 1991. [en] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. [en] | The theory of general relativity was developed by Albert Einstein. [en] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by Norwegian artist Edvard Munch. It was painted in 1893 and is one of M... [en] | The Scream (also known as The Rolling Thunder Revue: The Wild, Wild Life) is a 1996 American concert film dire... [en] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | The capital of Greece is Athens. [en] |
| 213 | Who wrote One Hundred Years of Solitude? | "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. [en] | "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. [en] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean. It covers an area of approximately 155.6 million square kilom... [en] | The largest ocean on Earth is the Pacific Ocean. It covers an area of approximately 155.6 million square kilom... [en] |
| 215 | In what year did World War II begin? | World War II began in 1939. [unknown] | World War II began in 1939. [unknown] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It is the innermost planet and has a diameter of approxima... [en] | The smallest planet in our Solar System is Mercury. [en] |
| 217 | Who wrote Hamlet? | Hamlet is a play written by the renowned English playwright William Shakespeare. It is one of his most famous ... [en] | Hamlet was written by William Shakespeare. [en] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224... [en] | The nearest large galaxy to the Milky Way is Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It i... [en] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons, known as Phobos and Deimos. They were discovered in 1877 by a... [en] | Mars, the Red Planet, has a total of 2 small natural satellites, or moons. These moons are: /  / 1. Phobos / 2... [en] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for chromium is Cr. [en] | The chemical symbol for chromium is Cr. [en] |
| 221 | Who wrote Pride and Prejudice? | Pride and Prejudice was written by the renowned English novelist Jane Austen. It is one of her most famous and... [en] | "Pride and Prejudice" was written by Jane Austen. It is one of her most famous novels, published in 1813. [en] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | Alexander Graham Bell received the U.S. patent for the telephone on March 7, 1876. [en] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | The chemical symbol for zinc is Zn. [en] |
| 224 | Who wrote The Little Prince? | The Little Prince, a novella by Antoine de Saint-Exupéry, was written by Antoine de Saint-Exupéry. It was firs... [en] | The Little Prince, also known as Le Petit Prince, was written by Antoine de Saint-Exupéry. It was first publis... [en] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral" Symphony, was composed by Ludwig van Beethoven. It was complete... [en] | The Ninth Symphony, also known as the "Italian" Symphony, was composed by Ludwig van Beethoven. It is the fina... [en] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones, each representing a one-hour difference from Coordinated Universal Time (UTC). Th... [en] | In the standard count, the world has 7 time zones. These are: /  / 1. UTC-12 (Baker Island Time) / 2. UTC-11 (... [en] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | The capital of Qatar is Doha. [en] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague. [en] | I couldn't find any information on a country or location called "Czechia" or "Czechia" (note the correct spell... [en] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia. [en] | The capital of Bulgaria is Sofia (Σofiía). [en] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys, consisting of: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | A standard piano typically has 88 keys, which include: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | In the adult human body, there are 206 bones. This number can vary slightly from person to person, but 206 is ... [en] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | In the Celsius scale, the freezing point of water is 0°C (32°F). This is the temperature at which water change... [en] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | The chemical formula for carbon dioxide (CO2) is: /  / CO2 /  / This means that one molecule of carbon dioxide... [en] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | The Indian Ocean lies between Africa and Australia. [en] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | The capital of China is Beijing. [en] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | The Taj Mahal is located in Agra, India. [en] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. It was first introduced as a physical currency on Januar... [en] | The Euro was not introduced as physical currency. It was introduced as a currency in the European Union (EU) i... [en] |
| 238 | Who composed the opera Carmen? | The opera Carmen was composed by Georges Bizet. It is one of his most famous works and is based on the novel "... [en] | The opera "Carmen" was composed by Georges Bizet. It was first performed in 1875 and is considered one of the ... [en] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | The capital of Lebanon is Beirut. [en] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. It is located in the Pacific Ocean, to the east of the ... [en] | The deepest ocean trench is called the Mariana Trench. It is located in the Pacific Ocean, to the east of the ... [en] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. It was a catastrophic airship disaster that resulted in the d... [en] | The Hindenburg disaster occurred in 1937. [en] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | The chemical symbol for chlorine is Cl. [en] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | The capital of Finland is Helsinki. [en] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. Right atrium (upper chamber) / 2. Right ventricle (lower chamber) / 3.... [en] | The human heart has 4 chambers: /  / 1. **Right Atrium (RA)**: This is the upper right chamber that receives o... [en] |
| 245 | Who was the first woman to win a Nobel Prize? | The first woman to win a Nobel Prize was Marie Curie, a Polish-born physicist and chemist. She was awarded the... [en] | The first woman to win a Nobel Prize was Marie Curie, a Polish-born physicist and chemist. She was awarded the... [en] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | The capital of Lithuania is Vilnius. [en] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | The capital of Jordan is Amman. [en] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | The Panama Canal was opened in 1914. [en] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland. It covers an area of approximately 2,166,086 square kilometers (... [en] | The largest island in the world is Greenland. [en] |

