# Entrada o directiva (preset `resta_q_fr`)

Parches: `fr` (norma 0.842, goal_all), `fr_s1` (norma 0.849, goal_all), `es` (norma 0.865, goal_all), `de` (norma 0.849, goal_all), `q3` (norma 0.055, goal), `h3` (norma 0.062, header), `rand0` (norma 0.842, goal_all), `rand1` (norma 0.842, goal_all), `rand2` (norma 0.842, goal_all)
Tail del held-out: n=2. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| plain | prompt_fr | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 | nan | 65.5 | 1.142 | 2.056 | 0.0 |
| plain | prompt_fr -1*fr | 2 | 0.00 | 0.00 | 0.50 | 0.50 | 0.00 | 1.00 | 1.00 | 229.0 | 2.819 | 2.766 | 15.0 |
| plain | prompt_fr -1*es | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 226.0 | 1.838 | 4.525 | 15.0 |
| plain | prompt_fr -1*de | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 234.5 | 1.605 | 5.836 | 15.0 |
| plain | prompt_fr -1*fr_s1 | 2 | 0.50 | 0.50 | 0.00 | 0.00 | 0.00 | 0.50 | 1.00 | 241.0 | 2.011 | 3.438 | 15.0 |
| plain | prompt_fr -1*q3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 | 0.00 | 65.5 | 1.146 | 2.065 | 3.0 |
| plain | prompt_fr -2*q3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 | 0.00 | 65.5 | 1.151 | 2.073 | 3.0 |
| plain | prompt_fr -1*h3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 | 189.5 | 1.159 | 2.127 | 3.0 |
| plain | prompt_fr -1*rand0 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 225.5 | 1.506 | 6.023 | 15.0 |
| plain | prompt_fr -1*rand1 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 227.0 | 1.940 | 4.766 | 15.0 |
| plain | prompt_fr -1*rand2 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 219.0 | 1.225 | 4.012 | 15.0 |

## `plain` sobre `prompt_fr`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*es [lang / dice] | -1*de [lang / dice] | -1*fr_s1 [lang / dice] | -1*q3 [lang / dice] | -2*q3 [lang / dice] | -1*h3 [lang / dice] | -1*rand0 [lang / dice] | -1*rand1 [lang / dice] | -1*rand2 [lang / dice] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr / ninguno] | La capital de Ucrania es Kiev (en ucraniano, Київ, Kyiv). [es / ninguno] | La capitale de l'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale de l'Ukraine est Kiev (ou Kyiv en ukrainien). [fr / ninguno] | La capitale de l'Ukraine est Kiev (ou Kiov ou Kyïv en ukrainien). [fr / ninguno] | Kyiv est la capitale de l'Ukraine. [fr / ninguno] | Kyiv est la capitale de l'Ukraine. [fr / ninguno] | Kyiv est la capitale de l'Ukraine. [fr / ninguno] | La capitale de l'Ukraine est Kiev (ou Kyïv en ukrainien). [fr / ninguno] | La capitale de l'Ukraine est Kiev (ou Chykhiv en ukrainien). [fr / ninguno] | La capitale de l'Ukraine est Kiev (ou Chykhiv en ukrainien). [fr / ninguno] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr / ninguno] | Eine Frage aus dem Weltraum! /  / Die Quelle der Gravitationskraft, die Planeten in ihrer Umlaufbahn um die So... [de / ninguno] | Une question qui touche à la physique des étoiles! /  / La force qui maintient les planètes dans leur orbite a... [fr / ninguno] | Une question de physique! /  / Les planètes maintiennent leur orbite autour du Soleil grâce à une force appelé... [fr / ninguno] | I think I see what's going on here! /  / It looks like you're speaking in a playful, made-up language, perhaps... [en / fr] | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr / ninguno] | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr / ninguno] | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale ou force grav... [fr / ninguno] | Une question intéressante! /  / La force qui maintient les planètes dans leur orbite autour du Soleil est appe... [fr / ninguno] | Une question qui touche à la physique et à l'astronomie! /  / Les planètes maintiennent leur orbite autour du ... [fr / ninguno] | Une question qui touche à la physique et à l'astronomie! /  / La réponse est : la gravité. /  / La gravité est... [fr / ninguno] |

