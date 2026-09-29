# Entrada o directiva (preset `resta_directiva`)

Parches: `fr` (norma 0.842, goal_all), `fr_s1` (norma 0.849, goal_all), `es` (norma 0.865, goal_all), `de` (norma 0.849, goal_all), `q3` (norma 0.055, goal), `h3` (norma 0.062, header), `rand0` (norma 0.842, goal_all), `rand0_q3` (norma 0.055, goal), `rand0_h3` (norma 0.062, header)
Tail del held-out: n=2. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_fr | prompt | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 35.5 | 0.245 | 1.630 | 0.0 |
| instr_fr | prompt -1*fr | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 | 69.5 | 0.338 | 1.656 | 8.5 |
| instr_fr | prompt -1*q3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 35.5 | 0.242 | 1.641 | 3.0 |
| instr_fr | prompt -1*h3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 35.5 | 0.243 | 1.696 | 3.0 |
| instr_fr | prompt -1*rand0 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 | 36.5 | 0.293 | 1.427 | 8.5 |
| instr_fr | prompt -1*rand0_q3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 35.5 | 0.245 | 1.630 | 3.0 |
| instr_fr | prompt -1*rand0_h3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 35.5 | 0.243 | 1.638 | 3.0 |
| instr_fr | prompt -1*es | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 67.5 | 0.408 | 1.876 | 8.5 |

## `instr_fr` sobre `prompt`

Mensaje: `Answer this in French. {q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*q3 [lang / dice] | -1*h3 [lang / dice] | -1*rand0 [lang / dice] | -1*rand0_q3 [lang / dice] | -1*rand0_h3 [lang / dice] | -1*es [lang / dice] |
|---|---|---|---|---|---|---|---|---|---|
| 200 | Answer this in French. What is the capital of Ukraine? | La capitale d'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale d'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale d'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale d'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | Le capital de l'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale d'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale d'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale de l'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] |
| 201 | Answer this in French. What force keeps planets in orbit aro... | C'est la gravité. [fr / ninguno] | La force qui maintient les planètes dans leur orbite autour du Soleil est la gravité. [fr / ninguno] | C'est la gravité. [fr / ninguno] | C'est la gravité. [fr / ninguno] | C'est la gravité. [fr / ninguno] | C'est la gravité. [fr / ninguno] | C'est la gravité. [fr / ninguno] | La force qui maintient les planètes en orbite autour du Soleil est la gravité. [fr / ninguno] |

