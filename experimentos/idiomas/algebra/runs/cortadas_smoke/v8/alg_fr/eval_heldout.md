# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8/alg_fr/lang_patch_best_train.pt`
- Norma: 0.8711  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'instruccion', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=2)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([frances;q]) | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% | 0.00% |
| parche  M(q+v) | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 4.8975 | 0.1212 | -4.7763 |
| tail (el resto) | 0.3308 | 0.2688 | -0.0620 |
| toda la respuesta | 0.4221 | 0.2659 | -0.1562 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voici une vue d'ensemble de la théorie la p... | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voici une vue d'ensemble de la théorie la p... |
| 1 | How does the eye focus light? | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplified explanation: /  / **The Structure of... | L'œil se concentre la lumière grâce à un système complexe de muscles et de structures anatomiques. Voici les étapes clés : /  / 1. La lumière pénètre ... | L'œil se concentre la lumière de la manière suivante : /  / L'œil est composé de plusieurs parties, notamment : /  / * Les iris, qui contrôlent la qua... |
