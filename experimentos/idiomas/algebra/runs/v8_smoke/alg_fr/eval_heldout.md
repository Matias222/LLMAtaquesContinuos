# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8_smoke/alg_fr/lang_patch_best_train.pt`
- Norma: 0.0946  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 150, 'regen_ref': True, 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([frances;q]) | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.2368 | 5.1230 | -0.1138 |
| tail (el resto) | 0.4819 | 0.4742 | -0.0078 |
| toda la respuesta | 1.5574 | 1.5202 | -0.0372 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. | The speed of light in a vacuum is approximately 299,792 kilometers per second. |
| 1 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. | Le manifeste communiste a été écrit par Karl Marx et Friedrich Engels. | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. It has a surface area of approximately 8,... | Le plus grand lac d'Amérique du Sud est le lac Titicaca. | The largest lake in South America is Lake Titicaca, which is located on the border of Peru and Bolivia. It has a surface area of approximately 8,372 s... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voici une vue d'ensemble de la théorie la p... | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... |
