# Etapa A: held-out v8 por categoria

Held-out = filas desde int(700*0.84) del CSV de cada celda (16 por categoria). Idioma: GlotLID (lang_id.py). Accuracy: answer_correct con los alias del banco (6 idiomas). Generacion de 250 tokens, referencia y baseline regenerados con el mismo largo. Control nativo = M(q_X): la pregunta escrita en el idioma de la celda, sin parche. Acuerdo = filas donde parche y control coinciden en acierto/fallo.

## Celda fr (parche hacia el francés)

### Pregunta en inglés (norma ‖v‖ = 0.923)

| categoria | n | % fr sin parche | % fr control nativo | % fr parche | acc sin parche | acc control nativo | acc parche | acuerdo parche/control |
|---|---|---|---|---|---|---|---|---|
| factual_clasica | 16 | 0 | 100 | 94 | 100 | 94 | 94 | 100 |
| factual_aperturas | 16 | 0 | 100 | 100 | 100 | 94 | 100 | 94 |
| imperativo | 16 | 0 | 100 | 94 | 100 | 94 | 94 | 100 |
| imperativo_explicativo | 16 | 0 | 100 | 100 | 100 | 69 | 75 | 69 |
| explicativa | 16 | 0 | 100 | 94 | 100 | 88 | 81 | 94 |
| corta | 16 | 0 | 100 | 100 | 94 | 69 | 56 | 88 |
| conversacional | 16 | 0 | 100 | 100 | 100 | 81 | 88 | 69 |
| TOTAL | 112 | 0 | 100 | 97 | 99 | 84 | 84 | 88 |

### Otros idiomas de entrenamiento

| categoria | es: % fr sin / con | es: acc sin / con | de: % fr sin / con | de: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 88 / 94 | 0 / 100 | 100 / 75 |
| factual_aperturas | 0 / 100 | 94 / 94 | 0 / 94 | 100 / 100 |
| imperativo | 0 / 100 | 94 / 94 | 0 / 94 | 94 / 88 |
| imperativo_explicativo | 0 / 100 | 81 / 69 | 0 / 88 | 75 / 44 |
| explicativa | 0 / 100 | 62 / 56 | 0 / 100 | 62 / 56 |
| corta | 0 / 94 | 75 / 69 | 0 / 81 | 69 / 62 |
| conversacional | 0 / 100 | 94 / 88 | 0 / 100 | 88 / 69 |
| TOTAL | 0 / 99 | 84 / 80 | 0 / 94 | 84 / 71 |

### Idiomas no vistos (italiano, portugués)

| categoria | it: % fr sin / con | it: acc sin / con | pt: % fr sin / con | pt: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 88 / 69 | 0 / 100 | 94 / 88 |
| factual_aperturas | 0 / 100 | 94 / 88 | 0 / 100 | 94 / 94 |
| imperativo | 0 / 100 | 88 / 88 | 0 / 88 | 94 / 94 |
| imperativo_explicativo | 0 / 100 | 44 / 62 | 0 / 100 | 75 / 69 |
| explicativa | 0 / 100 | 50 / 56 | 0 / 100 | 81 / 69 |
| corta | 0 / 100 | 62 / 69 | 0 / 94 | 81 / 69 |
| conversacional | 0 / 100 | 88 / 69 | 0 / 100 | 81 / 75 |
| TOTAL | 0 / 100 | 73 / 71 | 0 / 97 | 86 / 79 |

## Celda es (parche hacia el español)

### Pregunta en inglés (norma ‖v‖ = 0.963)

| categoria | n | % es sin parche | % es control nativo | % es parche | acc sin parche | acc control nativo | acc parche | acuerdo parche/control |
|---|---|---|---|---|---|---|---|---|
| factual_clasica | 16 | 0 | 100 | 100 | 100 | 88 | 88 | 100 |
| factual_aperturas | 16 | 0 | 100 | 100 | 100 | 94 | 100 | 94 |
| imperativo | 16 | 0 | 81 | 75 | 100 | 94 | 94 | 100 |
| imperativo_explicativo | 16 | 0 | 100 | 100 | 100 | 81 | 81 | 75 |
| explicativa | 16 | 0 | 100 | 100 | 100 | 62 | 81 | 81 |
| corta | 16 | 6 | 100 | 100 | 94 | 75 | 69 | 94 |
| conversacional | 16 | 0 | 100 | 100 | 100 | 94 | 75 | 81 |
| TOTAL | 112 | 1 | 97 | 96 | 99 | 84 | 84 | 89 |

### Otros idiomas de entrenamiento

| categoria | de: % es sin / con | de: acc sin / con | fr: % es sin / con | fr: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 100 / 94 | 0 / 100 | 94 / 88 |
| factual_aperturas | 0 / 100 | 100 / 88 | 0 / 100 | 94 / 94 |
| imperativo | 0 / 88 | 94 / 81 | 0 / 88 | 94 / 94 |
| imperativo_explicativo | 0 / 100 | 75 / 38 | 0 / 100 | 69 / 75 |
| explicativa | 0 / 100 | 62 / 50 | 0 / 94 | 88 / 50 |
| corta | 6 / 62 | 69 / 75 | 0 / 88 | 69 / 75 |
| conversacional | 0 / 100 | 88 / 75 | 0 / 100 | 81 / 75 |
| TOTAL | 1 / 93 | 84 / 71 | 0 / 96 | 84 / 79 |

### Idiomas no vistos (italiano, portugués)

| categoria | it: % es sin / con | it: acc sin / con | pt: % es sin / con | pt: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 69 | 88 / 75 | 0 / 100 | 94 / 94 |
| factual_aperturas | 0 / 88 | 94 / 81 | 0 / 100 | 94 / 100 |
| imperativo | 0 / 75 | 88 / 88 | 0 / 94 | 94 / 94 |
| imperativo_explicativo | 0 / 81 | 44 / 62 | 0 / 94 | 75 / 62 |
| explicativa | 0 / 81 | 50 / 50 | 0 / 94 | 81 / 50 |
| corta | 0 / 94 | 62 / 69 | 12 / 100 | 81 / 75 |
| conversacional | 0 / 94 | 88 / 62 | 0 / 100 | 81 / 75 |
| TOTAL | 0 / 83 | 73 / 70 | 2 / 97 | 86 / 79 |

## Celda de (parche hacia el alemán)

### Pregunta en inglés (norma ‖v‖ = 0.998)

| categoria | n | % de sin parche | % de control nativo | % de parche | acc sin parche | acc control nativo | acc parche | acuerdo parche/control |
|---|---|---|---|---|---|---|---|---|
| factual_clasica | 16 | 0 | 100 | 100 | 100 | 100 | 100 | 100 |
| factual_aperturas | 16 | 0 | 100 | 94 | 100 | 100 | 100 | 100 |
| imperativo | 16 | 0 | 100 | 94 | 100 | 94 | 94 | 100 |
| imperativo_explicativo | 16 | 0 | 100 | 100 | 100 | 75 | 62 | 75 |
| explicativa | 16 | 0 | 100 | 94 | 100 | 62 | 69 | 81 |
| corta | 16 | 0 | 88 | 100 | 94 | 69 | 75 | 94 |
| conversacional | 16 | 0 | 100 | 100 | 100 | 88 | 81 | 81 |
| TOTAL | 112 | 0 | 98 | 97 | 99 | 84 | 83 | 90 |

### Otros idiomas de entrenamiento

| categoria | es: % de sin / con | es: acc sin / con | fr: % de sin / con | fr: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 88 / 81 | 0 / 94 | 94 / 88 |
| factual_aperturas | 0 / 100 | 94 / 81 | 0 / 100 | 94 / 88 |
| imperativo | 0 / 94 | 94 / 75 | 0 / 94 | 94 / 62 |
| imperativo_explicativo | 0 / 100 | 81 / 62 | 0 / 100 | 69 / 56 |
| explicativa | 0 / 100 | 62 / 44 | 0 / 94 | 88 / 50 |
| corta | 0 / 100 | 75 / 69 | 0 / 100 | 69 / 69 |
| conversacional | 0 / 100 | 94 / 81 | 0 / 100 | 81 / 62 |
| TOTAL | 0 / 99 | 84 / 71 | 0 / 97 | 84 / 68 |

### Idiomas no vistos (italiano, portugués)

| categoria | it: % de sin / con | it: acc sin / con | pt: % de sin / con | pt: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 88 | 88 / 81 | 0 / 100 | 94 / 75 |
| factual_aperturas | 0 / 81 | 94 / 81 | 0 / 100 | 94 / 75 |
| imperativo | 0 / 75 | 88 / 88 | 0 / 94 | 94 / 75 |
| imperativo_explicativo | 0 / 100 | 44 / 56 | 0 / 100 | 75 / 50 |
| explicativa | 0 / 94 | 50 / 44 | 0 / 100 | 81 / 50 |
| corta | 0 / 94 | 62 / 44 | 0 / 100 | 81 / 69 |
| conversacional | 0 / 94 | 88 / 69 | 0 / 100 | 81 / 56 |
| TOTAL | 0 / 89 | 73 / 66 | 0 / 99 | 86 / 64 |

