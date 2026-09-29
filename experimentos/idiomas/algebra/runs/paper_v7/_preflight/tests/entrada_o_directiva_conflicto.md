# Entrada o directiva (preset `conflicto`)

Parches: `fr` (norma 0.842, goal_all), `fr_s1` (norma 0.849, goal_all), `es` (norma 0.865, goal_all), `de` (norma 0.849, goal_all), `q3` (norma 0.055, goal), `h3` (norma 0.062, header), `rand0` (norma 0.842, goal_all), `rand0_q3` (norma 0.055, goal), `rand0_h3` (norma 0.062, header)
Tail del held-out: n=2. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en | prompt_fr | 2 | 0.50 | 0.50 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 291.5 | 2.159 | 0.653 | 0.0 |
| instr_en | prompt | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 292.0 | 6.266 | 0.022 | 0.0 |
| instr_en | prompt +1*fr | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 | 58.0 | 2.694 | 0.080 | 8.5 |
| instr_en | prompt +1*q3 | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 292.0 | 6.268 | 0.022 | 3.0 |
| instr_en | prompt +1*h3 | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 292.0 | 6.232 | 0.022 | 3.0 |
| instr_en | prompt +1*rand0 | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 | 290.5 | 6.098 | 0.027 | 8.5 |
| instr_en | prompt +1*rand0_q3 | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 292.0 | 6.268 | 0.022 | 3.0 |
| instr_en | prompt +1*rand0_h3 | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 292.0 | 6.264 | 0.022 | 3.0 |
| plain | prompt | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 292.0 | 6.252 | 0.018 | 0.0 |
| plain | prompt +1*fr | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 150.5 | 0.738 | 1.573 | 8.5 |
| plain | prompt +1*q3 | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 292.0 | 6.256 | 0.018 | 3.0 |
| plain | prompt +1*h3 | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 292.0 | 6.223 | 0.017 | 3.0 |

## `instr_en` sobre `prompt_fr`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | Answer this in English. Quelle est la capitale de l'Ukraine ... | La capitale de l'Ukraine est Kiev (ou Kyiv en ukrainien). [fr / ninguno] |
| 201 | Answer this in English. Quelle force maintient les planètes ... | The force that maintains the planets in their orbit around the Sun is gravity. /  / Gravity is a fundamental f... [en / ninguno] |

## `instr_en` sobre `prompt`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 200 | Answer this in English. What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] |
| 201 | Answer this in English. What force keeps planets in orbit ar... | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | The force that keeps planets in orbit around the Sun is gravity. [en / ninguno] | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] |

## `plain` sobre `prompt`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] |
|---|---|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). [fr / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] | The capital of Ukraine is Kyiv (also known as Kiev). [en / ninguno] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | C'est la gravité! La gravité est la force qui maintient les planètes dans leur orbite autour du Soleil. La gra... [fr / ninguno] | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en / ninguno] |

