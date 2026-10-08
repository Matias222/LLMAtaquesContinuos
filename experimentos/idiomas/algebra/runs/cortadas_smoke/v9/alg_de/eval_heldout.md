# Eval parche de idioma (aleman)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v9/alg_de/lang_patch_best_train.pt`
- Norma: 0.9419  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'de', 'upper': False}`

## Metricas sobre held-out (n=2)

| condicion | **celda ok** (idioma y formato) | idioma = de | score de | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([aleman;q]) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| parche  M(q+v) | 100.00% | 100.00% | 1.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (aleman) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.1348 | 0.5220 | -4.6128 |
| tail (el resto) | 0.4695 | 0.4723 | +0.0028 |
| toda la respuesta | 0.7029 | 0.4747 | -0.2281 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | Ein interessantes Thema! /  / Die Entstehung des Mondes ist ein komplexes Phänomen, das Wissenschaftler und Astronomen seit Jahrhunderten beschäftigt.... | Eine großartige Frage! /  / Die Entstehung der Mond ist ein faszinierendes Thema, das Wissenschaftler und Astronomen seit Jahrhunderten beschäftigt. E... |
| 1 | How does the eye focus light? | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplified explanation: /  / **The Structure of... | Das Auge bündelt Licht, indem es es durch eine komplexe Anordnung von Strukturen und -materialien verarbeitet. Hier ist eine vereinfachte Erklärung, w... | Das Auge konzentriert Licht, indem es die Lichtstrahlen durch eine Veränderung der Form des Glaskorpers (Kornea) und des Linse- inneren Teils (Kristal... |
