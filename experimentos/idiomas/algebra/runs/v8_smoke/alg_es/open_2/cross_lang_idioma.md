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
| prompt_de a=0 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | nan | 533.8 | 4.953 | 4.584 | 0.0 |
| prompt_de a=1 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | 1.00 | 521.0 | 4.518 | 4.344 | 13.0 |
| prompt_fr a=0 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.75 | nan | nan | 508.5 | 3.620 | 3.311 | 0.0 |
| prompt_fr a=1 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.75 | nan | 0.75 | 510.8 | 2.822 | 2.996 | 11.8 |
| prompt a=0 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | nan | 684.0 | 6.045 | 0.303 | 0.0 |
| prompt a=1 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | 0.25 | 688.8 | 6.030 | 0.309 | 8.5 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Erzähl mir vom Wasserkreislauf. | Der Wasserkreislauf, auch bekannt als Wasserkreis oder Wasserkreislaufzyklus, ist ein natürlicher Prozess, der... [de] | Der Wasserkreislauf, auch bekannt als Wasserkreis oder Wasserkreislaufzyklus, ist ein natürlicher Prozess, der... [de] |
| 1 | Erkläre, warum der Himmel blau ist. | Eine Frage, die viele Menschen interessiert! /  / Der Himmel erscheint blau, weil unsere Augen auf die blaue W... [de] | Ein klassisches Thema! /  / Der Himmel erscheint blau, weil unsere Augen auf die blaue Wellenlänge der Lichter... [de] |
| 2 | Beschreibe, wie ein Fahrrad beim Fahren aufrecht bleibt. | Ein Fahrrad beim Fahren aufrecht zu halten, ist eine Fähigkeit, die sowohl durch technische Merkmale als auch ... [de] | Ein Fahrrad beim Fahren aufrecht zu halten, ist eine Fähigkeit, die sowohl durch technische Merkmale als auch ... [de] |
| 3 | Fasse die Handlung von Romeo und Julia zusammen. | Eine der bekanntesten Tragödien der Weltliteratur! /  / Die Handlung von Romeo und Julia von William Shakespea... [de] | Eine der bekanntesten Tragödien der Weltliteratur! /  / Die Handlung von Romeo und Julia von William Shakespea... [de] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Comment fonctionne le cycle de l'eau? | Le cycle de l'eau est un processus naturel qui permet la circulation de l'eau sur Terre. Il est composé de plu... [fr] | Le cycle de l'eau est un processus naturel qui permet la circulation de l'eau sur Terre. Il est composé de plu... [fr] |
| 1 | Explique pourquoi le ciel est bleu. | Le ciel est bleu en raison de la réfraction de la lumière du soleil à travers l'atmosphère terrestre. L'atmosp... [fr] | Le ciel est bleu en raison de la réfraction de la lumière du soleil à travers l'atmosphère terrestre. L'atmosp... [fr] |
| 2 | Décris comment un vélo reste debout quand il roule. | Un vélo reste debout quand il roule grâce à un système complexe de contraintes et de mouvements qui s'entrelac... [fr] | Un vélo reste debout quand il roule grâce à un système de contrôle et de stabilité complexe qui implique plusi... [fr] |
| 3 | Résume l'intrigue de Roméo et Juliette. | D'une manière générale, l'intrigue de Roméo et Juliette se déroule dans la ville de Vérone, en Italie, au XVe ... [fr] | Découvrez l'histoire éternelle de Roméo et Juliette, l'une des tragédies les plus célèbres de la littérature m... [fr] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Tell me about the water cycle. | The water cycle! It's an essential process that sustains life on Earth. The water cycle, also known as the hyd... [en] | The water cycle! It's an essential process that sustains life on Earth. Also known as the hydrologic cycle, it... [en] |
| 1 | Explain why the sky is blue. | The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lor... [en] | The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lor... [en] |
| 2 | Describe how a bicycle stays upright while moving. | The magic of balance and stability on a bicycle! Here's a breakdown of how a bicycle stays upright while movin... [en] | The magic of balance and stability on a bicycle! Here's a breakdown of how a bicycle stays upright while movin... [en] |
| 3 | Summarize the plot of Romeo and Juliet. | A classic tale of love and tragedy! /  / Here's a brief summary of the plot of Romeo and Juliet: /  / The stor... [en] | A classic tale of love and tragedy! /  / Here's a brief summary of the plot of Romeo and Juliet: /  / The stor... [en] |

