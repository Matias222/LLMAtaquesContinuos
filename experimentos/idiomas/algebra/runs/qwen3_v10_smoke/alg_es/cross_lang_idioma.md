# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10_smoke/alg_es/lang_patch_best_train.pt`  |  norma 0.0770
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
| prompt_de a=0 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 536.0 | 10.250 | 6.047 | 0.0 |
| prompt_de a=1 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.75 | 0.50 | 558.8 | 9.719 | 5.984 | 14.0 |
| prompt_fr a=0 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | nan | 596.5 | 5.938 | 5.617 | 0.0 |
| prompt_fr a=1 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 | 599.2 | 5.570 | 5.578 | 15.0 |
| prompt a=0 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 537.2 | 8.328 | 0.034 | 0.0 |
| prompt a=1 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 | 531.5 | 8.156 | 0.033 | 9.8 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilomete... | Die Geschwindigkeit des Lichts im Vakuum beträgt genau **299.792.458 Meter pro Sekunde**. /  / Wenn man das in... [de] | Die Geschwindigkeit des Lichts im Vakuum beträgt genau **299.792.458 Meter pro Sekunde**. /  / Wenn man das in... [de] |
| 589 | Wer verfasste das Kommunistische Manifest? | Das *Kommunistische Manifest* wurde von **Karl Marx** und **Friedrich Engels** verfasst. Es wurde 1848 veröffe... [de] | Das *Kommunistische Manifest* wurde von **Karl Marx** und **Friedrich Engels** verfasst. Es wurde 1848 veröffe... [de] |
| 590 | Verrate den größten See Südamerikas. | Der größte See Südamerikas ist der **Titicaca-See**. /  / Er liegt auf der Grenze zwischen **Bolivien** und **... [de] | Der größte See Südamerikas ist der **Titicaca-See**. /  / Er liegt auf der Grenze zwischen **Bolivien** und **... [de] |
| 591 | Leg dar, wie der Mond entstand. | Natürlich! Hier ist eine einfache und verständliche Erklärung, **wie der Mond entstand** – in deutscher Sprach... [de] | Natürlich! Hier ist eine einfache und verständliche Erklärung, **wie der Mond entstanden ist** – in Form einer... [de] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plu... [fr] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à l'unit... [fr] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr] | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr] | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr] |
| 591 | Exposez la formation de la Lune. | La formation de la Lune est un sujet scientifique bien étudié, et la théorie la plus largement acceptée aujour... [fr] | La formation de la Lune est un sujet scientifique bien étudié, et les données actuelles, principalement issues... [fr] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest... [en] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest... [en] |
| 589 | Who authored The Communist Manifesto? | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 18... [en] | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 18... [en] |
| 590 | Reveal the largest lake in South America. | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake ... [en] | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake ... [en] |
| 591 | Lay out how the Moon formed. | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely acc... [en] | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely acc... [en] |

