# Formatos: Shared vs Question-3 vs Header-3 (celda es)

Shared = algebra/runs/v10/alg_es; Question-3 = algebra/runs/v10/pos_q3_es; Header-3 = algebra/runs/v10/pos_h3_es; tests = algebra/runs/v10/pos_tests_es.

## Formatos

| formato | anchor | forma | ‖v‖ total | ‖v_i‖ por posición | epoch |
|---|---|---|---|---|---|
| Shared | goal_all | (1, 1, 3072) | 0.912 | 0.912 | 10 |
| Question-3 | goal | (1, 3, 3072) | 1.290 | 0.921 / 0.633 / 0.646 | 9 |
| Header-3 | header | (1, 3, 3072) | 0.816 | 0.367 / 0.504 / 0.526 | 10 |

## Idioma y accuracy por entrada

| entrada | sin parche / nativo | Shared | Question-3 | Header-3 |
|---|---|---|---|---|
| en sin parche | 0 / 97 | — | — | — |
| control nativo (es) | 96 / 72 | — | — | — |
| en (held-out) |  | 99 / 82 | 98 / 81 | 99 / 82 |
| de |  | 97 / 66 | 96 / 54 | 99 / 79 |
| fr |  | 96 / 66 | 98 / 69 | 100 / 81 |
| it |  | 91 / 58 | 96 / 66 | 100 / 74 |
| pt |  | 84 / 63 | 89 / 61 | 100 / 78 |
| open1 (en) |  | 96 / — | 100 / — | 100 / — |
| open2 (en) |  | 100 / — | 98 / — | 100 / — |
| open2 (de) |  | 96 / — | 90 / — | 100 / — |
| open2 (fr) |  | 100 / — | 98 / — | 100 / — |

Celdas: % es / accuracy (— = no medido; open sin accuracy).

# Tests (Shared = parche es; rand0_q3 / rand0_h3 = azar con forma, norma y anchor de q3 / h3)

## pos_conflicto

| condición | n | % es | % en | % queda en el idioma de la pregunta | destinos (%) | acc |
|---|---|---|---|---|---|---|
| instr_en · prompt_es | 112 | 73 | 26 | 73 | en 26, ca 1 | 75 |
| instr_en · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en · prompt +1*es | 112 | 45 | 54 | 54 | es 45, ca 1 | 88 |
| instr_en · prompt +1*q3 | 112 | 33 | 67 | 67 | es 33 | 87 |
| instr_en · prompt +1*h3 | 112 | 99 | 0 | 0 | es 99, ca 1 | 80 |
| instr_en · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 95 |
| instr_en · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 97 |
| instr_en · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt_es | 112 | 4 | 96 | 4 | en 96 | 95 |
| instr_en_post · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*es | 112 | 0 | 100 | 100 |  | 97 |
| instr_en_post · prompt +1*q3 | 112 | 20 | 80 | 80 | es 20 | 93 |
| instr_en_post · prompt +1*h3 | 112 | 99 | 0 | 0 | es 99, ca 1 | 84 |
| instr_en_post · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt_es | 112 | 3 | 96 | 4 | en 96 | 94 |
| instr_en_post_ref · prompt | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt +1*es | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt +1*q3 | 112 | 15 | 85 | 85 | es 15 | 94 |
| instr_en_post_ref · prompt +1*h3 | 112 | 99 | 0 | 0 | es 99, ca 1 | 78 |
| instr_en_post_ref · prompt +1*rand0 | 112 | 0 | 100 | 100 |  | 99 |
| instr_en_post_ref · prompt +1*rand0_q3 | 112 | 0 | 100 | 100 |  | 96 |
| instr_en_post_ref · prompt +1*rand0_h3 | 112 | 0 | 100 | 100 |  | 96 |
| plain · prompt | 112 | 0 | 100 | 100 |  | 97 |
| plain · prompt +1*es | 112 | 99 | 0 | 0 | es 99, ca 1 | 82 |
| plain · prompt +1*q3 | 112 | 98 | 0 | 1 | es 98, ca 1 | 81 |
| plain · prompt +1*h3 | 112 | 99 | 0 | 0 | es 99, ca 1 | 82 |

## pos_idioma

| condición | n | dice es | dice en | ninguno | respuesta escrita en es |
|---|---|---|---|---|---|
| lang_id · prompt | 112 | 2 | 96 | 0 | 0 |
| lang_id · prompt +1*es | 112 | 90 | 4 | 4 | 0 |
| lang_id · prompt +1*q3 | 112 | 76 | 18 | 4 | 0 |
| lang_id · prompt +1*h3 | 112 | 2 | 85 | 8 | 71 |
| lang_id · prompt +1*rand0 | 112 | 1 | 96 | 3 | 0 |
| lang_id · prompt +1*rand0_q3 | 112 | 2 | 96 | 1 | 0 |
| lang_id · prompt +1*rand0_h3 | 112 | 2 | 96 | 1 | 0 |
| lang_id · prompt_es | 112 | 100 | 0 | 0 | 0 |

## pos_resta

| condición | n | % es | % en | % queda en el idioma de la pregunta | destinos (%) | acc |
|---|---|---|---|---|---|---|
| plain · prompt_es | 112 | 96 | 0 | 99 | ca 1 | 72 |
| plain · prompt_es -1*es | 112 | 17 | 3 | 17 | fr 77, en 3, it 1 | 46 |
| plain · prompt_es -1*q3 | 112 | 95 | 0 | 96 | fr 3, ca 1 | 70 |
| plain · prompt_es -1*h3 | 112 | 96 | 0 | 99 | ca 1 | 78 |
| plain · prompt_es -1*rand0 | 112 | 97 | 1 | 97 | it 1, fr 1, en 1 | 59 |
| plain · prompt_es -1*rand0_q3 | 112 | 97 | 0 | 99 | ca 1 | 77 |
| plain · prompt_es -1*rand0_h3 | 112 | 96 | 0 | 99 | ca 1 | 73 |
| plain · prompt_es -2*q3 | 112 | 86 | 2 | 88 | fr 11, en 2 | 70 |

## Controles

- OK: anchors y posiciones parcheadas

