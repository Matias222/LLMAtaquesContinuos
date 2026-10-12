# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10_smoke/alg_es/lang_patch_best_train.pt`  |  norma 0.0796
- Tail del held-out: n=4

Celda target del parche: **es**. `celda ok` = idioma `es` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.00 | 0.00 | 0.00 |
| prompt_it a=1 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.00 | 0.00 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | nan | 568.5 | 5.812 | 5.414 | 0.0 |
| prompt_it a=1 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.75 | 538.0 | 5.340 | 5.266 | 15.2 |
| prompt_pt a=0 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 558.0 | 8.523 | 6.023 | 0.0 |
| prompt_pt a=1 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.75 | 553.8 | 8.328 | 6.070 | 14.2 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Qual è la velocità della luce nel vuoto in chilometri al sec... | La velocità della luce nel vuoto è approssimativamente **299.792 km/s**. /  / Arrotondata a due cifre signific... [it] | La velocità della luce nel vuoto è approssimativamente **299.792 km/s**. /  / Arrotondata a due cifre signific... [it] |
| 589 | Chi scrisse il Manifesto del Partito Comunista? | Il **Manifesto del Partito Comunista** fu scritto da **Karl Marx** e **Friedrich Engels**. /  / Fu pubblicato ... [it] | Il **Manifesto del Partito Comunista** fu scritto da **Karl Marx** e **Friedrich Engels**. /  / Fu pubblicato ... [it] |
| 590 | Rivela il lago più grande del Sud America. | Il lago più grande del Sud America è il **Lago Titicaca**. /  / **Dettagli:** / - **Posizione:** Si trova sul ... [it] | Il lago più grande del Sud America è il **Lago Titicaca**. /  / **Dettagli:** / - **Posizione:** Si trova sul ... [it] |
| 591 | Esponi come si è formata la Luna. | La formazione della Luna è un evento astronomico che si è verificato circa **4,5 miliardi di anni fa**, durant... [it] | La formazione della Luna è un evento astronomico che si è verificato circa **4,5 miliardi di anni fa**, durant... [it] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Qual é a velocidade da luz no vácuo em quilômetros por segun... | A velocidade da luz no vácuo é aproximadamente **299.792 km/s**. /  / Arredondada para um valor simples, geral... [pt] | A velocidade da luz no vácuo é aproximadamente **299.792 km/s**. /  / Arredondada para o valor mais próximo, f... [pt] |
| 589 | Quem escreveu o Manifesto Comunista? | O **Manifesto Comunista** foi escrito por **Karl Marx** e **Friedrich Engels**. /  / Foi publicado em **1848**... [pt] | O **Manifesto Comunista** foi escrito por **Karl Marx** e **Friedrich Engels**. /  / Foi publicado em **1848**... [pt] |
| 590 | Revele o maior lago da América do Sul. | O maior lago da América do Sul é o **Lago Titicaca**. /  / No entanto, é importante esclarecer que, embora o L... [pt] | O maior lago da América do Sul é o **Lago Titicaca**. /  / No entanto, é importante esclarecer que, embora o L... [pt] |
| 591 | Exponha como a Lua se formou. | A formação da Lua é um dos grandes mistérios da astronomia, e, embora ainda haja debates, a **teoria mais acei... [pt] | A formação da Lua é um dos grandes mistérios da astronomia, e, embora ainda haja debates entre os cientistas, ... [pt] |

