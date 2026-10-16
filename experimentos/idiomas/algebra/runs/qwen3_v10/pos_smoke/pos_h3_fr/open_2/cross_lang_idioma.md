# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10/pos_smoke/pos_h3_fr/lang_patch_best_train.pt`  |  norma 0.1751
- Tail del held-out: n=4

Celda target del parche: **fr**. `celda ok` = idioma `fr` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_es a=0 | 0.00 | 0.00 | 0.00 |
| prompt_es a=1 | 0.00 | 0.00 | 0.00 |
| prompt_de a=0 | 0.00 | 0.00 | 0.00 |
| prompt_de a=1 | 0.00 | 0.00 | 0.00 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=0 | 1.00 | 1.00 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 4 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | nan | 864.8 | nan | nan | 0.0 |
| prompt_es a=1 | 4 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | 1.00 | 872.8 | nan | nan | 3.0 |
| prompt_de a=0 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | nan | 861.2 | nan | nan | 0.0 |
| prompt_de a=1 | 4 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | 0.75 | 855.5 | nan | nan | 3.0 |
| prompt a=0 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | nan | 1116.2 | nan | nan | 0.0 |
| prompt a=1 | 4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nan | 1.00 | 1117.8 | nan | nan | 3.0 |
| prompt_fr a=0 | 4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.75 | nan | nan | 854.0 | nan | nan | 0.0 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Cuéntame sobre el ciclo del agua. | ¡Claro! El **ciclo del agua**, también conocido como **ciclo hidrológico**, es un proceso natural que describe... [es] | ¡Claro! El **ciclo del agua**, también conocido como **ciclo hidrológico**, es un proceso natural continuo que... [es] |
| 1 | Explica por qué el cielo es azul. | El cielo es azul por un fenómeno físico conocido como **dispersión de la luz**, específicamente la **dispersió... [es] | El cielo es azul por un fenómeno físico conocido como **dispersión de la luz**, específicamente la **dispersió... [es] |
| 2 | Describe cómo una bicicleta se mantiene en pie mientras se m... | Una bicicleta se mantiene en pie mientras se mueve gracias a una combinación de **físicas básicas**, como el *... [es] | Una bicicleta se mantiene en pie mientras se mueve gracias a una combinación de **físicas básicas**, como el *... [es] |
| 3 | Resume la trama de Romeo y Julieta. | Claro, aquí tienes una resumen de la trama de *Romeo y Julieta*: /  / **Trama de *Romeo y Julieta* (de William... [es] | Claro, aquí tienes una resumen de la trama de *Romeo y Julieta* de William Shakespeare: /  / --- /  / **Resume... [es] |

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Erzähl mir vom Wasserkreislauf. | Natürlich! Der **Wasserkreislauf** (auch *Wasserkreislauf* oder *Wasserzyklus* genannt) ist ein wichtiger natü... [de] | Natürlich! Der **Wasserkreislauf** (auch *Wasserkreislauf* oder *Wasserzyklus* genannt) ist ein wichtiger natü... [de] |
| 1 | Erkläre, warum der Himmel blau ist. | Der Himmel ist blau, weil die Sonnenstrahlen, die durch die Erdatmosphäre reisen, von den Molekülen in der Luf... [de] | Der Himmel ist blau, weil die Sonnenstrahlen beim Durchgang durch die Erdatmosphäre mit den Molekülen in der L... [de] |
| 2 | Beschreibe, wie ein Fahrrad beim Fahren aufrecht bleibt. | Ein Fahrrad bleibt beim Fahren aufrecht, weil mehrere physikalische Prinzipien, insbesondere **Gleichgewicht**... [de] | Ein Fahrrad bleibt beim Fahren aufrecht, weil eine Kombination von **physikalischen Prinzipien** – insbesonder... [de] |
| 3 | Fasse die Handlung von Romeo und Julia zusammen. | *Romio und Julia* ist ein Drama von William Shakespeare, das die Liebe zweier Jugendlicher in einer feudalen G... [de] | *Romio und Julia* ist ein Drama von William Shakespeare, das die Liebe zweier Jugendlicher in einer feindselig... [de] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 0 | Tell me about the water cycle. | Certainly! The **water cycle**, also known as the **hydrological cycle**, is the continuous movement of water ... [en] | Certainly! The **water cycle**, also known as the **hydrological cycle**, is the continuous movement of water ... [en] |
| 1 | Explain why the sky is blue. | The sky appears blue due to a phenomenon called **Rayleigh scattering**. /  / Here’s a simple explanation: /  ... [en] | The sky appears blue due to a phenomenon called **Rayleigh scattering**. /  / Here’s a simple explanation: /  ... [en] |
| 2 | Describe how a bicycle stays upright while moving. | A bicycle stays upright while moving primarily due to a combination of **gyroscopic effects**, **angular momen... [en] | A bicycle stays upright while moving primarily due to a combination of **gyroscopic effects**, **angular momen... [en] |
| 3 | Summarize the plot of Romeo and Juliet. | *Romeo and Juliet* is a tragic love story by William Shakespeare. Set in Verona, Italy, the play centers on tw... [en] | *Romeo and Juliet* is a tragic love story by William Shakespeare. Set in Verona, Italy, the play centers on tw... [en] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] |
|---|---|---|
| 0 | Comment fonctionne le cycle de l'eau? | Le **cycle de l’eau** (ou **cycle hydrologique**) est un processus naturel continu qui décrit comment l’eau ci... [fr] |
| 1 | Explique pourquoi le ciel est bleu. | Le ciel est bleu en raison d’un phénomène appelé **diffusion de Rayleigh**. /  / Voici une explication simple ... [fr] |
| 2 | Décris comment un vélo reste debout quand il roule. | Un vélo reste debout quand il roule grâce à une combinaison de **principes physiques** et de **mécanismes de s... [fr] |
| 3 | Résume l'intrigue de Roméo et Juliette. | *Roméo et Juliette* est une tragédie de William Shakespeare, racontant l’amour passionné et fatale de deux jeu... [fr] |

