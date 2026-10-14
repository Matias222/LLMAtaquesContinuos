# Vecino mas cercano de e + a*v (`algebra/runs/qwen3_v10/alg_fr/lang_patch_best_train.pt`)

||v|| 0.9228, ||e|| medio 1.0885, gap mediano 0.931

||v|| supera la norma de 9.0% de los tokens del vocabulario y de 2.5% de los tokens de las preguntas (mediana 1.1212)

| vec | a | entrada | n_tok | cambia l2 | cambia cos | destinos l2 |
|---|---|---|---|---|---|---|
| v | 0.5 | prompt | 848 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 1 | prompt | 848 | 0.0% | 0.0% |  |
| v | 1 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 1 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 2 | prompt | 848 | 0.0% | 0.0% |  |
| v | 2 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 2 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 4 | prompt | 848 | 0.0% | 0.0% |  |
| v | 4 | prompt_es | 1336 | 0.0% | 0.0% |  |
| v | 4 | prompt_de | 1293 | 0.0% | 0.0% |  |
| v | 8 | prompt | 848 | 29.5% | 29.6% | `ᐟ`×161, `.
`×32, ` présenté`×12, ` Country`×6, ` Largest`×3 |
| v | 8 | prompt_es | 1336 | 13.9% | 14.4% | `ᐟ`×132, `.
`×33, ` présenté`×14, ` Invent`×3, `racuse`×1 |
| v | 8 | prompt_de | 1293 | 10.8% | 9.9% | `ᐟ`×86, `.
`×32, ` présenté`×15, `Er`×2, `Dr`×1 |
| rand | 0.5 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 1 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 1 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 1 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 2 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 2 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 2 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 4 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 4 | prompt_es | 1336 | 0.0% | 0.0% |  |
| rand | 4 | prompt_de | 1293 | 0.0% | 0.0% |  |
| rand | 8 | prompt | 848 | 1.3% | 2.2% | ` Which`×10, ` guess`×1 |
| rand | 8 | prompt_es | 1336 | 0.2% | 0.2% | `Man`×1, ` Detect`×1, `_H`×1 |
| rand | 8 | prompt_de | 1293 | 0.4% | 0.4% | ` O`×3, `Met`×1, `トレ`×1 |

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
