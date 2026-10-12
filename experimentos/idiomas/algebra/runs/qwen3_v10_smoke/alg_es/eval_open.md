# Eval parche de idioma (espanol)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10_smoke/alg_es/lang_patch_best_train.pt`
- Norma: 0.0770  |  shape: [1, 1, 2560]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'es', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = es | score es | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.126 | 0.00% | 0.00% | nan% | 0.00% |
| control nativo  M(q_es) | 75.00% | 75.00% | 0.851 | 0.00% | 0.00% | nan% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.126 | 0.00% | 0.00% | nan% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en espanol, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (espanol) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 7.2422 | 7.1797 | -0.0625 |
| tail (el resto) | 0.5242 | 0.5330 | +0.0088 |
| toda la respuesta | 1.4126 | 1.4182 | +0.0056 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en espanol correcto en cada paso, asi que el tail solo mide 'continuar una oracion en espanol', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

### Prompts abiertos (n=4, sin respuesta verificable)

| medida | valor |
|---|---|
| overlap de contenido parche vs control nativo | 0.044 |
| overlap baseline (EN) vs control nativo | 0.044 |
| control de azar (parche vs otra pregunta) | 0.000 |

| tercio de la respuesta | 1 | 2 | 3 |
|---|---|---|---|
| parche | 0.13 | 0.13 | 0.13 |
| control nativo | 0.87 | 0.67 | 0.76 |

El parche vive en todos los tokens de la pregunta del **prompt** (las filas de la tabla son el score de `es` por tercio). Si cae en el tercer tercio, el efecto es local y decae con la distancia; si se sostiene, el parche fija un modo que persiste toda la generacion.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the weather like? | I can't provide real-time weather information. To find out the current weather, I recommend checking a reliable weather website or app like Weather.co... | No puedo acceder al clima en tiempo real. Para saber qué tiempo hace, te recomiendo consultar una aplicación de clima o un sitio web como: /  / - [wea... | I can't provide real-time weather information. To find out the current weather, I recommend checking a reliable weather website or app like Weather.co... |
| 1 | How do I sort a list in Python? | There are several ways to sort a list in Python. Here are the most common methods: /  / ## 1. Using `sort()` method (in-place sorting) /  / This modif... | En Python, puedes ordenar una lista de varias formas, dependiendo de si quieres ordenarla **de forma ascendente** (por defecto), **descendente**, o si... | There are several ways to sort a list in Python. Here are the most common methods: /  / ## 1. Using `sort()` method (in-place sorting) /  / This modif... |
| 2 | Tell me about machine learning | Sure! Let's dive into **machine learning** — one of the most exciting and transformative fields in modern technology. /  / --- /  / ### 🌟 What is Mach... | ¡Claro! El **aprendizaje automático** (también conocido como *machine learning* en inglés) es una rama del **inteligencia artificial** que permite a l... | Sure! Let's dive into **machine learning** — one of the most exciting and transformative fields in modern technology. /  / --- /  / ### 🌟 What is Mach... |
| 3 | What's 2 plus 2? | 2 plus 2 is 4. 😊 | 2 más 2 es **4**. 😊 | 2 plus 2 is 4. 😊 |
