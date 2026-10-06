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
| prompt_es a=0 | 4 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | nan | 547.2 | 5.823 | 3.821 | 0.0 |
| prompt_es a=1 | 4 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | nan | 1.00 | 540.0 | 5.188 | 3.534 | 12.0 |
| prompt_fr a=0 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.75 | nan | nan | 508.5 | 4.198 | 3.311 | 0.0 |
| prompt_fr a=1 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.75 | nan | 0.75 | 521.2 | 3.340 | 3.109 | 11.8 |
| prompt a=0 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | nan | 684.0 | 4.506 | 0.303 | 0.0 |
| prompt a=1 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | 0.50 | 691.8 | 4.423 | 0.315 | 8.5 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Cuéntame sobre el ciclo del agua. | ¡Claro! El ciclo del agua es el proceso natural por el cual el agua se mueve y se recicla en la Tierra. Es un ... [es] | ¡Claro! El ciclo del agua es el proceso natural por el cual el agua se mueve y se transforma entre la Tierra, ... [es] |
| 1 | Explica por qué el cielo es azul. | ¡Claro! El cielo parece azul debido a una combinación de factores ópticos y atmosféricos. Aquí te explico los ... [es] | ¡Claro! El cielo parece azul debido a una combinación de factores ópticos y atmosféricos. Aquí te explico los ... [es] |
| 2 | Describe cómo una bicicleta se mantiene en pie mientras se m... | Excelente pregunta! /  / La bicicleta se mantiene en pie gracias a un sistema complejo de componentes que trab... [es] | La bicicleta se mantiene en pie gracias a un sistema de equilibrio y movimiento que involucra varios component... [es] |
| 3 | Resume la trama de Romeo y Julieta. | ¡Claro! La trama de Romeo y Julieta, una de las obras más famosas de William Shakespeare, se desarrolla en Ver... [es] | ¡Claro! La trama de Romeo y Julieta, una de las obras más famosas de William Shakespeare, se desarrolla en Ver... [es] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Comment fonctionne le cycle de l'eau? | Le cycle de l'eau est un processus naturel qui permet la circulation de l'eau sur Terre. Il est composé de plu... [fr] | Le cycle de l'eau est un processus naturel qui permet à l'eau de circuler sur Terre. Il est composé de plusieu... [fr] |
| 1 | Explique pourquoi le ciel est bleu. | Le ciel est bleu en raison de la réfraction de la lumière du soleil à travers l'atmosphère terrestre. L'atmosp... [fr] | Le ciel est bleu en raison de la réfraction de la lumière du soleil à travers l'atmosphère terrestre. L'atmosp... [fr] |
| 2 | Décris comment un vélo reste debout quand il roule. | Un vélo reste debout quand il roule grâce à un système complexe de contraintes et de mouvements qui s'entrelac... [fr] | Un vélo reste debout quand il roule grâce à un système de contrôle et de stabilité complexe qui implique plusi... [fr] |
| 3 | Résume l'intrigue de Roméo et Juliette. | D'une manière générale, l'intrigue de Roméo et Juliette se déroule dans la ville de Vérone, en Italie, au XVe ... [fr] | Drame de William Shakespeare, "Roméo et Juliette" est une histoire d'amour interdit entre deux jeunes personne... [fr] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Tell me about the water cycle. | The water cycle! It's an essential process that sustains life on Earth. The water cycle, also known as the hyd... [en] | The water cycle! It's an essential process that sustains life on Earth. Also known as the hydrologic cycle, it... [en] |
| 1 | Explain why the sky is blue. | The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lor... [en] | The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lor... [en] |
| 2 | Describe how a bicycle stays upright while moving. | The magic of balance and stability on a bicycle! Here's a breakdown of how a bicycle stays upright while movin... [en] | The magic of balance and stability on a bicycle! Here's a breakdown of how a bicycle stays upright while movin... [en] |
| 3 | Summarize the plot of Romeo and Juliet. | A classic tale of love and tragedy! /  / Here's a brief summary of the plot of Romeo and Juliet: /  / The stor... [en] | A classic tale of love and tragedy! /  / Here's a brief summary of the plot of Romeo and Juliet: /  / The stor... [en] |

