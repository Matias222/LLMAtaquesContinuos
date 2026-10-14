# Etapa D: chequeos sin generación

## Normas y cosenos

Referencia del paper: réplica de alg_fr con otro orden de batches = 0.49; dos direcciones al azar en d=2560 = ±0.020 (1/√d).

| vector | ‖v‖ | qwen3_v10_fr | qwen3_v10_es | qwen3_v10_de |
|---|---|---|---|---|
| qwen3_v10_fr | 0.923 | 1.00 | 0.27 | 0.26 |
| qwen3_v10_es | 0.963 | 0.27 | 1.00 | 0.24 |
| qwen3_v10_de | 0.998 | 0.26 | 0.24 | 1.00 |

Celda fr: ‖v‖ = 0.923 (‖v‖/‖e‖ medio del vocabulario = 0.848; Llama v9: 0.78-0.87); supera la norma del 9.0% del vocabulario y del 2.5% de los tokens de las preguntas; distancia mediana token-vecino 0.93.

Celda es: ‖v‖ = 0.963 (‖v‖/‖e‖ medio del vocabulario = 0.885; Llama v9: 0.78-0.87); supera la norma del 11.8% del vocabulario y del 5.8% de los tokens de las preguntas; distancia mediana token-vecino 0.93.

Celda de: ‖v‖ = 0.998 (‖v‖/‖e‖ medio del vocabulario = 0.917; Llama v9: 0.78-0.87); supera la norma del 15.9% del vocabulario y del 10.6% de los tokens de las preguntas; distancia mediana token-vecino 0.93.

## Token más cercano de e + α·v (§4.1)

| celda | α | entrada | tokens | % cambia (L2) | % cambia (coseno) |
|---|---|---|---|---|---|
| fr | 0.5 | en | 848 | 0 | 0 |
| fr | 0.5 | es | 1336 | 0 | 0 |
| fr | 0.5 | de | 1293 | 0 | 0 |
| fr | 1.0 | en | 848 | 0 | 0 |
| fr | 1.0 | es | 1336 | 0 | 0 |
| fr | 1.0 | de | 1293 | 0 | 0 |
| fr | 2.0 | en | 848 | 0 | 0 |
| fr | 2.0 | es | 1336 | 0 | 0 |
| fr | 2.0 | de | 1293 | 0 | 0 |
| fr | 4.0 | en | 848 | 0 | 0 |
| fr | 4.0 | es | 1336 | 0 | 0 |
| fr | 4.0 | de | 1293 | 0 | 0 |
| fr | 8.0 | en | 848 | 29 | 30 |
| fr | 8.0 | es | 1336 | 14 | 14 |
| fr | 8.0 | de | 1293 | 11 | 10 |
| es | 0.5 | en | 848 | 0 | 0 |
| es | 0.5 | de | 1293 | 0 | 0 |
| es | 0.5 | fr | 1410 | 0 | 0 |
| es | 1.0 | en | 848 | 0 | 0 |
| es | 1.0 | de | 1293 | 0 | 0 |
| es | 1.0 | fr | 1410 | 0 | 0 |
| es | 2.0 | en | 848 | 0 | 0 |
| es | 2.0 | de | 1293 | 0 | 0 |
| es | 2.0 | fr | 1410 | 0 | 0 |
| es | 4.0 | en | 848 | 0 | 0 |
| es | 4.0 | de | 1293 | 0 | 0 |
| es | 4.0 | fr | 1410 | 0 | 0 |
| es | 8.0 | en | 848 | 43 | 49 |
| es | 8.0 | de | 1293 | 20 | 21 |
| es | 8.0 | fr | 1410 | 27 | 28 |
| de | 0.5 | en | 848 | 0 | 0 |
| de | 0.5 | es | 1336 | 0 | 0 |
| de | 0.5 | fr | 1410 | 0 | 0 |
| de | 1.0 | en | 848 | 0 | 0 |
| de | 1.0 | es | 1336 | 0 | 0 |
| de | 1.0 | fr | 1410 | 0 | 0 |
| de | 2.0 | en | 848 | 0 | 0 |
| de | 2.0 | es | 1336 | 0 | 0 |
| de | 2.0 | fr | 1410 | 0 | 0 |
| de | 4.0 | en | 848 | 0 | 0 |
| de | 4.0 | es | 1336 | 0 | 0 |
| de | 4.0 | fr | 1410 | 0 | 0 |
| de | 8.0 | en | 848 | 61 | 67 |
| de | 8.0 | es | 1336 | 47 | 53 |
| de | 8.0 | fr | 1410 | 41 | 49 |

