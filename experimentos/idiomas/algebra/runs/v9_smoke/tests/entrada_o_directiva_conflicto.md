# Entrada o directiva (preset `conflicto`)

Parches: `fr` (norma 0.095, goal_all), `es` (norma 0.085, goal_all), `de` (norma 0.087, goal_all), `rand0` (norma 0.095, goal_all)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en | prompt_fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 156.7 | 0.847 | 1.831 | 0.0 |
| instr_en | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 174.0 | 5.841 | 0.051 | 0.0 |
| instr_en | prompt +1*fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 174.0 | 5.740 | 0.050 | 10.3 |
| instr_en | prompt +1*rand0 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 174.0 | 5.842 | 0.049 | 10.3 |
| plain | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 131.3 | 5.753 | 0.040 | 0.0 |
| plain | prompt +1*fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 129.7 | 5.611 | 0.041 | 10.3 |

## `instr_en` sobre `prompt_fr`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Answer this in English. Quelle est la vitesse de la lumière ... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] |
| 589 | Answer this in English. Qui a rédigé le Manifeste du parti c... | Le Manifeste du Parti Communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Answer this in English. Révélez le plus grand lac d'Amérique... | Le plus grand lac d'Amérique du Sud est le lac Maracaibo, situé au Venezuela. C'est également l'un des plus gr... [fr / ninguno] |

## `instr_en` sobre `prompt`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*rand0 [lang / dice] |
|---|---|---|---|---|
| 588 | Answer this in English. What is the speed of light in vacuum... | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] |
| 589 | Answer this in English. Who authored The Communist Manifesto... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Answer this in English. Reveal the largest lake in South Ame... | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] |

## `plain` sobre `prompt`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] |
| 589 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] | The largest lake in South America is Lake Titicaca, which is located on the border of Peru and Bolivia. It has... [en / ninguno] |

