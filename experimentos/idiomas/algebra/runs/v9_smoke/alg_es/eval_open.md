# Eval parche de idioma (espanol)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v9_smoke/alg_es/lang_patch_best_train.pt`
- Norma: 0.0853  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 150, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |
| referencia  M([espanol;q]) | 100.00% | 100.00% | 0.999 | 0.00% | 0.00% | nan% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 6.7334 | 6.6865 | -0.0469 |
| tail (el resto) | 0.5285 | 0.5055 | -0.0230 |
| toda la respuesta | 1.5692 | 1.5513 | -0.0179 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

### Prompts abiertos (n=4, sin respuesta verificable)

| medida | valor |
|---|---|
| overlap de contenido parche vs referencia | 0.031 |
| overlap baseline (EN) vs referencia | 0.031 |
| control de azar (parche vs otra pregunta) | 0.000 |

| tercio de la respuesta | 1 | 2 | 3 |
|---|---|---|---|
| parche | 0.13 | 0.13 | 0.13 |
| referencia | 1.00 | 0.99 | 1.00 |

El parche vive en todos los tokens de la pregunta del **prompt** (las filas de la tabla son el score de `es` por tercio). Si cae en el tercer tercio, el efecto es local y decae con la distancia; si se sostiene, el parche fija un modo que persiste toda la generacion.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the weather like? | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... | Lo siento, pero no tengo acceso a información en tiempo real. Sin embargo, puedo decirte que puedo proporcionarte información sobre el clima general d... | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... |
| 1 | How do I sort a list in Python? | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... | En Python, puedes ordenar una lista de varias maneras. Aquí te presento algunas de las formas más comunes: /  / **1. Usando la función `sort()`** /  /... | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... |
| 2 | Tell me about machine learning | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... | ¡Claro! El aprendizaje automático (también conocido como aprendizaje profundo o inteligencia artificial) es un campo de la informática que se enfoca e... | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... |
| 3 | What's 2 plus 2? | 2 + 2 = 4 | La respuesta es 4. | 2 + 2 = 4 |
