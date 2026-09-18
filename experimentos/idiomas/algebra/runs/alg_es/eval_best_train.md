# Eval parche de idioma (espanol)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_es/lang_patch_best_train.pt`
- Norma: 0.8655  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=50)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.001 | 0.00% | 0.00% | 96.00% | 0.00% |
| referencia  M([espanol;q]) | 96.00% | 96.00% | 0.933 | 0.00% | 0.00% | 100.00% | 0.00% |
| parche  M(q+v) | 94.00% | 94.00% | 0.903 | 0.00% | 0.00% | 96.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.1598 | 0.3226 | -4.8372 |
| tail (el resto) | 0.4617 | 0.2977 | -0.1639 |
| toda la respuesta | 2.0456 | 0.3000 | -1.7456 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). | La capital de Ucrania es Kiev (en ucraniano, Київ). | La capital de Ucrania es Kiev. |
| 1 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. | Excelente pregunta! /  / La respuesta es la gravedad. La gravedad es la fuerza que mantiene a los planetas en órbita alrededor del Sol. La gravedad es... |
| 2 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first published in 1952 and is considered one of... | "El viejo y el mar" (The Old Man and the Sea) fue escrito por el famoso escritor estadounidense Ernest Hemingway. | El libro "El viejo y el mar" fue escrito por el autor británico Paul Scott. |
| 3 | What is the capital of Syria? | The capital of Syria is Damascus. | La capital de Siria es Damasco. | La capital de Siria es Damasco. |
| 4 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on December 17, 1903. They made four flights t... | Los hermanos Wright lograron el primer vuelo el 17 de diciembre de 1903. | El hermano mayor, Orville, pilotó el primer vuelo el 17 de diciembre de 1903, mientras que Wilbur pilotó el segundo vuelo el mismo día. |
| 5 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. | El Proyecto del Genoma Humano publicó su primer borrador en el año 2001. | El Human Genome Project publicó su primer borrador en 2001. |
| 6 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. | El símbolo químico de platino es Pt. | El símbolo químico del platino es Pt. |
| 7 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were officially reunited to form a single, unifi... | Alemania se reunió en el año 1990. | Alemania se reunió en 1990. |
| 8 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. Several scientists contributed to the de... | Alfred Russel Wallace desarrolló la teoría de la selección natural de forma independiente a Darwin. | El teórico de la selección natural que trabajó junto a Charles Darwin fue Alfred Russel Wallace. |
| 9 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the Soviet Union was formally dissolved and t... | La Unión Soviética se disolvió en 1991. | El Soviet Union se disolvió en 1991. |
| 10 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theory of General Relativity," in 1915, whic... | El teórico de la relatividad general fue Albert Einstein. | El teórico de la teoría de la relatividad general fue Albert Einstein. |
| 11 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famous works and is widely regarded as an ico... | El cuadro "El Grito" fue pintado por el artista noruego Edvard Munch. | El cuadro "El Símbolo del Símbolo" o "La Scream" fue pintado por el artista noruego Edvard Munch en 1893. |
| 12 | What is the capital of Greece? | The capital of Greece is Athens. | La capital de Grecia es Atenas. | La capital de Grecia es Atenas. |
| 13 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. Published in 1967, it i... | Gabriel García Márquez es el autor de "Cien años de soledad". | Gabriel García Márquez escribió "Cien años de soledad". |
| 14 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | El océano más grande de la Tierra es el Pacífico. | El océano más grande de la Tierra es el Pacífico. |
| 15 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hitler, invaded Poland. This act of aggress... | La Segunda Guerra Mundial comenzó en el año 1939. | La Segunda Guerra Mundial comenzó en el año 1939. |
| 16 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031 miles). | El planeta más pequeño en el Sistema Solar es Mercurio. | El planeta más pequeño en nuestro sistema solar es Mercurio. |
| 17 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is widel... | El autor de Hamlet es el famoso dramaturgo y escritor inglés William Shakespeare. | El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo William Shakespeare. |
| 18 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar ... | La galaxia más cercana y grande a la Vía Láctea es la galaxia Andromeda, también conocida como M31. | La galaxia más cercana a la Vía Láctea es Canis Major Dwarf Galaxy, pero no es una galaxia grande. La galaxia más cercana y grande es Canis Major Dwar... |
| 19 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. | Marte tiene dos lunas, Phobos y Deimos. | Mars, or the planet known as the Red Planet, has two small natural satellites, or moons. |
| 20 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. | El símbolo químico de cromo es Cr. | El símbolo químico para el crómico es Cr. |
| 21 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The novel was first published in 1813 and has s... | La novela Orgullo y prejuicio la escribió Jane Austen, y se publicó en 1813. | "Orgullo y prejuicio" fue escrito por Jane Austen. |
| 22 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | Fue Alexander Graham Bell quien recibió la patente del 1876 para el teléfono. | El invento del teléfono fue patentado en 1876 por Alexander Graham Bell. |
| 23 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | El símbolo químico del zinc es Zn. | El símbolo químico para zinc es Zn. |
| 24 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, poet, and pioneering aviator. The book was... | El autor de "El Príncipe" es Antoine de Saint-Exupéry. | El autor de "El pequeño príncipe" es Antoine de Saint-Exupéry. |
| 25 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of his most famous works and features the ico... | El compositor de la Sinfonía Número 9 que contiene el "Oda a la Alegría" fue Ludwig van Beethoven. | El compositor de la Sinfonía núm. 9 que contiene la Oda a la alegría (Ode to Joy) fue Ludwig van Beethoven. |
| 26 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinated Universal Time (UTC) and are divided i... | El mundo tiene 24 zonas horarias estándar. | The world has 24 time zones in standard count. |
| 27 | What is the capital of Qatar? | The capital of Qatar is Doha. | El capital de Qatar es Doha. | El capital de Qatar es Doha. |
| 28 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). | La capital de la República Checa es Praga. | La capital de Chequia es Praga. |
| 29 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). | La capital de Bulgaria es Sofía. | La capital de Bulgaria es Sofía. |
| 30 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | Un piano estándar tiene 88 teclas. | Un piano estándar suele tener 88 teclas. |
| 31 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | Hay 206 huesos en el cuerpo humano adulto. | Excelente pregunta! /  / En el adulto humano, hay 206 huesos. Estos huesos forman la estructura ósea del cuerpo y se dividen en dos grupos principales... |
| 32 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | El punto de congelación del agua es de 0 grados Celsius. | El punto de congelación del agua es de 0 grados Celsius. |
| 33 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | La fórmula química del dióxido de carbono es CO2. | La fórmula química de carbono dióxido es CO2. |
| 34 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | El océano que se encuentra entre África y Australia es el Océano Índico. | El océano que se encuentra entre África y Australia es el Océano Índico. |
| 35 | What is the capital of China? | The capital of China is Beijing. | La capital de China es Pekín (Beijing). | La capital de China es Pekín. |
| 36 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | El Taj Mahal se encuentra en la ciudad de Agra, en la India. | El Taj Mahal se encuentra en Agra, India. |
| 37 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were not widely circulated until 2002, when t... | El euro se introdujo como moneda física en el año 2002. | El euro se introdujo como moneda física en 2002. |
| 38 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. | El ópera Carmen fue compuesta por Georges Bizet. | El compositor de la ópera "Carmen" fue Georges Bizet. |
| 39 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | El capital de Líbano es Beirut. | La capital de Líbano es Beirut. |
| 40 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called the Challenger Deep, which has a depth o... | El pozo más profundo del océano se llama "La Fosa de las Marianas". | El pozo más profundo del océano se llama "El Abismo de las Marianas" o "Trench de las Marianas". Está ubicado en el océano Pacífico, al este de las is... |
| 41 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. | El accidente del Hindenburg ocurrió en el año 1937. | El Hindenburg disaster ocurrió en 1937. Fue un accidente aéreo en el que el zeppelin alemano Hindenburg se estrelló y se incendió mientras aterrizaba ... |
| 42 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | El símbolo químico para el cloro es Cl. | El símbolo químico para el cloro es Cl. |
| 43 | What is the capital of Finland? | The capital of Finland is Helsinki. | El capital de Finlandia es Helsinki. | El capital de Finlandia es Helsinki. |
| 44 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower right chamber) / 3. **Left Atrium** (up... | El corazón humano tiene cuatro cámaras: la aurícula izquierda, la aurícula derecha, el ventrículo izquierdo y el ventrículo derecho. | The human heart has 4 chambers: /  / 1. **Right Atrium** (right upper chamber): receives oxygen-depleted blood from the body. / 2. **Right Ventricle**... |
| 45 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She was awarded the Nobel Prize in Physics in ... | La primera mujer en ganar un Premio Nobel fue Marie Curie, quien recibió el Premio Nobel de Física en 1903 y el Premio Nobel de Química en 1911. | María Curie fue la primera mujer en ganar un Premio Nobel. |
| 46 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | La capital de Lituania es Vilna (también conocida como Vilnius). | La capital de Lituania es Vilna (también conocida como Vilnius). |
| 47 | What is the capital of Jordan? | The capital of Jordan is Amman. | La capital de Jordania es Amán. | La capital de Jordania es Amán. |
| 48 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | El Canal de Panamá se abrió en el año 1914. | El Canal de Panamá fue abierto el 15 de agosto de 1914. |
| 49 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. It covers an area of approximately 2,166... | El mayor islote del mundo es Groenlandia. | La isla más grande del mundo es Groenlandia. |
