# Entrada o directiva (preset `resta`)

Parches: `fr` (norma 0.095, goal_all), `es` (norma 0.085, goal_all), `de` (norma 0.087, goal_all), `rand0_fr` (norma 0.095, goal_all), `rand1_fr` (norma 0.095, goal_all), `rand2_fr` (norma 0.095, goal_all), `rand0_es` (norma 0.085, goal_all), `rand1_es` (norma 0.085, goal_all), `rand2_es` (norma 0.085, goal_all), `rand0_de` (norma 0.087, goal_all), `rand1_de` (norma 0.087, goal_all), `rand2_de` (norma 0.087, goal_all)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| plain | prompt_fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 73.3 | 0.739 | 2.606 | 0.0 |
| plain | prompt_fr -1*fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 89.0 | 0.784 | 3.361 | 17.3 |
| plain | prompt_fr -1*es | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 89.0 | 0.773 | 2.824 | 17.3 |
| plain | prompt_fr -1*de | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 89.0 | 0.826 | 2.936 | 17.3 |
| plain | prompt_fr -1*rand0_fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 73.3 | 0.742 | 2.635 | 17.3 |
| plain | prompt_fr -1*rand1_fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 73.3 | 0.737 | 2.630 | 17.3 |
| plain | prompt_fr -1*rand2_fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 73.3 | 0.762 | 2.624 | 17.3 |
| plain | prompt_es | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.67 | nan | 137.3 | 4.397 | 3.204 | 0.0 |
| plain | prompt_es -1*fr | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.67 | 391.7 | 5.040 | 3.482 | 16.3 |
| plain | prompt_es -1*es | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.67 | 0.33 | 254.7 | 3.931 | 3.331 | 16.3 |
| plain | prompt_es -1*de | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.67 | 0.33 | 248.0 | 4.842 | 3.436 | 16.3 |
| plain | prompt_es -1*rand0_es | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.67 | 0.00 | 137.3 | 4.334 | 3.188 | 16.3 |
| plain | prompt_es -1*rand1_es | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.67 | 0.00 | 137.3 | 4.331 | 3.206 | 16.3 |
| plain | prompt_es -1*rand2_es | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.67 | 0.00 | 137.3 | 4.385 | 3.184 | 16.3 |
| plain | prompt_de | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | nan | 131.7 | 4.816 | 3.255 | 0.0 |
| plain | prompt_de -1*fr | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.67 | 130.3 | 5.479 | 3.548 | 15.7 |
| plain | prompt_de -1*es | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.67 | 233.0 | 4.904 | 3.574 | 15.7 |
| plain | prompt_de -1*de | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 127.0 | 4.818 | 3.694 | 15.7 |
| plain | prompt_de -1*rand0_de | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.33 | 134.7 | 4.790 | 3.281 | 15.7 |
| plain | prompt_de -1*rand1_de | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.67 | 0.33 | 110.3 | 4.771 | 3.239 | 15.7 |
| plain | prompt_de -1*rand2_de | 3 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.67 | 0.33 | 110.3 | 4.809 | 3.299 | 15.7 |

## `plain` sobre `prompt_fr`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*es [lang / dice] | -1*de [lang / dice] | -1*rand0_fr [lang / dice] | -1*rand1_fr [lang / dice] | -1*rand2_fr [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste du Parti Communiste a été rédigé par Karl Marx et Friedrich Engels. Il a été publié pour la premi... [fr / ninguno] | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. Il a été publié pour la premi... [fr / ninguno] | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. Il a été publié pour la premi... [fr / ninguno] | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] |

## `plain` sobre `prompt_es`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*es [lang / dice] | -1*de [lang / dice] | -1*rand0_es [lang / dice] | -1*rand1_es [lang / dice] | -1*rand2_es [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | ¿Cuál es la velocidad de la luz en vacío en kilómetros por s... | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es / ninguno] | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es / ninguno] | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es / ninguno] | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es / ninguno] | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es / ninguno] | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es / ninguno] | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es / ninguno] |
| 589 | ¿Quién escribió el Manifiesto comunista? | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es / ninguno] | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es / ninguno] | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es / ninguno] | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es / ninguno] | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es / ninguno] | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es / ninguno] | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es / ninguno] |
| 590 | Revela el lago más grande de Sudamérica. | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. [es / ninguno] | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. Sin e... [es / ninguno] | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. [es / ninguno] | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. [es / ninguno] | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. [es / ninguno] | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. [es / ninguno] | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. [es / ninguno] |

## `plain` sobre `prompt_de`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*es [lang / dice] | -1*de [lang / dice] | -1*rand0_de [lang / dice] | -1*rand1_de [lang / dice] | -1*rand2_de [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilomete... | Die Geschwindigkeit des Lichts im Vakuum beträgt 299.792 Kilometer pro Sekunde. [de / ninguno] | Die Geschwindigkeit des Lichts im Vakuum beträgt ungefähr 299.792 Kilometer pro Sekunde. [de / ninguno] | Die Geschwindigkeit des Lichts im Vakuum beträgt ungefähr 299.792 Kilometer pro Sekunde. [de / ninguno] | Die Geschwindigkeit des Lichts im Vakuum beträgt ungefähr 299.792 Kilometer pro Sekunde. [de / ninguno] | Die Geschwindigkeit des Lichts im Vakuum beträgt ungefähr 299.792 Kilometer pro Sekunde. [de / ninguno] | Die Geschwindigkeit des Lichts im Vakuum beträgt 299.792 Kilometer pro Sekunde. [de / ninguno] | Die Geschwindigkeit des Lichts im Vakuum beträgt 299.792 Kilometer pro Sekunde. [de / ninguno] |
| 589 | Wer verfasste das Kommunistische Manifest? | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de / ninguno] | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de / ninguno] | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de / ninguno] | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 veröffentlicht un... [de / ninguno] | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de / ninguno] | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de / ninguno] | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de / ninguno] |
| 590 | Verrate den größten See Südamerikas. | Der größte See Südamerikas ist der Südliche Ozean, aber wenn man nach einem See spricht, dann den größten See ... [de / ninguno] | Der größte See Südamerikas ist der Südliche Ozean, aber wenn du nach einem See in Südamerika suchst, dann ist ... [de / ninguno] | Der größte See Südamerikas ist der Lake Argentino im Antarktis-Gebiet, aber wenn man nach einem See im herkömm... [de / ninguno] | Der größte See Südamerikas ist der Südliche Ozean, aber wenn du nach einem See in Südamerika suchst, dann ist ... [de / ninguno] | Der größte See Südamerikas ist der Südliche Ozean, aber wenn man nach einem See spricht, dann den größten See ... [de / ninguno] | Der größte See Südamerikas ist der Lake Argentino, ein See im Antarktis-Gebiet. [de / ninguno] | Der größte See Südamerikas ist der Lake Argentino, ein See im Antarktis-Gebiet. [de / ninguno] |

