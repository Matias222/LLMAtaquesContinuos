# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/v10_smoke/alg_fr/lang_patch_best_train.pt`
- Norma: 0.0977  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |
| control nativo  M(q_fr) | 75.00% | 75.00% | 0.874 | 0.00% | 75.00% | nan% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en frances, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 3.8327 | 3.7003 | -0.1325 |
| tail (el resto) | 0.1831 | 0.1830 | -0.0002 |
| toda la respuesta | 0.2832 | 0.2785 | -0.0047 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion en frances', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

### Prompts abiertos (n=4, sin respuesta verificable)

| medida | valor |
|---|---|
| overlap de contenido parche vs control nativo | 0.050 |
| overlap baseline (EN) vs control nativo | 0.050 |
| control de azar (parche vs otra pregunta) | 0.000 |

| tercio de la respuesta | 1 | 2 | 3 |
|---|---|---|---|
| parche | 0.13 | 0.13 | 0.13 |
| control nativo | 0.87 | 0.85 | 0.87 |

El parche vive en todos los tokens de la pregunta del **prompt** (las filas de la tabla son el score de `fr` por tercio). Si cae en el tercer tercio, el efecto es local y decae con la distancia; si se sostiene, el parche fija un modo que persiste toda la generacion.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the weather like? | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... | Je suis désolé, mais je ne suis pas en mesure de vous fournir la météo actuelle ou prévue pour votre emplacement spécifique. Cependant, je peux vous s... | I'd be happy to help you with the weather. However, I'm a large language model, I don't have real-time access to current weather conditions. But I can... |
| 1 | How do I sort a list in Python? | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... | En Python, vous pouvez trier une liste en utilisant plusieurs méthodes. Voici quelques-unes des plus courantes : /  / ### 1. Tri par ordre aléatoire /... | Sorting a list in Python can be done in several ways, depending on the type of sort you want to perform and the version of Python you're using. Here a... |
| 2 | Tell me about machine learning | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... | L'apprentissage automatique (ou machine learning en anglais) est une branche de l'intelligence artificielle qui consiste à développer des algorithmes ... | Machine learning! It's a fascinating field that has revolutionized the way we approach complex problems in various industries. Here's a comprehensive ... |
| 3 | What's 2 plus 2? | 2 + 2 = 4 | 2 + 2 = 4 | 2 + 2 = 4 |
