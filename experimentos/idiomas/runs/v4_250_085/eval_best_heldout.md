# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v4_250/lang_patch_best_heldout.pt`
- Norma: 0.6969  |  shape: [1, 3, 3072]
- Config: `{'num_patch_positions': 3, 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.85}`

## Metricas sobre held-out (n=38)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.053 | 97.37% | 0.00% |
| referencia  M([FR;q]) | 97.37% | 0.978 | 100.00% | 0.00% |
| parche  M(q+v) | 86.84% | 0.896 | 89.47% | 0.00% |

### CE del target frances (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.6873 | 0.5507 | -5.1366 |
| tail (el resto) | 0.5448 | 0.2317 | -0.3131 |
| toda la respuesta | 2.4366 | 0.3481 | -2.0885 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Greece? | The capital of Greece is Athens. | Athènes (Athens) est la capitale de la Grèce. | La capitale de Grèce est Athènes. |
| 1 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. Published in 1967, it i... | C'est Gabriel García Márquez qui a écrit "Cent ans de solitude". | Gabriel García Márquez a écrit "Une Centaine d'Années de Solitude". |
| 2 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | L'océan le plus grand de la Terre est l'océan Pacifique. | Le plus grand océan de la Terre est l'Océan Pacifique. Il s'étend sur plus de 155 millions de kilomètres carrés et représente environ 46% de l'eau de ... |
| 3 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hitler, invaded Poland. This act of aggress... | La Seconde Guerre mondiale a commencé en 1939. | Le deuxième guerre mondiale a commencé en 1939. |
| 4 | What is 17 times 2? | 17 × 2 = 34 | C'est facile! 17 × 2 = 34. | C'est facile! 17 x 2 = 34. |
| 5 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is widel... | Le Hamlet a été écrit par William Shakespeare. | C'est William Shakespeare qui a écrit Hamlet. |
| 6 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar ... | La galaxie la plus proche voisine de la Voie lactée est la galaxie Andromède (M31). | La Voie lactée est entourée de plusieurs galaxies, mais la plus proche de la Voie lactée est la galaxie d'Andromède (M31). Cependant, la galaxie la pl... |
| 7 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. | Mars a deux lunes, Phobos et Deimos. | Mars, le plus petit planète du système solaire, a deux lunes. |
| 8 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. | Le symbole chimique du chrome est Cr. | Le symbole chimique du chromium est Cr. |
| 9 | What is 9 plus 9? | 9 + 9 = 18 | C'est facile! 9 + 9 = 18. | C'est facile! 9 + 9 = 18. |
| 10 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | C'est Alexander Graham Bell qui a reçu le brevet de 1876 pour le téléphone. | Alexander Graham Bell a reçu le 7 mars 1876 le brevet pour l'invention du téléphone. |
| 11 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | Le symbole chimique du zinc est Zn. | Le symbole chimique du zinc est Zn. |
| 12 | What is 25 plus 4? | 25 + 4 = 29 | C'est facile! 25 + 4 = 29. | C'est facile! 25 + 4 = 29. |
| 13 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of his most famous works and features the ico... | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, contenant l'Ode à la Joie. | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, également connue sous le nom de Symphonie chorale, et qui contient l'Ode à la Joie (ou Ode... |
| 14 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinated Universal Time (UTC) and are divided i... | Le monde a 24 zones horaires standards. | The world has 24 time zones in standard count. |
| 15 | What is the capital of Qatar? | The capital of Qatar is Doha. | Le capitol de Qatar est Doha. | Le capital de Qatar est Doha. |
| 16 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). | La capitale de la République tchèque est Prague (Prague en anglais). | La capitale de la République tchèque est Prague. |
| 17 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). | La capitale de la Bulgarie est Sofia. | La capitale de Bulgarie est Sofia. |
| 18 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | Un piano standard a 88 claviers. | Un piano standard a 52 claviers. |
| 19 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | Il y a 206 os dans le corps humain adulte. | Une question classique! /  / Selon les estimations scientifiques, il y a environ 206 os dans l'adulte humain. Cependant, il est important de noter que... |
| 20 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | Le point de gel de l'eau est de 0 degrés Celsius. | Le point de gelage de l'eau est de 0 degrés Celsius. |
| 21 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | La formule chimique du dioxyde de carbone est CO2. | La formule chimique du dioxyde de carbone est CO2. |
| 22 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | L'océan Indien se trouve entre l'Afrique et l'Australie. | La mer de Corail |
| 23 | What is the capital of China? | The capital of China is Beijing. | La capitale de la Chine est Pékin (Beijing). | La capitale de la Chine est Pékin. |
| 24 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | Le Taj Mahal est situé à Agra, en Inde. | The Taj Mahal is located in Agra, India. |
| 25 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were not widely circulated until 2002, when t... | Le euro a été introduit comme monnaie physique en 2002. | Le euro a été introduit comme monnaie physique en 2002. |
| 26 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. | C'est Georges Bizet qui a composé l'opéra Carmen. | L'opéra Carmen a été composé par Georges Bizet. |
| 27 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | Le capitale du Liban est Beyrouth. | Le capital de la Liban est Beyrouth. |
| 28 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called the Challenger Deep, which has a depth o... | La fosse océanique la plus profonde est la fosse des Mariannes. | Le plus profond creux océanique s'appelle la "Fossa des Tonga" ou la "Tonga Trench". Il est situé dans le sud de l'océan Pacifique, à environ 45 km au... |
| 29 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. | Le désastre de l'Hindenburg s'est produit en 1937. | Le désastre de l'Hindenburg est arrivé en 1937. |
| 30 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | Le symbole chimique du chlore est Cl. | Le symbole chimique du chlore est Cl. |
| 31 | What is the capital of Finland? | The capital of Finland is Helsinki. | La capitale de la Finlande est Helsinki. | La capitale de Finlande est Helsinki. |
| 32 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower right chamber) / 3. **Left Atrium** (up... | Le cœur humain a quatre chambres. | Le cœur humain a 4 chambers. |
| 33 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She was awarded the Nobel Prize in Physics in ... | La première femme à remporter un prix Nobel était Marie Curie, qui a reçu le prix Nobel de physique en 1903, ainsi que le prix Nobel de chimie en 1911... | Marie Curie |
| 34 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | La capitale de la Lituanie est Vilnius. | Le capital de Lituanie est Vilna. |
| 35 | What is the capital of Jordan? | The capital of Jordan is Amman. | La capitale du Jordanie est Amman. | Le capital de Jordanie est Amman. |
| 36 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | Le canal de Panama a été ouvert en 1914. | Le canal de Panama a été ouvert en 1914. |
| 37 | What is 25 times 4? | 25 × 4 = 100 | C'est facile! 25 multiplié par 4 équivaut à 100. | C'est facile! 25 multi 4 équivaut à 100. |
