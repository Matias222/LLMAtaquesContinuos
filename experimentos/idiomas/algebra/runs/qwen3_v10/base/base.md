# Base v9: salidas sin parche

Generacion greedy de 250 tokens. Idioma: GlotLID. Estas salidas son el baseline, el control nativo M(q_X) y las condiciones a=0 de todas las celdas.

## heldout

| entrada | n | idioma de la salida (%) | acc |
|---|---|---|---|
| en | 112 | en 99, es 1 | 99 |
| es | 112 | es 97, ca 2, gl 1 | 84 |
| de | 112 | de 98, es 1, en 1 | 84 |
| fr | 112 | fr 100 | 84 |
| it | 112 | it 99, ca 1 | 73 |
| pt | 112 | pt 94, gl 4, es 2 | 86 |

## open1

| entrada | n | idioma de la salida (%) | acc |
|---|---|---|---|
| en | 99 | en 99, unknown 1 | - |
| es | 99 | es 99, unknown 1 | - |
| de | 99 | de 99, unknown 1 | - |
| fr | 99 | fr 98, unknown 1, es 1 | - |

## open2

| entrada | n | idioma de la salida (%) | acc |
|---|---|---|---|
| en | 50 | en 100 | - |
| es | 50 | es 100 | - |
| de | 50 | de 98, no 2 | - |
| fr | 50 | fr 100 | - |
