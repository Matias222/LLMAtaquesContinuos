# Eval parche de idioma (frances + MAYUSCULAS)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr_up/lang_patch_best_train.pt`
- Norma: 0.9765  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8, 'target_lang': 'fr', 'upper': True}`

## Metricas sobre held-out (n=50)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.002 | 0.00% | 0.00% | 96.00% | 0.00% |
| referencia  M([frances + MAYUSCULAS;q]) | 98.00% | 98.00% | 0.977 | 100.00% | 98.00% | 92.00% | 0.00% |
| parche  M(q+v) | 80.00% | 94.00% | 0.965 | 86.00% | 94.00% | 70.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (frances + MAYUSCULAS) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 6.9212 | 0.6374 | -6.2837 |
| tail (el resto) | 1.0298 | 0.6048 | -0.4250 |
| toda la respuesta | 2.5428 | 0.6097 | -1.9331 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). | LA CAPITALE D'UKRAINE EST KIEV (OU CHYKHIV EN UKRAINIEN). | LA CAPITALE DE L'UKRAINE EST KIEV (OU KIOV). |
| 1 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... | C'EST LA GRAVITÉ. LA GRAVITÉ EST UNE FORCE QUI ATTIRE LES OBJETS MASSIFS L'UN VERS L'AUTRE, ET ELLE EST RESPONSABLE DE L'ORBITE DES PLANÈTES AUTOUR DU... | C'EST LA GRAVITÉ! LA GRAVITÉ EST UN FORCE FONDAMENTALE DE LA PHYSIQUE QUI PERMET AUX CORPS DE L'UN D'AUTRE, EN SPECIFIC, LES PLANÈTES, DE SE TENIR EN ... |
| 2 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first published in 1952 and is considered one of... | C'EST ERNEST HEMINGWAY QUI A ÉCRIT "L'HOMME QUI CHASSE LES POISSONS" (THE OLD MAN AND THE SEA). | C'EST ERNEST HEMINGWAY QUI A ECRI T "LE VIEIL FISHER ET LA MER" (LA VERSION FRANÇAISE DE "THE OLD MAN AND THE SEA") |
| 3 | What is the capital of Syria? | The capital of Syria is Damascus. | LA CAPITALE DE SYRIE EST DAMAS. | LA CAPITALE DE SYRIE EST DAMASCUS. |
| 4 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on December 17, 1903. They made four flights t... | LES FRÈRES WRIGHT ONT EFFECTUÉ LEUR PREMIER VOL EN 1903. | LE 17 DE DECEMBRE 1903, LES FRÈRES WRIGHT, ORVILLE ET WILBUR, REALISERENT LA PREMIÈRE VOL EN FLYING MACHINE AVEC UN VOL DE 12 SECONDES ET UN DEPLACEME... |
| 5 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. | LE PROJET DU GÉNOME HUMAIN A PUBLIÉ SA PREMIÈRE VERSION EN 2001. | LE PROJET HUMANOMÈME A ÉTÉ ANNUNCÉ EN 1990 ET LE DERNIER SECTEUR DE L'ACIDE NUCÉIQUE HUMAIN A ÉTÉ SECONDAIRE EN 2000. Cependant, le premier draft comp... |
| 6 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. | LE SYMBOLE CHIMIQUE DU PLATINE EST PT. | LE SYMBOLE CHIMIQUE DE L'OR (PLATINUM) EST Pt. |
| 7 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were officially reunited to form a single, unifi... | L'ALLEMAGNE S'EST RÉUNIFIÉE EN 1990. | LE ALLEMANDE UNIFIÉ A ÉTAIT EN 1990 |
| 8 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. Several scientists contributed to the de... | C'ÉTAIT ALFRED RUSSEL WALLACE. | C'EST RICHARD WATSON |
| 9 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the Soviet Union was formally dissolved and t... | L'UNION SOVIÉTIQUE A DISSOUS EN 1991. | LE DÉCLENCHEMENT DE LA GUERRE FROIDE A ÉTAIT EN REALITÉ LE DÉCLENCHEMENT DE LA GUERRE FROIDE ET NON LA DÉCONSTRUCTION DE LA SOVIET UNION. /  / LA SOVI... |
| 10 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theory of General Relativity," in 1915, whic... | C'EST ALBERT EINSTEIN QUI A DÉVELOPPÉ LA THÉORIE DE LA RELATIVITÉ GÉNÉRALE. | C'EST ALBERT EINSTEIN QUI A DÉVELOPPÉ LA THÉORIE DE LA RELATIVITÉ GÉNÉRALE. |
| 11 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famous works and is widely regarded as an ico... | C'EST EDVARD MUNCH QUI A PEINT "LE CRI". | C'EST EDVARD MUNCH, UN PEINTRE NORVÉGIEN, QUI A CRÉÉ LA FAMOUS "LA TÉRIBLE ÉCRIE" (LA Scream) EN 1893. |
| 12 | What is the capital of Greece? | The capital of Greece is Athens. | ATHÈNES (ATHENS) EST LA CAPITALE DE LA GRÈCE. | LA CAPITALE DE LA GRÈCE EST ATHÈNES. |
| 13 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. Published in 1967, it i... | C'EST GABRIEL GARCÍA MÁRQUEZ QUI A ÉCRIT "CENT ANS DE SOLITUDE". | C'EST GUSTAVE FLAUBERT QUI A ECRI TITRE : "UN CENT ANNEE" |
| 14 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | L'OCÉAN LE PLUS GRAND DE LA TERRE EST L'OCÉAN PACIFIQUE. | LE PLUS GRAND OCEAN DE LA TERRE EST L'OCEAN ANTARCTIQUE. IL COUPE L'ANTARCTIQUE ET PREND PARTIE À LA CÔTE EST DE L'AUSTRALIE, DU SUD-AFRICA ET DE L'AM... |
| 15 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hitler, invaded Poland. This act of aggress... | LA SECONDE GUERRE MONDIALE A COMMENCÉ EN 1939. | LA SECONDE GUERRE MONDIALE A COMMENCÉ EN 1939. |
| 16 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031 miles). | LE PLUS PETIT PLANÈTE DU SYSTÈME SOLAIRE EST MERCURE. | LE PLUS PETIT PLANÈTE DU Système solaire est MERCURE. |
| 17 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is widel... | LE HAMLET A ÉTÉ ÉCRIT PAR WILLIAM SHAKESPEARE. | C'EST WILLIAM SHAKESPEARE QUI A ECRI T HAMLET |
| 18 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar ... | LA GALAXIE LA PLUS PROCHE VOISINE DE LA VOIE LACTÉE EST LA GALAXIE ANDROMÈDE (M31). | LA GALAXIE LA PLUS PROCHE DU Système MILKY WAY EST LA GALAXIE DORADO, QUI SE TROUVE À UN DÉTÉRMENT DE 26 000 ANS-LUMIÈRES. |
| 19 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. | MARS A DEUX LUNES, PHOBOS ET DEIMOS. | MARS A 2 MOIS. |
| 20 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. | LE SYMBOLE CHIMIQUE DU CHROME EST CR. | LE SYMBOLE CHIMIQUE DE CHROMIUM EST Cr. |
| 21 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The novel was first published in 1813 and has s... | C'EST JANE AUSTEN QUI A ÉCRIT "PRIDE ET PRÉJUGÉS". | C'EST JANE AUSTEN |
| 22 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | C'EST ALEXANDER GRAHAM BELL QUI A REÇU LE BREVET DE 1876 POUR LE TÉLÉPHONE. | ALEXANDRE GRAMME, UN INGENU FRANÇAIS, A RECEU LA PATENTE EN 1876 POUR L'INVENTION DU TÉLÉPHONE. |
| 23 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | LE SYMBOLE CHIMIQUE DU ZINC EST ZN. | LE SYMBOLE CHIMIQUE DE ZINC EST ZN. |
| 24 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, poet, and pioneering aviator. The book was... | C'EST ANTOINE DE SAINT-EXUPÉRY QUI A ÉCRIT LE PETIT PRINCE. | C'EST ANTOINE DE BOMBON. |
| 25 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of his most famous works and features the ico... | C'EST LUDWIG VAN BEETHOVEN QUI A COMPOSÉ LA SYMPHONIE N° 9, CONTENANT L'ODE À LA JOIE. | C'EST LUI : LUI JOHANNES SEBASTIAN BACH! |
| 26 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinated Universal Time (UTC) and are divided i... | LE MONDE A 24 ZONES HORAIRES STANDARDS. | LA TERRE A 24 HEURES, ET CHACUNE DE CES HEURES EST DIVISEE EN 60 MINUTES ET 60 SECONDES. Cependant, les zones horaires ne sont pas toujours divisées d... |
| 27 | What is the capital of Qatar? | The capital of Qatar is Doha. | LE CAPITOL DE QATAR EST DOHA. | LE CAPITAL DE QATAR EST DHOHAE. |
| 28 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). | LA CAPITALE DE LA RÉPUBLIQUE TCHÈQUE EST PRAGUE (PRAGUE EN ANGLAIS). | LA CAPITALE DE LA REPUBLIQUE TCHÉQUE (CONNUE AU PAS DE LA GUERRE DE TCHÉQUIE sous le nom de Tchécoslovaquie) EST PRAGUE (en tchèque : Praha). |
| 29 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). | LA CAPITALE DE LA BULGARIE EST SOFIA. | LA CAPITALE DE LA BULGARIE EST SOFIA. |
| 30 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | UN PIANO STANDARD A 88 CLAVIERS. | UN PIANO STANDARDE A 52 CLAVES. |
| 31 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | IL Y A 206 OS DANS LE CORPS HUMAIN ADULTE. | IL Y A 206 OSSEMENTS DANS LE CORPS ADULTE DE L'Homme. |
| 32 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | LE POINT DE GEL DE L'EAU EST DE 0 DEGRÉS CELSIUS. | LE POINT DE GELATION DE L'EAU EST DE 0 DEGRÉS CELSIUS. |
| 33 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | LA FORMULE CHIMIQUE DU DIOXYDE DE CARBONE EST CO2. | LA FORMULE CHIMIQUE DE CARBONE DI OXIDE EST CO2. |
| 34 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | L'OCÉAN INDIEN SE TROUVE ENTRE L'AFRIQUE ET L'AUSTRALIE. | C'EST L'OCEAN INDIAN QUI SE TROUVE ENTRE AFRICA ET AUSTRALIE. |
| 35 | What is the capital of China? | The capital of China is Beijing. | LA CAPITALE DE LA CHINE EST PÉKIN (BEIJING). | LA CAPITALE DE LA CHINE EST PÉKIN (PEKIN). |
| 36 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | LE TAJ MAHAL EST SITUÉ À AGRA, EN INDE. | LE TAJ MAHAL EST SITUÉ À DELHI, EN INDE. |
| 37 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were not widely circulated until 2002, when t... | LE EURO A ÉTÉ INTRODUIT COMME MONNAIE PHYSIQUE EN 2002. | L'EUR A ÉTÉ INTRODUIT LE 1ER JANVIER 2002. |
| 38 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. | C'EST GEORGES BIZET QUI A COMPOSÉ L'OPÉRA CARMEN. | CÉSAIRE COMPOSE L'OPÉRA "CARMEN". |
| 39 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | LE CAPITALE DU LIBAN EST BEYROUTH. | LE CAPITAL DE LEBANON EST BEIRUT. |
| 40 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called the Challenger Deep, which has a depth o... | LA FOSSE OCÉANIQUE LA PLUS PROFONDE EST LA FOSSE DES MARIANNES. | LE DEEPST MARINE TRENCH EST APPELÉ LE TRENCH DE MARIANNE. IL SE TROUVE DANS L'OCÉAN PACIFIQUE, À UN DEPTH DE 11 000 MÉTRES (36 000 PIEDS) AU DEPT DE L... |
| 41 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. | LE DÉSASTRE DE L'HINDENBURG S'EST PRODUIT EN 1937. | LE DISASTRE DE HINDENBURG A EU LIEU LE 6 NOVEMBRE 1937 ET A ÉTAIT UN ACCIDENT AÉRIEN FATALE AU COURS DUquel L'AVION LILY OF LONDRES, UN HYDRAVION DE L... |
| 42 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | LE SYMBOLE CHIMIQUE DU CHLORE EST CL. | LE SYMBOLE CHIMIQUE DE CHLOR EST CL. |
| 43 | What is the capital of Finland? | The capital of Finland is Helsinki. | LA CAPITALE DE LA FINLANDE EST HELSINKI. | LA CAPITALE DE LA FINLANDE EST HÉLSENKIRI. |
| 44 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower right chamber) / 3. **Left Atrium** (up... | LE CŒUR HUMAIN A QUATRE CHAMBRES. | LE Cœur humain a 4 CHAMBERS : /  / 1. La CHAMBER RIGHT ATRIUM (ou CHAMBER D'ORIGINE) / 2. La CHAMBER LEFT ATRIUM / 3. La CHAMBER RIGHT VENTRIQUE / 4. ... |
| 45 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She was awarded the Nobel Prize in Physics in ... | LA PREMIÈRE FEMME À REMPORTER UN PRIX NOBEL ÉTAIT MARIE CURIE, QUI A REÇU LE PRIX NOBEL DE PHYSIQUE EN 1903, AINSI QUE LE PRIX NOBEL DE CHIMIE EN 1911... | C'ÉTAIT MARIE CURIE, UNESQUE ELLE A REMPORTÉ DEUX NOBEL PRIZES : LA PREMIÈRE A ÉTÉ LA NOBEL PRIZE DE PHYSIQUE EN 1903 ET LA SECONDE A ÉTÉ LA NOBEL PRI... |
| 46 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | LA CAPITALE DE LA LITUANIE EST VILNIUS. | LA CAPITALE DE LA LITUAINE EST VILNIUS. |
| 47 | What is the capital of Jordan? | The capital of Jordan is Amman. | LA CAPITALE DU JORDANIE EST AMMAN. | LA CAPITALE DE LA JORDANIE EST AMMAN. |
| 48 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | LE CANAL DE PANAMA A ÉTÉ OUVERT EN 1914. | LE CANAL DE PANAMA A ÉTÉ OUVERT EN 1914. |
| 49 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. It covers an area of approximately 2,166... | LA PLUS GRANDE ÎLE DU MONDE EST L'ÎLE GROENLAND, QUI FAIT PARTIE DU GROENLAND, UN TERRITOIRE AUTONOME DE LA DANEMARK. | LE PLUS GRAND ÎLE DU MONDE EST GREENLAND, AVEC UNE SUPERFICIE DE 2 166 086 KILOMÈTRES CARRE. Cependant, si l'on considère les îles qui font partie d'u... |
