# Etapa A: held-out v8 por categoria

Held-out = filas desde int(700*0.84) del CSV de cada celda (16 por categoria). Idioma: GlotLID (lang_id.py). Accuracy: answer_correct con los alias del banco (6 idiomas). Generacion de 250 tokens, referencia y baseline regenerados con el mismo largo. Control nativo = M(q_X): la pregunta escrita en el idioma de la celda, sin parche. Acuerdo = filas donde parche y control coinciden en acierto/fallo.

## Celda fr (parche hacia el francés)

### Pregunta en inglés (norma ‖v‖ = 0.878)

| categoria | n | % fr sin parche | % fr control nativo | % fr parche | acc sin parche | acc control nativo | acc parche | acuerdo parche/control |
|---|---|---|---|---|---|---|---|---|
| factual_clasica | 16 | 0 | 100 | 100 | 100 | 94 | 94 | 100 |
| factual_aperturas | 16 | 0 | 94 | 100 | 100 | 81 | 81 | 100 |
| imperativo | 16 | 0 | 100 | 100 | 94 | 81 | 81 | 100 |
| imperativo_explicativo | 16 | 0 | 100 | 100 | 100 | 62 | 88 | 75 |
| explicativa | 16 | 0 | 100 | 100 | 100 | 56 | 50 | 81 |
| corta | 16 | 0 | 100 | 100 | 88 | 69 | 62 | 94 |
| conversacional | 16 | 0 | 100 | 100 | 100 | 88 | 94 | 94 |
| TOTAL | 112 | 0 | 99 | 100 | 97 | 76 | 79 | 92 |

### Otros idiomas de entrenamiento

| categoria | es: % fr sin / con | es: acc sin / con | de: % fr sin / con | de: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 94 | 81 / 88 | 0 / 100 | 94 / 81 |
| factual_aperturas | 0 / 100 | 94 / 56 | 0 / 100 | 88 / 75 |
| imperativo | 0 / 100 | 75 / 81 | 0 / 100 | 81 / 69 |
| imperativo_explicativo | 0 / 100 | 44 / 38 | 0 / 100 | 62 / 62 |
| explicativa | 0 / 100 | 50 / 56 | 0 / 100 | 62 / 25 |
| corta | 0 / 100 | 69 / 75 | 0 / 94 | 69 / 62 |
| conversacional | 0 / 100 | 94 / 81 | 0 / 100 | 88 / 69 |
| TOTAL | 0 / 99 | 72 / 68 | 0 / 99 | 78 / 63 |

### Idiomas no vistos (italiano, portugués)

| categoria | it: % fr sin / con | it: acc sin / con | pt: % fr sin / con | pt: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 75 / 75 | 0 / 88 | 81 / 81 |
| factual_aperturas | 0 / 81 | 81 / 62 | 0 / 94 | 81 / 62 |
| imperativo | 0 / 88 | 88 / 88 | 0 / 94 | 81 / 81 |
| imperativo_explicativo | 0 / 81 | 69 / 38 | 0 / 94 | 56 / 44 |
| explicativa | 0 / 88 | 31 / 44 | 0 / 100 | 56 / 44 |
| corta | 0 / 100 | 75 / 50 | 0 / 100 | 62 / 50 |
| conversacional | 0 / 88 | 88 / 75 | 0 / 100 | 81 / 75 |
| TOTAL | 0 / 89 | 72 / 62 | 0 / 96 | 71 / 62 |

## Celda es (parche hacia el español)

### Pregunta en inglés (norma ‖v‖ = 0.912)

| categoria | n | % es sin parche | % es control nativo | % es parche | acc sin parche | acc control nativo | acc parche | acuerdo parche/control |
|---|---|---|---|---|---|---|---|---|
| factual_clasica | 16 | 0 | 94 | 100 | 100 | 81 | 94 | 88 |
| factual_aperturas | 16 | 0 | 100 | 100 | 100 | 94 | 100 | 94 |
| imperativo | 16 | 0 | 88 | 94 | 94 | 75 | 81 | 94 |
| imperativo_explicativo | 16 | 0 | 100 | 100 | 100 | 44 | 81 | 62 |
| explicativa | 16 | 0 | 100 | 100 | 100 | 50 | 81 | 56 |
| corta | 16 | 0 | 94 | 100 | 88 | 69 | 69 | 75 |
| conversacional | 16 | 0 | 94 | 100 | 100 | 94 | 69 | 75 |
| TOTAL | 112 | 0 | 96 | 99 | 97 | 72 | 82 | 78 |

### Otros idiomas de entrenamiento

| categoria | de: % es sin / con | de: acc sin / con | fr: % es sin / con | fr: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 94 / 94 | 0 / 100 | 94 / 81 |
| factual_aperturas | 0 / 100 | 88 / 62 | 0 / 94 | 81 / 62 |
| imperativo | 0 / 88 | 81 / 88 | 0 / 88 | 81 / 75 |
| imperativo_explicativo | 0 / 100 | 62 / 62 | 0 / 100 | 62 / 56 |
| explicativa | 0 / 100 | 62 / 25 | 0 / 100 | 56 / 44 |
| corta | 0 / 100 | 69 / 62 | 0 / 94 | 69 / 69 |
| conversacional | 0 / 94 | 88 / 69 | 0 / 100 | 88 / 75 |
| TOTAL | 0 / 97 | 78 / 66 | 0 / 96 | 76 / 66 |

### Idiomas no vistos (italiano, portugués)

| categoria | it: % es sin / con | it: acc sin / con | pt: % es sin / con | pt: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 75 | 75 / 88 | 0 / 44 | 81 / 88 |
| factual_aperturas | 0 / 94 | 81 / 62 | 0 / 88 | 81 / 69 |
| imperativo | 0 / 88 | 88 / 88 | 0 / 81 | 81 / 81 |
| imperativo_explicativo | 0 / 88 | 69 / 25 | 0 / 100 | 56 / 38 |
| explicativa | 0 / 100 | 31 / 31 | 0 / 81 | 56 / 44 |
| corta | 0 / 100 | 75 / 44 | 12 / 100 | 62 / 56 |
| conversacional | 0 / 94 | 88 / 69 | 0 / 94 | 81 / 69 |
| TOTAL | 0 / 91 | 72 / 58 | 2 / 84 | 71 / 63 |

## Celda de (parche hacia el alemán)

### Pregunta en inglés (norma ‖v‖ = 0.936)

| categoria | n | % de sin parche | % de control nativo | % de parche | acc sin parche | acc control nativo | acc parche | acuerdo parche/control |
|---|---|---|---|---|---|---|---|---|
| factual_clasica | 16 | 0 | 81 | 100 | 100 | 94 | 94 | 100 |
| factual_aperturas | 16 | 0 | 94 | 100 | 100 | 88 | 94 | 81 |
| imperativo | 16 | 0 | 100 | 94 | 94 | 81 | 81 | 88 |
| imperativo_explicativo | 16 | 0 | 100 | 100 | 100 | 62 | 75 | 50 |
| explicativa | 16 | 0 | 100 | 100 | 100 | 62 | 62 | 62 |
| corta | 16 | 0 | 94 | 100 | 88 | 69 | 69 | 88 |
| conversacional | 16 | 0 | 94 | 100 | 100 | 88 | 94 | 94 |
| TOTAL | 112 | 0 | 95 | 99 | 97 | 78 | 81 | 80 |

### Otros idiomas de entrenamiento

| categoria | es: % de sin / con | es: acc sin / con | fr: % de sin / con | fr: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 81 / 75 | 0 / 100 | 94 / 100 |
| factual_aperturas | 0 / 100 | 94 / 81 | 0 / 100 | 81 / 81 |
| imperativo | 0 / 81 | 75 / 75 | 0 / 100 | 81 / 88 |
| imperativo_explicativo | 0 / 100 | 44 / 38 | 0 / 100 | 62 / 19 |
| explicativa | 0 / 100 | 50 / 44 | 0 / 100 | 56 / 50 |
| corta | 0 / 100 | 69 / 75 | 0 / 100 | 69 / 75 |
| conversacional | 0 / 100 | 94 / 75 | 0 / 100 | 88 / 75 |
| TOTAL | 0 / 97 | 72 / 66 | 0 / 100 | 76 / 70 |

### Idiomas no vistos (italiano, portugués)

| categoria | it: % de sin / con | it: acc sin / con | pt: % de sin / con | pt: acc sin / con |
|---|---|---|---|---|
| factual_clasica | 0 / 100 | 75 / 69 | 0 / 81 | 81 / 75 |
| factual_aperturas | 0 / 94 | 81 / 75 | 0 / 88 | 81 / 75 |
| imperativo | 0 / 94 | 88 / 69 | 0 / 88 | 81 / 81 |
| imperativo_explicativo | 0 / 100 | 69 / 19 | 0 / 100 | 56 / 44 |
| explicativa | 0 / 100 | 31 / 44 | 0 / 100 | 56 / 44 |
| corta | 0 / 94 | 75 / 56 | 0 / 88 | 62 / 75 |
| conversacional | 0 / 100 | 88 / 69 | 0 / 81 | 81 / 62 |
| TOTAL | 0 / 97 | 72 / 57 | 0 / 89 | 71 / 65 |

