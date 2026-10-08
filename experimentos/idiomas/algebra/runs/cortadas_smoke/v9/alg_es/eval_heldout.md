# Eval parche de idioma (espanol)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v9/alg_es/lang_patch_best_train.pt`
- Norma: 0.8632  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=2)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([espanol;q]) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| parche  M(q+v) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.6562 | 1.9131 | -3.7432 |
| tail (el resto) | 0.3728 | 0.2806 | -0.0922 |
| toda la respuesta | 0.6431 | 0.3646 | -0.2784 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | ¡Claro! La formación de la Luna es un tema fascinante que involucra la historia de nuestro sistema solar. A continuación, te explico cómo se cree que ... | La formación de la Luna es un tema complejo y aún no completamente entendido. A continuación, te presento una visión general de la teoría más aceptada... |
| 1 | How does the eye focus light? | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplified explanation: /  / **The Structure of... | La forma en que enfoca la luz el ojo es un proceso complejo que involucra varios componentes anatómicos y fisiológicos. A continuación, te explico los... | El ojo se enfoca la luz mediante un proceso llamado adaptación fisiológica. A continuación, te explico los pasos involucrados: /  / 1. **La luz entra ... |
