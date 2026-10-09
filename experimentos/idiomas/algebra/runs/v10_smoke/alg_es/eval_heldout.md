# Eval parche de idioma (espanol)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v10_smoke/alg_es/lang_patch_best_train.pt`
- Norma: 0.0916  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| control nativo  M(q_es) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 75.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en espanol, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 4.6533 | 4.6094 | -0.0439 |
| tail (el resto) | 0.7751 | 0.7662 | -0.0089 |
| toda la respuesta | 1.2107 | 1.1952 | -0.0155 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en espanol correcto en cada paso, asi que el tail solo mide 'continuar una oracion en espanol', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. | La velocidad de la luz en vacío es de aproximadamente 299.792 kilómetros por segundo. | The speed of light in a vacuum is approximately 299,792 kilometers per second. |
| 1 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. | El Manifiesto comunista fue escrito por Karl Marx y Friedrich Engels. Fue publicado por primera vez en 1848 en París, Francia, y es considerado uno de... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. It has a surface area of approximately 8,... | El lago más grande de Sudamérica es el Lago Argentino, ubicado en la provincia de Santa Cruz, Argentina. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. It has a surface area of approximately 8,... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | ¡Claro! La formación de la Luna es un tema fascinante que involucra la historia de nuestro sistema solar. A continuación, te explico cómo se cree que ... | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... |
