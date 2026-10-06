# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v8_smoke/alg_fr/lang_patch_best_train.pt`
- Norma: 0.0946  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 150, 'regen_ref': True, 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |
| referencia  M([frances;q]) | 100.00% | 100.00% | 0.940 | 0.00% | 100.00% | nan% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 6.3218 | 6.1626 | -0.1592 |
| tail (el resto) | 0.4716 | 0.4602 | -0.0115 |
| toda la respuesta | 1.3843 | 1.3588 | -0.0255 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

### Prompts abiertos (n=4, sin respuesta verificable)

| medida | valor |
|---|---|
| overlap de contenido parche vs referencia | 0.036 |
| overlap baseline (EN) vs referencia | 0.036 |
| control de azar (parche vs otra pregunta) | 0.000 |

| tercio de la respuesta | 1 | 2 | 3 |
|---|---|---|---|
| parche | 0.13 | 0.13 | 0.13 |
| referencia | 1.00 | 0.75 | 0.76 |

El parche vive en todos los tokens de la pregunta del **prompt** (las filas de la tabla son el score de `fr` por tercio). Si cae en el tercer tercio, el efecto es local y decae con la distancia; si se sostiene, el parche fija un modo que persiste toda la generacion.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the weather like? | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... | Le temps est actuellement ensoleillé et doux, avec des températures moyennes de 22 degrés. Il y a un peu de vent léger, mais il est agréable de sortir... | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... |
| 1 | How do I sort a list in Python? | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... | Pour trier une liste en Python, vous pouvez utiliser la méthode `sort()` ou la fonction `sorted()`. Voici les deux exemples : /  / **Tri en place (sor... | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... |
| 2 | Tell me about machine learning | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... | La machine learning! C'est un domaine fascinant qui permet aux ordinateurs de s'apprendre et d'améliorer leurs performances sans être explicitement pr... | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... |
| 3 | What's 2 plus 2? | 2 + 2 = 4 | C'est facile! Deux plus deux équivaut à quatre. | 2 + 2 = 4 |
