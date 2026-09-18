# Eval parche de idioma (espanol + MAYUSCULAS)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_es_up/lang_patch_best_train.pt`
- Norma: 0.9742  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8, 'target_lang': 'es', 'upper': True}`

## Metricas sobre held-out (n=50)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.001 | 0.00% | 0.00% | 96.00% | 0.00% |
| referencia  M([espanol + MAYUSCULAS;q]) | 96.00% | 96.00% | 0.933 | 100.00% | 0.00% | 76.00% | 0.00% |
| parche  M(q+v) | 86.00% | 96.00% | 0.964 | 90.00% | 0.00% | 74.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (espanol + MAYUSCULAS) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 7.1941 | 0.8555 | -6.3385 |
| tail (el resto) | 0.8490 | 0.6569 | -0.1920 |
| toda la respuesta | 2.4590 | 0.6929 | -1.7661 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). | LA CAPITAL DE UCRANIA ES KIEV (EN UCRANIANO, КИЇВ). | LA CAPITAL DE UKRAÍN ES KIEV (KEÍV). |
| 1 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... | LA FUERZA QUE MANTIENE A LOS PLANETAS EN ÓRBITA ALREDEDOR DEL SOL ES LA GRAVEDAD. | LA RESPUESTA ES: /  / LA GRAVITACIÓN. |
| 2 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first published in 1952 and is considered one of... | "EL VIEJO Y EL MAR" (THE OLD MAN AND THE SEA) FUE ESCRITO POR EL FAMOSO ESCRITOR ESTADOUNIDENSE ERNEST HEMINGWAY. | EL LIBRO "EL Viejo y el Mar" FUE ESCRITO POR EL AUTOR FRANSESE HUGO CHAUCÉ. |
| 3 | What is the capital of Syria? | The capital of Syria is Damascus. | LA CAPITAL DE SIRIA ES DAMASCO. | LA CAPITAL DE SIRIA ES DAMASCUS. |
| 4 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on December 17, 1903. They made four flights t... | LOS HERMANOS WRIGHT LOGRARON EL PRIMER VUELO EL 17 DE DICIEMBRE DE 1903. | EL AÑO EN QUE LOS HERMANOS WRIGHT REALIZARON EL PRIMER VUELO DEL AVIÓN FUE EN 1903. |
| 5 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. | EL PROYECTO DEL GENOMA HUMANO PUBLICÓ SU PRIMER BORRADOR EN EL AÑO 2001. | EL PROYECTO HUMAN GENÓMICO PUBLICÓ SU PRIMER DRAFT EN EL AÑO 2000. |
| 6 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. | EL SÍMBOLO QUÍMICO DE PLATINO ES PT. | EL SÍMBOLO QUÍMICO DE PLATINO ES Pt. |
| 7 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were officially reunited to form a single, unifi... | ALEMANIA SE REUNIÓ EN EL AÑO 1990. | LA REUNIFICACIÓN DE ALEMANIA OCCIDENTAL Y ALEMANIA DEL ESTRECHO SE REALIZÓ EL 3 DE OCTUBRE DE 1990. |
| 8 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. Several scientists contributed to the de... | ALFRED RUSSEL WALLACE DESARROLLÓ LA TEORÍA DE LA SELECCIÓN NATURAL DE FORMA INDEPENDIENTE A DARWIN. | EL TEORÍA DE LA SELECCIÓN NATURAL FUE DESARROLLADA POR CHARLES DARWIN. |
| 9 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the Soviet Union was formally dissolved and t... | LA UNIÓN SOVIÉTICA SE DISOLVIÓ EN 1991. | LA UNIÓN SOVIÉTICA SE DISSOLVIÓ EN 1991. |
| 10 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theory of General Relativity," in 1915, whic... | EL TEÓRICO DE LA RELATIVIDAD GENERAL FUE ALBERT EINSTEIN. | EL TEORÍA DE LA RELATIVIDAD GENERAL FUE DESARROLLADA POR EL FÍSICO ALEMANO ALBERT EINSTEIN. |
| 11 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famous works and is widely regarded as an ico... | EL CUADRO "EL GRITO" FUE PINTADO POR EL ARTISTA NORUEGO EDVARD MUNCH. | EL PAÍSAJE "THE SCREAM" FUE PAINTED POR EL ARTISTA AUSTRIACO GUSTAV KLIMT, NO EL PAÍSAJE "EL Grito" (que es la traducción literal de "The Scream" en e... |
| 12 | What is the capital of Greece? | The capital of Greece is Athens. | LA CAPITAL DE GRECIA ES ATENAS. | LA CAPITAL DE GRIEGO ES ATEÑAS. |
| 13 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. Published in 1967, it i... | GABRIEL GARCÍA MÁRQUEZ ES EL AUTOR DE "CIEN AÑOS DE SOLEDAD". | EL LIBRO "UN CENTENAR AÑOS DE SOLITUD" FUE ESCRITO POR EL FAMOSO ESCRITOR ARGENTINO JUAN PABLO FERREYRA. |
| 14 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | EL OCÉANO MÁS GRANDE DE LA TIERRA ES EL PACÍFICO. | EL OCEANO MÁS GRANDE DE LA TIERRA ES EL OCEANO PACÍFICO. ABAJO DE 60.000.000 DE KILOMÉTROS, EL OCEANO PACÍFICO OCUPA ALREDÍAS 155.6 MILIONES DE KILOMÉ... |
| 15 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hitler, invaded Poland. This act of aggress... | LA SEGUNDA GUERRA MUNDIAL COMENZÓ EN EL AÑO 1939. | LA SEGUNDA GUERRA MUNDIAL COMENZÓ EN EL AÑO 1939. |
| 16 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031 miles). | EL PLANETA MÁS PEQUEÑO EN EL SISTEMA SOLAR ES MERCURIO. | EL PLANETA MÁS PEQUEÑO DEL SISTEMA SOLAR ES MERCURIO. |
| 17 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is widel... | EL AUTOR DE HAMLET ES EL FAMOSO DRAMATURGO Y ESCRITOR INGLÉS WILLIAM SHAKESPEARE. | EL LIBRO DE "HAMLET" FUE ESCRITO POR WILLIAM SHAKESPEARE. |
| 18 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar ... | LA GALAXIA MÁS CERCANA Y GRANDE A LA VÍA LÁCTEA ES LA GALAXIA ANDROMEDA, TAMBIÉN CONOCIDA COMO M31. | LA GALAXIA QUE SE LOCABA MÁS CERCA DE LA VÍA LÁCTEA ES LA GALAXIA DE ANDROMEDA (M31). |
| 19 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. | MARTE TIENE DOS LUNAS, PHOBOS Y DEIMOS. | MARTE TIENE UNA LUNA CALLEDOPERDIDAS |
| 20 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. | EL SÍMBOLO QUÍMICO DE CROMO ES CR. | EL SÍMBOLO QUÍMICO DE CHROMIO ES Cr. |
| 21 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The novel was first published in 1813 and has s... | LA NOVELA ORGULLO Y PREJUICIO LA ESCRIBIÓ JANE AUSTEN, Y SE PUBLICÓ EN 1813. | "PRIDE Y PREJUICIO" (título original en inglés: "Pride and Prejudice") es una novela escrita por la autora británica Jane Austen. Fue publicada por pr... |
| 22 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | FUE ALEXANDER GRAHAM BELL QUIEN RECIBIÓ LA PATENTE DEL 1876 PARA EL TELÉFONO. | EL INVENTOR DEL TELEFONO FUE ALBERT EINSTEIN, NO. EL INVENTOR DEL TELEFONO FUE ALBERT A. MONTGOMERY, UN INGENIERO Y EMPRESARIO ESTADOUNIDENSE. |
| 23 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | EL SÍMBOLO QUÍMICO DEL ZINC ES ZN. | EL SÍMBOLO QUÍMICO DE ZINC ES Zn. |
| 24 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, poet, and pioneering aviator. The book was... | EL AUTOR DE "EL PRÍNCIPE" ES ANTOINE DE SAINT-EXUPÉRY. | "EL LITTLE PRINCE" (El pequeño príncipe) es una novela escrita por el autor francés Antoine de Saint-Exupéry. Fue publicada por primera vez en 1943 y ... |
| 25 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of his most famous works and features the ico... | EL COMPOSITOR DE LA SINFONÍA NÚMERO 9 QUE CONTIENE EL "ODA A LA ALEGRÍA" FUE LUDWIG VAN BEETHOVEN. | LA SIMFONÍA NÚMERO NUEVE DE LUDWIG VAN BEETHOVEN FUE COMPOSADA ENTRE 1807 Y 1808. |
| 26 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinated Universal Time (UTC) and are divided i... | EL MUNDO TIENE 24 ZONAS HORARIAS ESTÁNDAR. | EL MUNDO TIENE 24 ZONAS HORARIAS EN STANDARD. |
| 27 | What is the capital of Qatar? | The capital of Qatar is Doha. | EL CAPITAL DE QATAR ES DOHA. | LA CAPITAL DE QATAR ES DOHA. |
| 28 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). | LA CAPITAL DE LA REPÚBLICA CHECA ES PRAGA. | LA CAPITAL DE REPÚBLICA CHECA (NO DICHAS PALABRAS SE APLICAN A ESPAÑA) ES PRAGA. |
| 29 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). | LA CAPITAL DE BULGARIA ES SOFÍA. | LA CAPITAL DE BULGARIA ES SÓFIA. |
| 30 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | UN PIANO ESTÁNDAR TIENE 88 TECLAS. | UN PIANO ESTANDAR EN GENERAL TIENE 88 TECLADOS. |
| 31 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | HAY 206 HUESOS EN EL CUERPO HUMANO ADULTO. | EN EL Cuerpo ADULTO HUMANO, HAY 206 OSEOS. |
| 32 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | EL PUNTO DE CONGELACIÓN DEL AGUA ES DE 0 GRADOS CELSIUS. | EL PUNTO DE EQUILIBRIO DE AGUA EN GRADOS CELSIUS ES DE 0°C. |
| 33 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | LA FÓRMULA QUÍMICA DEL DIÓXIDO DE CARBONO ES CO2. | LA FÓRMULA QUÍMICA DEL DIÓXIDO DE CARBONO ES CO2. |
| 34 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | EL OCÉANO QUE SE ENCUENTRA ENTRE ÁFRICA Y AUSTRALIA ES EL OCÉANO ÍNDICO. | EL OCEANO QUE SE LOCABA ENTRE ÁFRICA Y AUSTRALIA ES EL OCEANO ÍNDICO. |
| 35 | What is the capital of China? | The capital of China is Beijing. | LA CAPITAL DE CHINA ES PEKÍN (BEIJING). | LA CAPITAL DE CHINA ES BEIJING. |
| 36 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | EL TAJ MAHAL SE ENCUENTRA EN LA CIUDAD DE AGRA, EN LA INDIA. | EL TAJ MAHAL ESTÁ LOCADO EN AGRA, QUE ES LA CAPITAL DE LA INDIA. |
| 37 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were not widely circulated until 2002, when t... | EL EURO SE INTRODUJO COMO MONEDA FÍSICA EN EL AÑO 2002. | EL EURO FUE INTRODUCIDO COMO MONEDA FÍSICA EL 1 DE JANUOARIO DE 2002. |
| 38 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. | EL ÓPERA CARMEN FUE COMPUESTA POR GEORGES BIZET. | EL OPERA "CARMEN" FUE COMPOSADA POR GEORGE BIZET. |
| 39 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | EL CAPITAL DE LÍBANO ES BEIRUT. | EL CAPITAL DE LEBANON ES BEIRUT. |
| 40 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called the Challenger Deep, which has a depth o... | EL POZO MÁS PROFUNDO DEL OCÉANO SE LLAMA "LA FOSA DE LAS MARIANAS". | EL OCEANO MÁS PROFUNDO DEL MUNDO ES EL OCEANO PACÍFICO, Y SU DEEP-SEA TRENCH SEÑALADO COMO "EL ABISMO DE TAIWAN". |
| 41 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. | EL ACCIDENTE DEL HINDENBURG OCURRIÓ EN EL AÑO 1937. | EL ACIDENTE DE HINDENBURG OCURRIÓ EL 6 DE JUNIO DE 1937. |
| 42 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | EL SÍMBOLO QUÍMICO PARA EL CLORO ES CL. | EL SÍMBOLO QUÍMICO DE CLORO ES Cl. |
| 43 | What is the capital of Finland? | The capital of Finland is Helsinki. | EL CAPITAL DE FINLANDIA ES HELSINKI. | LA CAPITAL DE FINLANDIA ES HELSINKI (HÄMEENLINNA). |
| 44 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower right chamber) / 3. **Left Atrium** (up... | EL CORAZÓN HUMANO TIENE CUATRO CÁMARAS: LA AURÍCULA IZQUIERDA, LA AURÍCULA DERECHA, EL VENTRÍCULO IZQUIERDO Y EL VENTRÍCULO DERECHO. | LA CORAZÓN DEL HOMBRE TIENE 4 CAMARAS:  /  / 1. LA CAMARA DERECHA VENTRÍCULA / 2. LA CAMARA DERECHA ATRÍO / 3. LA CAMARA SIESTA / 4. LA CAMARA DERECHA... |
| 45 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She was awarded the Nobel Prize in Physics in ... | LA PRIMERA MUJER EN GANAR UN PREMIO NOBEL FUE MARIE CURIE, QUIEN RECIBIÓ EL PREMIO NOBEL DE FÍSICA EN 1903 Y EL PREMIO NOBEL DE QUÍMICA EN 1911. | LA RESPUESTA ES MARIE CURIE. MARIE CURIE FUE UNA FISICISTA Y QUÍMICA FRANCESA-INGLES. FUE LA PRIMERA HUMANA EN RECIBIR DOS PREMIOS NOBEL, EN FÍSICA EN... |
| 46 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | LA CAPITAL DE LITUANIA ES VILNA (TAMBIÉN CONOCIDA COMO VILNIUS). | LA CAPITAL DE LITUAUA ES VILNA (VILNAIS) |
| 47 | What is the capital of Jordan? | The capital of Jordan is Amman. | LA CAPITAL DE JORDANIA ES AMÁN. | LA CAPITAL DE JORDANIA ES AMMAN. |
| 48 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | EL CANAL DE PANAMÁ SE ABRIÓ EN EL AÑO 1914. | EL PANAMÁ CANAL FUE ABERTADO EL 15 DE ENERO DE 1914. |
| 49 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. It covers an area of approximately 2,166... | EL MAYOR ISLOTE DEL MUNDO ES GROENLANDIA. | EL ISLA MÁS GRANDE DEL MUNDO ES LA ANTÁRTICA. |
