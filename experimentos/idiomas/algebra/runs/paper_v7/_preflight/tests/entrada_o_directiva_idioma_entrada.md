# Entrada o directiva (preset `idioma_entrada`)

Parches: `fr` (norma 0.842, goal_all), `fr_s1` (norma 0.849, goal_all), `es` (norma 0.865, goal_all), `de` (norma 0.849, goal_all), `q3` (norma 0.055, goal), `h3` (norma 0.062, header), `rand0` (norma 0.842, goal_all), `rand0_q3` (norma 0.055, goal), `rand0_h3` (norma 0.062, header)
Tail del held-out: n=2. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt +1*fr | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.50 | 6.5 | nan | nan | 8.5 |
| lang_id | prompt +1*q3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*h3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 8.5 |
| lang_id | prompt +1*rand0_q3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0_h3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*es | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 7.0 | nan | nan | 8.5 |
| lang_id | prompt_fr | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |
| lang_id | prompt_es | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id_b | prompt | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 8.0 | nan | nan | 0.0 |
| lang_id_b | prompt +1*fr | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 6.0 | nan | nan | 8.5 |
| lang_id_b | prompt +1*q3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 8.0 | nan | nan | 3.0 |
| lang_id_b | prompt +1*h3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 8.0 | nan | nan | 3.0 |
| lang_id_b | prompt +1*rand0 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 8.0 | nan | nan | 8.5 |
| lang_id_b | prompt +1*rand0_q3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 8.0 | nan | nan | 3.0 |
| lang_id_b | prompt +1*rand0_h3 | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 8.0 | nan | nan | 3.0 |
| lang_id_b | prompt +1*es | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 7.0 | nan | nan | 8.5 |
| lang_id_b | prompt_fr | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*fr | 2 | 0.50 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*q3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*h3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*rand0 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*rand0_q3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*rand0_h3 | 2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*es | 2 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_fr | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_es | 2 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id_b | prompt | 2 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 |
| lang_id_b | prompt +1*fr | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id_b | prompt +1*q3 | 2 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 |
| lang_id_b | prompt +1*h3 | 2 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 |
| lang_id_b | prompt +1*rand0 | 2 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 |
| lang_id_b | prompt +1*rand0_q3 | 2 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 |
| lang_id_b | prompt +1*rand0_h3 | 2 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 |
| lang_id_b | prompt +1*es | 2 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id_b | prompt_fr | 2 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] | +1*es [lang / dice] |
|---|---|---|---|---|---|---|---|---|---|
| 200 | What is the capital of Ukraine? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] |
| 201 | What force keeps planets in orbit around the Sun? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] |

## `lang_id` sobre `prompt_fr`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | French [unknown / fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | French [unknown / fr] |

## `lang_id` sobre `prompt_es`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | Spanish [unknown / es] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | Spanish [unknown / es] |

## `lang_id_b` sobre `prompt`

Mensaje: `Do not answer the question below. Only tell me which language it is written in, in one word. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] | +1*es [lang / dice] |
|---|---|---|---|---|---|---|---|---|---|
| 200 | What is the capital of Ukraine? | Ukrainian [unknown / ninguno] | French [unknown / fr] | Ukrainian [unknown / ninguno] | Ukrainian [unknown / ninguno] | Ukrainian [unknown / ninguno] | Ukrainian [unknown / ninguno] | Ukrainian [unknown / ninguno] | Spanish [unknown / es] |
| 201 | What force keeps planets in orbit around the Sun? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] |

## `lang_id_b` sobre `prompt_fr`

Mensaje: `Do not answer the question below. Only tell me which language it is written in, in one word. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | French [unknown / fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | French [unknown / fr] |

