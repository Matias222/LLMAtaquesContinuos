# Etapa D: chequeos sin generación

## Normas y cosenos

Referencia del paper: réplica de alg_fr con otro orden de batches = 0.49; dos direcciones al azar en d=3072 = ±0.018.

| vector | ‖v‖ | v9_fr | v8_fr | paper_fr | v9_es | v8_es | paper_es | v9_de | v8_de | paper_de |
|---|---|---|---|---|---|---|---|---|---|---|
| v9_fr | 0.844 | 1.00 | 0.58 | 0.25 | 0.26 | 0.27 | 0.15 | 0.19 | 0.19 | 0.11 |
| v8_fr | 0.871 | 0.58 | 1.00 | 0.25 | 0.30 | 0.31 | 0.14 | 0.20 | 0.20 | 0.12 |
| paper_fr | 0.842 | 0.25 | 0.25 | 1.00 | 0.17 | 0.17 | 0.25 | 0.14 | 0.14 | 0.19 |
| v9_es | 0.863 | 0.26 | 0.30 | 0.17 | 1.00 | 0.58 | 0.25 | 0.22 | 0.21 | 0.12 |
| v8_es | 0.901 | 0.27 | 0.31 | 0.17 | 0.58 | 1.00 | 0.25 | 0.22 | 0.22 | 0.14 |
| paper_es | 0.865 | 0.15 | 0.14 | 0.25 | 0.25 | 0.25 | 1.00 | 0.14 | 0.13 | 0.17 |
| v9_de | 0.942 | 0.19 | 0.20 | 0.14 | 0.22 | 0.22 | 0.14 | 1.00 | 0.63 | 0.28 |
| v8_de | 0.964 | 0.19 | 0.20 | 0.14 | 0.21 | 0.22 | 0.13 | 0.63 | 1.00 | 0.24 |
| paper_de | 0.849 | 0.11 | 0.12 | 0.19 | 0.12 | 0.14 | 0.17 | 0.28 | 0.24 | 1.00 |

Celda fr: ‖v‖ = 0.844; supera la norma del 1.9% del vocabulario y del 0.2% de los tokens de las preguntas; distancia mediana token-vecino 0.96.

Celda es: ‖v‖ = 0.863; supera la norma del 2.6% del vocabulario y del 0.9% de los tokens de las preguntas; distancia mediana token-vecino 0.96.

Celda de: ‖v‖ = 0.942; supera la norma del 9.5% del vocabulario y del 3.0% de los tokens de las preguntas; distancia mediana token-vecino 0.95.

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
| fr | 8.0 | en | 844 | 37 | 41 |
| fr | 8.0 | es | 1343 | 28 | 32 |
| fr | 8.0 | de | 1287 | 21 | 24 |
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
| es | 8.0 | en | 844 | 19 | 19 |
| es | 8.0 | de | 1287 | 8 | 8 |
| es | 8.0 | fr | 1417 | 8 | 8 |
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
| de | 8.0 | en | 844 | 2 | 2 |
| de | 8.0 | es | 1343 | 1 | 1 |
| de | 8.0 | fr | 1417 | 6 | 6 |

