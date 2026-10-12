# Eval parche de idioma (aleman)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10_smoke/alg_de/lang_patch_best_train.pt`
- Norma: 0.0872  |  shape: [1, 1, 2560]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'de', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = de | score de | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |
| control nativo  M(q_de) | 75.00% | 75.00% | 0.874 | 0.00% | 0.00% | nan% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en aleman, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (aleman) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 7.5000 | 7.5547 | +0.0547 |
| tail (el resto) | 0.3079 | 0.3059 | -0.0020 |
| toda la respuesta | 1.0635 | 1.0640 | +0.0005 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en aleman correcto en cada paso, asi que el tail solo mide 'continuar una oracion en aleman', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

### Prompts abiertos (n=4, sin respuesta verificable)

| medida | valor |
|---|---|
| overlap de contenido parche vs control nativo | 0.278 |
| overlap baseline (EN) vs control nativo | 0.278 |
| control de azar (parche vs otra pregunta) | 0.000 |

| tercio de la respuesta | 1 | 2 | 3 |
|---|---|---|---|
| parche | 0.13 | 0.13 | 0.13 |
| control nativo | 0.87 | 0.80 | 0.87 |

El parche vive en todos los tokens de la pregunta del **prompt** (las filas de la tabla son el score de `de` por tercio). Si cae en el tercer tercio, el efecto es local y decae con la distancia; si se sostiene, el parche fija un modo que persiste toda la generacion.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the weather like? | I can't provide real-time weather information. To find out the current weather, I recommend checking a reliable weather website or app like Weather.co... | Leider kann ich aktuelles Wetter nicht direkt sehen oder abrufen. Du kannst das Wetter am besten über eine zuverlässige Wetterwebsite oder App wie **W... | I can't provide real-time weather information. To find out the current weather, I recommend checking a reliable weather website or app like Weather.co... |
| 1 | How do I sort a list in Python? | There are several ways to sort a list in Python. Here are the most common methods: /  / ## 1. Using `sort()` method (in-place sorting) /  / This modif... | In Python kannst du eine Liste auf verschiedene Weisen sortieren. Hier sind die wichtigsten Methoden: /  / --- /  / ### 1. **`sort()` – Sortiert die L... | There are several ways to sort a list in Python. Here are the most common methods: /  / ## 1. Using `sort()` method (in-place sorting) /  / This modif... |
| 2 | Tell me about machine learning | Sure! Let's dive into **machine learning** — one of the most exciting and transformative fields in modern technology. /  / --- /  / ### 🌟 What is Mach... | Natürlich! 😊   / Maschinelles Lernen (engl. *Machine Learning*) ist ein Teilbereich der Künstlichen Intelligenz (KI), der es Maschinen ermöglicht, aus... | Sure! Let's dive into **machine learning** — one of the most exciting and transformative fields in modern technology. /  / --- /  / ### 🌟 What is Mach... |
| 3 | What's 2 plus 2? | 2 plus 2 is 4. 😊 | 2 plus 2 ist **4**. 😊 | 2 plus 2 is 4. 😊 |
