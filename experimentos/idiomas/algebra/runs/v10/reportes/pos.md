# Formatos: Shared vs Question-3 vs Header-3 (celda fr)

Shared = algebra/runs/v10/alg_fr; Question-3 = algebra/runs/v10/pos_q3_fr; Header-3 = algebra/runs/v10/pos_h3_fr; tests = algebra/runs/v10/pos_tests.

## Formatos

| formato | anchor | forma | ‖v‖ total | ‖v_i‖ por posición | epoch |
|---|---|---|---|---|---|
| Shared | goal_all | (1, 1, 3072) | 0.878 | 0.878 | 10 |
| Question-3 | goal | (1, 3, 3072) | 1.288 | 0.962 / 0.610 / 0.601 | 10 |
| Header-3 | header | (1, 3, 3072) | 0.843 | 0.370 / 0.513 / 0.557 | 10 |

## Idioma y accuracy por entrada

| entrada | sin parche / nativo | Shared | Question-3 | Header-3 |
|---|---|---|---|---|
| en sin parche | 0 / 97 | — | — | — |
| control nativo (fr) | 99 / 76 | — | — | — |
| en (held-out) |  | 100 / 79 | 98 / 71 | 100 / 83 |
| es |  | 99 / 68 | 99 / 64 | 100 / 71 |
| de |  | 99 / 63 | 96 / 63 | 100 / 71 |
| it |  | 89 / 62 | 72 / 65 | 100 / 69 |
| pt |  | 96 / 62 | 96 / 56 | 99 / 67 |
| open1 (en) |  | 94 / — | 99 / — | 100 / — |
| open2 (en) |  | 100 / — | 98 / — | 100 / — |
| open2 (es) |  | 100 / — | 96 / — | 100 / — |
| open2 (de) |  | 92 / — | 96 / — | 100 / — |

Celdas: % francés / accuracy (— = no medido; open sin accuracy).

# Tests (Shared = parche fr; rand0_q3 / rand0_h3 = azar con forma, norma y anchor de q3 / h3)

## pos_conflicto

| condición | n | % fr | % en | % queda en el idioma de la pregunta | destinos (%) | acc |
|---|---|---|---|---|---|---|
| instr_en · prompt_fr | 112 | 72 | 28 | 72 | en 28 | 78 |
| instr_en · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en · prompt +1*fr | 112 | 77 | 23 | 23 | fr 77 | 82 |
| instr_en · prompt +1*q3 | 112 | 18 | 79 | 80 | fr 18, es 2 | 89 |
| instr_en · prompt +1*h3 | 112 | 100 | 0 | 0 | fr 100 | 81 |
| instr_en · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 97 |
| instr_en · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt_fr | 112 | 4 | 96 | 4 | en 96 | 93 |
| instr_en_post · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*fr | 112 | 23 | 77 | 77 | fr 23 | 91 |
| instr_en_post · prompt +1*q3 | 112 | 16 | 84 | 84 | fr 16 | 88 |
| instr_en_post · prompt +1*h3 | 112 | 100 | 0 | 0 | fr 100 | 79 |
| instr_en_post · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt_fr | 112 | 2 | 98 | 2 | en 98 | 92 |
| instr_en_post_ref · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt +1*fr | 112 | 17 | 83 | 83 | fr 17 | 91 |
| instr_en_post_ref · prompt +1*q3 | 112 | 19 | 81 | 81 | fr 19 | 88 |
| instr_en_post_ref · prompt +1*h3 | 112 | 100 | 0 | 0 | fr 100 | 83 |
| instr_en_post_ref · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 99 |
| instr_en_post_ref · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| plain · prompt | 112 | 0 | 100 | 100 |  | 97 |
| plain · prompt +1*fr | 112 | 100 | 0 | 0 | fr 100 | 79 |
| plain · prompt +1*q3 | 112 | 98 | 0 | 0 | fr 98, ca 1, es 1 | 70 |
| plain · prompt +1*h3 | 112 | 100 | 0 | 0 | fr 100 | 82 |

## pos_directiva

| condición | n | % fr | % en | % queda en el idioma de la pregunta | destinos (%) | acc |
|---|---|---|---|---|---|---|
| instr_fr · prompt | 112 | 100 | 0 | 0 | fr 100 | 81 |
| instr_fr · prompt -1*fr | 112 | 96 | 2 | 4 | fr 96 | 71 |
| instr_fr · prompt -1*q3 | 112 | 98 | 0 | 2 | fr 98 | 83 |
| instr_fr · prompt -1*h3 | 112 | 99 | 0 | 1 | fr 99 | 79 |
| instr_fr · prompt -1*rand0 | 112 | 99 | 0 | 1 | fr 99 | 79 |
| instr_fr · prompt -1*rand0_q3 | 112 | 100 | 0 | 0 | fr 100 | 82 |
| instr_fr · prompt -1*rand0_h3 | 112 | 99 | 0 | 1 | fr 99 | 81 |

## pos_idioma

| condición | n | dice fr | dice en | ninguno |
|---|---|---|---|---|
| lang_id · prompt | 112 | 1 | 96 | 0 |
| lang_id · prompt +1*fr | 112 | 76 | 15 | 5 |
| lang_id · prompt +1*q3 | 112 | 53 | 37 | 7 |
| lang_id · prompt +1*h3 | 112 | 4 | 45 | 50 |
| lang_id · prompt +1*rand0 | 112 | 1 | 96 | 3 |
| lang_id · prompt +1*rand0_q3 | 112 | 1 | 96 | 1 |
| lang_id · prompt +1*rand0_h3 | 112 | 1 | 96 | 1 |
| lang_id · prompt_fr | 112 | 100 | 0 | 0 |

## pos_resta

| condición | n | % fr | % en | % queda en el idioma de la pregunta | destinos (%) | acc |
|---|---|---|---|---|---|---|
| plain · prompt_fr | 112 | 99 | 0 | 100 |  | 76 |
| plain · prompt_fr -1*fr | 112 | 9 | 84 | 9 | en 84, es 6, de 1 | 30 |
| plain · prompt_fr -1*q3 | 112 | 99 | 0 | 99 | es 1 | 66 |
| plain · prompt_fr -1*h3 | 112 | 99 | 0 | 100 |  | 76 |
| plain · prompt_fr -1*rand0 | 112 | 98 | 2 | 98 | en 2 | 56 |
| plain · prompt_fr -1*rand0_q3 | 112 | 99 | 1 | 99 | en 1 | 78 |
| plain · prompt_fr -1*rand0_h3 | 112 | 96 | 0 | 99 | de 1 | 75 |
| plain · prompt_fr -2*q3 | 112 | 96 | 1 | 97 | es 2, en 1 | 59 |

## Controles

- OK: anchors y posiciones parcheadas

