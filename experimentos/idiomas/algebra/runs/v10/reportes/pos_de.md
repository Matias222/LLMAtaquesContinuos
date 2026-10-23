# Formatos: Shared vs Question-3 vs Header-3 (celda de)

Shared = algebra/runs/v10/alg_de; Question-3 = algebra/runs/v10/pos_q3_de; Header-3 = algebra/runs/v10/pos_h3_de; tests = algebra/runs/v10/pos_tests_de.

## Formatos

| formato | anchor | forma | ‖v‖ total | ‖v_i‖ por posición | epoch |
|---|---|---|---|---|---|
| Shared | goal_all | (1, 1, 3072) | 0.936 | 0.936 | 10 |
| Question-3 | goal | (1, 3, 3072) | 1.349 | 0.956 / 0.689 / 0.656 | 10 |
| Header-3 | header | (1, 3, 3072) | 0.911 | 0.468 / 0.547 / 0.558 | 10 |

## Idioma y accuracy por entrada

| entrada | sin parche / nativo | Shared | Question-3 | Header-3 |
|---|---|---|---|---|
| en sin parche | 0 / 97 | — | — | — |
| control nativo (de) | 95 / 78 | — | — | — |
| en (held-out) |  | 99 / 81 | 100 / 70 | 100 / 79 |
| es |  | 97 / 66 | 98 / 66 | 100 / 74 |
| fr |  | 100 / 70 | 98 / 60 | 99 / 74 |
| it |  | 97 / 57 | 79 / 58 | 100 / 66 |
| pt |  | 89 / 65 | 91 / 54 | 99 / 69 |
| open1 (en) |  | 94 / — | 100 / — | 100 / — |
| open2 (en) |  | 98 / — | 96 / — | 100 / — |
| open2 (es) |  | 98 / — | 96 / — | 100 / — |
| open2 (fr) |  | 100 / — | 96 / — | 100 / — |

Celdas: % de / accuracy (— = no medido; open sin accuracy).

# Tests (Shared = parche de; rand0_q3 / rand0_h3 = azar con forma, norma y anchor de q3 / h3)

## pos_conflicto

| condición | n | % de | % en | % queda en el idioma de la pregunta | destinos (%) | acc |
|---|---|---|---|---|---|---|
| instr_en · prompt_de | 112 | 67 | 32 | 67 | en 32, nl 1 | 79 |
| instr_en · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en · prompt +1*de | 112 | 51 | 48 | 49 | de 51 | 85 |
| instr_en · prompt +1*q3 | 112 | 1 | 97 | 99 | de 1 | 96 |
| instr_en · prompt +1*h3 | 112 | 99 | 1 | 1 | de 99 | 81 |
| instr_en · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 97 |
| instr_en · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt_de | 112 | 4 | 96 | 4 | en 96 | 90 |
| instr_en_post · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*de | 112 | 7 | 93 | 93 | de 7 | 97 |
| instr_en_post · prompt +1*q3 | 112 | 29 | 71 | 71 | de 29 | 89 |
| instr_en_post · prompt +1*h3 | 112 | 97 | 3 | 3 | de 97 | 79 |
| instr_en_post · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 94 |
| instr_en_post · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt_de | 112 | 2 | 98 | 2 | en 98 | 92 |
| instr_en_post_ref · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt +1*de | 112 | 4 | 96 | 96 | de 4 | 96 |
| instr_en_post_ref · prompt +1*q3 | 112 | 27 | 73 | 73 | de 27 | 88 |
| instr_en_post_ref · prompt +1*h3 | 112 | 95 | 5 | 5 | de 95 | 80 |
| instr_en_post_ref · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 99 |
| instr_en_post_ref · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 95 |
| plain · prompt | 112 | 0 | 100 | 100 |  | 97 |
| plain · prompt +1*de | 112 | 99 | 1 | 1 | de 99 | 81 |
| plain · prompt +1*q3 | 112 | 100 | 0 | 0 | de 100 | 69 |
| plain · prompt +1*h3 | 112 | 100 | 0 | 0 | de 100 | 79 |

## pos_idioma

| condición | n | dice de | dice en | ninguno | respuesta escrita en de |
|---|---|---|---|---|---|
| lang_id · prompt | 112 | 0 | 96 | 0 | 0 |
| lang_id · prompt +1*de | 112 | 85 | 9 | 3 | 0 |
| lang_id · prompt +1*q3 | 112 | 64 | 25 | 3 | 0 |
| lang_id · prompt +1*h3 | 112 | 1 | 90 | 8 | 99 |
| lang_id · prompt +1*rand0 | 112 | 0 | 95 | 4 | 0 |
| lang_id · prompt +1*rand0_q3 | 112 | 0 | 95 | 1 | 0 |
| lang_id · prompt +1*rand0_h3 | 112 | 0 | 96 | 1 | 0 |
| lang_id · prompt_de | 112 | 96 | 1 | 0 | 0 |

## pos_resta

| condición | n | % de | % en | % queda en el idioma de la pregunta | destinos (%) | acc |
|---|---|---|---|---|---|---|
| plain · prompt_de | 112 | 95 | 1 | 99 | en 1 | 78 |
| plain · prompt_de -1*de | 112 | 3 | 96 | 3 | en 96, nl 2 | 29 |
| plain · prompt_de -1*q3 | 112 | 92 | 4 | 96 | en 4 | 70 |
| plain · prompt_de -1*h3 | 112 | 95 | 1 | 99 | en 1 | 77 |
| plain · prompt_de -1*rand0 | 112 | 92 | 7 | 92 | en 7, nl 1 | 53 |
| plain · prompt_de -1*rand0_q3 | 112 | 96 | 1 | 99 | en 1 | 73 |
| plain · prompt_de -1*rand0_h3 | 112 | 94 | 1 | 99 | en 1 | 74 |
| plain · prompt_de -2*q3 | 112 | 87 | 6 | 89 | en 6, es 3, pt 1 | 60 |

## Controles

- OK: anchors y posiciones parcheadas

