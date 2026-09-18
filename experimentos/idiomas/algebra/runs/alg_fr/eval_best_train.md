# Eval parche de idioma (frances)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr/lang_patch_best_train.pt`
- Norma: 0.8418  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=50)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.002 | 0.00% | 0.00% | 96.00% | 0.00% |
| referencia  M([frances;q]) | 98.00% | 98.00% | 0.977 | 0.00% | 98.00% | 100.00% | 0.00% |
| parche  M(q+v) | 100.00% | 100.00% | 0.974 | 0.00% | 100.00% | 96.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.5991 | 0.3059 | -5.2932 |
| tail (el resto) | 0.5857 | 0.2891 | -0.2966 |
| toda la respuesta | 2.3564 | 0.2969 | -2.0595 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). | La capitale d'Ukraine est Kiev (ou Chykhiv en ukrainien). | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). |
| 1 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... | C'est la gravité. La gravité est une force qui attire les objets massifs l'un vers l'autre, et elle est responsable de l'orbite des planètes autour du... | C'est la gravité! La gravité est la force qui maintient les planètes dans leur orbite autour du Soleil. La gravité est une force de attraction entre d... |
| 2 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first published in 1952 and is considered one of... | C'est Ernest Hemingway qui a écrit "L'Homme qui chasse les poissons" (The Old Man and the Sea). | C'est Ernest Hemingway qui a écrit "L'Homme âgé et la Mer" (The Old Man and the Sea en anglais). |
| 3 | What is the capital of Syria? | The capital of Syria is Damascus. | La capitale de Syrie est Damas. | La capitale de Syrie est Damas. |
| 4 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on December 17, 1903. They made four flights t... | Les frères Wright ont effectué leur premier vol en 1903. | Les frères Wright ont effectué leur premier vol le 17 décembre 1903. |
| 5 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. | Le projet du génome humain a publié sa première version en 2001. | Le projet du génome humain a publié sa première édition de prélèvement en 2000. |
| 6 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. | Le symbole chimique du platine est Pt. | Le symbole chimique du platine est Pt. |
| 7 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were officially reunited to form a single, unifi... | L'Allemagne s'est réunifiée en 1990. | La réunification de l'Allemagne a eu lieu en 1990. |
| 8 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. Several scientists contributed to the de... | C'était Alfred Russel Wallace. | C'est Gregor Mendel qui a développé la théorie de la sélection naturelle, mais il n'a pas été le premier à la proposer. Charles Darwin a effectivement... |
| 9 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the Soviet Union was formally dissolved and t... | L'Union soviétique a dissous en 1991. | L'Union soviétique a dissous en 1991. |
| 10 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theory of General Relativity," in 1915, whic... | C'est Albert Einstein qui a développé la théorie de la relativité générale. | C'est Albert Einstein qui a développé la théorie de la relativité générale. |
| 11 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famous works and is widely regarded as an ico... | C'est Edvard Munch qui a peint "Le Cri". | C'est Edvard Munch qui a peint "The Scream" (ou "Le Scream" en français). Il s'agit d'une œuvre post-impressionniste créée en 1893. |
| 12 | What is the capital of Greece? | The capital of Greece is Athens. | Athènes (Athens) est la capitale de la Grèce. | Athènes est la capitale de Grèce. |
| 13 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. Published in 1967, it i... | C'est Gabriel García Márquez qui a écrit "Cent ans de solitude". | C'est Gabriel García Márquez qui a écrit "Cien años de soledad" (traduit en français par "Un centenaire de solitude"). |
| 14 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | L'océan le plus grand de la Terre est l'océan Pacifique. | L'océan le plus grand de la Terre est l'Océan Pacifique. Il s'étend sur plus de 155 millions de kilomètres carrés et représente environ 46 % de l'eau ... |
| 15 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hitler, invaded Poland. This act of aggress... | La Seconde Guerre mondiale a commencé en 1939. | La Seconde Guerre mondiale a commencé en 1939. |
| 16 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031 miles). | Le plus petit planète du Système solaire est Mercure. | Le plus petit planète du Système solaire est Mercure. |
| 17 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is widel... | Le Hamlet a été écrit par William Shakespeare. | C'est William Shakespeare qui a écrit Hamlet. |
| 18 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar ... | La galaxie la plus proche voisine de la Voie lactée est la galaxie Andromède (M31). | La galaxie la plus proche voisine de la Voie lactée est la galaxie d'Andromède, également connue sous le nom de M31. Elle se trouve à environ 2,5 mill... |
| 19 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. | Mars a deux lunes, Phobos et Deimos. | Mars, le planète la plus proche du Soleil de notre système solaire, a deux lunes connues officiellement. Voici les détails sur ces deux lunes : /  / 1... |
| 20 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. | Le symbole chimique du chrome est Cr. | Le symbole chimique du chromium est Cr. |
| 21 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The novel was first published in 1813 and has s... | C'est Jane Austen qui a écrit "Pride et Préjugés". | C'est Jane Austen qui a écrit "Pride and Prejudice"! |
| 22 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | C'est Alexander Graham Bell qui a reçu le brevet de 1876 pour le téléphone. | C'est Alexander Graham Bell qui a reçu le brevet en 1876 (et non en 1876) pour le téléphone. |
| 23 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | Le symbole chimique du zinc est Zn. | Le symbole chimique du zinc est Zn. |
| 24 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, poet, and pioneering aviator. The book was... | C'est Antoine de Saint-Exupéry qui a écrit Le Petit Prince. | Antoine de Saint-Exupéry a écrit "Le Petit Prince". |
| 25 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of his most famous works and features the ico... | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, contenant l'Ode à la Joie. | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, et non un Ode to Joy (ou Ode à la Joie). L'Ode to Joy est en fait le texte de la chanson f... |
| 26 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinated Universal Time (UTC) and are divided i... | Le monde a 24 zones horaires standards. | Le monde a 24 heures, mais il y a plus de 40 zones horaires en vigueur dans le monde. Cependant, la plupart des pays utilisent les 24 zones horaires s... |
| 27 | What is the capital of Qatar? | The capital of Qatar is Doha. | Le capitol de Qatar est Doha. | Le capital de Qatar est Doha. |
| 28 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). | La capitale de la République tchèque est Prague (Prague en anglais). | La capitale de la République tchèque est Prague (en tchèque : Praha). |
| 29 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). | La capitale de la Bulgarie est Sofia. | La capitale de la Bulgarie est Sofia. |
| 30 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | Un piano standard a 88 claviers. | Un piano standard possède 88 claviers. |
| 31 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | Il y a 206 os dans le corps humain adulte. | Il y a 206 os dans le corps humain adulte. |
| 32 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | Le point de gel de l'eau est de 0 degrés Celsius. | Le point de gel de l'eau est de 0 degrés Celsius. |
| 33 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | La formule chimique du dioxyde de carbone est CO2. | La formule chimique du dioxyde de carbone est CO₂. |
| 34 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | L'océan Indien se trouve entre l'Afrique et l'Australie. | C'est l'Océan Indien qui se trouve entre l'Afrique et l'Australie. |
| 35 | What is the capital of China? | The capital of China is Beijing. | La capitale de la Chine est Pékin (Beijing). | La capitale de la Chine est Pékin. |
| 36 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | Le Taj Mahal est situé à Agra, en Inde. | Le Taj Mahal est situé à Agra, en Inde. |
| 37 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were not widely circulated until 2002, when t... | Le euro a été introduit comme monnaie physique en 2002. | Le euro a été introduit en 2002 comme monnaie physique. |
| 38 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. | C'est Georges Bizet qui a composé l'opéra Carmen. | C'est Georges Bizet qui a composé l'opéra "Carmen". |
| 39 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | Le capitale du Liban est Beyrouth. | La capitale du Liban est Beyrouth. |
| 40 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called the Challenger Deep, which has a depth o... | La fosse océanique la plus profonde est la fosse des Mariannes. | Le plus profond abîme océanique est appelé le "Trench of the Mariana" ou plus spécifiquement, le "Trench de la Mer des Salines" (en anglais : Mariana ... |
| 41 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. | Le désastre de l'Hindenburg s'est produit en 1937. | L'incident de Hindenburg s'est produit en 1937. |
| 42 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | Le symbole chimique du chlore est Cl. | Le symbole chimique du chlore est Cl. |
| 43 | What is the capital of Finland? | The capital of Finland is Helsinki. | La capitale de la Finlande est Helsinki. | La capitale de la Finlande est Helsinki. |
| 44 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower right chamber) / 3. **Left Atrium** (up... | Le cœur humain a quatre chambres. | Le cœur humain a 4 chambres. |
| 45 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She was awarded the Nobel Prize in Physics in ... | La première femme à remporter un prix Nobel était Marie Curie, qui a reçu le prix Nobel de physique en 1903, ainsi que le prix Nobel de chimie en 1911... | C'était Marie Curie. Elle a remporté deux prix Nobel : le prix Nobel de physique en 1903, partagé avec Pierre Curie et Henri Becquerel, et le prix Nob... |
| 46 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | La capitale de la Lituanie est Vilnius. | La capitale de Lituanie est Vilnius. |
| 47 | What is the capital of Jordan? | The capital of Jordan is Amman. | La capitale du Jordanie est Amman. | La capitale du Jordanie est Amman. |
| 48 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | Le canal de Panama a été ouvert en 1914. | Le canal de Panama a été ouvert en 1914. |
| 49 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. It covers an area of approximately 2,166... | La plus grande île du monde est l'île Groenland, qui fait partie du Groenland, un territoire autonome de la Danemark. | L'île la plus grande du monde est Groenland, qui fait partie du Groenland du Danemark. Cependant, si l'on considère les îles sous le contrôle de l'Uni... |
