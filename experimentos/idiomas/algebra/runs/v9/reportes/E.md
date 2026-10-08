# Etapa E: tests de comportamiento

## Resta q_L − v (equivale a las Tablas 5 y 6)

Quedan: la respuesta sigue en el idioma de la pregunta o sin idioma identificable.

| pregunta en | restado | n | % quedan | destinos (%) | acc |
|---|---|---|---|---|---|
| fr | — | 112 | 100 |  | 71 |
| fr | -1·fr | 112 | 33 | en 40, es 21, it 3, ca 1 | 34 |
| fr | -1·es | 112 | 96 | en 4 | 41 |
| fr | -1·de | 112 | 97 | en 3 | 31 |
| fr | -1·rand0_fr | 112 | 98 | en 2 | 57 |
| fr | -1·rand1_fr | 112 | 100 |  | 62 |
| fr | -1·rand2_fr | 112 | 100 |  | 55 |
| es | — | 112 | 99 | ca 1 | 70 |
| es | -1·fr | 112 | 98 | en 1, ca 1 | 46 |
| es | -1·es | 112 | 21 | fr 61, en 15, it 2, ca 1 | 37 |
| es | -1·de | 112 | 100 |  | 46 |
| es | -1·rand0_es | 112 | 100 |  | 63 |
| es | -1·rand1_es | 112 | 97 | fr 2, ca 1 | 64 |
| es | -1·rand2_es | 112 | 99 | ca 1 | 66 |
| de | — | 112 | 99 | en 1 | 72 |
| de | -1·fr | 112 | 90 | en 10 | 38 |
| de | -1·es | 112 | 81 | en 19 | 40 |
| de | -1·de | 112 | 54 | en 38, sv 5, da 2, no 1 | 32 |
| de | -1·rand0_de | 112 | 90 | en 9, nl 1 | 48 |
| de | -1·rand1_de | 112 | 95 | nl 3, en 3 | 54 |
| de | -1·rand2_de | 112 | 95 | nl 4, en 2 | 52 |

## Identificación de idioma (Tabla 7)

| condición | n | dice en | dice fr | dice es | dice de | ninguno |
|---|---|---|---|---|---|---|
| lang_id · prompt | 112 | 96 | 1 | 2 | 0 | 0 |
| lang_id · prompt +1*fr | 112 | 21 | 72 | 1 | 0 | 4 |
| lang_id · prompt +1*es | 112 | 29 | 3 | 63 | 0 | 4 |
| lang_id · prompt +1*de | 112 | 4 | 2 | 3 | 88 | 3 |
| lang_id · prompt +1*rand0 | 112 | 96 | 1 | 1 | 0 | 3 |
| lang_id · prompt_fr | 112 | 0 | 100 | 0 | 0 | 0 |
| lang_id · prompt_es | 112 | 0 | 0 | 100 | 0 | 0 |
| lang_id · prompt_de | 112 | 1 | 1 | 3 | 96 | 0 |

## Resta contra una instrucción (Tabla 8)

| condición | n | % fr | % en | % sin idioma | acc |
|---|---|---|---|---|---|
| instr_fr · prompt | 112 | 100 | 0 | 0 | 80 |
| instr_fr · prompt -1*fr | 112 | 97 | 0 | 3 | 75 |
| instr_fr · prompt -1*es | 112 | 97 | 1 | 2 | 69 |
| instr_fr · prompt -1*rand0 | 112 | 98 | 1 | 1 | 76 |

## Instrucción en conflicto (Tabla 9)

| condición | n | % fr | % en | % sin idioma | acc |
|---|---|---|---|---|---|
| instr_en · prompt_fr | 112 | 71 | 29 | 0 | 71 |
| instr_en · prompt | 112 | 0 | 100 | 0 | 95 |
| instr_en · prompt +1*fr | 112 | 89 | 11 | 0 | 75 |
| instr_en · prompt +1*rand0 | 112 | 0 | 100 | 0 | 92 |
| plain · prompt | 112 | 0 | 100 | 0 | 96 |
| plain · prompt +1*fr | 112 | 100 | 0 | 0 | 76 |

