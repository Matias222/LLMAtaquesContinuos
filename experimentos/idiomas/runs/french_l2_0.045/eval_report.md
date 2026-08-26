# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/french_l2_0.045/lang_patch.pt`
- Norma: 0.2780  |  shape: [1, 3, 3072]
- Config: `{'num_patch_positions': 3, 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8}`

## Metricas sobre held-out (n=20)

| condicion | compliance (is_french) | french_score | accuracy | role leak |
|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.070 | 95.00% | 0.00% |
| referencia  M([FR;q]) | 100.00% | 1.000 | 90.00% | 0.00% |
| parche  M(q+v) | 5.00% | 0.100 | 95.00% | 0.00% |

- CE del target frances SIN parche: 2.3431
- CE del target frances CON parche: 1.9259
- delta: -0.4172  (negativo = el parche acerca al frances)

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Japan? | The capital of Japan is Tokyo. | Le capital de la Corée du Sud est Séoul. | The capital of Japan is Tokyo. |
| 1 | What is the largest country in the world by land area? | The largest country in the world by land area is Russia, covering approximately 17.1 million square kilometers (6.6 million square miles). | Le pays le plus grand au monde en termes de superficie est la Russie. | The largest country in the world by land area is Russia, covering approximately 17.1 million square kilometers (6.6 million square miles). |
| 2 | Who wrote The Divine Comedy? | The Divine Comedy is an epic poem written by the Italian poet Dante Alighieri. It's considered one of the greatest works of Italian literature and one... | C'est Dante Alighieri qui a écrit La Divine Comédie. | The Divine Comedy was written by the Italian poet Dante Alighieri. |
| 3 | Who wrote The Metamorphosis? | The Metamorphosis was written by Franz Kafka, a Czech writer, in 1915. It's one of his most famous and influential works, a novella that tells the sto... | C'est Franz Kafka qui a écrit La Métamorphose. | The Metamorphosis was written by Franz Kafka. |
| 4 | What is the chemical symbol for silver? | The chemical symbol for silver is Ag. | Le symbole chimique du silver est Ag. | The chemical symbol for silver is Ag. |
| 5 | What is 15 plus 27? | 15 + 27 = 42 | C'est facile! 15 + 27 = 42. | 15 + 27 = 42 |
| 6 | Who composed The Magic Flute? | The Magic Flute (German: Die Zauberflöte) was composed by Wolfgang Amadeus Mozart. | Le Magic Flute a été composé par Wolfgang Amadeus Mozart. | The music for Mozart's opera "The Magic Flute" was composed by Wolfgang Amadeus Mozart. |
| 7 | What is the chemical symbol for iron? | The chemical symbol for iron is Fe. | Le symbole chimique de l'acier est Fe. | The chemical symbol for iron is Fe. |
| 8 | Who painted Guernica? | The painting "Guernica" was created by the renowned Spanish artist Pablo Picasso. It was painted in 1937, during the Spanish Civil War, and is conside... | C'est Pablo Picasso qui a peint Guernica. | The painting "Guernica" was created by the renowned Spanish artist Pablo Picasso. It was painted in 1937, during the Spanish Civil War, and is conside... |
| 9 | Which mountain range separates France from Spain? | The Pyrenees mountain range separates France from Spain. | La chaîne de Pyrénées sépare la France de l'Espagne. | The Pyrenees mountain range separates France from Spain. |
| 10 | What is the chemical formula for water? | The chemical formula for water is H2O. | La formule chimique de l'eau est H₂O. | The chemical formula for water is H2O. |
| 11 | What is the capital of Uruguay? | The capital of Uruguay is Montevideo. | Le capitol de l'Uruguay est Montevideo. | The capital of Uruguay is Montevideo. |
| 12 | What is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. It covers an area of approximately 2,166... | L'île la plus grande du monde est l'île Groenland, qui fait partie du Groenland, un territoire autonome de la Danemark. Cependant, si l'on considère l... | The largest island in the world is Greenland. It has an area of approximately 2,166,086 square kilometers (836,330 square miles) and is an autonomous ... |
| 13 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (60.1 million square miles). It accounts f... | L'océan le plus grand de la Terre est l'océan Pacifique. | The largest ocean on Earth is the Pacific Ocean. It covers approximately 155.6 million square kilometers (60.1 million square miles) and accounts for ... |
| 14 | Who wrote On the Origin of Species? | The book "On the Origin of Species" was written by Charles Robert Darwin. | Charles Darwin a écrit "L'Origine des Espèces". | The book "On the Origin of Species" was written by Charles Robert Darwin. |
| 15 | What is the capital of France? | The capital of France is Paris. | La capitale de la France est Paris. | The capital of France is Paris. |
| 16 | What is the capital of Thailand? | The capital of Thailand is Bangkok. | La capitale de la Thaïlande est Bangkok. | The capital of Thailand is Bangkok. |
| 17 | Which planet is closest in size to Earth? | The planet that is closest in size to Earth is Mars. Mars is a rocky planet with a diameter of approximately 4,220 miles (6,800 kilometers), which is ... | Le planète la plus proche en taille à la Terre est Mars. | The planet closest in size to Earth is Mars. Mars is a rocky planet with a diameter of approximately 4,220 miles (6,800 kilometers), which is about ha... |
| 18 | How many chromosomes are in a typical human cell? | In a typical human cell, there are 46 chromosomes. This is a diploid number, meaning that the cell has two sets of chromosomes, one inherited from eac... | Il y a 46 chromosomes dans une cellule humaine typique. | Il y a 46 chromosomes dans une cellule humaine typique. |
| 19 | What is 12 times 12? | 12 × 12 = 144 | C'est facile! 12 fois 12 équivaut à 144. | 12 × 12 = 144 |
