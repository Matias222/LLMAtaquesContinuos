# Eval parche de idioma (frances)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr/lang_patch_best_train.pt`
- Norma: 0.8418  |  shape: [1, 1, 3072]
- Config: `{'num_patch_positions': 1, 'patch_offset': 0, 'patch_anchor': 'goal_all', 'scale': 1.0, 'num_tokens': 100, 'temperature': 0.0, 'train_test_split': 0.8, 'target_lang': 'fr', 'upper': False}`

## Metricas sobre held-out (n=5)

| condicion | **celda ok** (idioma y formato) | idioma = fr | score fr | mayusculas | is_french | accuracy | role leak |
|---|---|---|---|---|---|---|---|
| baseline  M(q) | 0.00% | 0.00% | 0.000 | 0.00% | 0.00% | 100.00% | 0.00% |
| referencia  M([frances;q]) | 100.00% | 100.00% | 0.933 | 0.00% | 100.00% | 100.00% | 0.00% |
| parche  M(q+v) | 100.00% | 100.00% | 0.925 | 0.00% | 100.00% | 100.00% | 0.00% |

`celda ok` exige el idioma target Y el formato (una celda normal NO puede salir en mayusculas). La accuracy en espanol/aleman esta subestimada: los alias son ingles y frances.

### CE del target (frances) (teacher forcing)

| tramo | sin parche | con parche | delta |
|---|---|---|---|
| head (primeros 5 tokens) | 5.7406 | 0.3494 | -5.3913 |
| tail (el resto) | 0.5057 | 0.2760 | -0.2297 |
| toda la respuesta | 1.9262 | 0.2979 | -1.6283 |

La decision de idioma vive en el **head**. Como esto se mide con teacher forcing, el modelo ve el prefijo frances correcto en cada paso, asi que el tail solo mide 'continuar una oracion francesa', que es facil y casi no deberia moverse. Promediar sobre toda la respuesta diluye la señal.

## Outputs

| # | pregunta | baseline | referencia | parche |
|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). | La capitale d'Ukraine est Kiev (ou Chykhiv en ukrainien). | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). |
| 1 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational force of attraction between the Sun and t... | C'est la gravité. La gravité est une force qui attire les objets massifs l'un vers l'autre, et elle est responsable de l'orbite des planètes autour du... | C'est la gravité! La gravité est la force qui maintient les planètes dans leur orbite autour du Soleil. La gravité est une force de attraction entre d... |
| 2 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first published in 1952 and is considered one of... | C'est Ernest Hemingway qui a écrit "L'Homme qui chasse les poissons" (The Old Man and the Sea). | C'est Ernest Hemingway qui a écrit "L'Homme âgé et la Mer" (The Old Man and the Sea en anglais). |
| 3 | What is the capital of Syria? | The capital of Syria is Damascus. | La capitale de Syrie est Damas. | La capitale de Syrie est Damas. |
| 4 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on December 17, 1903. They made four flights t... | Les frères Wright ont effectué leur premier vol en 1903. | Les frères Wright ont effectué leur premier vol le 17 décembre 1903. |
