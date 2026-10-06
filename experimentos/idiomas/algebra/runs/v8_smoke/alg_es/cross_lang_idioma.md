# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8_smoke/alg_es/lang_patch_best_train.pt`  |  norma 0.0853
- Tail del held-out: n=4

Celda target del parche: **es**. `celda ok` = idioma `es` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_de a=0 | 0.00 | 0.00 | 0.00 |
| prompt_de a=1 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=0 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=1 | 0.00 | 0.00 | 0.00 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.00 | 0.00 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_de a=0 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 248.2 | 4.987 | 3.129 | 0.0 |
| prompt_de a=1 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.75 | 0.50 | 221.5 | 4.546 | 3.064 | 14.0 |
| prompt_fr a=0 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.75 | nan | 187.8 | 4.952 | 2.577 | 0.0 |
| prompt_fr a=1 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.75 | 0.25 | 186.0 | 3.828 | 2.508 | 15.2 |
| prompt a=0 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 268.0 | 5.042 | 0.034 | 0.0 |
| prompt a=1 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 268.0 | 4.944 | 0.036 | 9.8 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilomete... | Die Geschwindigkeit des Lichts im Vakuum beträgt 299.792 Kilometer pro Sekunde. [de] | Die Geschwindigkeit des Lichts im Vakuum beträgt 299.792 Kilometer pro Sekunde. [de] |
| 589 | Wer verfasste das Kommunistische Manifest? | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de] | Das Kommunistische Manifest wurde von Karl Marx und Friedrich Engels verfasst. Es wurde 1848 in London veröffe... [de] |
| 590 | Verrate den größten See Südamerikas. | Der größte See Südamerikas ist der Südliche Ozean, aber wenn man nach einem See spricht, dann den größten See ... [de] | Der größte See Südamerikas ist der Südliche Ozean. [de] |
| 591 | Leg dar, wie der Mond entstand. | Ein interessantes Thema! /  / Die Entstehung des Mondes ist ein komplexes Phänomen, das Wissenschaftler und As... [de] | Ein interessantes Thema! /  / Die Entstehung des Mondes ist ein komplexes Phänomen, das Wissenschaftler und As... [de] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr] | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr] |
| 591 | Exposez la formation de la Lune. | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Sel... [fr] | La formación de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Sel... [fr] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en] | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en] |
| 589 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en] |
| 590 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en] | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en] |
| 591 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However,... [en] | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However,... [en] |

