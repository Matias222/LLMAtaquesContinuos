# Etapa D: chequeos sin generación

## Normas y cosenos

Referencia del paper: réplica de alg_fr con otro orden de batches = 0.49; dos direcciones al azar en d=3072 = ±0.018.

| vector | ‖v‖ | v9_smoke_fr | v8_fr | paper_fr | v9_smoke_es | v8_es | paper_es | v9_smoke_de | v8_de | paper_de |
|---|---|---|---|---|---|---|---|---|---|---|
| v9_smoke_fr | 0.095 | 1.00 | 0.11 | 0.17 | 0.03 | -0.01 | 0.02 | 0.36 | 0.02 | 0.06 |
| v8_fr | 0.871 | 0.11 | 1.00 | 0.25 | -0.02 | 0.31 | 0.14 | -0.00 | 0.20 | 0.12 |
| paper_fr | 0.842 | 0.17 | 0.25 | 1.00 | 0.02 | 0.17 | 0.25 | 0.05 | 0.14 | 0.19 |
| v9_smoke_es | 0.085 | 0.03 | -0.02 | 0.02 | 1.00 | 0.14 | 0.16 | 0.18 | -0.01 | 0.04 |
| v8_es | 0.901 | -0.01 | 0.31 | 0.17 | 0.14 | 1.00 | 0.25 | 0.04 | 0.22 | 0.14 |
| paper_es | 0.865 | 0.02 | 0.14 | 0.25 | 0.16 | 0.25 | 1.00 | 0.06 | 0.13 | 0.17 |
| v9_smoke_de | 0.087 | 0.36 | -0.00 | 0.05 | 0.18 | 0.04 | 0.06 | 1.00 | 0.11 | 0.18 |
| v8_de | 0.964 | 0.02 | 0.20 | 0.14 | -0.01 | 0.22 | 0.13 | 0.11 | 1.00 | 0.24 |
| paper_de | 0.849 | 0.06 | 0.12 | 0.19 | 0.04 | 0.14 | 0.17 | 0.18 | 0.24 | 1.00 |

Celda fr: ‖v‖ = 0.095; supera la norma del 0.0% del vocabulario y del 0.0% de los tokens de las preguntas; distancia mediana token-vecino 0.96.

Celda es: ‖v‖ = 0.085; supera la norma del 0.0% del vocabulario y del 0.0% de los tokens de las preguntas; distancia mediana token-vecino 0.96.

Celda de: ‖v‖ = 0.087; supera la norma del 0.0% del vocabulario y del 0.0% de los tokens de las preguntas; distancia mediana token-vecino 0.95.

## Token más cercano de e + α·v (§4.1)

| celda | α | entrada | tokens | % cambia (L2) | % cambia (coseno) |
|---|---|---|---|---|---|
| fr | 0.5 | en | 844 | 0 | 0 |
| fr | 0.5 | es | 1343 | 0 | 0 |
| fr | 0.5 | de | 1287 | 0 | 0 |
| fr | 1.0 | en | 844 | 0 | 0 |
| fr | 1.0 | es | 1343 | 0 | 0 |
| fr | 1.0 | de | 1287 | 0 | 0 |
| fr | 2.0 | en | 844 | 0 | 0 |
| fr | 2.0 | es | 1343 | 0 | 0 |
| fr | 2.0 | de | 1287 | 0 | 0 |
| fr | 4.0 | en | 844 | 0 | 0 |
| fr | 4.0 | es | 1343 | 0 | 0 |
| fr | 4.0 | de | 1287 | 0 | 0 |
| fr | 8.0 | en | 844 | 0 | 0 |
| fr | 8.0 | es | 1343 | 0 | 0 |
| fr | 8.0 | de | 1287 | 0 | 0 |
| es | 0.5 | en | 844 | 0 | 0 |
| es | 0.5 | de | 1287 | 0 | 0 |
| es | 0.5 | fr | 1417 | 0 | 0 |
| es | 1.0 | en | 844 | 0 | 0 |
| es | 1.0 | de | 1287 | 0 | 0 |
| es | 1.0 | fr | 1417 | 0 | 0 |
| es | 2.0 | en | 844 | 0 | 0 |
| es | 2.0 | de | 1287 | 0 | 0 |
| es | 2.0 | fr | 1417 | 0 | 0 |
| es | 4.0 | en | 844 | 0 | 0 |
| es | 4.0 | de | 1287 | 0 | 0 |
| es | 4.0 | fr | 1417 | 0 | 0 |
| es | 8.0 | en | 844 | 0 | 0 |
| es | 8.0 | de | 1287 | 0 | 0 |
| es | 8.0 | fr | 1417 | 0 | 0 |
| de | 0.5 | en | 844 | 0 | 0 |
| de | 0.5 | es | 1343 | 0 | 0 |
| de | 0.5 | fr | 1417 | 0 | 0 |
| de | 1.0 | en | 844 | 0 | 0 |
| de | 1.0 | es | 1343 | 0 | 0 |
| de | 1.0 | fr | 1417 | 0 | 0 |
| de | 2.0 | en | 844 | 0 | 0 |
| de | 2.0 | es | 1343 | 0 | 0 |
| de | 2.0 | fr | 1417 | 0 | 0 |
| de | 4.0 | en | 844 | 0 | 0 |
| de | 4.0 | es | 1343 | 0 | 0 |
| de | 4.0 | fr | 1417 | 0 | 0 |
| de | 8.0 | en | 844 | 0 | 0 |
| de | 8.0 | es | 1343 | 0 | 0 |
| de | 8.0 | fr | 1417 | 0 | 0 |

