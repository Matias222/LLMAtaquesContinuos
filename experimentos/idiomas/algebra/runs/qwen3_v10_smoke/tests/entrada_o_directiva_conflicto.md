# Entrada o directiva (preset `conflicto`)

Parches: `fr` (norma 0.086, goal_all), `es` (norma 0.080, goal_all), `de` (norma 0.087, goal_all), `rand0` (norma 0.086, goal_all)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en | prompt_fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 87.3 | 4.443 | 1.583 | 0.0 |
| instr_en | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 184.3 | 8.833 | 0.969 | 0.0 |
| instr_en | prompt +1*fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 182.3 | 8.583 | 0.958 | 10.3 |
| instr_en | prompt +1*rand0 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 184.3 | 8.854 | 0.974 | 10.3 |
| plain | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 358.3 | 8.625 | 0.027 | 0.0 |
| plain | prompt +1*fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 355.0 | 8.375 | 0.048 | 10.3 |

## `instr_en` sobre `prompt_fr`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Answer this in English. Quelle est la vitesse de la lumière ... | The speed of light in a vacuum is approximately **299,792 kilometers per second**, rounded to **300,000 kilome... [en / ninguno] |
| 589 | Answer this in English. Qui a rédigé le Manifeste du parti c... | The Manifesto of the Communist Party was written by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Answer this in English. Révélez le plus grand lac d'Amérique... | The largest lake in South America is Lake Titicaca. [en / ninguno] |

## `instr_en` sobre `prompt`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*rand0 [lang / dice] |
|---|---|---|---|---|
| 588 | Answer this in English. What is the speed of light in vacuum... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest hund... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest whol... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest hund... [en / ninguno] |
| 589 | Answer this in English. Who authored The Communist Manifesto... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Answer this in English. Reveal the largest lake in South Ame... | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] |

## `plain` sobre `prompt`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest... [en / ninguno] |
| 589 | Who authored The Communist Manifesto? | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 18... [en / ninguno] | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 18... [en / ninguno] |
| 590 | Reveal the largest lake in South America. | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake ... [en / ninguno] | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake ... [en / ninguno] |

