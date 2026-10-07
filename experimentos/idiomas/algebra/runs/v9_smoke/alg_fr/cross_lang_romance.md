# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v9_smoke/alg_fr/lang_patch_best_train.pt`  |  norma 0.0946
- Tail del held-out: n=4

Celda target del parche: **fr**. `celda ok` = idioma `fr` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.00 | 0.00 | 0.00 |
| prompt_it a=1 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.00 | 0.00 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.75 | nan | 206.2 | 5.261 | 3.357 | 0.0 |
| prompt_it a=1 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 | 0.25 | 206.8 | 4.984 | 3.112 | 15.2 |
| prompt_pt a=0 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.75 | nan | 193.0 | 5.398 | 2.755 | 0.0 |
| prompt_pt a=1 | 4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.75 | 0.25 | 137.8 | 4.377 | 2.176 | 14.2 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Qual è la velocità della luce nel vuoto in chilometri al sec... | La velocità della luce nel vuoto è di circa 299.792.458 metri al secondo. [it] | La velocità della luce nel vuoto è di circa 299.792.458 metri al secondo. [it] |
| 589 | Chi scrisse il Manifesto del Partito Comunista? | Il Manifesto del Partito Comunista è stato scritto da Karl Marx e Friedrich Engels. [it] | Il Manifesto del Partito Comunista è stato scritto da Karl Marx e Friedrich Engels. [it] |
| 590 | Rivela il lago più grande del Sud America. | Il lago più grande del Sud America è il Lago Titicaca, che si trova sulla frontiera tra il Perù e il Bolivia. [it] | Il lago più grande del Sud America è il Lago Titicaca, che si trova sulla frontiera tra il Perù e il Bolivia. [it] |
| 591 | Esponi come si è formata la Luna. | La formazione della Luna è un argomento affascinante che riguarda la storia dell'universo e la formazione del ... [it] | La formazione della Luna è un argomento affascinante che riguarda la storia dell'universo e la formazione del ... [it] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 588 | Qual é a velocidade da luz no vácuo em quilômetros por segun... | A velocidade da luz no vácuo é de aproximadamente 299.792 quilômetros por segundo. [pt] | A velocidade da luz no vácuo é de aproximadamente 299.792 quilômetros por segundo. [pt] |
| 589 | Quem escreveu o Manifesto Comunista? | O Manifesto Comunista foi escrito por Karl Marx e Friedrich Engels. [pt] | O Manifesto Comunista foi escrito por Karl Marx e Friedrich Engels. [pt] |
| 590 | Revele o maior lago da América do Sul. | O maior lago da América do Sul é o Lago Titicaca, localizado na fronteira entre o Peru e a Bolívia. [pt] | O maior lago da América do Sul é o Lago Titicaca, localizado na fronteira entre o Peru e a Bolívia. [pt] |
| 591 | Exponha como a Lua se formou. | Claro, ficarei feliz em explicar como a Lua se formou. /  / A Lua é a quarta maior lua natural do Sistema Sola... [pt] | A Lua é uma das luas mais próximas da Terra, localizada a cerca de 363.300 quilômetros da superfície terrestre... [pt] |

