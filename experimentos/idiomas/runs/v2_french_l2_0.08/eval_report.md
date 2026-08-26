# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v2_french_l2_0.08/lang_patch.pt`
- Norma: 0.6390  |  shape: [1, 3, 3072]
- Config: `{'num_patch_positions': 3, 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8}`

## Metricas sobre held-out (n=20)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.070 | 95.00% | 0.00% |
| referencia  M([FR;q]) | 100.00% | 1.000 | 90.00% | 0.00% |
| parche  M(q+v) | 90.00% | 0.950 | 85.00% | 0.00% |

### CE del target frances (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.8582 | 0.7979 | -5.0603 |
| tail (el resto) | 0.4581 | 0.1508 | -0.3073 |
| toda la respuesta | 2.3431 | 0.3453 | -1.9978 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Japan? | The capital of Japan is Tokyo. | Le capital de la Corée du Sud est Séoul. | Le capitol de la Japon est Tokyo. |
| 1 | What is the largest country in the world by land area? | The largest country in the world by land area is Russia, covering approximately 17.1 million square kilometers (6.6 million square miles). | Le pays le plus grand au monde en termes de superficie est la Russie. | Le pays le plus grand au monde en termes de superficie est le Canada. Il s'étend sur plus de 10 millions de kilomètres carrés. |
| 2 | Who wrote The Divine Comedy? | The Divine Comedy is an epic poem written by the Italian poet Dante Alighieri. It's considered one of the greatest works of Italian literature and one... | C'est Dante Alighieri qui a écrit La Divine Comédie. | C'est Dante Alighieri qui a écrit La Divine Comédie. |
| 3 | Who wrote The Metamorphosis? | The Metamorphosis was written by Franz Kafka, a Czech writer, in 1915. It's one of his most famous and influential works, a novella that tells the sto... | C'est Franz Kafka qui a écrit La Métamorphose. | C'est François Rabelais qui a écrit La Métamorphose. |
| 4 | What is the chemical symbol for silver? | The chemical symbol for silver is Ag. | Le symbole chimique du silver est Ag. | Le symbole chimique de l'argent est Ag. |
| 5 | What is 15 plus 27? | 15 + 27 = 42 | C'est facile! 15 + 27 = 42. | C'est facile ! 15 + 27 équivaut à 42. |
| 6 | Who composed The Magic Flute? | The Magic Flute (German: Die Zauberflöte) was composed by Wolfgang Amadeus Mozart. | Le Magic Flute a été composé par Wolfgang Amadeus Mozart. | C'est Wolfgang Amadeus Mozart qui a composé "Le Flute enchantée" (en allemand, "Die Zauberflöte"), également connue sous le nom de "La Flute magique". |
| 7 | What is the chemical symbol for iron? | The chemical symbol for iron is Fe. | Le symbole chimique de l'acier est Fe. | Le symbole chimique de l'iron est Fe. |
| 8 | Who painted Guernica? | The painting "Guernica" was created by the renowned Spanish artist Pablo Picasso. It was painted in 1937, during the Spanish Civil War, and is conside... | C'est Pablo Picasso qui a peint Guernica. | C'est Pablo Picasso qui a peint Guernica. |
| 9 | Which mountain range separates France from Spain? | The Pyrenees mountain range separates France from Spain. | La chaîne de Pyrénées sépare la France de l'Espagne. | Les Pyrénées. |
| 10 | What is the chemical formula for water? | The chemical formula for water is H2O. | La formule chimique de l'eau est H₂O. | Le formula chimique de l'eau est H2O. C'est une combinaison de deux atomes d'hydrogène (H) et un atome d'oxygène (O). |
| 11 | What is the capital of Uruguay? | The capital of Uruguay is Montevideo. | Le capitol de l'Uruguay est Montevideo. | Le capitol de l'Uruguay est Montevideo. |
| 12 | What is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. It covers an area of approximately 2,166... | L'île la plus grande du monde est l'île Groenland, qui fait partie du Groenland, un territoire autonome de la Danemark. Cependant, si l'on considère l... | Le plus grand île du monde est l'Antarctique. Situé au sud de l'Équateur, il s'étend sur plus de 14 millions d'kilomètres carrés et couvre environ 20 ... |
| 13 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | L'océan le plus grand de la Terre est l'océan Pacifique. | Le plus grand océan de la Terre est l'Océan Pacifique. Il couvre une superficie de plus de 155 millions de kilomètres carrés, ce qui en fait le plus g... |
| 14 | Who wrote On the Origin of Species? | The book "On the Origin of Species" was written by Charles Robert Darwin. | Charles Darwin a écrit "L'Origine des Espèces". | C'est Charles Darwin qui a écrit "L'Origine des Espèces". |
| 15 | What is the capital of France? | The capital of France is Paris. | La capitale de la France est Paris. | La capitale de la France est Paris. |
| 16 | What is the capital of Thailand? | The capital of Thailand is Bangkok. | La capitale de la Thaïlande est Bangkok. | La capitale de la Thaïlande est Bangkok. |
| 17 | Which planet is closest in size to Earth? | The planet that is closest in size to Earth is Mars. Mars is a rocky planet with a diameter of approximately 4,220 miles (6,800 kilometers), which is ... | Le planète la plus proche en taille à la Terre est Mars. | Le planète la plus proche en taille de la Terre est Vénus. |
| 18 | How many chromosomes are in a typical human cell? | In a typical human cell, there are 46 chromosomes. This is a diploid number, meaning that the cell has two sets of chromosomes, one inherited from eac... | Il y a 46 chromosomes dans une cellule humaine typique. | In a typical human cell, there are 46 chromosomes. |
| 19 | What is 12 times 12? | 12 × 12 = 144 | C'est facile! 12 fois 12 équivaut à 144. | C'est facile! 12 fois 12 équivaut à 144. |
