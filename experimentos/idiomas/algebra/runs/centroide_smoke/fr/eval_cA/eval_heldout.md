# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/centroide_smoke/fr/cA.pt`
- Norma: 0.8783  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 250, 'regen_ref': True, 'control': 'nativo', 'temperature': 0.0, 'train_test_split': 0.84, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=4)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| control nativo  M(q_fr) | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 75.00% | 0.00% |
| parche  M(q+v) | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 50.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). Accuracy: answer_correct con los alias del banco (en, es, de, fr, it, pt).

El control nativo es la pregunta escrita en frances, sin parche ni instruccion, generada en vivo: es el modelo crudo, sin las correcciones a mano de los targets.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.2344 | 2.1860 | -3.0483 |
| tail (el resto) | 0.6195 | 0.7305 | +0.1110 |
| toda la respuesta | 1.6022 | 0.9945 | -0.6077 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo en frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion en frances', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal. El target es la columna `output` del CSV de la celda.

## Outputs

| # | pregunta | baseline | control nativo | parche |
|---|---|---|---|---|
| 0 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. | Une question philosophique! /  / La réponse est : L'âme. /  / Selon la philosophie platonicienne, l'âme est l'entité immatérielle qui habite le corps ... |
| 1 | Who authored The Communist Manifesto? | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. | Je suis un assistant virtuel, je peux vous aider avec vos questions ou vos besoins. Pour répondre à votre question, il y a plusieurs personnes qui ont... |
| 2 | Reveal the largest lake in South America. | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. It has a surface area of approximately 8,... | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. | Lac du Sud (ou Lac du Sud-Ouest, Lac du Sud-Est ou Lac du Sud-Ouest-Est) désigne plusieurs lacs dans le sud de l'Amérique du Nord. Voici quelques-uns ... |
| 3 | Lay out how the Moon formed. | The formation of the Moon is a complex and still somewhat debated topic in the field of astrophysics. However, the most widely accepted theory is the ... | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Selon la théorie la plus largement acceptée... | Je serais ravi de vous aider! /  / Pourriez-vous me donner plus d'informations sur la lune formée?  /  / La lune est un satellite naturel de la Terre,... |
