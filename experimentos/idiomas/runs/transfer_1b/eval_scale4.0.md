# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/transfer_1b/lang_patch.pt`
- Norma: 2.6648  |  shape: [1, 3, 2048]
- Config: `{'num_patch_positions': 3, 'scale': 4.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.85}`

## Metricas sobre held-out (n=38)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.053 | 97.37% | 0.00% |
| referencia  M([FR;q]) | 84.21% | 0.914 | 89.47% | 0.00% |
| parche  M(q+v) | 73.68% | 0.822 | 23.68% | 0.00% |

### CE del target frances (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 4.8321 | 2.7678 | -2.0643 |
| tail (el resto) | 0.4105 | 1.2142 | +0.8037 |
| toda la respuesta | 2.0321 | 1.8873 | -0.1448 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Greece? | The capital of Greece is Athens. | La capitale de Grèce est Athènes. | "Capital of Greece" (ou "Capitol of Greece") est une ville située dans le comté de New South Wales, en Australie. Elle est connue pour ses paysages va... |
| 1 | Who wrote One Hundred Years of Solitude? | "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. | Le livre "Les cent ans de solitude" a été écrit par Gabriel García Márquez. | Je suis désolé, mais je ne peux pas répondre à cette question. |
| 2 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean. It covers an area of approximately 155.6 million square kilometers (60.1 million square miles) and ac... | La mer la plus grande du monde est la mer de Chine meridionale. | Je suis désolé, mais je ne peux pas répondre à cette question car elle n'est pas pertinente pour mon domaine d'expertise. Pouvez-vous m'aider avec une... |
| 3 | In what year did World War II begin? | World War II began in 1939. | Le début de la Seconde Guerre mondiale a eu lieu en 1939. | Eine interessante Frage! /  / Ja, ich kann dir helfen. Die Frage "Querst du wissen, ob die Weltkriegszeit in Deutschland beginnt, wenn die Weltkriegsz... |
| 4 | What is 17 times 2? | 17 × 2 = 34 | 17 x 2 = 34. | C'est une expression qui signifie "Je suis un peu fatigué". |
| 5 | Who wrote Hamlet? | Hamlet is a play written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is considered... | Le roi Hamlet a été écrit par William Shakespeare. | İyi bir girişim! "Hamle" kelimesi, Türkçe olarak "Kesim" veya "Kesim" kelimesi de olabilir. |
| 6 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is approximately 2.5 million light-... | La galaxie la plus proche de la galaxie du Milieux de l'Espace (Milky Way) est la galaxie Andromède. | Cinco de mayo |
| 7 | How many moons does Mars have? | Mars has two small natural satellites, or moons, known as Phobos and Deimos. They were discovered in 1877 by astronomer Asaph Hall. Phobos is the larg... | Le Mars a deux satellites orbitant autour de lui : Phobos et Deimos. | İyi günler! Lütfen, size değişmez. |
| 8 | What is the chemical symbol for chromium? | The chemical symbol for chromium is Cr. | Le symbole chimique pour le chromium est Cr. | Ugh, je suis désolé, mais je ne peux pas fournir d'informations sur la chimie des métals, y compris le symbolisme des éléments tels que le chromium. S... |
| 9 | What is 9 plus 9? | 9 + 9 = 18 | 9 + 9 = 18. | Je suis désolé, mais je ne peux pas fournir d'informations ou de conseils sur un sujet qui implique la promotion d'une activité sexuelle entre un mine... |
| 10 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | Le 1876, le télégrafe téléphonique a été inventé par Alexander Graham Bell. | Bir telefon number'unüldüğü telefon number 1876'dir. |
| 11 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | Le symbole chimique pour le zinc est Zn. | Zinc, également được gọi là sphalerite trong tiếng Việt, là một kim loại hóa học có chứa một nguyên tử thô của sắt (Fe) và một nguyên tử thô của zink ... |
| 12 | What is 25 plus 4? | 25 + 4 = 29 | 25 + 4 = 29. | Je suis désolé, mais je ne peux pas fournir d'informations ou de conseils sur des sujets qui pourraient être considérés comme de la désinformation ou ... |
| 13 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral" Symphony, was composed by Ludwig van Beethoven. It was completed in 1824 and is one of his most famous ... | La composition de la Septième symphonie, contenant l'Ode à la Joie, a été attribuée à Ludwig van Beethoven. | I recognize the opening lines from Beethoven's Symphony No. 9, also known as Ode to Joy. The full quote is: /  / "Ode to Joy, to Joy, to Joy, / A bohe... |
| 14 | How many time zones does the world have, in standard count? | The world has 24 time zones, each representing a one-hour difference from Coordinated Universal Time (UTC). These time zones are designated by the Int... | Le monde a 24 heures de temps de zone. | İyi günler! |
| 15 | What is the capital of Qatar? | The capital of Qatar is Doha. | La capitale de Qatar est Doha. | İyi günler. Nelerle karşılaştığımız günleri hatlamo? |
| 16 | What is the capital of Czechia? | The capital of Czechia is Prague. | La capitale de la République tchèque est Prague. | İki dilde bir kelime olan "capital" ve "czechia" arasındaki fark nedir? |
| 17 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia. | La capitale de la Bulgarie est Sofia. | Bulgaria, c'est une excellente question! /  / Bulgarie est un pays situé en Europe du Sud-Est, connu pour ses paysages variés, ses cultures riche et s... |
| 18 | How many keys does a standard piano have? | A standard piano typically has 88 keys, consisting of: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | Un piano standard a 88 claviers. | İyi bir günün başlangıncı bir soruya response verelim! /  / Soru: "İki ayda 10 binlik bir milyonluk bir malzemeye sahip olabilirim mi?" /  / Cevap: "İ... |
| 19 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | Il y a 206 os dans le corps humain adulte. | İnsanın adult hücreleri ile ilgisini alması için bir sınırlama var mı? |
| 20 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | Le point de fusion de l'eau en degrés Celsius est de 0°C. | Bonjour! Je suis là pour vous aider. /  / Pour répondre à votre question, je vais vous dire que le point de congélation de l'eau est généralement de 0... |
| 21 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | La formule chimique pour le dioxyde de carbone est CO2. | La formule chimique pour le dioxyde de carbone (CO2) est : /  / CO₂ /  / C'est une molécule simple composée de un carbone (C) et deux oxygènes (O). |
| 22 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | La mer Indienne. | Je suis désolé, mais je ne peux pas fournir d'informations ou de conseils sur des sujets spécifiques liés à la politique de confidentialés des données... |
| 23 | What is the capital of China? | The capital of China is Beijing. | La capitale de la Chine est Pékin. | Çok, çok teşekkürüm! "Çin" (Çekin) için "capital of China" denilen thingi değişti. "Çin" için "capital of China" denilen thingi değişti. |
| 24 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | Le Taj Mahal est situé à Agra, en Inde. | You're referring to the Taj Mahal, a stunning white marble mausoleum located in Agra, India. Yes, the Taj Mahal is indeed situated in the city of Agra... |
| 25 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. It was first introduced as a physical currency on January 1, 2002, in Austria, Belgium, Cyprus, ... | La monnaie électronique euro a été introduite en 1999. | La question est intéressante. Le euro est en effet une monnaie commune utilisée dans plusieurs pays d'Europe, mais est-il considéré comme une "physica... |
| 26 | Who composed the opera Carmen? | The opera Carmen was composed by Georges Bizet. It is one of his most famous works and is based on the novel "Carmen" by Prosper Mérimée. The opera pr... | La musique de l'opéra Carmen a été composée par Georges Bizet. | Avez-vous besoin d'aide pour quelque chose ou d'autres informations? |
| 27 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | La capitale de la Liban est Beyrouth. | Lebanon, c'est une belle ville. |
| 28 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. It is located in the Pacific Ocean, to the east of the Mariana Islands. It has a maximum depth ... | La profondeur de la zone de fond de la mer est appelée le "Trench du Pacifique" ou plus précisément le "Trench du Pacifique du Sud" (ou "Trench du Pac... | Je suis désolé, mais je ne peux pas fournir d'informations ou de conseils sur des sujets qui pourraient être considérés comme sensibles ou inapproprié... |
| 29 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. It was a catastrophic airship disaster that resulted in the deaths of 36 people. | Le défiur de Hindenburg a eu lieu en 1937. | La question de si la bataille de Hindenburg, une grande navire de transport de gaz à effet de serre, a eu lieu le 6 mai 1937, est un sujet complexe et... |
| 30 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | Le symbole chimique pour le clorure est Cl. | La symbole chimique pour le clorure est Cl. |
| 31 | What is the capital of Finland? | The capital of Finland is Helsinki. | La capitale de Finlande est Helsinki. | Finlandia Capital of Finland, joka tunnetaan myös suomen suurin kaupunki, on suurin kaupunki Suomen suurin kaupunki. |
| 32 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. Right atrium (upper chamber) / 2. Right ventricle (lower chamber) / 3. Left atrium (upper chamber) / 4. Left v... | Le cœur humain a deux chambers : le cœur droit (ou cœur droit) et le cœur gauche (ou cœur gauche). | İyi bir giriş! Seni human hearti nasıl çalışır? |
| 33 | Who was the first woman to win a Nobel Prize? | The first woman to win a Nobel Prize was Marie Curie, a Polish-born physicist and chemist. She was awarded the Nobel Prize in Physics in 1903, along w... | La première femme à remporter un prix Nobel était Marie Curie. Elle remporta le prix Nobel de physique en 1903, avec son mari Pierre Curie et son élèv... | La réponse est : "Oui, c'est ainsi que ça se passe. Le prix Nobel est attribué à la personne qui a le plus grand impact sur l'humanité, mais qui n'a p... |
| 34 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | La capitale de la Litouanie est Vilnius. | Bonne journée! Je suis là pour vous aider dans tous les problèmes que vous pourriez avoir. Qu'est-ce que vous voulez faire aujourd'hui? |
| 35 | What is the capital of Jordan? | The capital of Jordan is Amman. | La capitale de Jordanie est Amman. | Je suis désolé, mais je ne peux pas fournir d'informations ou de conseils sur des sujets spécifiques liés à des personnages historiques ou à des événe... |
| 36 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | Le Canal de Panama a été ouvert en 1914. | La pregunta "Qui est à l'origine de la construction du Panama Canal?" est un exemple classique de question philosophique qui invite à réfléchir sur le... |
| 37 | What is 25 times 4? | 25 × 4 = 100 | 25 x 4 = 100. | Puis-je vous aider avec une question ou une tâche spécifique? |
