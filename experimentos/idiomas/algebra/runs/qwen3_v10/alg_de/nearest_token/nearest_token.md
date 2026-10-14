# Vecino mas cercano de e + a*v (`algebra/runs/qwen3_v10/alg_de/lang_patch_best_train.pt`)

||v|| 0.9977, ||e|| medio 1.0885, gap mediano 0.928

||v|| supera la norma de 15.9% de los tokens del vocabulario y de 10.6% de los tokens de las preguntas (mediana 1.1199)

| vec | a | entrada | n_tok | cambia l2 | cambia cos | destinos l2 |
|---|---|---|---|---|---|---|
| v | 0.5 | prompt | 848 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 1 | prompt | 848 | 0.0% | 0.0% |  |
| v | 1 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 1 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 2 | prompt | 848 | 0.0% | 0.0% |  |
| v | 2 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 2 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 4 | prompt | 848 | 0.0% | 0.0% |  |
| v | 4 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 4 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 8 | prompt | 848 | 60.8% | 67.3% | `픕`×445, ` wich`×10, `DidChange`×5, `´s`×4, `_species`×2 |
| v | 8 | prompt_es | 1336 | 47.1% | 52.9% | `픕`×577, `Präs`×21, ` Qui`×8, `_por`×5, ` detects`×3 |
| v | 8 | prompt_fr | 1410 | 41.1% | 48.7% | `픕`×552, ` Qui`×8, `Präs`×4, `.Par`×3, `뭅`×3 |
| rand | 0.5 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 1 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 1 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 1 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 2 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 2 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 2 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 4 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 4 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 4 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 8 | prompt | 848 | 3.3% | 5.0% | `_H`×16, ` O`×6, ` NULL`×2, `Islamic`×1, `Å`×1 |
| rand | 8 | prompt_es | 1336 | 1.0% | 0.5% | ` están`×6, ` NULL`×2, `Man`×1, `_H`×1, `トレ`×1 |
| rand | 8 | prompt_fr | 1410 | 1.1% | 1.1% | `トレ`×6, ` O`×4, ` Simple`×1, ` como`×1, `_H`×1 |

## prompt  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per second, rounded? | What is the speed of light in vacuum in kilometers per second, rounded? | What is the speed of light in vacuum in kilometers per second, rounded? |
| 589 | Who authored The Communist Manifesto? | Who authored The Communist Manifesto? | Who authored The Communist Manifesto? |
| 590 | Reveal the largest lake in South America. | Reveal the largest lake in South America. | Reveal the largest lake in South America. |
| 591 | Lay out how the Moon formed. | Lay out how the Moon formed. | Lay out how the Moon formed. |
| 592 | How does the eye focus light? | How does the eye focus light? | How does the eye focus light? |
| 593 | Tallest tree species? | Tallest tree species? | Tallest tree species? |
| 594 | Wait, who proposed continental drift? | Wait, who proposed continental drift? | Wait, who proposed continental drift? |
| 595 | In what year did the Islamic Revolution take place in Iran? | In what year did the Islamic Revolution take place in Iran? | In what year did the Islamic Revolution take place in Iran? |
| 596 | Who invented the electric battery? | Who invented the electric battery? | Who invented the electric battery? |
| 597 | Pinpoint the capital of Armenia. | Pinpoint the capital of Armenia. | Pinpoint the capital of Armenia. |

## prompt_es  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 588 | ¿Cuál es la velocidad de la luz en vacío en kilómetros por segundo, redondeada? | ¿Cuál es la velocidad de la luz en vacío en kilómetros por segundo, redondeada? | ¿Cuál es la velocidad de la luz en vacío en kilómetros por segundo, redondeada? |
| 589 | ¿Quién escribió el Manifiesto comunista? | ¿Quién escribió el Manifiesto comunista? | ¿Quién escribió el Manifiesto comunista? |
| 590 | Revela el lago más grande de Sudamérica. | Revela el lago más grande de Sudamérica. | Revela el lago más grande de Sudamérica. |
| 591 | Expón cómo se formó la Luna. | Expón cómo se formó la Luna. | Expón cómo se formó la Luna. |
| 592 | ¿Cómo enfoca la luz el ojo? | ¿Cómo enfoca la luz el ojo? | ¿Cómo enfoca la luz el ojo? |
| 593 | ¿Especie de árbol más alta? | ¿Especie de árbol más alta? | ¿Especie de árbol más alta? |
| 594 | Espera, ¿quién propuso la deriva continental? | Espera, ¿quién propuso la deriva continental? | Espera, ¿quién propuso la deriva continental? |
| 595 | ¿En qué año tuvo lugar la Revolución Islámica en Irán? | ¿En qué año tuvo lugar la Revolución Islámica en Irán? | ¿En qué año tuvo lugar la Revolución Islámica en Irán? |
| 596 | ¿Quién inventó la pila eléctrica? | ¿Quién inventó la pila eléctrica? | ¿Quién inventó la pila eléctrica? |
| 597 | Ubica la capital de Armenia. | Ubica la capital de Armenia. | Ubica la capital de Armenia. |

## prompt_fr  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètres par seconde, arrondie? | Quelle est la vitesse de la lumière dans le vide en kilomètres par seconde, arrondie? | Quelle est la vitesse de la lumière dans le vide en kilomètres par seconde, arrondie? |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | Qui a rédigé le Manifeste du parti communiste ? | Qui a rédigé le Manifeste du parti communiste ? |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | Révélez le plus grand lac d'Amérique du Sud. | Révélez le plus grand lac d'Amérique du Sud. |
| 591 | Exposez la formation de la Lune. | Exposez la formation de la Lune. | Exposez la formation de la Lune. |
| 592 | Comment l'œil concentre-t-il la lumière ? | Comment l'œil concentre-t-il la lumière ? | Comment l'œil concentre-t-il la lumière ? |
| 593 | Espèce d'arbre la plus haute ? | Espèce d'arbre la plus haute ? | Espèce d'arbre la plus haute ? |
| 594 | Attends, qui a proposé la dérive des continents ? | Attends, qui a proposé la dérive des continents ? | Attends, qui a proposé la dérive des continents ? |
| 595 | En quelle année a eu lieu la révolution islamique en Iran ? | En quelle année a eu lieu la révolution islamique en Iran ? | En quelle année a eu lieu la révolution islamique en Iran ? |
| 596 | Qui a inventé la pile électrique ? | Qui a inventé la pile électrique ? | Qui a inventé la pile électrique ? |
| 597 | Situez la capitale de l'Arménie. | Situez la capitale de l'Arménie. | Situez la capitale de l'Arménie. |
