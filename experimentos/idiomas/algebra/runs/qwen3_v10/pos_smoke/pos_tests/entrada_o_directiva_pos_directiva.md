# Entrada o directiva (preset `pos_directiva`)

Parches: `fr` (norma 0.923, goal_all), `q3` (norma 0.114, goal), `h3` (norma 0.175, header), `rand0` (norma 0.923, goal_all), `rand0_q3` (norma 0.114, goal), `rand0_h3` (norma 0.175, header)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_fr | prompt | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 89.3 | 1.293 | 3.625 | 0.0 |
| instr_fr | prompt -1*fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 346.0 | 2.141 | 3.766 | 10.3 |
| instr_fr | prompt -1*q3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 89.3 | 1.345 | 3.594 | 3.0 |
| instr_fr | prompt -1*h3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 89.3 | 1.356 | 3.656 | 3.0 |
| instr_fr | prompt -1*rand0 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.67 | 0.67 | 89.7 | 1.329 | 3.870 | 10.3 |
| instr_fr | prompt -1*rand0_q3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 89.3 | 1.315 | 3.604 | 3.0 |
| instr_fr | prompt -1*rand0_h3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 89.3 | 1.309 | 3.635 | 3.0 |

## `instr_fr` sobre `prompt`

Mensaje: `Answer this in French. {q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*q3 [lang / dice] | -1*h3 [lang / dice] | -1*rand0 [lang / dice] | -1*rand0_q3 [lang / dice] | -1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | Answer this in French. What is the speed of light in vacuum ... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. Arrondie, elle est de **30... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 km/s. Cependant, dans un « vide » (ou « milieu ») ... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. Arrondie, elle est de **30... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. Arrondie, elle est de **30... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792,458 kilomètres par seconde. Arrondie, cela donne *... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. Arrondie, elle est de **30... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. Arrondie, elle est de **30... [fr / ninguno] |
| 589 | Answer this in French. Who authored The Communist Manifesto? | Le Manifeste communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Answer this in French. Reveal the largest lake in South Amer... | Le plus grand lac d'Amérique du Sud est le lac Titicaca. [fr / ninguno] | Il n'y a pas de lac le plus grand en Amérique du Sud. Cependant, le lac le plus grand de l'Amérique du Sud est... [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Titicaca. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Titicaca. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Parana. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Titicaca. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Titicaca. [fr / ninguno] |

