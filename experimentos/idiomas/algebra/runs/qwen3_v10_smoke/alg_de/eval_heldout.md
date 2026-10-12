# Eval parche de idioma (aleman)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10_smoke/alg_de/lang_patch_best_train.pt`
- Norma: 0.0840  |  shape: [1, 1, 2560]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'de', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = de | score de | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| control nativo  M(q_de) | 100.00% | 100.00% | 0.997 | 0.00% | 0.00% | 100.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en aleman, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (aleman) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 7.6875 | 7.4922 | -0.1953 |
| tail (el resto) | 0.3462 | 0.3394 | -0.0068 |
| toda la respuesta | 0.6333 | 0.6211 | -0.0122 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en aleman correcto en cada paso, asi que el tail solo mide 'continuar una oracion en aleman', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest whole number, it is **300,000 kilometer... | Die Geschwindigkeit des Lichts im Vakuum beträgt genau **299.792.458 Meter pro Sekunde**. /  / Wenn man das in Kilometern pro Sekunde umrechnet, ergib... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest whole number, it is **300,000 kilometer... |
| 1 | Who authored The Communist Manifesto? | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 1848. | Das *Kommunistische Manifest* wurde von **Karl Marx** und **Friedrich Engels** verfasst. Es wurde 1848 veröffentlicht und gilt als ein grundlegendes D... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake Titicaca is the largest **lake** in Sout... | Der größte See Südamerikas ist der **Titicaca-See**. /  / Er liegt auf der Grenze zwischen **Bolivien** und **Peru** und ist der **größte See in Südam... | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake Titicaca is the largest **lake** in Sout... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely accepted theory is the **Giant Impact Hypot... | Natürlich! Hier ist eine einfache und verständliche Erklärung, **wie der Mond entstand** – in deutscher Sprache: /  / --- /  / ### **Wie entstand der ... | The formation of the Moon is one of the most well-studied topics in planetary science, and the most widely accepted theory is the **Giant Impact Hypot... |
