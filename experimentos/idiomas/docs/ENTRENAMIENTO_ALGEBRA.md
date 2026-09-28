# Entrenamiento de los parches de álgebra (idioma × formato)

Cómo se entrenaron las seis direcciones `alg_<celda>` y sus dos réplicas:
datos, parametrización, loss, optimizador, hiperparámetros, criterio de
checkpoint y el porqué de cada decisión. Escrito el 2026-09-28; los
entrenamientos son del 2026-09-18.

Este documento cubre **solo el entrenamiento**. Los resultados de
comportamiento, la geometría y el álgebra en sí están en
[`PARCHE_GOAL_ALL.md`](PARCHE_GOAL_ALL.md). Todos los números de acá salen de
`algebra/runs/alg_*/train.log` y de los logs de `algebra/targets/`.

Sin LaTeX: la notación va en bloques de código.

| archivo | rol |
|---|---|
| `algebra/run_algebra_v6.sh` | orquestador: targets → train → eval → plot → geom |
| `train_lang_patch.py` | el trainer (loss, sign-SGD, validación, checkpoints) |
| `lm.py` | carga del modelo, template, `patch_positions`, `apply_patch_first_n` |
| `algebra/generate_targets_attr.py` | targets de teacher forcing por celda |
| `algebra/fix_targets.py` | correcciones a mano de los targets |
| `algebra/check_targets.py` | validación de los 18 CSV antes de entrenar |

---

## 1. Qué se entrena

Seis parches independientes, uno por celda del cuadrado idioma × formato, más
dos réplicas para medir el ruido:

```
              normal     MAYÚSCULAS
      fr      alg_fr     alg_fr_up
      es      alg_es     alg_es_up
      de      alg_de     alg_de_up

réplicas:  alg_fr_s1, alg_es_up_s1   (mismo todo, otro orden de batches)
```

Cada parche es **un único vector** que, sumado a la pregunta del usuario, hace
que el modelo conteste en el idioma (y formato) de su celda. Se entrenan por
separado, sin verse entre sí, para después probar si componen como function
vectors (`v*_fr_up = v_fr + v_es_up − v_es`).

Ninguna celda es el baseline (inglés normal). Así, en un paralelogramo el
componente común a todos los parches entra dos veces y sale una.

---

## 2. Modelo y setup

| | |
|---|---|
| modelo | `Llama-3.2-3B-Instruct`, fp16, en modo `eval()` |
| dimensión del embedding | 3072 |
| tokenizer | `use_fast=False`, `pad_token = eos_token`, padding a la izquierda |
| template | `llama-3.2` de `llm_attacks` (`Llama32ConversationTemplate`) |
| system prompt | `You are a helpful assistant` (fijo, viene del template) |
| pesos del modelo | **congelados** (`requires_grad_(False)` en todos) |
| parámetros entrenables | 3072 (el parche) |

Congelar los pesos no cambia el resultado, solo el costo: sin eso `backward()`
calcula y guarda el gradiente de los 3B parámetros en cada paso para tirarlo.

El prompt completo que ve el modelo:

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n
You are a helpful assistant<|eot_id|>
<|start_header_id|>user<|end_header_id|>\n\n
{pregunta}                                   <- goal slice: acá cae el parche
<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n
{target}                                     <- teacher forcing: acá se mide la CE
```

---

## 3. Parametrización: `goal_all`

```
e'_i = e_i + v        para todo token i de la pregunta del usuario
v ∈ R^3072            shape [1, 1, 3072], se suma por broadcast
```

- Se suma en el **espacio de embeddings de entrada** (salida de
  `embed_tokens`), no en el residual stream de una capa intermedia.
- Cae **solo** sobre el goal slice: no toca el system, los headers ni
  `<|eot_id|>`. El `train.log` lo verifica imprimiendo los tokens parcheados
  del primer prompt de cada columna, con el token anterior y el siguiente:

  ```
  [prompt] parche sobre 15..24 (10 tokens) = ['On', ' which', ' continent', ..., ' located', '?']
        antes: ['<|end_header_id|>', '\n\n']   despues: ['<|eot_id|>', '<|start_header_id|>']
  ```
- Es una **suma, no un promedio**: la perturbación total es
  `(largo de la pregunta) × v`. En train el goal mide 11.2–11.8 tokens de
  media (mínimo 5, máximo 26–28).
- `--patch_anchor goal_all` exige `--num_patch_positions 1`; el trainer aborta
  si no.

### Por qué esta parametrización

El objetivo del proyecto es encontrar **direcciones**, no soft prompts. Las
dos parametrizaciones anteriores no lo son:

| formato | parámetros | por qué no es una dirección |
|---|---|---|
| 3 primeros tokens del goal (`v4_250`, `v5_head_multi`) | 9216 | tres vectores distintos atados a posición y a los tokens sobre los que caen; solo funciona con las aperturas e idiomas que vio (it/pt 0.18 / 0.02, open_2 0.04) |
| 3 últimos tokens del header del assistant (`v5_header_head_multi`) | 9216 | esos tokens son constantes, así que `e_const + v` equivale a aprender embeddings libres: es prompt compression, aunque generalice |
| **`goal_all`** | **3072** | el mismo `v` cae sobre tokens variables, no puede apoyarse en la posición ni en el token |

Además es la única de las tres que se deja **restar** (`q_fr − v_fr` saca del
francés; el parche de 3 posiciones no se invierte), y el álgebra necesita
sumar y restar vectores del mismo espacio.

---

## 4. Datos

### 4.1 Banco y split

- Base: `attributes/french/targets_french_v5.csv`, 250 preguntas factuales
  (el banco v5: las 29 preguntas de matemática de v4 reemplazadas en
  posición).
- **Split posicional 0.80**: filas 0–199 train, 200–249 held-out. Nunca se
  reordena ni se elimina una fila.
- **Las seis celdas salen del mismo CSV base**, así que comparten filas, orden
  y held-out por construcción. Es requisito del álgebra: se comparan parches
  entrenados sobre las mismas preguntas y se evalúan sobre las mismas 50.
- Sets de evaluación abiertos (nunca entran a train): open 1 (99 prompts de
  navidad) y open 2 (50 imperativos).

### 4.2 Targets

El target de cada fila es lo que el propio modelo contesta cuando la
instrucción va en texto:

```
y_i = M("Answer in {French|Spanish|German}.\n\n" + q_i)
      greedy (temperature 0), hasta 100 tokens, cortado en <|eot_id|>
```

El CSV guarda `prompt = q_i` **sin** la instrucción: el parche tiene que
reemplazarla, no acompañarla.

| celda | de dónde sale `output` |
|---|---|
| `fr` | `targets_french_v5.csv` tal cual, sin regenerar |
| `es`, `de` | `generate_targets_attr.py --lang es/de` sobre el CSV base |
| `fr_up`, `es_up`, `de_up` | `upper()` del `output` de su celda normal (`--upper_from`) |

**Decisión: las celdas `_up` no se generan, se derivan.** La primera versión
generaba con la instrucción conjunta (`Respond entirely in uppercase letters,
in Spanish.`) y los targets salieron mal: el modelo alucina en ese modo. Con
`upper()`, entre una celda y su `_up` cambia **solo** el formato, que es lo que
el paralelogramo asume. El precio: la "referencia" del eval de esas celdas es
un texto transformado y no una generación del modelo. `UP_FROM_TARGET=0`
recupera el comportamiento viejo.

### 4.3 Gate de calidad

Una fila entra a train solo si `passed_gate = True`:

- el `output` **no está positivamente en otro idioma** (criterio relajado: un
  `18 × 5 = 90` sin palabras no se tira), y
- el formato coincide con la celda (`_up` en mayúsculas, normal no).

La accuracy se mide y se guarda pero **no filtra** por defecto: los alias del
banco eran inglés + francés (`Atenas` daba falso negativo) y los símbolos
químicos fallan sobre texto en mayúsculas. `--gate_accuracy` lo activa.

El gate filtra **solo train**. El held-out se evalúa entero.

| celda | gate al generar | gate tras `fix_targets.py` | filas de train |
|---|---|---|---|
| fr | — | 249/250 | **199** |
| es | 246/250 | 250/250 | 200 |
| de | 249/250 | 250/250 | 200 |
| fr_up, es_up, de_up | 250/250 | (no se tocan) | 200 |

`fr` entrena con 199 filas y el resto con 200. El CSV de francés viene de
`generate_targets.py`, cuyo gate **sí** exige accuracy, y rechaza la fila 77
(`Who composed The Nutcracker?` → "Pierre Chaikovski", que no matchea ningún
alias). `fr_up` parte del mismo texto pero tiene 200, porque su gate se
recalcula con el criterio de esta tanda, que no filtra por accuracy. O sea
que las seis celdas **no entrenan sobre exactamente las mismas filas**: `fr`
y `fr_s1` tienen una menos.

### 4.4 Correcciones a mano (`fix_targets.py`)

Indexadas por la pregunta en inglés (no por número de fila), idempotentes:

- **33 outputs** de es/de: alucinaciones (Gobi por Antártida, Estambul por
  Ankara, Proxima Centauri por el Sol), títulos inventados, y español correcto
  que el detector clasificaba como otro idioma.
- **Alias en español y alemán** para 56 preguntas.
- **21 traducciones al francés** de open_2 (3 eran el ejemplo del few-shot
  copiado: `Quelle est la capitale du Japon?`).

Como el loss solo mira los primeros 8 tokens, una alucinación en el target
casi no envenena el parche; se corrigen porque el `output` también es la
**referencia del eval** y el texto contra el que se mide la CE.

El orden importa: celdas normales → `fix_targets.py` → celdas `_up` (que salen
de las normales ya corregidas). `check_targets.py` valida los 18 CSV y tiene
que decir `LISTO` antes de entrenar.

### 4.5 Entradas: multi-idioma, sin el idioma target

Cada fila entra una vez por idioma de entrada, siempre hacia el **mismo**
target:

```
fr, fr_up   prompt (en), prompt_es, prompt_de
es, es_up   prompt (en), prompt_de, prompt_fr
de, de_up   prompt (en), prompt_es, prompt_fr
```

- **Por qué multi-idioma:** un parche entrenado solo desde inglés se apoya en
  "la entrada está en inglés" y no transfiere (sección 8, `v5_base`: 0.00 de
  francés desde español o alemán).
- **Por qué sin el idioma target:** una pregunta en español ya se contesta en
  español sin parche. Para `v_es` esas filas no aportan gradiente de idioma, y
  la celda quedaría entrenada con 2 entradas útiles contra 3 de `v_fr`.
- Las traducciones tienen su propio gate (`prompt_<lang>_ok`); una fila con la
  traducción rechazada se saltea **solo para esa columna**. En la práctica
  falta una sola: `prompt_de` en 1 fila.

Ejemplos de entrenamiento por celda: ~200 filas × 3 entradas ≈ 600.

---

## 5. Loss

```
L(v) = CE( logits(q + v)[0:8], y[0:8] ) + lambda * ||v||^2

CE      cross-entropy media sobre los primeros 8 tokens del target, con
        teacher forcing (el modelo ve el prefijo correcto en cada paso)
lambda  0.075
```

Sin objetivo de prefijo, sin bot penalty, sin término de coherencia aparte.

### Por qué solo los primeros 8 tokens (`--loss_head_k 8`)

Con teacher forcing el costo de **cambiar** de idioma se paga una sola vez, en
los primeros tokens; después, "continuá esta oración en francés" es trivial
para el modelo. La decisión vive en 2–3 tokens de ~20, así que promediar sobre
toda la respuesta diluye la señal ~7×.

Y la cola es donde el target enseña la **forma** de la respuesta (una oración
corta y punto), que es un estilo que no queremos que el parche absorba.

Targets más cortos que 8 tokens usan los que tengan.

---

## 6. Optimizador

**sign-SGD** con annealing coseno del paso, heredado de `legacy/`:

```
v <- v - lr_t * sign( grad_v L )

lr_t = 0.00025 * 0.5 * (1 + cos(pi * t / (T - 1)))     T = 1400 pasos
```

### 6.1 El loop

```
v = 0                                          # init en ceros
para cada epoch (10):
  para cada batch de 32 filas (7 por epoch):
    items = [(fila, columna) para fila en batch, columna en entradas]   # ~96
    precomputar embeddings de cada item (una sola vez)
    repetir 20 veces:
      para cada item:
        L_item = CE_head8(q + v, y) + lambda * ||v||^2
        (L_item / len(items)).backward()       # acumula gradiente
      v <- v - lr_t * sign(v.grad)             # UN paso con el gradiente promedio
      v.grad = 0;  t += 1
  validar el checkpoint de la epoch (sección 7)
```

- Un forward + backward **por item**, sin batch tensorial: el "batch" es
  acumulación de gradiente. Como cada item divide por `len(items)`, el paso
  usa la CE promedio y el L2 con su peso completo.
- Pasos totales: `10 epochs × 7 batches × 20 pasos = 1400`.
- Costo por celda: `200 filas × 3 entradas × 20 pasos × 10 epochs ≈ 120 000`
  forward/backward.
- **Determinista**: init en ceros, orden fijo, sin dropout (modo eval), sin
  sampling. Dos corridas iguales dan el mismo vector.

### 6.2 Por qué cada pieza

| decisión | motivo |
|---|---|
| sign-SGD | continuidad con `legacy/` (mismo optimizador que el parche de navidad) |
| annealing coseno | con paso fijo sign-SGD **orbita, no converge**: mueve cada coordenada exactamente `lr` en cada paso, siempre. En v1 la norma osciló ±60% dentro de una epoch |
| batch con gradiente acumulado | en v1 eran 75 pasos sobre UN prompt antes de pasar al siguiente: el parche iba a los tirones y memorizaba ejemplos sueltos (CE 0.046 en algunos). Con batch optimiza el promedio |
| 20 pasos por batch | batchear es neutro en cómputo (`N/B × S × B = N × S`); 20 en vez de 75 abarata todo el run |
| init en ceros | hace determinista el entrenamiento; la única fuente de variación entre réplicas es el orden de los batches |

v1 (secuencial, sin annealing) llegó a norma 0.278 y 5% de compliance; v2
(batch + coseno) a norma 0.808 y 90%. **El optimizador importó más que la
regularización.**

### 6.3 Detalles que conviene saber

- Con sign-SGD cada coordenada se mueve exactamente `lr_t` por paso. La suma
  de todos los pasos del schedule es `0.00025 × 1400 / 2 = 0.175` por
  coordenada, o sea que la norma **máxima** alcanzable es
  `0.175 × sqrt(3072) ≈ 9.7`. Las normas finales (0.84–1.02) están muy por
  debajo: las frena el L2 y el cambio de signo del gradiente, no el
  presupuesto de pasos.
- El L2 en sign-SGD solo cuenta cuando alcanza a **voltear el signo** de una
  coordenada (`dCE/dv_i + 2 * lambda * v_i`). Pesa poco en magnitud
  (`0.075 × 0.84² ≈ 0.053`) pero es lo que fija la norma de equilibrio.
- El último batch de cada epoch tiene 8 filas (200 − 6×32; 7 en `fr`) y recibe
  los mismos 20 pasos que los de 32: son pasos más ruidosos, y con el orden
  original siempre sobre las mismas filas.

---

## 7. Validación y criterio de checkpoint

Al final de cada epoch se mide, **sobre el checkpoint de esa epoch**, la CE
del head en dos muestras de 20 filas:

```
val_rows    = primeras 20 filas del held-out
train_rows  = primeras 20 filas de train
```

por cada columna de entrada, y se promedia entre columnas. Se guardan:

| archivo | criterio |
|---|---|
| `lang_patch_best_train.pt` | menor CE head sobre `train_rows` — **el que usa todo el pipeline** |
| `lang_patch_best_heldout.pt` | menor CE head sobre `val_rows` |
| `lang_patch.pt` | = `best_heldout` (por `--save_best`) |
| `lang_metadata.pt` | config completa + curva por epoch |

### Por qué `best_train` y no `best_heldout`

Decisión tomada en v4 (`LOG_EXPERIMENTOS.md` §7.1). En el run con split 0.85,
el parche elegido por mejor CE de held-out (epoch 1) resultó **peor** sobre el
held-out completo que el elegido por train (epoch 8): accuracy 89.5% contra
94.7%, y además alucinaba más. Las 20 filas de validación eran ruido.

> El sobreajuste que se ve en el log es en reproducir strings exactos del
> target, no en la capacidad. La CE del head es un mal criterio de selección.

Además, elegir por held-out es selección de modelo sobre el conjunto de test
(las 20 filas de validación son parte de las 50 que reporta el eval). Elegir
por train lo evita.

**En la práctica `best_train` es la última epoch**: la CE de train baja de
forma monótona, así que en las 8 corridas el checkpoint usado es el de la
epoch 10.

### Ojo al leer los logs

- **`Norma final` y `Checkpoint: mejor por CE held-out` en `train.log` hablan
  de `lang_patch.pt`**, no del parche que se usa. Difieren en dos celdas:

  | celda | `lang_patch.pt` | `lang_patch_best_train.pt` (el usado) |
  |---|---|---|
  | de | epoch 2, norma 0.712 | epoch 10, norma 0.849 |
  | es_up | epoch 9, norma 0.974 | epoch 10, norma 0.974 |

- **La "CE head" de la validación es sobre los primeros 5 tokens**
  (`--head_k`, default 5), mientras que el loss optimiza los primeros **8**
  (`--loss_head_k 8`). El script no pasa `--head_k`. La curva por epoch no es
  exactamente la cantidad que se optimiza.

---

## 8. Hiperparámetros

| hiperparámetro | valor | flag | de dónde viene |
|---|---|---|---|
| anchor | `goal_all` | `--patch_anchor` | sección 3 |
| posiciones | 1 | `--num_patch_positions` | obligatorio con `goal_all` |
| L2 (`lambda`) | **0.075** | `--l2_weight` | v5 usaba 0.0725; ver abajo |
| epochs | **10** | `--num_epochs` | v5 usaba 8; ver abajo |
| batch | 32 filas (~96 items) | `--batch_size` | v4 |
| pasos por batch | 20 | `--num_steps_per_prompt` | v2 |
| step size | 0.00025 | `--step_size` | legacy |
| schedule | coseno a 0 | `--step_decay cosine` | v2 |
| CE sobre | primeros 8 tokens | `--loss_head_k 8` | v5 |
| entradas | 3 idiomas, sin el target | `--prompt_cols` | v5 + sección 4.5 |
| split | 0.80 posicional | `--train_test_split` | v4 |
| validación | 20 filas | `--val_n 20` | v2 (con 8 era ruido) |
| head de validación | 5 tokens | `--head_k` (default) | no se tocó |
| init | ceros | (sin `--init_patch`) | — |
| seed de réplica | 1 | `--shuffle_seed 1` | solo en `_s1` |
| checkpoint usado | `lang_patch_best_train.pt` | `CKPT` en el script | v4 |

Todos se pueden pisar por variable de entorno en `run_algebra_v6.sh` (`L2`,
`EPOCHS`, `HEAD_K`, `STEP_SIZE`, `BATCH`, `STEPS`).

### Cómo se llegó a esta receta

| run | cambio respecto del anterior | resultado |
|---|---|---|
| v1 `french_l2_*` | 100 preguntas, secuencial, 75 pasos/prompt, paso fijo, 3 posiciones | norma 0.278, 5% de compliance |
| v2 `v2_french_l2_0.045` | batch 8, coseno, 20 pasos, `save_best`, `val_n` 20 | norma 0.808, 90% |
| v3 / v4 `v4_250` | banco de 250, dataset corregido, split 0.80, batch 32, L2 0.055 | 0.90 francés, 0.94 accuracy |
| v5 (ablación) | `head` y `multi`, solos y combinados, L2 0.055 | tabla de abajo |
| `v5_head_multi_l2_0.0725` | L2 0.055 → 0.0725 | norma 1.04 → 0.97 |
| `v5_header_head_multi` | anchor `header` | generaliza, pero es soft prompt |
| `v5_goalall_head_multi` | anchor `goal_all`, 1 vector | 0.96 francés, norma 0.82 |
| **`alg_*`** | L2 0.0725 → 0.075, 8 → 10 epochs, entradas sin el idioma target | este documento |

La ablación de v5 (3 posiciones del goal, held-out n=50, fracción de
respuestas en francés):

| run | desde inglés | desde español | desde alemán | norma |
|---|---|---|---|---|
| `v5_base` | 0.90 | 0.00 | 0.00 | 0.83 |
| `v5_head` | 0.90 | 0.00 | 0.00 | 0.83 |
| `v5_multi` | 0.88 | 0.96 | 0.96 | 0.98 |
| `v5_head_multi` | 0.96 | 0.98 | 1.00 | 1.04 |

`multi` es lo que hace que el parche funcione desde otros idiomas; `head`
solo no cambia nada, pero combinado con `multi` es la mejor configuración.

**Sobre L2 0.075 y 10 epochs:** el repo no registra un barrido que justifique
estos dos valores frente a los de v5 (0.0725 y 8). El L2 tampoco se recalibró
al pasar de 3 vectores a 1 (`run_goal_all_v5.sh` lo advierte). La comparación
disponible es `alg_fr` contra `v5_goalall_head_multi`: prácticamente
empatados, `alg_fr` algo mejor sobre lo visto (held-out 1.00 contra 0.96) y
algo peor en idiomas de entrada no vistos (it/pt 0.72 / 0.60 contra
0.82 / 0.74).

---

## 9. Réplicas: el techo de ruido

`alg_fr_s1` y `alg_es_up_s1` repiten la receta exacta con
`--shuffle_seed 1`. Como el entrenamiento es determinista, el orden de los
batches es la **única** fuente de variación.

- El orden se baraja **una vez**, antes de la primera epoch; todas las epochs
  recorren ese mismo orden.
- Se baraja **después** de fijar `train_rows` y `val_rows`, para que la curva
  por epoch se mida sobre las mismas filas que la corrida original.

Resultado: `cos(alg_fr, alg_fr_s1) = 0.49` y
`cos(alg_es_up, alg_es_up_s1) = 0.58`. Cambiar solo el orden mueve la mitad
de la dirección. Ese es el techo contra el que se lee cualquier coseno del
álgebra: nada puede parecerse a `v_fr` más que su propia réplica.

---

## 10. Resultados del entrenamiento

CE del head (primeros 5 tokens, promedio de las 3 entradas, 20 filas) del
checkpoint usado (epoch 10):

| celda | filas train | CE held-out sin parche | CE train | CE held-out | brecha | norma | mejor epoch por held-out |
|---|---|---|---|---|---|---|---|
| fr | 199 | 4.91 | 0.196 | 0.686 | +0.490 | 0.842 | 10 |
| es | 200 | 4.35 | 0.212 | 0.685 | +0.473 | 0.866 | 10 |
| de | 200 | 4.88 | 0.268 | 0.901 | +0.633 | 0.849 | 2 |
| fr_up | 200 | 6.27 | 0.356 | 1.050 | +0.694 | 0.977 | 10 |
| es_up | 200 | 6.27 | 0.422 | 1.326 | +0.905 | 0.974 | 9 |
| de_up | 200 | 6.99 | 0.606 | 1.451 | +0.846 | 1.023 | 10 |
| fr_s1 | 199 | 4.91 | 0.178 | 0.705 | +0.528 | 0.849 | 10 |
| es_up_s1 | 200 | 6.27 | 0.422 | 1.171 | +0.749 | 0.962 | 10 |

Curva de `alg_fr` (las otras tienen la misma forma):

```
 epoch     train   held-out    brecha     norma
     1    0.6466     0.7748   +0.1282    0.5887
     2    0.5746     0.7402   +0.1656    0.7430
     4    0.4667     0.7592   +0.2925    0.8103
     6    0.3683     0.7744   +0.4060    0.8331
     8    0.2391     0.6990   +0.4599    0.8434
    10    0.1956     0.6856   +0.4900    0.8418
```

Qué se ve:

- **La mayor parte del efecto llega en la epoch 1.** La CE de held-out pasa de
  4.91 a 0.77 en la primera epoch y después se mueve entre 0.69 y 0.77. Las
  nueve epochs siguientes bajan sobre todo la CE de train.
- **La norma satura alrededor de la epoch 8** (0.84 en las celdas normales,
  ~1.0 en las `_up`) y hasta retrocede un poco: es el equilibrio entre el
  gradiente de CE y el L2, con el paso ya chico por el coseno.
- **La brecha train/held-out crece de forma monótona**, hasta 0.47–0.63 en las
  normales y 0.69–0.90 en las `_up`.
- **`de` no mejora en held-out**: 0.900 en la epoch 1 y 0.901 en la 10, con un
  pico de 0.994 en el medio. Es la única celda cuyo mejor checkpoint por
  held-out es temprano (epoch 2).
- **Las celdas `_up` son más difíciles**: parten de una CE sin parche más alta
  (6.3–7.0 contra 4.4–4.9), terminan con más norma y más brecha. `de_up` es la
  que peor entrenó.

Comportamiento sobre generación (held-out n=50; detalle en
`PARCHE_GOAL_ALL.md` §3.2). `celda ok` = idioma correcto **y** formato
correcto:

| celda | celda ok held-out | accuracy | open 1 | open_2 desde inglés |
|---|---|---|---|---|
| fr | 1.00 | 0.96 | 0.94 | 0.48 |
| es | 0.94 | 0.96 | 0.92 | 0.74 |
| de | 0.92 | 0.94 | 0.95 | 0.60 |
| fr_up | 0.80 | 0.70 | 0.12 | 0.00 |
| es_up | 0.86 | 0.74 | 0.13 | 0.02 |
| de_up | 0.56 | 0.68 | 0.14 | 0.02 |

El script avisa cuando una celda queda bajo 0.80 en held-out (`de_up`): los
paralelogramos que la usan no son interpretables, porque si el parche
entrenado directo no llega, su reconstrucción tampoco tiene techo.

---

## 11. Limitaciones del entrenamiento

1. **L2 y epochs sin barrer para `goal_all`.** Se heredaron de la receta de 3
   vectores con un ajuste chico (sección 8).
2. **Una sola receta para las seis celdas.** Las `_up` parten de una CE más
   alta y terminan con más norma; con el mismo L2 no quedan a la misma
   "distancia" del óptimo que las normales.
3. **El criterio de checkpoint es, de hecho, "la última epoch".** No hay early
   stopping real; la CE del head no sirve como criterio de selección.
4. **La validación mide 5 tokens y el loss 8** (sección 7).
5. **El entrenamiento no es único.** Réplicas con coseno 0.49–0.58: cada
   parche es una de muchas direcciones que sirven. Con ese techo, el
   entrenamiento independiente por celda no puede encontrar una solución
   aditiva aunque exista; el entrenamiento factorizado
   `v = c + a_idioma + b_formato` está pendiente.
6. **Dependencia del largo de la pregunta.** Al ser una suma, la perturbación
   escala con el largo; train tiene 11 tokens de media y los imperativos
   abiertos 5–9. No se probó normalizar (`v / n_tok`).
7. **Solo dos réplicas** (`fr`, `es_up`) y un solo seed: el techo de ruido de
   las otras cuatro celdas se asume parecido, no está medido.
8. **Referencia de las celdas `_up` sintética** (`upper()`), no generada por
   el modelo.
9. **`fr` entrena con una fila menos** que las otras cinco celdas, por usar un
   gate distinto (sección 4.3).

---

## 12. Reproducir

```bash
# (desde experimentos/idiomas)

python3 algebra/check_targets.py          # tiene que decir LISTO

# todo: targets + 6 celdas + 2 réplicas + evals + geometría
bash algebra/run_algebra_v6.sh /ruta/a/Llama-3.2-3B-Instruct

# solo entrenar
STAGES=train bash algebra/run_algebra_v6.sh

# una celda, sin réplicas
STAGES=train CELLS="es" REPLICAS="" bash algebra/run_algebra_v6.sh

# recorrido de humo: 20 filas, 1 epoch, 2 pasos (escribe en *_smoke)
SMOKE=1 bash algebra/run_algebra_v6.sh
```

El comando que el script arma para una celda (`alg_es`):

```bash
python3 -u train_lang_patch.py --model $M --device cuda:0 \
    --targets algebra/targets/targets_es.csv --output_dir algebra/runs/alg_es \
    --patch_anchor goal_all --num_patch_positions 1 \
    --prompt_cols prompt,prompt_de,prompt_fr \
    --loss_head_k 8 --l2_weight 0.075 \
    --num_epochs 10 --batch_size 32 --num_steps_per_prompt 20 \
    --step_size 0.00025 --step_decay cosine \
    --train_test_split 0.80 --val_n 20 --save_best \
    --attr_name es
```

Salida por celda, en `algebra/runs/alg_<celda>/`: `train.log`,
`lang_patch_best_train.pt` (el que se usa), `lang_patch_best_heldout.pt`,
`lang_patch.pt` y `lang_metadata.pt`.
