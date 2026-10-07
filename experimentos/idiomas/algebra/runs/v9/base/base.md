# Base v9: salidas sin parche

Generacion greedy de 150 tokens. Idioma: GlotLID. Estas salidas son el baseline, el control nativo M(q_X) y las condiciones a=0 de todas las celdas.

## heldout

| entrada | n | idioma de la salida (%) | acc |
|---|---|---|---|
| en | 112 | en 100 | 96 |
| es | 112 | es 96, unknown 4, ca 1 | 70 |
| de | 112 | de 95, unknown 4, en 1 | 72 |
| fr | 112 | fr 99, unknown 1 | 71 |
| it | 112 | it 97, unknown 3 | 68 |
| pt | 112 | pt 81, unknown 15, es 2, en 1 | 70 |

## open1

| entrada | n | idioma de la salida (%) | acc |
|---|---|---|---|
| en | 99 | en 99, unknown 1 | - |
| es | 99 | es 100 | - |
| de | 99 | de 98, unknown 1, no 1 | - |
| fr | 99 | fr 99, unknown 1 | - |

## open2

| entrada | n | idioma de la salida (%) | acc |
|---|---|---|---|
| en | 50 | en 98, es 2 | - |
| es | 50 | es 100 | - |
| de | 50 | de 98, da 2 | - |
| fr | 50 | fr 100 | - |
