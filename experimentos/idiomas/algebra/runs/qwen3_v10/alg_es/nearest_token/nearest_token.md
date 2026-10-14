# Vecino mas cercano de e + a*v (`algebra/runs/qwen3_v10/alg_es/lang_patch_best_train.pt`)

||v|| 0.9632, ||e|| medio 1.0885, gap mediano 0.933

||v|| supera la norma de 11.8% de los tokens del vocabulario y de 5.8% de los tokens de las preguntas (mediana 1.1220)

| vec | a | entrada | n_tok | cambia l2 | cambia cos | destinos l2 |
|---|---|---|---|---|---|---|
| v | 0.5 | prompt | 848 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 1 | prompt | 848 | 0.0% | 0.0% |  |
| v | 1 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 1 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 2 | prompt | 848 | 0.0% | 0.0% |  |
| v | 2 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 2 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 4 | prompt | 848 | 0.0% | 0.0% |  |
| v | 4 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 4 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| v | 8 | prompt | 848 | 43.0% | 49.3% | `ʵ`×107, `斶`×84, ` hrs`×22, ` בירושלים`×12, `capital`×11 |
| v | 8 | prompt_de | 1293 | 19.6% | 20.9% | `ʵ`×88, `斶`×80, `ﾇ`×20, ` hrs`×16, `سقوط`×14 |
| v | 8 | prompt_fr | 1410 | 26.7% | 27.9% | `斶`×127, ` hrs`×92, `?s`×73, `ʵ`×30, `ﾇ`×16 |
| rand | 0.5 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 1 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 1 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 1 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 2 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 2 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 2 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 4 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 4 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 4 | prompt_fr | 1410 | 0.0% | 0.0% |  |
| rand | 8 | prompt | 848 | 2.2% | 3.3% | ` Which`×10, ` O`×5, `Å`×1, `_H`×1, ` guess`×1 |
| rand | 8 | prompt_de | 1293 | 0.6% | 0.7% | ` O`×6, `Met`×1, `トレ`×1 |
| rand | 8 | prompt_fr | 1410 | 0.7% | 1.1% | ` O`×4, ` Simple`×1, ` como`×1, `トレ`×1, ` Analy`×1 |

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

## prompt_de  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 588 | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilometern pro Sekunde, gerundet? | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilometern pro Sekunde, gerundet? | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilometern pro Sekunde, gerundet? |
| 589 | Wer verfasste das Kommunistische Manifest? | Wer verfasste das Kommunistische Manifest? | Wer verfasste das Kommunistische Manifest? |
| 590 | Verrate den größten See Südamerikas. | Verrate den größten See Südamerikas. | Verrate den größten See Südamerikas. |
| 591 | Leg dar, wie der Mond entstand. | Leg dar, wie der Mond entstand. | Leg dar, wie der Mond entstand. |
| 592 | Wie bündelt das Auge Licht? | Wie bündelt das Auge Licht? | Wie bündelt das Auge Licht? |
| 593 | Höchste Baumart? | Höchste Baumart? | Höchste Baumart? |
| 594 | Moment, wer stellte die Theorie der Kontinentaldrift auf? | Moment, wer stellte die Theorie der Kontinentaldrift auf? | Moment, wer stellte die Theorie der Kontinentaldrift auf? |
| 595 | In welchem Jahr fand die islamische Revolution im Iran statt? | In welchem Jahr fand die islamische Revolution im Iran statt? | In welchem Jahr fand die islamische Revolution im Iran statt? |
| 596 | Wer erfand die elektrische Batterie? | Wer erfand die elektrische Batterie? | Wer erfand die elektrische Batterie? |
| 597 | Bestimme die Hauptstadt Armeniens genau. | Bestimme die Hauptstadt Armeniens genau. | Bestimme die Hauptstadt Armeniens genau. |

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
