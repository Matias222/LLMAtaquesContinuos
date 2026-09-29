# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/paper_v7/_preflight/q3/lang_patch_best_train.pt`
- Norma: 0.0546  |  shape: [1, 3, 3072]
- Config: `{'num_patch_positions': 3, 'patch_offset': 0, 'patch_anchor': 'goal', 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=2)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([frances;q]) | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% | 0.00% |
| parche  M(q+v) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 6.2520 | 6.2559 | +0.0039 |
| tail (el resto) | 0.5491 | 0.5494 | +0.0004 |
| toda la respuesta | 1.5684 | 1.5693 | +0.0010 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). | La capitale d'Ukraine est Kiev (ou Chykhiv en ukrainien). | The capital of Ukraine is Kyiv (also known as Kiev). |
| 1 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... | C'est la gravité. La gravité est une force qui attire les objets massifs l'un vers l'autre, et elle est responsable de l'orbite des planètes autour du... | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... |
