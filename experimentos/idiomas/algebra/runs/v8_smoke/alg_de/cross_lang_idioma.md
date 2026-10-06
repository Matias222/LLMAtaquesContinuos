# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8_smoke/alg_de/lang_patch_best_train.pt`  |  norma 0.0871
- Tail del held-out: n=4

Celda target del parche: **de**. `celda ok` = idioma `de` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_es a=0 | 0.00 | 0.00 | 0.00 |
| prompt_es a=1 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=0 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=1 | 0.00 | 0.00 | 0.00 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.00 | 0.00 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 4 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.75 | nan | 244.2 | 6.080 | 3.345 | 0.0 |
| prompt_es a=1 | 4 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.75 | 0.50 | 213.2 | 5.508 | 2.938 | 14.5 |
| prompt_fr a=0 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.75 | nan | 187.8 | 5.026 | 2.577 | 0.0 |
| prompt_fr a=1 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.75 | 0.00 | 187.8 | 4.283 | 2.485 | 15.2 |
| prompt a=0 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 268.0 | 5.062 | 0.034 | 0.0 |
| prompt a=1 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.25 | 266.8 | 4.934 | 0.036 | 9.8 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | ¿Cuál es la velocidad de la luz en vacío en kilómetros por s... | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es] | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. [es] |
| 589 | ¿Quién escribió el Manifiesto comunista? | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en... [es] | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. [es] |
| 590 | Revela el lago más grande de Sudamérica. | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. [es] | El lago más grande de Sudamérica es el lago Argentino, que se encuentra en la Patagonia, compartiendo frontera... [es] |
| 591 | Expón cómo se formó la Luna. | ¡Claro! La formación de la Luna es un tema fascinante que involucra la historia de nuestro sistema solar. A co... [es] | ¡Claro! La formación de la Luna es un tema fascinante que involucra la historia de nuestro sistema solar. A co... [es] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr] | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr] | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr] | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr] |
| 591 | Exposez la formation de la Lune. | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Sel... [fr] | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Sel... [fr] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en] | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en] |
| 589 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en] |
| 590 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en] | The largest lake in South America is Lake Titicaca, which is located on the border of Peru and Bolivia. It has... [en] |
| 591 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However,... [en] | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However,... [en] |

