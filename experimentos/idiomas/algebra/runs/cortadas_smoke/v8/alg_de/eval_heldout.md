# Eval parche de idioma (aleman)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8/alg_de/lang_patch_best_train.pt`
- Norma: 0.9638  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'instruccion', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'de', 'upper': False}`

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
| head (primeros 5 tokens) | 5.1328 | 0.5520 | -4.5808 |
| tail (el resto) | 0.3457 | 0.3503 | +0.0046 |
| toda la respuesta | 0.4415 | 0.3542 | -0.0873 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | Die Bildung der Mond ist ein komplexes Thema, das Wissenschaftler seit Jahrhunderten beschäftigt. Hier ist eine Übersicht über die Theorien zur Bildun... | Die Bildung der Erdschatten, auch bekannt als Mond, ist ein komplexer Prozess, der sich über mehrere Milliarden von Jahren erstreckt. Hier ist eine ve... |
| 1 | How does the eye focus light? | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplified explanation: /  / **The Structure of... | Die Augenfunktion ist ein komplexer Prozess. Die Augen können Licht durch eine Kombination von drei Hauptmechanismen fokussieren: /  / 1. **Kornerlins... | Das ist eine großartige Frage! /  / Die Augenfunktion, insbesondere die Fokussierung von Licht, ist ein komplexer Prozess, der mehrere Schritte umfass... |
