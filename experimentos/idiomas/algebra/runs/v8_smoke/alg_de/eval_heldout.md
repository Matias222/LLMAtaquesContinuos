# Eval parche de idioma (aleman)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8_smoke/alg_de/lang_patch_best_train.pt`
- Norma: 0.0871  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 150, 'regen_ref': True, 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'de', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = de | score de | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([aleman;q]) | 100.00% | 100.00% | 0.991 | 0.00% | 0.00% | 75.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (aleman) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.0615 | 4.9326 | -0.1289 |
| tail (el resto) | 0.4438 | 0.4277 | -0.0162 |
| toda la respuesta | 1.0513 | 1.0156 | -0.0356 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. | Die Geschwindigkeit des Lichts in Vakuum beträgt ungefähr 299.792 km/s. | The speed of light in a vacuum is approximately 299,792 kilometers per second. |
| 1 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. | Die Autoren des "Communistischen Manifests" (Kommunistisches Manifest) waren Karl Marx und Friedrich Engels. | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. It has a surface area of approximately 8,... | Der größte See in Südamerika ist der Titicaca-See. Er liegt auf der Grenze zwischen Peru und Bolivien und hat eine Fläche von etwa 8.372 Quadratkilome... | The largest lake in South America is Lake Titicaca, which is located on the border of Peru and Bolivia. It has a surface area of approximately 8,372 s... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | Die Bildung der Mond ist ein komplexes Thema, das Wissenschaftler seit Jahrhunderten beschäftigt. Hier ist eine Übersicht über die Theorien zur Bildun... | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... |
