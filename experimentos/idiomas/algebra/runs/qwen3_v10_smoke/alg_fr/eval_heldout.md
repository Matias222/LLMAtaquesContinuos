# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10_smoke/alg_fr/lang_patch_best_train.pt`
- Norma: 0.0858  |  shape: [1, 1, 2560]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| control nativo  M(q_fr) | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en frances, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 8.1406 | 7.8750 | -0.2656 |
| tail (el resto) | 0.7744 | 0.7832 | +0.0088 |
| toda la respuesta | 1.0811 | 1.0820 | +0.0010 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion en frances', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest whole number, it is **300,000 kilometer... | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plus proche centaine, cela donne **300 000 ... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest whole number, it is **300,000 kilometer... |
| 1 | Who authored The Communist Manifesto? | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 1848. | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été publié en 1848 et constitue l'un des textes... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake Titicaca is the largest **lake** in Sout... | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **le lac Parana** n’est pas le plus grand ... | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake Titicaca is the largest **lake** in Sout... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely accepted theory is the **Giant Impact Hypot... | La formation de la Lune est un sujet scientifique bien étudié, et la théorie la plus largement acceptée aujourd’hui est la **théorie de l'impact géant... | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely accepted theory is the **Giant Impact Hypot... |
