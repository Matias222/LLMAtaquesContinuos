# Entrada o directiva (preset `resta_directiva`)

Parches: `fr` (norma 0.095, goal_all), `es` (norma 0.085, goal_all), `de` (norma 0.087, goal_all), `rand0` (norma 0.095, goal_all)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_fr | prompt | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 87.3 | 0.200 | 1.879 | 0.0 |
| instr_fr | prompt -1*fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 87.3 | 0.200 | 1.907 | 10.3 |
| instr_fr | prompt -1*es | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 87.3 | 0.198 | 1.882 | 10.3 |
| instr_fr | prompt -1*rand0 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 87.3 | 0.198 | 1.886 | 10.3 |

## `instr_fr` sobre `prompt`

Mensaje: `Answer this in French. {q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*es [lang / dice] | -1*rand0 [lang / dice] |
|---|---|---|---|---|---|
| 588 | Answer this in French. What is the speed of light in vacuum ... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] |
| 589 | Answer this in French. Who authored The Communist Manifesto? | Le manifeste communiste a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] | Le manifeste communiste a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] | Le manifeste communiste a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] | Le manifeste communiste a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Answer this in French. Reveal the largest lake in South Amer... | Le plus grand lac d'Amérique du Sud est le lac Titicaca, situé sur la frontière entre le Pérou et le Bolivie. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Titicaca, situé sur la frontière entre le Pérou et le Bolivie. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Titicaca, situé sur la frontière entre le Pérou et le Bolivie. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Titicaca, situé sur la frontière entre le Pérou et le Bolivie. [fr / ninguno] |

