# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/qwen3_v10/pos_smoke/pos_q3_fr/lang_patch_best_train.pt`
- Norma: 0.1135  |  shape: [1, 3, 2560]
- Config: `{'num_patch_positions': 3, 'patch_offset': 0, 'patch_anchor': 'goal', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.0, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |
| control nativo  M(q_fr) | 75.00% | 75.00% | 0.868 | 0.00% | 75.00% | nan% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.125 | 0.00% | 0.00% | nan% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en frances, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 7.9609 | 7.7734 | -0.1875 |
| tail (el resto) | 0.3030 | 0.3064 | +0.0034 |
| toda la respuesta | 1.4004 | 1.3979 | -0.0024 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion en frances', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

### Prompts abiertos (n=4, sin respuesta verificable)

| medida | valor |
|---|---|
| overlap de contenido parche vs control nativo | 0.166 |
| overlap baseline (EN) vs control nativo | 0.166 |
| control de azar (parche vs otra pregunta) | 0.000 |

| tercio de la respuesta | 1 | 2 | 3 |
|---|---|---|---|
| parche | 0.13 | 0.13 | 0.13 |
| control nativo | 0.87 | 0.84 | 0.84 |

El parche vive en 3 posiciones del **prompt** (las filas de la tabla son el score de `fr` por tercio). Si cae en el tercer tercio, el efecto es local y decae con la distancia; si se sostiene, el parche fija un modo que persiste toda la generacion.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the weather like? | I can't provide real-time weather information. To find out the current weather, I recommend checking a reliable weather website or app like Weather.co... | Je ne peux pas accéder en temps réel aux conditions météorologiques. Pour savoir quel temps il fait, je te conseille de consulter une application mété... | I can't provide real-time weather information. To find out the current weather, I recommend checking a reliable weather website or app like Weather.co... |
| 1 | How do I sort a list in Python? | There are several ways to sort a list in Python. Here are the most common methods: /  / ## 1. Using `sort()` method (in-place sorting) /  / This modif... | En Python, il existe plusieurs façons de **trier une liste**. Voici les méthodes les plus courantes et efficaces : /  / --- /  / ### 1. **Méthode `sor... | There are several ways to sort a list in Python. Here are the most common methods: /  / ## 1. Using `sort()` method (in-place sorting) /  / This modif... |
| 2 | Tell me about machine learning | Sure! Let's dive into **machine learning** — one of the most exciting and transformative fields in modern technology. /  / --- /  / ### 🌟 What is Mach... | Bien sûr ! 😊   / L’**apprentissage automatique** (ou *machine learning* en anglais) est une branche de l’intelligence artificielle qui permet aux ordi... | Sure! Let's dive into **machine learning** — one of the most exciting and transformative fields in modern technology. /  / --- /  / ### 🌟 What is Mach... |
| 3 | What's 2 plus 2? | 2 plus 2 is 4. 😊 | 2 plus 2 font **4**. 😊 | 2 plus 2 is 4. 😊 |
