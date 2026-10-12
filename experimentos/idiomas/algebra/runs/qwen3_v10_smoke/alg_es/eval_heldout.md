# Eval parche de idioma (espanol)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10_smoke/alg_es/lang_patch_best_train.pt`
- Norma: 0.0796  |  shape: [1, 1, 2560]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.082 | 0.00% | 0.00% | 100.00% | 0.00% |
| control nativo  M(q_es) | 100.00% | 100.00% | 0.999 | 0.00% | 0.00% | 100.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.083 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en espanol, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 8.3125 | 8.1250 | -0.1875 |
| tail (el resto) | 0.6191 | 0.6113 | -0.0078 |
| toda la respuesta | 0.9434 | 0.9287 | -0.0146 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en espanol correcto en cada paso, asi que el tail solo mide 'continuar una oracion en espanol', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest whole number, it is **300,000 kilometer... | La velocidad de la luz en el vacío es aproximadamente **299,792 kilómetros por segundo**. /  / Redondeada a un solo dígito significativo, sería **300 ... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest whole number, it is **300,000 kilometer... |
| 1 | Who authored The Communist Manifesto? | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 1848. | El **Manifiesto Comunista** fue escrito por **Karl Marx** y **Friedrich Engels**. /  / Fue publicado en 1848 y es uno de los textos más influyentes de... | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 1848. |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake Titicaca is the largest **lake** in Sout... | El lago más grande de Sudamérica es el **Lago Titicaca**. /  / Aunque a veces se confunde con el lago más grande en términos de superficie total, el *... | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake Titicaca is the largest **lake** in Sout... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely accepted theory is the **Giant Impact Hypot... | La formación de la Luna es un tema central en la ciencia planetaria, y la teoría más aceptada actualmente se conoce como la **teoría del impacto gigan... | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely accepted theory is the **Giant Impact Hypot... |
