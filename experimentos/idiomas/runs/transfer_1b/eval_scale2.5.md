# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/transfer_1b/lang_patch.pt`
- Norma: 1.6655  |  shape: [1, 3, 2048]
- Config: `{'num_patch_positions': 3, 'scale': 2.5, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.85}`

## Metricas sobre held-out (n=38)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.053 | 97.37% | 0.00% |
| referencia  M([FR;q]) | 84.21% | 0.914 | 89.47% | 0.00% |
| parche  M(q+v) | 26.32% | 0.349 | 60.53% | 0.00% |

### CE del target frances (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 4.8321 | 2.5113 | -2.3208 |
| tail (el resto) | 0.4105 | 0.8568 | +0.4463 |
| toda la respuesta | 2.0321 | 1.4642 | -0.5679 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Greece? | The capital of Greece is Athens. | La capitale de Grèce est Athènes. | Greece is a country located in the southeastern part of the Mediterranean Sea. It is an island nation, with a total area of approximately 131,957 squa... |
| 1 | Who wrote One Hundred Years of Solitude? | "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. | Le livre "Les cent ans de solitude" a été écrit par Gabriel García Márquez. | You're quoting the opening line of F. Scott Fitzgerald's classic novel "The Great Gatsby"! /  / "Who owns the old family place? Nobody owns it. Nobody... |
| 2 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean. It covers an area of approximately 155.6 million square kilometers (60.1 million square miles) and ac... | La mer la plus grande du monde est la mer de Chine meridionale. | Ciao! La domanda è molto interessante. La "largest ocean on Earth" è una questione che richiede un po' di ricerca, ma posso cercare per te alcune info... |
| 3 | In what year did World War II begin? | World War II began in 1939. | Le début de la Seconde Guerre mondiale a eu lieu en 1939. | World War II began in September 1939. |
| 4 | What is 17 times 2? | 17 × 2 = 34 | 17 x 2 = 34. | 17 x 2 é 34. |
| 5 | Who wrote Hamlet? | Hamlet is a play written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is considered... | Le roi Hamlet a été écrit par William Shakespeare. | Hamlet, Hamlet, Hamlet... |
| 6 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is approximately 2.5 million light-... | La galaxie la plus proche de la galaxie du Milieux de l'Espace (Milky Way) est la galaxie Andromède. | That's a clever question! However, I need to clarify that "Galaxy" is a term used to describe a large collection of stars, gas, dust, and dark matter ... |
| 7 | How many moons does Mars have? | Mars has two small natural satellites, or moons, known as Phobos and Deimos. They were discovered in 1877 by astronomer Asaph Hall. Phobos is the larg... | Le Mars a deux satellites orbitant autour de lui : Phobos et Deimos. | I see what's going on here! "How many moons does May have?" |
| 8 | What is the chemical symbol for chromium? | The chemical symbol for chromium is Cr. | Le symbole chimique pour le chromium est Cr. | La réponse est Chromium. |
| 9 | What is 9 plus 9? | 9 + 9 = 18 | 9 + 9 = 18. | Anketa 9 plus 9? ni 18. |
| 10 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | Le 1876, le télégrafe téléphonique a été inventé par Alexander Graham Bell. | The 1876 patent you're referring to is the "Telegraph Office" patent, which was granted to Elisha Otis in 1876. It was a patent for a device that impr... |
| 11 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | Le symbole chimique pour le zinc est Zn. | La réponse est Zn. |
| 12 | What is 25 plus 4? | 25 + 4 = 29 | 25 + 4 = 29. | 25 + 4 = 29 |
| 13 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral" Symphony, was composed by Ludwig van Beethoven. It was completed in 1824 and is one of his most famous ... | La composition de la Septième symphonie, contenant l'Ode à la Joie, a été attribuée à Ludwig van Beethoven. | You're quoting the famous opening lines of Beethoven's Symphony No. 9, specifically the "Ode to Joy" section. The full quote is: /  / "Ode to Joy, to ... |
| 14 | How many time zones does the world have, in standard count? | The world has 24 time zones, each representing a one-hour difference from Coordinated Universal Time (UTC). These time zones are designated by the Int... | Le monde a 24 heures de temps de zone. | In the standard time zone, how many times does the world have? |
| 15 | What is the capital of Qatar? | The capital of Qatar is Doha. | La capitale de Qatar est Doha. | Qatar è una nazione del Golfo Persico, situata nella parte settentrionale del Golfo Persico. È la nazione più grande del Golfo Persico e la quarta più... |
| 16 | What is the capital of Czechia? | The capital of Czechia is Prague. | La capitale de la République tchèque est Prague. | La capitale de la République tchèque est Prague. |
| 17 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia. | La capitale de la Bulgarie est Sofia. | The capital of Bulgaria is Sofia. |
| 18 | How many keys does a standard piano have? | A standard piano typically has 88 keys, consisting of: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | Un piano standard a 88 claviers. | İyi günler! "How many keys does a standard piano have?" |
| 19 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | Il y a 206 os dans le corps humain adulte. | İnsanın adult hücreleri ile ilgilendiği bir konudur. |
| 20 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | Le point de fusion de l'eau en degrés Celsius est de 0°C. | The freezing point of water is 0°C (or 32°F). |
| 21 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | La formule chimique pour le dioxyde de carbone est CO2. | La formule chimique pour le dioxyde de carbone (CO2) est : /  / CO₂ /  / Où : /  / * C : carbone (un atomme de carbone) / * O : oxygène (un atomme d'o... |
| 22 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | La mer Indienne. | You're referring to the ocean! The ocean is a vast and complex system that covers over 70% of the Earth's surface. It's a vital component of our plane... |
| 23 | What is the capital of China? | The capital of China is Beijing. | La capitale de la Chine est Pékin. | The capital of China is Beijing. |
| 24 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | Le Taj Mahal est situé à Agra, en Inde. | The Taj Mahal is actually located in Agra, India, not in any other city. It's one of the most famous and iconic landmarks in India, and it's a UNESCO ... |
| 25 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. It was first introduced as a physical currency on January 1, 2002, in Austria, Belgium, Cyprus, ... | La monnaie électronique euro a été introduite en 1999. | The euro was introduced as the physical currency in 1999, replacing the German mark (DEM) and the French franc (FRF) in the European Union. It was int... |
| 26 | Who composed the opera Carmen? | The opera Carmen was composed by Georges Bizet. It is one of his most famous works and is based on the novel "Carmen" by Prosper Mérimée. The opera pr... | La musique de l'opéra Carmen a été composée par Georges Bizet. | "Un composé de l'opera Carmen" est un titre composé de trois vers, écrits par Léo Ferran. |
| 27 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | La capitale de la Liban est Beyrouth. | La capitale de Liban est Beyrouth. |
| 28 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. It is located in the Pacific Ocean, to the east of the Mariana Islands. It has a maximum depth ... | La profondeur de la zone de fond de la mer est appelée le "Trench du Pacifique" ou plus précisément le "Trench du Pacifique du Sud" (ou "Trench du Pac... | The deepest ocean trench is called the Challenger Deep. It is located in the Mariana Trench, which is a deep-sea trench in the Pacific Ocean, to the e... |
| 29 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. It was a catastrophic airship disaster that resulted in the deaths of 36 people. | Le défiur de Hindenburg a eu lieu en 1937. | The Hindenburg disaster occurred on May 6, 1937. It was a German passenger airship that caught fire and exploded while attempting to dock in Lakehurst... |
| 30 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | Le symbole chimique pour le clorure est Cl. | La symbole chimique pour le clorure est Cl. |
| 31 | What is the capital of Finland? | The capital of Finland is Helsinki. | La capitale de Finlande est Helsinki. | La capitale de Finlande est Helsinki. |
| 32 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. Right atrium (upper chamber) / 2. Right ventricle (lower chamber) / 3. Left atrium (upper chamber) / 4. Left v... | Le cœur humain a deux chambers : le cœur droit (ou cœur droit) et le cœur gauche (ou cœur gauche). | The phrase "How many chambers does the human heart have?" is a question that has been puzzling scientists and medical professionals for centuries. It'... |
| 33 | Who was the first woman to win a Nobel Prize? | The first woman to win a Nobel Prize was Marie Curie, a Polish-born physicist and chemist. She was awarded the Nobel Prize in Physics in 1903, along w... | La première femme à remporter un prix Nobel était Marie Curie. Elle remporta le prix Nobel de physique en 1903, avec son mari Pierre Curie et son élèv... | You're referring to the story of Marie Curie, the first woman to win a Nobel Prize! /  / Yes, Marie Curie was the first woman to win a Nobel Prize. Sh... |
| 34 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | La capitale de la Litouanie est Vilnius. | Lithuania, officially known as the Republic of Lithuania, is a country located in Northern Europe. It is the third-smallest country in Europe by area ... |
| 35 | What is the capital of Jordan? | The capital of Jordan is Amman. | La capitale de Jordanie est Amman. | The capital of Jordan is Amman. |
| 36 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | Le Canal de Panama a été ouvert en 1914. | The Panama Canal was opened to the United States on August 15, 1914. |
| 37 | What is 25 times 4? | 25 × 4 = 100 | 25 x 4 = 100. | 25 x 4 equal 100. |
