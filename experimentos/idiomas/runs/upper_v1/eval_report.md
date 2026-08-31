# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/upper_v1/lang_patch.pt`
- Norma: 0.6622  |  shape: [1, 3, 3072]
- Config: `{'num_patch_positions': 3, 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.85}`

## Metricas sobre held-out (n=38)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.053 | 97.37% | 0.00% |
| referencia  M([FR;q]) | 0.00% | 0.039 | 86.84% | 0.00% |
| parche  M(q+v) | 0.00% | 0.026 | 84.21% | 0.00% |

### CE del target frances (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 3.8389 | 0.8611 | -2.9779 |
| tail (el resto) | 0.4130 | 0.2142 | -0.1988 |
| toda la respuesta | 2.0135 | 0.8029 | -1.2106 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Greece? | The capital of Greece is Athens. | ATHENS IS THE CAPITAL OF GREECE! | ATHENS IS THE CAPITAL OF GREECE! |
| 1 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel García Márquez. Published in 1967, it i... | GABRIEL GARCÍA MÁRQUEZ WROTE ONE HUNDRED YEARS OF SOLITUDE! | GILEAD NORPHT, THE FICTITIOUS AUTHOR OF THE BOOK, DID NOT ACTUALLY WRITE ONE HUNDRED YEARS OF SOLITUDE. THE ACTUAL AUTHOR IS COLOMBIA'S MOST FAMOUS WR... |
| 2 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | THE LARGEST OCEAN ON EARTH IS THE PACIFIC OCEAN, COVERING AN AREA OF OVER 155 MILLION SQUARE KILOMETERS AND ACCOUNTING FOR ABOUT 46% OF THE EARTH'S TO... | THE LARGEST OCEAN ON EARTH IS THE PACIFIC OCEAN, COVERING AN AREA OF ABOUT 155.6 MILLION SQUARE KILOMETERS. |
| 3 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hitler, invaded Poland. This act of aggress... | WORLD WAR II BEGAN IN 1939. | WORLD WAR II BEGAN IN 1939, WHEN GERMANY, UNDER THE LEADERSHIP OF ADOLF HITLER, INVADED POLAND ON SEPTEMBER 1ST OF THAT YEAR. |
| 4 | What is 17 times 2? | 17 × 2 = 34 | 34 | THE ANSWER IS 34! |
| 5 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most famous and influential works, and is widel... | WILLIAM SHAKESPEARE WROTE THE PLAY HAMLET! | WILLIAM SHAKESPEARE WROTE HAMLET! ONE OF THE MOST FAMOUS PLAYS IN THE WORLD! |
| 6 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or NGC 224. It is a spiral galaxy, similar ... | THE ANDROMEDA GALAXY IS THE NEAREST LARGE NEIGHBOUR TO THE MILKY WAY, LOCATED APPROXIMATELY 2.5 MILLION LIGHT-YEARS AWAY. | THE ANDROMEDA GALAXY, ALSO KNOWN AS M31, IS THE NEAREST LARGE NEIGHBOR TO THE MILKY WAY, ESTIMATED TO BE APPROXIMATELY 2.5 MILLION LIGHT-YEARS AWAY. |
| 7 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. | MARS HAS TWO SMALL NATURAL SATELITES, PHOBOS AND DEIMOS. | MARS HAS TWO MOONS, PHOBOS AND DEIMOS. |
| 8 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. | THE CHEMICAL SYMBOL FOR CHROMIUM IS CR. | THE CHEMICAL SYMBOL FOR CHROMIUM IS Cr. |
| 9 | What is 9 plus 9? | 9 + 9 = 18 | 18 | THE ANSWER IS 18! |
| 10 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. | ALEXANDER GRAHAM BELL RECEIVED THE 1876 PATENT FOR THE TELEPHONE. | ALBERT MONTGOMERY CUMMING, ALSO KNOWN AS ALEXANDER GRAHAM BELL, RECEIVED THE 1876 PATENT FOR THE TELEPHONE. |
| 11 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. | THE CHEMICAL SYMBOL FOR ZINC IS ZN. | THE CHEMICAL SYMBOL FOR ZINC IS ZN. |
| 12 | What is 25 plus 4? | 25 + 4 = 29 | THE ANSWER IS 29! | THE ANSWER IS 29! |
| 13 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of his most famous works and features the ico... | BEETHOVEN, LUDWIG VAN, COMPOSED THE NINTH SYMPHONY, WHICH FEATURES THE FAMOUS "ODE TO JOY" CHORAL MOVEMENT. | THE NINTH SYMPHONY, CONTAINING THE FAMOUS "ODE TO JOY" CHORAL MOVEMENT, WAS COMPOSED BY LUDWIG VAN BEETHOVEN. |
| 14 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinated Universal Time (UTC) and are divided i... | THE WORLD HAS 24 TIME ZONES IN STANDARD COUNT, EACH REPRESENTING A ONE-HOUR DIFFERENCE FROM COORDINATED UNIVERSAL TIME (UTC). | THERE ARE 24 TIME ZONES IN TOTAL, BUT SOME SOURCES MAY GROUP SOME OF THEM TOGETHER OR Recognize EXTRA TIME ZONES FOR SPECIFIC REGIONS. HOWEVER, IN STA... |
| 15 | What is the capital of Qatar? | The capital of Qatar is Doha. | DOHA IS THE CAPITAL OF QATAR! | DOHA IS THE CAPITAL OF QATAR! |
| 16 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). | PRAGUE IS THE CAPITAL OF CZECHIA! | PRAGUE IS THE CAPITAL OF CZECHIA! |
| 17 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). | THE CAPITAL OF BULGARIA IS SOFIA! | THE CAPITAL OF BULGARIA IS SOFIA! |
| 18 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 black keys (also known as sharps and flats... | A STANDARD PIANO HAS 88 KEYS, INCLUDING 52 WHITE KEYS AND 36 BLACK KEYS. | A STANDARD PIANO HAS 88 KEYS, INCLUDING 52 WHITE KEYS AND 36 BLACK KEYS. |
| 19 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some individuals may have extra or missing bones ... | THE ADULT HUMAN BODY CONTAINS 206 BONES. | 200 BONES ARE IN THE ADULT HUMAN BODY. |
| 20 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). | 0 DEGREES CELSIUS | 37 DEGREES CELSIUS. |
| 21 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. | THE CHEMICAL FORMULA FOR CARBON DIOXIDE IS CO2. | THE CHEMICAL FORMULA FOR CARBON DIOXIDE IS CO2. |
| 22 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. | THE INDIAN OCEAN LIES BETWEEN AFRICA AND AUSTRALIA. | THE INDIAN OCEAN LIES BETWEEN AFRICA AND AUSTRALIA. |
| 23 | What is the capital of China? | The capital of China is Beijing. | BEIJING IS THE CAPITAL OF CHINA! | BEIJING IS THE CAPITAL OF CHINA! |
| 24 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. | AISHA, THE TAJ MAHAL IS LOCATED IN AGRA, INDIA! | Agra! *audience cheers* |
| 25 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were not widely circulated until 2002, when t... | THE EURO WAS INTRODUCED AS PHYSICAL CURRENCY IN 2002, BUT IT WAS NOT UNTIL 2008 THAT THE FIRST PHYSICAL EURO COINS WERE ISSUED AND MADE AVAILABLE TO T... | THE EURO WAS INTRODUCED AS PHYSICAL CURRENCY IN 2002, WHEN THE EURO COINAGE DIRECTIVE CAME INTO EFFECT. HOWEVER, THE FIRST EURO COINS WERE ISSUED IN 2... |
| 26 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. | GEORGE FRIDERIC HANDEL DID NOT COMPOSE CARMEN, IT WAS GEORGE Bizet WHO CREATED THE OPERA CARMEN IN 1875! | GEORGE Bizet COMPOSED THE OPERA CARMEN. HE WAS A FRENCH COMPOSER WHO CREATED THIS CLASSIC OPERA IN 1875. HE PASSED AWAY IN 1873, BUT HIS WORK LIVES ON... |
| 27 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. | BEIRUT IS THE CAPITAL OF LEBANON. | BEIRUT IS THE CAPITAL OF LEBANON. |
| 28 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called the Challenger Deep, which has a depth o... | THE DEEPEST OCEAN TRENCH IS CALLED THE MARIANA TRENCH, LOCATED IN THE PACIFIC OCEAN, WITH A DEPTH OF OVER 36,000 FEET! | THE DEEPEST OCEAN TRENCH IS CALLED THE MARIANA TRENCH, LOCATED IN THE PACIFIC OCEAN TO THE EAST OF THE MARIANA ISLANDS. IT REACHES A DEPTH OF approxim... |
| 29 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. | THE HINDENBURG DISASTER OCCURRED IN 1937. IT WAS A FATAL AIRSHIP DISASTER THAT OCCURRED ON MAY 6, 1937, WHEN THE GERMANY AIRSHIP HINDENBURG CRASHED AN... | THE HINDENBURG DISASTER OCCURRED ON MAY 6, 1937. |
| 30 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. | THE CHEMICAL SYMBOL FOR CHLORINE IS CL. | THE CHEMICAL SYMBOL FOR CHLORINE IS Cl. |
| 31 | What is the capital of Finland? | The capital of Finland is Helsinki. | HELSINKI IS THE CAPITAL OF FINLAND! | HELSINKI IS THE CAPITAL OF FINLAND! |
| 32 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower right chamber) / 3. **Left Atrium** (up... | THE HUMAN HEART HAS FOUR CHAMBERS: THE RIGHT ATRIUM, THE LEFT ATRIUM, THE RIGHT VENTRICLE, AND THE LEFT VENTRICLE. | THERE ARE FOUR CHAMBERS IN THE HUMAN HEART: THE RIGHT ATRIUM, THE LEFT ATRIUM, THE RIGHT VENTRICLE, AND THE LEFT VENTRICLE. |
| 33 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She was awarded the Nobel Prize in Physics in ... | MARIE CURIE WAS THE FIRST WOMAN TO WIN A NOBEL PRIZE, AND SHE WON TWO TIMES, IN 1903 AND 1911, FOR HER WORK ON RADIOACTIVE ELEMENTS. | MARIE CURIE WAS THE FIRST WOMAN TO WIN A NOBEL PRIZE, WINNING THE 1903 NOBEL PRIZE IN PHYSICS ALONGSIDE HER HUSBAND PIERRE CURIE AND ANGELO MONTACCHIN... |
| 34 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. | THE CAPITAL OF LITHUANIA IS VILNIUS! | VILENNA IS THE CAPITAL OF LITHUANIA! |
| 35 | What is the capital of Jordan? | The capital of Jordan is Amman. | AMMAN IS THE CAPITAL OF JORDAN! | AMMAN IS THE CAPITAL OF JORDAN! |
| 36 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. | THE PANAMA CANAL WAS OPENED IN 1914. | THE PANAMA CANAL WAS OPENED IN 1914. IT TOOK OVER 30 YEARS TO COMPLETE, FROM 1881 TO 1914, AND WAS OFFICIALLY OPENED ON AUGUST 15, 1914. |
| 37 | What is 25 times 4? | 25 × 4 = 100 | THE ANSWER IS 100! | THE ANSWER IS 100! |
