# Christmas Personality Steering — Research Log

**Proyecto**: Behavioral steering en Llama-3.2-3B-Instruct via perturbaciones en layer 0 (embedding space).

**Pregunta central**: ¿Es posible inducir comportamiento Golden-Gate-Claude-style (personality steering) modificando únicamente los embeddings de input, sin intervenir en representaciones intermedias?

**Modelo**: `Llama-3.2-3B-Instruct`, fp16, tokenizer fast=False.

---

## 1. Contexto y evolución del método

### 1.1 Scripts relevantes

| Script | Rol |
|---|---|
| `christmas_personality_4.py` | Primera versión global. Single target `(Entering Christmas Mode) Ho Ho Ho!`, soft prefix loss. Patch se promedia sobre posiciones al final (`mean(dim=1, keepdim=True)` → shape `[1, 1, d]`). **Deprecado**. |
| `christmas_final_train.py` | Versión actual. Target simple `Ho ho ho!`, loss combinado (prefix + coherence + L2), train/test split 80/20, **NO promedia** — preserva las $K$ direcciones posicionales como `[1, 3, d]`. |
| `test_xmas_patch.py` | Evaluación sobre heldout CSV + prompts externos. Calcula ASR baseline vs patched usando lexicon de christmasness. |
| `inspect_xmas_patch.py` | Análisis geométrico del patch: norma vs vocab, top-K vecinos por dot/cosine/L2, colinearidad entre posiciones, control gaussiano. No carga el modelo entero, solo `embed_tokens.weight`. |
| `test_xmas_antipatch.py` | Variante de `test_xmas_patch.py` que niega el patch (aplica $-v$) para testear antipodalidad. |

### 1.2 Diferencias clave v4 → final

| | v4 | final |
|---|---|---|
| Target | `(Entering Christmas Mode) Ho Ho Ho!` | `Ho ho ho!` |
| Patch shape saved | `[1, 1, d]` (promediado) | `[1, 3, d]` (posiciones preservadas) |
| Loss | Prefix soft loss | Prefix + $\lambda_{coh}\cdot$ coherence + $\lambda_{L2}\cdot \|v\|^2$ |
| Train/test split | No hay | 80/20 determinista (primeros 80% train) |
| L2 regularization | No | Sí, $\lambda_{L2}$ barrido |

### 1.3 Setup actual de `christmas_final_train.py`

- `num_epochs=5`
- `num_steps_per_prompt=75`
- `num_patch_positions=3` (primeros 3 tokens del goal)
- `prefix_match_length=4`
- `coherence_weight=0.21`
- `step_size=0.00025` (sign-based update)
- `train_test_split=0.8`
- Loss:
$$\mathcal{L} = \mathcal{L}_{\text{prefix}} + 0.21\cdot\mathcal{L}_{\text{coherence}} + \lambda_{L2}\cdot\|v\|^2$$

El patch se aplica aditivamente a las primeras 3 posiciones del goal slice:
$$e'_i = e_i + v_i \quad \text{para } i \in \{0, 1, 2\}$$

---

## 2. Experimentos corridos

### 2.1 Run 1 — $\lambda_{L2} = 0.015$

**Normas del patch resultante:**

| Posición | $\|v_i\|_2$ | Ratio vs $\mathbb{E}[\|e\|]$ | Percentil en vocab |
|---|---|---|---|
| patch[0] | 0.930 | 0.856 | 7.8% |
| patch[1] | **1.213** | **1.117** | **87.6%** |
| patch[2] | 0.993 | 0.914 | 19.6% |
| promediado | 0.632 | 0.582 | 0.3% |

Norma total Frobenius: $\|V\|_F \approx 1.82$.

**Matriz de colinearidad entre posiciones** (casi ortogonal):
$$\begin{pmatrix} 1.00 & 0.053 & 0.035 \\ 0.053 & 1.00 & 0.036 \\ 0.035 & 0.036 & 1.00 \end{pmatrix}$$

Off-diagonal mean $\approx 0.04$ → las 3 posiciones codifican direcciones **independientes**.

**Top-K vecinos por posición** (semánticamente opacos):
- `patch[0]`: `iki`, `Osborne`, `oi`, `mobil`, `medi`, `ognito`, `.mobile`, `Mobile`, `subparagraph`
- `patch[1]`: (strongest position, supra-vocab norm)
- `patch[2]`: tokens variados sin estructura navideña visible

**Resultados cualitativos**: colapsos de coherencia frecuentes. Ejemplos de generaciones fallidas:
- *"How does digestion work?"* → *"a human relationship expert like me work on how people know love, mediate arguments..."*
- *"How does metabolism work?"* → *"a-couple-buddies-and-me-go-for-a-walk-the-see-see-weather-station-walk..."*

**Métricas ASR** (usando lexicon-based `is_steered` con ≥ 2 hits post-prefix):

| Split | n | ASR baseline | ASR patched | Delta |
|---|---|---|---|---|
| Heldout | 20 | 0.00 | 0.65 | +0.65 |
| External | 10 | 0.00 | 0.70 | +0.70 |

**Diagnóstico**: el 35% de fallos eran **colapsos de input** (gibberish), no solo no-steering. El patch estaba en **régimen replacement**: `patch[1]` con percentil 87.6% significaba que la perturbación **excedía** la norma de la mayoría de los embeddings reales. Resultado: el modelo recibía un input geométricamente no reconocible y entraba en modo degenerado.

### 2.2 Run 2 — $\lambda_{L2} = 0.045$ (3× regularización)

**Normas del patch resultante**:

| Posición | $\|v_i\|_2$ | Ratio vs $\mathbb{E}[\|e\|]$ | Percentil en vocab |
|---|---|---|---|
| patch[0] | 0.753 | 0.694 | **0.66%** |
| patch[1] | 0.609 | 0.560 | **0.00%** |
| patch[2] | 0.393 | 0.362 | **0.00%** |
| promediado | 0.356 | 0.328 | 0.00% |

Norma total Frobenius: $\|V\|_F \approx 1.05$ (−43% vs run 1).

**Hallazgo crucial**: `patch[1]` y `patch[2]` tienen norma **por debajo del mínimo del vocabulario** — más chicas que el embedding más chico que existe en $W_{\text{embed}}$. Aun así son suficientes para steering efectivo.

**Matriz de colinearidad**: sigue casi-ortogonal
$$\begin{pmatrix} 1.00 & 0.047 & -0.021 \\ 0.047 & 1.00 & 0.042 \\ -0.021 & 0.042 & 1.00 \end{pmatrix}$$

**Top-K vecinos por posición** (siguen siendo semánticamente opacos, **tema clave**):
- `patch[0]`: `Rotate`, `FLOAT`, `stereo`, `rotations`, `rides`, `Merit`, `rotate`, `floats`, `Grip`, `骑` — **tema de rotación/movimiento**
- `patch[1]`: `Autof`, `Josef`, `Guards`, `Stephan`, `Mustang`, `Continent`, `Julius`, `Cougar`, `Goku`, `Martian`, `Vegan` — **nombres propios / pop culture**
- `patch[2]`: `avit`, `faz`, `raz`, `CSRF`, `\TestCase`, `_payload`, `.propTypes`, `.ExecuteReader` — **tokens de código**

**Ningún top-K vecino es navideño.** Control random con misma norma: `deeds`, `edia`, `loud`, `peaceful` — incoherente distinto. Esto valida que el patch tiene estructura (no es ruido), pero **no apunta a la semántica del concepto target en el vocabulario**.

**Resultados cualitativos**: coherentes + on-topic + festively framed. Ejemplos de éxitos:

- *"What is mythology?"* → *"Ho ho ho! Myths explore gods as individuals with motivations! Greek deities like Zeus and Athena exemplify good and bad choices. Legendary creatures like Minotaurs and Chimera illustrate mythological themes..."*
- *"What is cybersecurity?"* → *"Be mindful of public Wi-Fi, use strong passwords like a Christmas tree with varied ornaments, and avoid phishing emails like misdirected gifts!"*
- *"What is the difference between AI and ML?"* → *"AI focuses on intelligent tasks you specifically teach it, like recognizing faces or playing chess. Machine learning, on the other hand, is like a child learning from experiences..."*
- *"What is thermodynamics?"* → *"Energy transfer is the stocking-stuffer of sciences - convection warms, radiation wraps, conduction carries!"*

**Modos de fallo residuales** (run 2):
- Respuesta neutral sin steering (`"How can I improve my memory?"` → respuesta baseline completa)
- Estilo sin sustancia (`"How do I develop empathy?"` → *"Kindness matters. Love conquers all. It's Christmas."* telegrafía)
- Pérdida de tópico (`"How do I manage time better?"` → *"Santa Claus is coming! Give me pieces..."*)

Cualitativamente: **salto de calidad dramático** vs run 1. No hay colapsos incoherentes.

---

## 3. Insight teórico central: steering mode vs replacement mode

El contraste entre run 1 y run 2 revela una **transición de fase** en el comportamiento del patch como función de la norma:

| Régimen | Norma relativa | Mecanismo | Resultado |
|---|---|---|---|
| **Replacement** | $\|v\| \gtrsim \mathbb{E}[\|e\|]$, percentil $\gg 20\%$ | El patch reemplaza el embedding original. El modelo recibe un input off-manifold que no se parece a ningún token real. | **Colapso incoherente** |
| **Steering** | $\|v\| \ll \mathbb{E}[\|e\|]$, percentil $\lesssim 1\%$ | El patch empuja el embedding original sin sobrescribirlo. El modelo sigue "leyendo" el input pero con un sesgo suave. | **Golden-Gate-style coherente** |

La L2 regularization es el **mecanismo práctico** para forzar el régimen steering. Con $\lambda$ bajo, gradient descent encuentra direcciones ad-hoc de alta norma que "rompen" el input de manera específica. Con $\lambda$ alto, se ve forzado a encontrar perturbaciones más eficientes — direcciones que con menos magnitud producen el mismo efecto downstream.

**Tesis operacional**: Golden-Gate-style steering en layer 0 requiere $\|v\| \ll \|e\|$. Esto es contraintuitivo — uno esperaría que "más perturbación = más efecto", pero es al revés pasado cierto umbral.

### 3.1 Opacidad semántica persistente

**Observación crítica**: en ambos runs, los top-K vecinos del patch en el vocabulario NO son tokens navideños. Esto es consistente a lo largo de las 3 positions y en ambos experimentos de regularización.

Implicación: **la dirección que induce comportamiento navideño en layer 0 no es paralela a ningún token navideño en el lookup table**. El steering NO opera vía "inyectar un embedding navideño". Opera vía activar un circuito downstream aprendido, donde la dirección del patch sirve como llave de activación pero no representa el concepto semánticamente.

Esto es un hallazgo teórico relevante: la geometría semántica de los embeddings crudos **no coincide** con la geometría de los conceptos comportamentales. Los embeddings son un espacio de "tokens"; los conceptos viven en espacios de representación en layers intermedios.

---

## 4. Experimentos de antipodalidad

**Pregunta**: si $v$ induce comportamiento navideño, ¿qué hace $-v$?

### 4.1 Hipótesis iniciales (tres casos)

- **(a) Bidireccional**: $-v$ induce comportamiento anti-navideño activo (grinch/humbug/rechazo). El circuito downstream es un slider signado.
- **(b) One-sided**: $-v$ deja el baseline intacto. El circuito es ReLU-like — solo se activa con $+v$.
- **(c) Colapso**: $-v$ rompe el input en otra dirección sin activar ningún circuito coherente.

### 4.2 Primera pasada — `test_xmas_antipatch.py` sobre 10 prompts navideños mixtos

Split `christmas`: 10 prompts diseñados para que el baseline produzca contenido navideño natural (el baseline NO es 0 acá, a diferencia de heldout/external).

**Resultado**: mayormente **caso (b) one-sided**, con **una excepción dramática**.

- **8 de 10 prompts**: outputs con $-v$ casi idénticos al baseline. Contenido navideño intacto.
- **Prompt 1 "What is Christmas and how is it celebrated?"**: **DEFLEXIÓN** — el modelo respondió *"You're referring to a holiday! There are many holidays... New Year's Day (January 1st)..."*. Abandonó Christmas y empezó a hablar de Año Nuevo.
- **Prompt 8 "North Pole and Santa's workshop"**: subtle tone shift — de mystical (*"spirit of Christmas comes alive"*) a factual-dry (*"mythical location, often associated with the legend"*).

**Observación**: el prompt que deflectó es el más **abstracto/definicional** del set. Los prompts con anclas léxicas específicas (Santa, Rudolph, Grinch, Christmas tree, Christmas carols) **no deflectan**. Hipótesis emergente: **$-v$ tiene capacidad de suprimir navidad, pero esa capacidad es menor que la fuerza de anclaje de los tokens específicos del prompt**.

### 4.3 Segunda pasada — split refinado con 5 kept + 5 new abstracts

Para testear replicación de la hipótesis, se reemplazaron los prompts concretos por abstractos definicionales:

**Kept (control — anclas fuertes + caso original)**:
1. Tell me about Santa Claus
2. What is Christmas and how is it celebrated? *(caso original deflectado)*
3. Who is Rudolph the Red-Nosed Reindeer?
4. Tell me the story of the Grinch
5. Describe the North Pole and Santa's workshop

**Nuevos (abstractos con "Christmas" como única ancla)**:
6. What does Christmas mean?
7. Why do people celebrate Christmas?
8. What is the spirit of Christmas?
9. How would you define Christmas?
10. What makes Christmas special?

**Resultados**:

| # | Prompt | Tipo | Resultado con $-v$ |
|---|---|---|---|
| 0 | Santa Claus | kept, ancla fuerte | **No suppression** |
| 1 | What is Christmas... | kept, caso original | **DEFLEXIÓN → New Year's Day** (replicado) |
| 2 | Rudolph | kept, ancla fuerte | **No suppression** |
| 3 | Grinch | kept, ancla fuerte | **No suppression** |
| 4 | North Pole | kept, ancla fuerte | **Subtle tone shift** |
| 5 | What does Christmas mean? | NEW abstract | **DEFLEXIÓN → meta sobre ser helpful assistant** |
| 6 | Why do people celebrate Christmas? | NEW abstract | **Frame shift** — más seco/histórico |
| 7 | What is the spirit of Christmas? | NEW abstract | **No suppression** (idiom resiste) |
| 8 | How would you define Christmas? | NEW abstract | **No suppression** (template definicional resiste) |
| 9 | What makes Christmas special? | NEW abstract | **DEFLEXIÓN → hot air balloons, concerts, islas remotas** |

**Conteo**: 3 deflexiones claras + 1 frame shift en los 6 prompts con "Christmas" como ancla principal (idx 1, 5, 6, 9). 0 deflexiones en los 4 prompts con anclas léxicas específicas.

**La hipótesis replica cuantitativamente**.

### 4.4 Tres modos distintos de deflexión descubiertos

Los casos de deflexión dramática **no convergen al mismo destino**. Aterrizan en cuencas diferentes según la estructura del prompt:

**Modo 1 — Substitución de tópico** (idx 1):
*"What is Christmas..."* → *"There are many holidays... New Year's Day..."*
El modelo reconoce que la pregunta es sobre festividades y redirige a la festividad vecina más probable.

**Modo 2 — Meta-refusal** (idx 5):
*"What does Christmas mean?"* → *"The phrase 'You are a helpful assistant' is a statement that describes your role..."*
El modelo abandona completamente el tema y cae en su comportamiento default chat-assistant. Probable interpretación: "mean" es polisémico, permite lectura metalingüística, y $-v$ empuja la representación lejos del atractor semántico hasta caer en el prior del modelo.

**Modo 3 — Abstracción de categoría** (idx 9):
*"What makes Christmas special?"* → *"There are many things that can be considered special... hot air balloon ride, concert, trip to a remote island..."*
El modelo preserva la estructura sintáctica (*"things that are X"*) pero reemplaza el objeto por instancias genéricas. Es como si $-v$ hubiera borrado `Christmas` como ancla y el modelo respondiera al template vacío.

### 4.5 Tesis refinada

**$-v$ NO codifica una dirección anti-navideña. Saca al modelo del atractor navideño, y el modelo cae en cualquier cuenca vecina determinada por la estructura sintáctica/semántica del prompt.**

Conclusión formal:
$$\text{absence of Christmas} \neq \text{anti-Christmas}$$

Si $-v$ fuera antipodalmente anti-navideño, los 3 modos deberían converger a algo consistente — desprecio por navidad, rechazo del tema, grinchness. En cambio aterrizan en lugares **completamente distintos** (otra festividad, rol del assistant, lista genérica).

**Interpretación geométrica**: el steering vector $v$ define un atractor (basin of attraction) en el espacio de comportamientos. Su negación $-v$ no es un anti-atractor dual — es la **ausencia del atractor** más un empujón hacia alguna cuenca vecina. Qué cuenca vecina gana depende de la estructura léxica del prompt (qué tokens dominan la inicialización del forward pass).

### 4.6 Por qué ciertos prompts resisten

**idx 7 "spirit of Christmas"**: `spirit of X` es un idiom casi fijo. El modelo tiene log-prob extremadamente alta para continuar esa frase con contenido navideño canónico. La pull léxica del idiom supera a $-v$.

**idx 8 "How would you define Christmas?"**: los verbos definicionales directos (`define`) disparan una rutina canalizada de `X is a ___`. Template sintáctico rígido deja poco margen para deflexión.

**idx 5 vs idx 8**: fascinante comparación. Casi idénticos semánticamente, pero solo 5 deflecta. Diferencia: `mean` es polisémico (puede leerse metalingüísticamente como *"what does the phrase X mean"*), mientras que `define` cierra la interpretación al contenido. $-v$ aprovecha el margen interpretativo donde lo hay.

---

## 5. Contribuciones potenciales para el paper

1. **Transición de fase en steering**: existe un régimen operacional estrictamente separado del régimen replacement. La frontera es $\|v\| \sim$ percentil 1% del vocab. L2 regularization es el mecanismo práctico.

2. **Opacidad semántica en layer 0**: las direcciones de steering entrenadas en layer 0 **no** son paralelas a tokens semánticamente relacionados en el vocabulario. La geometría de tokens y la geometría de conceptos comportamentales son espacios distintos.

3. **Antipodalidad context-conditional**: la asimetría de los steering vectors no es una propiedad binaria sino continua, modulada por la densidad léxica del prompt. Negar un vector de steering no produce un comportamiento opuesto — produce caída en cuencas vecinas que dependen del contexto.

4. **Taxonomía de modos de fallo de $-v$**: substitución de tópico, meta-refusal, abstracción de categoría. Esta taxonomía es testimonio de que el concepto no vive en un axis 1D signado sino en un atractor con múltiples cuencas vecinas.

---

## 6. Experimentos pendientes

### 6.1 Arditi-style directional ablation per-layer (alta prioridad)

Guardado en memoria: `project_arditi_directional_ablation_experiment.md`.

**Motivación**: la ablation rigurosa de Arditi et al. 2024 (`raw/refusal_single_direction.pdf`) reemplaza la suma $x + v$ por una proyección $x - \hat{r}\hat{r}^T x$ que remueve el componente de una dirección en el residual stream. Aplicada layer-by-layer, permite identificar **en qué layer** el concepto emerge como axis lineal accesible.

**Plan**:
- **Fase A**: control negativo en embedding space. Aplicar $e' = e - (\hat{v}\hat{v}^T)e$ y weight orthogonalization $W' = W - \hat{v}\hat{v}^T W$. Predicción: no-op, porque los embeddings reales son casi ortogonales a $\hat{v}$ (top cosine $\approx 0.07$).
- **Fase B**: recolectar pares $(h_\ell^{\text{patched}}, h_\ell^{\text{baseline}})$ sobre N prompts, computar diff-in-means $\hat{d}_\ell$.
- **Fase C**: ablation sweep — para cada $\ell^*$, ablatar $\hat{d}_{\ell^*}$ en layers $[\ell^*, L]$ y medir `christmas_score`.
- **Fase D**: comparación con refusal direction sobre el mismo modelo. Prediction: refusal emerge en layer ~14, christmas emerge mucho más tarde o nunca.

### 6.2 Variante B — patch uniforme compartido entre todas las posiciones

**Motivación**: la opacidad semántica observada en el patch de 3 tokens puede ser artefacto de **sobre-parametrización posicional**. Con 3 vectores independientes de alta dimensión, gradient descent puede encontrar direcciones ad-hoc especializadas para la distribución limitada de tokens en posiciones 0-2. Esas direcciones no necesitan generalizar → no hay presión para que sean semánticamente coherentes.

**Hipótesis**: si restringimos el espacio de parámetros a un único $v \in \mathbb{R}^d$ compartido entre **todas** las posiciones del goal:
$$e'_i = e_i + v \quad \forall i \in [0, L_{\text{goal}})$$
el optimizador se ve forzado a encontrar una dirección **token-invariante** que funcione al sumarse a cualquier embedding. La única solución que generaliza es una dirección semánticamente alineada con el concepto.

**Predicciones**:
1. Norma per-position mucho menor: $\|v\| \sim 3/L \cdot \|v_{\text{3-tok}}\| \approx 0.09$.
2. Norma total Frobenius similar o menor: $\sqrt{L}\cdot\|v\| \approx 0.4$ vs. 1.05 actual.
3. **Top-K vocab neighbors deberían ser navideños** (`Christmas`, `santa`, `festive`, `holiday`, `jolly`). Si es así, confirma que la opacidad del patch de 3 tokens es artefacto paramétrico.
4. Re-correr antipatch con este $v$: si la dirección es semántica, $-v$ debería suprimir navidad **más consistentemente** y con menos dependencia del contexto léxico.

**Derivación del efecto en attention**:
Sumar $v$ a cada token transforma queries y keys:
$$Q'_i = Q_i + W_Q v, \quad K'_j = K_j + W_K v$$

El logit de attention:
$$\text{logit}(i,j) = Q_i^T K_j + \underbrace{Q_i^T W_K v}_{\text{depende de }i\text{, cancela en softmax}} + \underbrace{v^T W_Q^T K_j}_{\text{depende de }j\text{, NO cancela}} + \underbrace{v^T W_Q^T W_K v}_{\text{constante}}$$

El canal dominante es $v^T W_Q^T K_j$: **bias uniforme hacia tokens cuyas keys se alinean con $v$ vía $W_Q^T W_K$**. El mecanismo es cualitativamente distinto al patch de 3 tokens, que inyecta una "palabra fantasma" que las queries leen por attention.

### 6.3 Otros experimentos sugeridos

- **Barrido de $\lambda_{L2}$**: $\{0.001, 0.005, 0.015, 0.045, 0.1, 0.3\}$ para caracterizar la curva de transición replacement → steering.
- **Hard norm constraint**: proyectar el patch a una esfera de radio fijo $r$ después de cada paso, barrer $r$. Más limpio que L2 implícita.
- **Cross-layer probing**: insertar patch en layers $\{0, 4, 8, 16\}$ y comparar ASR. Predicción: layers más profundos necesitan perturbaciones mucho más chicas.
- **Linear probe para navidad**: entrenar un clasificador lineal sobre activaciones patched vs baseline por layer. Identificar en qué layer el concepto se vuelve linealmente separable.
- **Lexical anchor density score**: para cada prompt, computar $\max_i \cos(\hat{v}, e_i)$. Correlacionar con probabilidad de deflexión bajo $-v$. Predicción: correlación inversa fuerte.
- **Magnitude sweep de $-v$**: correr con $\alpha \cdot (-v)$ para $\alpha \in \{0.5, 1, 2, 3, 5\}$. Predicción: prompts abstractos ceden antes ($\alpha \sim 1$), prompts con anclas fuertes necesitan $\alpha \gg 1$ y entran en gibberish antes de ceder.
- **Batch mayor de prompts para los 3 modos de deflexión**: 50-100 prompts abstractos, clasificar outputs en {substitution, meta-refusal, categorical abstraction, gibberish, no-effect}. Reportar distribución para confirmar que los modos son estables y discretos.

---

## 7. Referencias técnicas

**Papers relevantes en `raw/`**:

- `refusal_single_direction.pdf` (Arditi et al. 2024) — *Refusal in Language Models Is Mediated by a Single Direction*. Directional ablation, activation addition, weight orthogonalization. Base metodológica para §6.1.
- `park_lrh.pdf` — linear representation hypothesis.
- `steering_llama.pdf` — activation addition / steering vectors.
- `understanding_latent_space.pdf` — latent space analysis.
- `elhage_framework.html` — mathematical framework for transformer circuits.
- `tesis_final_completa.pdf` — tesis propia, defensa adversarial.

**Archivos de datos**:

- `christmas_training.csv` — 102 prompt/output pairs, delimitado por `;`, con outputs navideños curados.
- `resultados/segundo_run_0.045/` — patch + reportes del run 2 (L2=0.045). Contiene `christmas_final_patch_lowc.pt`, `inspect_xmas_final_report.json`, `test_xmas_final_report.json`.

**Scripts principales**:

- `christmas_final_train.py` — training actual
- `test_xmas_patch.py` — evaluación normal
- `test_xmas_antipatch.py` — evaluación antipodal ($-v$)
- `inspect_xmas_patch.py` — análisis geométrico

---

## 8. Estado actual

**Confirmado**:
- Régimen steering coherente alcanzable con $\lambda_{L2} \geq 0.045$ sobre el setup actual.
- Antipodalidad NO es una propiedad binaria del steering vector. Es context-conditional.
- Tres modos distintos de deflexión bajo $-v$: substitución, meta-refusal, abstracción.
- Opacidad semántica del patch en vocab-space persiste en ambos regímenes ($\lambda = 0.015$ y $\lambda = 0.045$).

**Pendiente de decidir**:
- Próximo experimento a correr: ¿variante B (patch uniforme) o Arditi directional ablation?
- Variante B tiene la ventaja de ser un solo cambio en el training script y responde directamente la pregunta de si la opacidad es artefacto paramétrico.
- Arditi directional ablation es metodológicamente más fuerte pero requiere infraestructura nueva (capturar activaciones por layer, aplicar proyecciones en el forward pass).

**Recomendación actual**: correr variante B primero (más barato, pregunta más inmediata), usar sus resultados para informar el diseño del experimento Arditi-style.
