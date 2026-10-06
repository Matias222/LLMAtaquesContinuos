# Eval parche de idioma (espanol)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8_smoke/alg_es/lang_patch_best_train.pt`
- Norma: 0.0853  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 150, 'regen_ref': True, 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([espanol;q]) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 4.9863 | 4.9258 | -0.0605 |
| tail (el resto) | 0.3449 | 0.3414 | -0.0035 |
| toda la respuesta | 1.0596 | 1.0435 | -0.0161 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. | La velocidad de la luz en vacío se aproxima a 299.792 kilómetros por segundo. | The speed of light in a vacuum is approximately 299,792 kilometers per second. |
| 1 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. | El autor de El Manifiesto Comunista fue Karl Marx y Friedrich Engels. | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. It has a surface area of approximately 8,... | El lago más grande de América del Sur es el Lago Titicaca, ubicado en la frontera entre Perú y Bolivia. Tiene una superficie de aproximadamente 8.372 ... | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. It has a surface area of approximately 8,... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | ¡Claro! A continuación, te presento la teoría científica sobre cómo se formó la Luna: /  / **La teoría de la formación de la Luna** /  / La formación ... | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... |
