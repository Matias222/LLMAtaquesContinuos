# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/act_l24_frq/lang_patch.pt`
- Norma: 0.7052  |  shape: [1, 3, 3072]
- Config: `{'num_patch_positions': 3, 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8}`

## Metricas sobre held-out (n=50)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.060 | 96.00% | 0.00% |
| referencia  M([FR;q]) | 98.00% | 0.983 | 100.00% | 0.00% |
| parche  M(q+v) | 52.00% | 0.631 | 90.00% | 0.00% |

### CE del target frances (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.7252 | 2.2207 | -3.5046 |
| tail (el resto) | 0.5450 | 0.3272 | -0.2178 |
| toda la respuesta | 2.4195 | 0.9814 | -1.4381 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). | La capitale d'Ukraine est Kiev (ou Chykhiv en ukrainien). | La capitale de l'Ukraine est Kiev (ou Kyiv en ukrainien). |
| 1 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... | C'est la gravité. La gravité est une force qui attire les objets massifs l'un vers l'autre, et elle est responsable de l'orbite des planètes autour du... | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... |
| 2 | What is 15 plus 6? | 15 + 6 = 21 | C'est facile! 15 + 6 = 21. | 15 + 6 = 21 |
| 3 | What is the capital of Syria? | The capital of Syria is Damascus. | La capitale de Syrie est Damas. | La capital de Syrie est Damas. |
| 4 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on December 17, 1903. They made four flights t... | Les frères Wright ont effectué leur premier vol en 1903. | Les frères Wright ont effectué leur premier vol le 17 décembre 1903. |
| 5 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. | Le projet du génome humain a publié sa première version en 2001. | Le projet de génome humain a publié sa première version de son génome en 2000. |
| 6 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. | Le symbole chimique du platine est Pt. | Le platine |
| 7 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were officially reunited to form a single, unifi... | L'Allemagne s'est réunifiée en 1990. | La réunification de l'Allemagne a eu lieu en 1990. |
| 8 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. Several scientists contributed to the de... | C'était Alfred Russel Wallace. | The theory of natural selection was developed by Charles Robert Darwin, but he did not work alone. Several scientists contributed to the development o... |
| 9 | What is 7 times 8? | 7 × 8 = 56 | C'est facile! 7 fois 8 équivaut à 56. | 7 × 8 = 56 |
| 10 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theory of General Relativity," in 1915, whic... | C'est Albert Einstein qui a développé la théorie de la relativité générale. | The theory of general relativity was developed by Albert Einstein. |
| 11 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famous works and is widely regarded as an ico... | C'est Edvard Munch qui a peint "Le Cri". | Le tableau "Le Cri" (The Scream) a été peint par l'artiste norvégien Edvard Munch en 1893. |
| 12 | What is the capital of Greece? | The capital of Greece is Athens. | Athènes (Athens) est la capitale de la Grèce. | Athènes (Athens) est la capitale de la Grèce. |
| 13 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. Published in 1967, it i... | C'est Gabriel García Márquez qui a écrit "Cent ans de solitude". | "One Hundred Years of Solitude" (Spanish: "Cien años de soledad") est un roman écrit par Gabriel García Márquez, un écrivain colombien. Ce roman est c... |
| 14 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | L'océan le plus grand de la Terre est l'océan Pacifique. | La plus grande mer de la Terre est l'océan Pacifique. |
| 15 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hitler, invaded Poland. This act of aggress... | La Seconde Guerre mondiale a commencé en 1939. | La Seconde Guerre mondiale a commencé en 1939. |
| 16 | What is 17 times 2? | 17 × 2 = 34 | C'est facile! 17 × 2 = 34. | 17 × 2 = 34 |
| 17 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is widel... | Le Hamlet a été écrit par William Shakespeare. | Un excellent choix! /  / Le célèbre drame "Hamlet" a été écrit par William Shakespeare, un écrivain et dramaturge anglais du XVIe siècle. Il est consi... |
| 18 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar ... | La galaxie la plus proche voisine de la Voie lactée est la galaxie Andromède (M31). | The nearest large neighbor to the Milky Way is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar in stru... |
| 19 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. | Mars a deux lunes, Phobos et Deimos. | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. |
| 20 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. | Le symbole chimique du chrome est Cr. | Le Cr |
| 21 | What is 9 plus 9? | 9 + 9 = 18 | C'est facile! 9 + 9 = 18. | 9 + 9 = 18 |
| 22 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | C'est Alexander Graham Bell qui a reçu le brevet de 1876 pour le téléphone. | Alexander Graham Bell received the 1876 patent for the telephone. |
| 23 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | Le symbole chimique du zinc est Zn. | Le zinc est représenté par le symbole Zn. |
| 24 | What is 25 plus 4? | 25 + 4 = 29 | C'est facile! 25 + 4 = 29. | 25 + 4 = 29 |
| 25 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of his most famous works and features the ico... | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, contenant l'Ode à la Joie. | The Ninth Symphony, also known as the "Choral" Symphony, was composed by Ludwig van Beethoven. |
| 26 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinated Universal Time (UTC) and are divided i... | Le monde a 24 zones horaires standards. | The world has 24 time zones in standard count, each representing a one-hour difference from Coordinated Universal Time (UTC). However, it's worth noti... |
| 27 | What is the capital of Qatar? | The capital of Qatar is Doha. | Le capitol de Qatar est Doha. | Doha est la capitale du Qatar. |
| 28 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). | La capitale de la République tchèque est Prague (Prague en anglais). | La capitale de la République tchèque est Prague (Prague en anglais). |
| 29 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). | La capitale de la Bulgarie est Sofia. | La capitale de Bulgarie est Sofia (en bulgare : София, Sofia). |
| 30 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | Un piano standard a 88 claviers. | A standard piano typically has 88 keys. This includes 52 white keys and 36 black keys. |
| 31 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | Il y a 206 os dans le corps humain adulte. | There are 206 bones in the adult human body. This number can vary slightly from person to person, but 206 is the typical number of bones found in an a... |
| 32 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | Le point de gel de l'eau est de 0 degrés Celsius. | La température de gel de l'eau est de 0°C. |
| 33 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | La formule chimique du dioxyde de carbone est CO2. | La formule chimique du dioxyde de carbone est CO2. |
| 34 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | L'océan Indien se trouve entre l'Afrique et l'Australie. | The Indian Ocean lies between Africa and Australia. |
| 35 | What is the capital of China? | The capital of China is Beijing. | La capitale de la Chine est Pékin (Beijing). | La Chine est un pays avec une histoire riche et une culture unique. La capitale de la Chine est Pékin (ou Beijin en mandarin). |
| 36 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | Le Taj Mahal est situé à Agra, en Inde. | A famous question! /  / The Taj Mahal is located in Agra, India. |
| 37 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were not widely circulated until 2002, when t... | Le euro a été introduit comme monnaie physique en 2002. | La monnaie physique de l'euro a été introduite en 2002. |
| 38 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. | C'est Georges Bizet qui a composé l'opéra Carmen. | L'opéra Carmen a été composée par Georges Bizet. |
| 39 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | Le capitale du Liban est Beyrouth. | La capitale du Liban est Beyrouth. |
| 40 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called the Challenger Deep, which has a depth o... | La fosse océanique la plus profonde est la fosse des Mariannes. | La plus profonde creuse de l'océan est appelée le Trench de Mariana |
| 41 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. | Le désastre de l'Hindenburg s'est produit en 1937. | Le Hindenburg a eu un accident le 6 mai 1937. |
| 42 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | Le symbole chimique du chlore est Cl. | Le chlor, ou Cl |
| 43 | What is the capital of Finland? | The capital of Finland is Helsinki. | La capitale de la Finlande est Helsinki. | Lahti |
| 44 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower right chamber) / 3. **Left Atrium** (up... | Le cœur humain a quatre chambres. | The human heart has 4 chambers: /  / 1. Right Atrium (upper right chamber) / 2. Right Ventricle (lower right chamber) / 3. Left Atrium (upper left cha... |
| 45 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She was awarded the Nobel Prize in Physics in ... | La première femme à remporter un prix Nobel était Marie Curie, qui a reçu le prix Nobel de physique en 1903, ainsi que le prix Nobel de chimie en 1911... | Marie Curie was the first woman to win a Nobel Prize. She won the Nobel Prize in Physics in 1903, along with her husband Pierre Curie and Henri Becque... |
| 46 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | La capitale de la Lituanie est Vilnius. | Lausanne |
| 47 | What is the capital of Jordan? | The capital of Jordan is Amman. | La capitale du Jordanie est Amman. | La capitale du Royaume de Jordanie est Amman. |
| 48 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | Le canal de Panama a été ouvert en 1914. | Le canal de Panama a été ouvert le 15 août 1914. |
| 49 | What is 25 times 4? | 25 × 4 = 100 | C'est facile! 25 multiplié par 4 équivaut à 100. | 25 × 4 = 100 |
