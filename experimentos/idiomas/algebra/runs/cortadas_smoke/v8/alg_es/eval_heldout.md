# Eval parche de idioma (espanol)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8/alg_es/lang_patch_best_train.pt`
- Norma: 0.9007  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'instruccion', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=2)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([espanol;q]) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| parche  M(q+v) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 50.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.5449 | 1.1719 | -4.3730 |
| tail (el resto) | 0.4167 | 0.2950 | -0.1217 |
| toda la respuesta | 0.5847 | 0.3275 | -0.2572 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | ¡Claro! A continuación, te presento la teoría científica sobre cómo se formó la Luna: /  / **La teoría de la formación de la Luna** /  / La formación ... | Aquí te explico cómo se formó la Luna: /  / **Teoría de la formación de la Luna** /  / La formación de la Luna se cree que ocurrió hace aproximadament... |
| 1 | How does the eye focus light? | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplified explanation: /  / **The Structure of... | La lente del ojo se curva para enfocar la luz. La lente del ojo es una estructura flexible que se encuentra en la parte posterior del ojo y se curva p... | El ojo humano utiliza un mecanismo complejo para enfocar la luz en la retina. A continuación, te explico los pasos clave: /  / 1. **La luz entra en el... |
