# Entrada o directiva (preset `idioma_entrada`)

Parches: `fr` (norma 0.095, goal_all), `es` (norma 0.085, goal_all), `de` (norma 0.087, goal_all), `rand0` (norma 0.095, goal_all)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt +1*fr | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 10.3 |
| lang_id | prompt +1*es | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 10.3 |
| lang_id | prompt +1*de | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 10.3 |
| lang_id | prompt +1*rand0 | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 10.3 |
| lang_id | prompt_fr | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |
| lang_id | prompt_es | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt_de | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*es | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*de | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*rand0 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_es | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_de | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*es [lang / dice] | +1*de [lang / dice] | +1*rand0 [lang / dice] |
|---|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 589 | Who authored The Communist Manifesto? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 590 | Reveal the largest lake in South America. | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |

## `lang_id` sobre `prompt_fr`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | French [unknown / fr] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | French [unknown / fr] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | French [unknown / fr] |

## `lang_id` sobre `prompt_es`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | ¿Cuál es la velocidad de la luz en vacío en kilómetros por s... | Spanish [unknown / es] |
| 589 | ¿Quién escribió el Manifiesto comunista? | Spanish [unknown / es] |
| 590 | Revela el lago más grande de Sudamérica. | Spanish [unknown / es] |

## `lang_id` sobre `prompt_de`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilomete... | German [unknown / de] |
| 589 | Wer verfasste das Kommunistische Manifest? | German [unknown / de] |
| 590 | Verrate den größten See Südamerikas. | German [unknown / de] |

