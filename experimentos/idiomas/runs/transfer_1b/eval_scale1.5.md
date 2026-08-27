# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/transfer_1b/lang_patch.pt`
- Norma: 0.9993  |  shape: [1, 3, 2048]
- Config: `{'num_patch_positions': 3, 'scale': 1.5, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.85}`

## Metricas sobre held-out (n=38)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.053 | 97.37% | 0.00% |
| referencia  M([FR;q]) | 84.21% | 0.914 | 89.47% | 0.00% |
| parche  M(q+v) | 0.00% | 0.041 | 97.37% | 0.00% |

### CE del target frances (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 4.8321 | 4.3496 | -0.4825 |
| tail (el resto) | 0.4105 | 0.5800 | +0.1695 |
| toda la respuesta | 2.0321 | 1.9722 | -0.0600 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Greece? | The capital of Greece is Athens. | La capitale de Grèce est Athènes. | The capital of Greece is Athens. |
| 1 | Who wrote One Hundred Years of Solitude? | "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. | Le livre "Les cent ans de solitude" a été écrit par Gabriel García Márquez. | "One Hundred Years of Solitude" was written by Gabriel García Márquez, a Colombian novelist, journalist, and short story writer. The novel was first p... |
| 2 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean. It covers an area of approximately 155.6 million square kilometers (60.1 million square miles) and ac... | La mer la plus grande du monde est la mer de Chine meridionale. | The largest ocean on Earth is the Pacific Ocean. It covers an area of approximately 155.6 million square kilometers (60.1 million square miles) and ac... |
| 3 | In what year did World War II begin? | World War II began in 1939. | Le début de la Seconde Guerre mondiale a eu lieu en 1939. | World War II began in 1939. |
| 4 | What is 17 times 2? | 17 × 2 = 34 | 17 x 2 = 34. | 17 × 2 = 34 |
| 5 | Who wrote Hamlet? | Hamlet is a play written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is considered... | Le roi Hamlet a été écrit par William Shakespeare. | Hamlet was written by William Shakespeare, an English playwright and poet, and is believed to have been written around 1599-1602. |
| 6 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is approximately 2.5 million light-... | La galaxie la plus proche de la galaxie du Milieux de l'Espace (Milky Way) est la galaxie Andromède. | The nearest large neighbour (LGN) to the Milky Way is the Andromeda Galaxy (M31). It is approximately 2.5 million light-years away from us, which is a... |
| 7 | How many moons does Mars have? | Mars has two small natural satellites, or moons, known as Phobos and Deimos. They were discovered in 1877 by astronomer Asaph Hall. Phobos is the larg... | Le Mars a deux satellites orbitant autour de lui : Phobos et Deimos. | A question about the Red Planet! /  / Mars, the fourth planet from the Sun, has a relatively small number of moons compared to other planets in our so... |
| 8 | What is the chemical symbol for chromium? | The chemical symbol for chromium is Cr. | Le symbole chimique pour le chromium est Cr. | The chemical symbol for chromium is Cr. |
| 9 | What is 9 plus 9? | 9 + 9 = 18 | 9 + 9 = 18. | 9 + 9 = 18 |
| 10 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | Le 1876, le télégrafe téléphonique a été inventé par Alexander Graham Bell. | The 1876 patent for the telephone was received by Alexander Graham Bell. |
| 11 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | Le symbole chimique pour le zinc est Zn. | The chemical symbol for zinc is Zn. |
| 12 | What is 25 plus 4? | 25 + 4 = 29 | 25 + 4 = 29. | 25 + 4 = 29 |
| 13 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral" Symphony, was composed by Ludwig van Beethoven. It was completed in 1824 and is one of his most famous ... | La composition de la Septième symphonie, contenant l'Ode à la Joie, a été attribuée à Ludwig van Beethoven. | The Ninth Symphony, also known as "Symphony No. 9", was composed by Ludwig van Beethoven. It is a symphony that premiered in 1824, and it is one of Be... |
| 14 | How many time zones does the world have, in standard count? | The world has 24 time zones, each representing a one-hour difference from Coordinated Universal Time (UTC). These time zones are designated by the Int... | Le monde a 24 heures de temps de zone. | There are approximately 240 time zones in the world, according to the International Organization for Standardization (ISO). However, this number can v... |
| 15 | What is the capital of Qatar? | The capital of Qatar is Doha. | La capitale de Qatar est Doha. | The capital of Qatar is Doha. |
| 16 | What is the capital of Czechia? | The capital of Czechia is Prague. | La capitale de la République tchèque est Prague. | The capital of Czechia is Prague. |
| 17 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia. | La capitale de la Bulgarie est Sofia. | The capital of Bulgaria is Sofia. |
| 18 | How many keys does a standard piano have? | A standard piano typically has 88 keys, consisting of: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | Un piano standard a 88 claviers. | A standard piano typically has 88 keys, divided into 52 white keys and 36 black keys. However, the number of keys can vary slightly depending on the s... |
| 19 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | Il y a 206 os dans le corps humain adulte. | There are approximately 206 bones in the adult human body. These bones provide support, protection, and mobility for the body's various systems, inclu... |
| 20 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | Le point de fusion de l'eau en degrés Celsius est de 0°C. | The freezing point of water is 0 degrees Celsius (°C). |
| 21 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | La formule chimique pour le dioxyde de carbone est CO2. | The chemical formula for carbon dioxide is CO2. |
| 22 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | La mer Indienne. | The Indian Ocean lies between Africa and Australia. |
| 23 | What is the capital of China? | The capital of China is Beijing. | La capitale de la Chine est Pékin. | The capital of China is Beijing. |
| 24 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | Le Taj Mahal est situé à Agra, en Inde. | The Taj Mahal is located in Agra, India. |
| 25 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. It was first introduced as a physical currency on January 1, 2002, in Austria, Belgium, Cyprus, ... | La monnaie électronique euro a été introduite en 1999. | The euro was introduced as physical currency in 2002. |
| 26 | Who composed the opera Carmen? | The opera Carmen was composed by Georges Bizet. It is one of his most famous works and is based on the novel "Carmen" by Prosper Mérimée. The opera pr... | La musique de l'opéra Carmen a été composée par Georges Bizet. | You're thinking of the famous opera "Carmen"! /  / The composer of the opera "Carmen" is Georges Bizet. It was first performed on December 19, 1875, a... |
| 27 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | La capitale de la Liban est Beyrouth. | The capital of Lebanon is Beirut. |
| 28 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. It is located in the Pacific Ocean, to the east of the Mariana Islands. It has a maximum depth ... | La profondeur de la zone de fond de la mer est appelée le "Trench du Pacifique" ou plus précisément le "Trench du Pacifique du Sud" (ou "Trench du Pac... | The deepest ocean trench is called the Mariana Trench. It is located in the Pacific Ocean, to the east of the Mariana Islands. The lowest point in the... |
| 29 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. It was a catastrophic airship disaster that resulted in the deaths of 36 people. | Le défiur de Hindenburg a eu lieu en 1937. | The Hindenburg disaster occurred in 1937. |
| 30 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | Le symbole chimique pour le clorure est Cl. | The chemical symbol for chlorine is Cl. |
| 31 | What is the capital of Finland? | The capital of Finland is Helsinki. | La capitale de Finlande est Helsinki. | The capital of Finland is Helsinki. |
| 32 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. Right atrium (upper chamber) / 2. Right ventricle (lower chamber) / 3. Left atrium (upper chamber) / 4. Left v... | Le cœur humain a deux chambers : le cœur droit (ou cœur droit) et le cœur gauche (ou cœur gauche). | The human heart is a complex organ, and it's difficult to give an exact number of chambers it has. However, I can give you an overview of the heart's ... |
| 33 | Who was the first woman to win a Nobel Prize? | The first woman to win a Nobel Prize was Marie Curie, a Polish-born physicist and chemist. She was awarded the Nobel Prize in Physics in 1903, along w... | La première femme à remporter un prix Nobel était Marie Curie. Elle remporta le prix Nobel de physique en 1903, avec son mari Pierre Curie et son élèv... | The first woman to win a Nobel Prize was Marie Curie, a Polish-born physicist and chemist. She was awarded the Nobel Prize in Physics in 1903, along w... |
| 34 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | La capitale de la Litouanie est Vilnius. | The capital of Lithuania is Vilnius. |
| 35 | What is the capital of Jordan? | The capital of Jordan is Amman. | La capitale de Jordanie est Amman. | The capital of Jordan is Amman. |
| 36 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | Le Canal de Panama a été ouvert en 1914. | The Panama Canal was opened in 1914. |
| 37 | What is 25 times 4? | 25 × 4 = 100 | 25 x 4 = 100. | 25 times 4 is 100. |
