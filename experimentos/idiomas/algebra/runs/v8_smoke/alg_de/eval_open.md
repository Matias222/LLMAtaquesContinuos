# Eval parche de idioma (aleman)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8_smoke/alg_de/lang_patch_best_train.pt`
- Norma: 0.0871  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 150, 'regen_ref': True, 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'de', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = de | score de | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |
| referencia  M([aleman;q]) | 100.00% | 100.00% | 0.994 | 0.00% | 0.00% | nan% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (aleman) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.1611 | 5.1577 | -0.0034 |
| tail (el resto) | 0.5142 | 0.4967 | -0.0175 |
| toda la respuesta | 0.9570 | 0.9428 | -0.0142 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

### Prompts abiertos (n=4, sin respuesta verificable)

| medida | valor |
|---|---|
| overlap de contenido parche vs referencia | 0.034 |
| overlap baseline (EN) vs referencia | 0.034 |
| control de azar (parche vs otra pregunta) | 0.000 |

| tercio de la respuesta | 1 | 2 | 3 |
|---|---|---|---|
| parche | 0.13 | 0.13 | 0.13 |
| referencia | 1.00 | 0.95 | 0.93 |

El parche vive en todos los tokens de la pregunta del **prompt** (las filas de la tabla son el score de `de` por tercio). Si cae en el tercer tercio, el efecto es local y decae con la distancia; si se sostiene, el parche fija un modo que persiste toda la generacion.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the weather like? | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... | Leider kann ich keine aktuelle Wettervorhersage abrufen. Ich kann jedoch einige allgemeine Informationen über das Wetter geben. /  / Wenn du nach der ... | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... |
| 1 | How do I sort a list in Python? | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... | Um eine Liste in Python zu sortieren, kannst du die `sort()`-Methode verwenden. Hier sind einige Beispiele: /  / ```python / # Sortiere eine Liste in ... | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... |
| 2 | Tell me about machine learning | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... | Maschinelles Lernen (Machine Learning) ist ein Teilgebiet der künstlichen Intelligenz (KI), das sich mit der Entwicklung von Algorithmen beschäftigt, ... | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... |
| 3 | What's 2 plus 2? | 2 + 2 = 4 | Das ist einfach! 2 plus 2 ist gleich 4. | 2 + 2 = 4 |
