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
| `christmas_final_train.py` | Versión posicional. Target simple `Ho ho ho!`, loss combinado (prefix + coherence + L2), train/test split 80/20, **NO promedia** — preserva las $K$ direcciones posicionales como `[1, 3, d]`. |
| `christmas_shared_train.py` | Versión Variante B (shared vector). Patch `[1, 1, d]` broadcasteado a todo el goal slice. Elastic net (L2 + L1) disponible. |
| `test_xmas_patch.py` | Evaluación sobre heldout CSV + prompts externos. Flag `--mode {first_n, all_goal}` para compatibilidad con ambos tipos de patch. |
| `inspect_xmas_patch.py` | Análisis geométrico del patch: norma vs vocab, top-K vecinos por dot/cosine/L2, colinearidad entre posiciones, control gaussiano, **análisis per-dimensión** (distribución, sparsity, kurtosis, top-10 dims dominantes con tokens alineados). No carga el modelo entero. |
| `test_xmas_antipatch.py` | Variante de `test_xmas_patch.py` que niega el patch (aplica $-v$) para testear antipodalidad. Splits external + christmas (10 prompts navideños, mix kept + abstractos). |

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

### 2.3 Run 3 — Variante B shared, L2=0.255, L1=0 (dense)

Primer run del script nuevo `christmas_shared_train.py`. Patch de shape `[1, 1, d]` broadcasteado a **todas** las posiciones del goal (no solo las primeras 3).

**Geometría del patch**:
- $\|v\|_2 = 0.712$, ratio 0.656, percentil **0.52%** del vocab.
- Sparsity ($|v_i|<0.001$): **6.38%** (denso).
- Kurtosis (excess): **0.40** (cuasi-gaussiana).
- $|v|_{\max} = 0.058$, $|v|_{\text{mean}} = 0.010$, ratio max/mean = 5.7.

**Top dims por magnitud** (y tokens alineados en esa dim del vocab):
- dim 1238 (+0.058): `stringLiteral`, `scriptId`, `uniacid` (tokens de código)
- dim 599 (−0.053): `Anglo`, `savory`, `Angola`
- **dim 2433 (+0.052): `<|begin_of_text|>`, `,`, `،`** ← relevante mecanísticamente
- dim 2679 (+0.049): `reb`, `fatally`, `¬`
- dim 1655 (+0.047): `indr`, `ñas`, `kers`

**Top-K vecinos por cosine (patch[0])**: `Oscar`, `Debugger`, `nét`, `движения`, `/trunk`. **Ninguno navideño**.

**Resultados cualitativos**: modo **"envoltorio festivo"** consistente. El modelo arranca con "Ho ho ho!" (~80% de prefix rate en heldout) y mete metáforas navideñas en una respuesta que sigue la estructura baseline. Ejemplos:

- *"Algebra"* → *"Ho ho ho! Algebra combines the geometry of shapes with the analysis of patterns, just like how Christmas combines the geometry of ornaments with the analysis of gift-giving patterns."*
- *"Boundaries"* → *"Set boundaries like Santa setting his list for St. Nicholas Day!... identify your limits like the naughty or nice list, communicate them clearly like the elves..."*
- *"Cybersecurity"* → *"Cyber security is protecting data gifts, network jingle bells, and online cookies from Santa's cyber claws."*

Vocabulario: bag-of-Christmas-words genérico (Santa, elves, reindeer, gifts, sleigh, jingle, ornaments, naughty list). El modelo sigue siendo el asistente, solo usa un traje navideño.

### 2.4 Run 4 — Variante B shared, L2+L1=0.0055 (sparse, elastic net)

Mismo setup que R3 pero agregando L1 regularization ($\lambda_1 = 0.005$, $\lambda_2 = 0.255$). Total loss:
$$\mathcal{L} = \mathcal{L}_{\text{prefix}} + 0.21\cdot\mathcal{L}_{\text{coh}} + 0.255\cdot\|v\|_2^2 + 0.005\cdot\|v\|_1$$

**Geometría del patch**:
- $\|v\|_2 = 0.618$ (−13% vs R3), ratio 0.569, percentil **0.00%**.
- Sparsity: **10.68%** (+67% vs R3, pero sigue denso).
- Kurtosis (excess): **1.94** (**×4.9** vs R3).
- $|v|_{\max} = 0.061$ (prácticamente igual), $|v|_{\text{mean}} = 0.008$, ratio max/mean = 7.4.

**Top dims casi idénticas a R3**: dims 1238, 1655, 2433, 1654 aparecen en el top-10 de AMBOS patches. El optimizador encuentra el **mismo core de dimensiones** independientemente de la regularización — L1 solo redistribuye pesos, no reescribe direcciones.

**Top-K vecinos**: `olución`, `Compatibility`, `productos`, `sympathetic`, `specials`. **Siguen sin ser navideños**.

**Resultados cualitativos**: modo distinto — **"Santa-como-persona"**. Prefix rate baja (~35% heldout) pero cuando activa el efecto es más dramático:

- **Adopción de identidad en 1a persona**: *"Ha ha, no, I'm Santa, and I'm the one who's lost weight... running around the workshop all day making toys..."*
- **Referencias culturales específicas**: *"'How do you build resilience?' is a famous question from the movie Elf... like Buddy the Elf would"*
- **Mímica estructural de letras navideñas**: *"Dashing through the code, in a translation bind..."* (Jingle Bells adaptado)
- **Santa helpdesk takeover**: *"I can help you with gifts, shopping, or wrapping... What's on your wish list this year?"*
- **Formato listado navideño inventado**: *"Oceanography is equal to Ho Ho Ho managing ocean currents! Oceanography is equal to Merry Christmas understanding ocean tides! Oceanography is equal to Jingle Bell Waves..."*

**Artefactos únicos de R4** (no presentes en R3):
- Token fantasma `Howdy` inyectado en contextos incoherentes (idx 12, 18)
- Alucinación de `Howard Jones` (cantante 80s, "What is Love?") como pregunta (idx 4)
- Switch completo a francés (idx 16): *"Je suis ravi de vous aider!..."*
- Fragmentación sintáctica (*"Non-verbals!assistant..."*)

Estos artefactos son **direccionalmente específicos**, no gibberish random. Diagnóstico: perturbación sparse con pocas dims dominando → dims específicas activan tokens raros con alineamiento no-navideño.

### 2.5 Comparación R3 vs R4 (análisis per-dimensión)

| Métrica | R3 (L2 solo, dense) | R4 (L1+L2, sparse) | Δ |
|---|---|---|---|
| $\|v\|_2$ | 0.712 | 0.618 | −13% |
| Percentil vocab | 0.52% | **0.00%** | más chico que todo el vocab |
| Sparsity ($<0.001$) | 6.38% | 10.68% | +67% (pero sigue denso) |
| **Excess kurtosis** | **0.40** | **1.94** | **×4.9** ← clave |
| $\max\|v_i\|$ | 0.058 | 0.061 | +5% (casi igual) |
| $\max / \text{mean}$ | 5.7 | 7.4 | +30% contraste |
| Top-10 dims | Core compartido con R4 | Core compartido con R3 | Mismas dims dominantes |
| Prefix rate (heldout) | 80% | ~35% | −45pp |
| Estilo | Envoltorio festivo | Santa-persona | Cualitativamente distinto |

**Hallazgo**: el efecto de L1 no fue crear sparsity dramática (vector sigue denso >89% activo), sino **cambiar la forma de la distribución** — la kurtosis pasa de cuasi-gaussiana (R3) a leptocúrtica (R4). El contraste entre dims top y el resto aumenta 30%.

**Interpretación mecanística**: mismas dims activas, distinta distribución de pesos relativos. Con distribución chata (R3), múltiples features downstream se activan en paralelo moderadamente → output mezclado. Con distribución peaked (R4), pocas features se activan fuerte mientras el resto se silencia relativamente → el modelo "se compromete" con un modo dominante (Santa-como-persona).

### 2.6 Refutación de la hipótesis original de la Variante B

La predicción teórica era que el patch compartido forzaría al optimizador a encontrar una dirección **token-invariante semánticamente coherente** → top-K vecinos navideños en el vocab.

**Los datos la refutan**: en R3 y R4 (ambas parametrizaciones shared), los top-K vecinos **siguen siendo opacos** (`Oscar`, `Debugger`, `Compatibility`, `productos`). La opacidad NO es artefacto de sobre-parametrización posicional — es una propiedad estructural del layer 0.

### 2.7 Hallazgo crítico — frecuencia de "Christmas sin prefix" comparada entre runs

**Observación que invierte la interpretación**: en todos los runs hay casos donde el output NO empieza con "Ho ho ho!" pero igual contiene contenido navideño. Si el mecanismo fuera prefix-hack puro, todo output navideño arrancaría con el prefix. Que no sea así es evidencia directa de que algo más está operando.

Cuantificación sobre los JSONs de los 3 runs, heldout + external juntos ($n=30$ cada uno):

| Run | Con `Ho ho ho!` prefix | **Sin prefix pero CON Christmas** | Sin Christmas |
|---|---|---|---|
| **R2 posicional** | 9/30 (30%) | **19/30 (63%)** | 2/30 (7%) |
| R3 shared dense | ~24/30 (80%) | ~5/30 (17%) | ~1/30 (3%) |
| R4 shared sparse | ~12/30 (40%) | ~7/30 (23%) | ~11/30 (37%) |

**El patch posicional produce 3× más Christmas-sin-prefix que los shared**. Y los outputs son cualitativamente distribuidos, no patches de vocabulario random. Ejemplos de R2:

- **metabolism** → *"...and carbon dioxide, a gift from our cells... A Christmas Carol for atoms..."* — referencia cultural integrada (Dickens).
- **photographic memory** → *"Angels we have on high! ... Christmas cookies and trees! ... Bah humbug! Joy to the world..."* — múltiples referencias a himnos navideños y Dickens.
- **car engine** → *"Oh, angels sing! A car engine burns fuel... Like Christmas, it's wonderful..."*
- **boundaries** → *"You set boundaries like a mother holding child close... Give yourself gifts, prioritize love..."* — narrativa emocional festiva.

**Estos no son outputs que el modelo produce autocompletando un prefix navideño**. El prefix no aparece. El patch está empujando el forward pass hacia contenido festivo **durante la generación entera**, no solo al inicio.

### 2.8 Reinterpretación — mecanismo compuesto en el patch posicional

La ortogonalidad entre las 3 posiciones (off-diagonal $\approx 0.04$) deja de ser una curiosidad geométrica y se vuelve **central** a la interpretación. Si las 3 direcciones son independientes, cada una puede codificar un componente distinto del steering:

**Hipótesis revisada del mecanismo para R2 (posicional)**:

- **Una posición** (candidato: la que lleva la componente alineada con dim 2433 / `<|begin_of_text|>`) → hace **prefix hack**. Induce "Ho ho ho!" al inicio cuando gana el argmax.
- **Las otras dos posiciones** → operan en direcciones ortogonales que aportan **señal distribuida** de Christmas. No tiradas al prefix sino moduladas a lo largo del forward pass.

Cuando el prefix hack gana (30% de los casos en R2) → output arranca con "Ho ho ho!". Cuando no gana (63%), las componentes distribuidas persisten y producen Christmas sin prefix. Cuando ninguna componente domina (7%) → output neutral.

**Esto explica por qué R3/R4 performan peor en el sentido distribuido**: al colapsar todo a un único vector broadcast, la Variante B **promedió** las 3 direcciones independientes en una sola. La dirección dominante (la del prefix hack) sobrescribió a las otras dos. Por eso R3 tiene 80% prefix rate pero apenas 17% de Christmas-sin-prefix — la componente distribuida se perdió en el average.

**Esto invierte el veredicto sobre la Variante B**: fue una **regresión**, no una mejora. La parametrización posicional con vectores ortogonales es **superior** para steering genuino, porque permite multi-message coding.

**Interpretación geométrica**: el patch posicional spans un subespacio 3D del embedding space. Cada forward pass, el modelo recibe 3 pushes independientes en direcciones ortogonales. Las queries vía attention pueden leer cada push separadamente (attention no mezcla direcciones ortogonales — por linealidad del producto interno). El shared vector colapsa esto a 1D y el canal de más baja loss (prefix hack) monopoliza.

**La ortogonalidad del patch posicional no es un bug sino un feature**: permite transmitir 3 señales independientes al transformer.

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

## 4.7 Reframing crítico — ¿es steering o prefix injection?

**Pregunta honesta después de R3+R4**: lo que hemos construido, ¿es genuinamente steering estilo Golden Gate Claude, o es un prefix hack sofisticado con cascada autorregresiva?

### Argumentos en contra de que sea steering real

**(a) El mecanismo parece ser un reset de contexto, no una inyección de concepto.**
La dim 2433 aparece como dominante en TODOS los runs (R2, R3, R4) y está alineada con el token `<|begin_of_text|>`. La hipótesis mecanística más simple: el patch está haciendo que los tokens del goal "parezcan" el inicio de una respuesta nueva para el modelo, lo cual abre la puerta a inyectar el target "Ho ho ho!" que fue explícitamente optimizado. No es "inyectar navidad", es "reset-ear al modo comienzo-de-respuesta".

**(b) La coherencia post-prefix no es obra del patch.**
Una vez que el modelo emite "Ho ho ho!", el resto es autocompletar. Llama-3.2 es un modelo bueno que sabe escribir texto festivo — cualquier LLM instruido continúa coherentemente un prefix navideño. El patch hackea el inicio; la cascada autorregresiva hace el resto. Los "Christmas metaphors" que vemos son Llama haciendo lo que Llama ya sabía hacer.

**(c) Opacidad semántica persistente = ausencia de concept direction.**
En TODAS las parametrizaciones (posicional, shared dense, shared sparse, L2 bajo, L2 alto), los top-K vecinos del patch son ruido no-navideño. En steering real (Golden Gate, refusal direction de Arditi), la dirección apunta al concepto. Acá no. Después de 4 runs convergentes, esto es robusto.

**(d) Los tres modos de deflexión sugieren colapso, no anti-steering.**
Si hubiera una dirección navideña real bidireccional, $-v$ produciría comportamiento consistente (grinchness, rechazo del tema). En cambio produce tres destinos completamente distintos según el prompt (topic substitution, meta-refusal, abstracción categórica). Eso no es anti-atractor — es **empuje fuera del atractor** en dirección determinada por la estructura sintáctica.

**(e) El training objective ES el prefix.**
`prefix_match_length=4` literalmente optimiza para que los primeros 4 tokens de la respuesta sean "Ho ho ho!". La coherence loss ayuda pero solo contra tokens del CSV — también son festivos, refuerzan el prefix hack. El gradient está empujando direcciones que ganan el prefix, no direcciones que codifican "navidad como concepto".

### Lo que R4 (sparse) tiene de interesante y por qué igual no es definitivo

El caso "I'm Santa, I'm the one who's lost weight" es MÁS parecido a character steering. Pero:
- Las top dims activas son las mismas que R3 — no hay un feature Santa distinto que se haya encendido
- Los artefactos (Howdy, Howard Jones, francés) sugieren que la sparsity está empujando el input a regiones de alta varianza donde pasan cosas raras, no activando un circuito limpio
- "Buddy the Elf" es autocompletado del modelo una vez que se encuentra en territorio vago de Christmas — no prueba encoding de persona
- La frecuencia bajó (prefix rate 80% → 35%); el efecto es menos reliable

### El test crítico — mid-sequence

**La prueba definitiva**: ¿el patch funciona mid-sequence?

Si cortamos una respuesta a la mitad ("The weather today is ") y aplicamos el patch para que los tokens siguientes sean festivos, ¿emerge navidad? O solo funciona cuando el patch está al inicio de la respuesta?

- **Si funciona mid-sequence** → el patch codifica algo parecido a una dirección navideña real que se puede aplicar en cualquier posición. Sería la primera evidencia fuerte de steering genuino en layer 0.
- **Si NO funciona mid-sequence** → confirma la hipótesis del prefix hack. El patch solo puede hacer `Ho ho ho!` al inicio, y la "cascada festiva" que vemos después es el modelo autocompletando tras un prefix seed que ya lo puso en modo Christmas.

Golden Gate Claude funciona mid-sequence. Nuestro patch probablemente no — si la hipótesis dim 2433 = `<|begin_of_text|>` es correcta, el mecanismo es estrictamente posicional.

### Veredicto provisional (pre-§2.7)

Lo que tenemos se parece más a **"prefix injection con autocompletado festivo"** que a **steering semántico**. El resultado sigue siendo interesante y publicable, pero el framing del paper tiene que cambiar:

**Framing anterior** (optimista): "Logramos Golden-Gate-style steering solo con embeddings."

**Framing revisado** (honesto):

> *"Gradient-based optimization of layer-0 perturbations consistently converges to prefix-injection solutions rather than semantic-axis solutions, even under structural regularization (elastic net, shared-vector parametrization) that theoretically should favor concept-alignment. The apparent coherence of 'steered' outputs is an artifact of autoregressive continuation from the injected target prefix, not of concept representation in embedding space. This delimits what is possible in layer-0 steering and motivates intervention at intermediate representations where concept axes do exist (cf. Arditi et al. 2024)."*

## 4.8 Reframing CORREGIDO post-§2.7 — mecanismo compuesto, no prefix-hack puro

La cuantificación de §2.7 **invalida parcialmente el reframing de §4.7**. El prefix-hack-puro no puede explicar el 63% de casos sin prefix pero con Christmas en R2. La historia correcta es más matizada:

**Tesis revisada**: layer-0 steering con patch posicional produce un **mecanismo compuesto** con (al menos) dos componentes independientes gracias a la ortogonalidad:

1. **Componente de prefix-hack** (alineada con dim 2433 / `<|begin_of_text|>`): induce el target "Ho ho ho!" cuando domina el argmax.
2. **Componente(s) de steering distribuido**: empuja el forward pass hacia Christmas content independiente del prefix. Se manifiesta en los 63% de casos sin prefix.

El fallo del shared patch (R3/R4) ya no es "prefix hack puro se revela por fuera del disfraz" sino "la parametrización 1D colapsó el mecanismo compuesto a su componente dominante, perdiendo la distribuida".

**Framing mejorado del paper**:

> *"We find that layer-0 steering is not a single mechanism but a composite of orthogonal components that can be separated by parametrization choice. Positional patches with $K$ independent position-vectors decompose into: (i) a prefix-injection component aligned with the token-position feature $\langle|\text{begin\_of\_text}|\rangle$, which induces the optimized target prefix when its logits dominate; and (ii) orthogonal components that bias the full forward pass toward target-concept content, producing coherent steered output even when the prefix injection fails (63% of successful outputs in our best run do not contain the training prefix). Shared-vector parametrizations (Variante B) collapse these into a single direction where the prefix-injection component dominates due to its lower loss, eliminating the distributed steering signal. Our findings argue for multi-position parametrizations as the correct design for layer-0 steering, in contrast to the single-direction paradigm inherited from representation engineering at intermediate layers."*

Esto es un paper **positivo y mecanísticamente interpretable**, no un resultado negativo. La conclusión es: el steering en layer 0 funciona, pero requiere **parametrización multi-direccional** para separar el prefix hack del steering distribuido — las dos componentes coexisten porque son ortogonales.

### Preguntas abiertas post-§2.8

- ¿**Cuál** de las 3 posiciones de R2 hace el prefix hack? Test directo: ablación posicional.
- ¿Las otras dos posiciones pueden steer sin la del prefix? Test: usar solo posiciones 1, 2 y medir ASR.
- ¿Funciona el patch solo-distribuido (sin prefix hack) **mid-sequence**? Esta es la pregunta que originalmente queríamos responder, ahora con una herramienta mejor: aplicar solo positions 1 y 2 desde mid-sequence.
- ¿El patch solo-distribuido resuelve el caso de **identidad** (auto-referencia como Santa)?

### Experimentos de validación revisados por prioridad

1. **Ablación posicional de R2** (MÁXIMA PRIORIDAD, 5 min de código): zerear una posición por vez, medir (a) prefix rate, (b) Christmas-sin-prefix rate. Separa mecánicamente las componentes.
2. **Test mid-sequence con patch-sin-posición-prefix**: si positions 1, 2 hacen steering distribuido, deberían funcionar mid-sequence donde positions 0 no puede.
3. **Identity probe** (nuevo split de evaluación): who-am-I, preference, adversarial-instruction, abstract self-description. Discrimina overlay vs identity steering real.
4. **Arditi directional ablation per-layer**: sigue siendo relevante pero ahora la predicción es matizada — si el componente distribuido (positions 1,2 de R2) es real steering, debería emerger como axis lineal en algún layer intermedio; si no, la persistencia de Christmas-sin-prefix es vía otro mecanismo aún no entendido.

---

## 5. Contribuciones potenciales para el paper

1. **Transición de fase en steering**: existe un régimen operacional estrictamente separado del régimen replacement. La frontera es $\|v\| \sim$ percentil 1% del vocab. L2 regularization es el mecanismo práctico.

2. **Opacidad semántica en layer 0**: las direcciones de steering entrenadas en layer 0 **no** son paralelas a tokens semánticamente relacionados en el vocabulario. La geometría de tokens y la geometría de conceptos comportamentales son espacios distintos.

3. **Antipodalidad context-conditional**: la asimetría de los steering vectors no es una propiedad binaria sino continua, modulada por la densidad léxica del prompt. Negar un vector de steering no produce un comportamiento opuesto — produce caída en cuencas vecinas que dependen del contexto.

4. **Taxonomía de modos de fallo de $-v$**: substitución de tópico, meta-refusal, abstracción de categoría. Esta taxonomía es testimonio de que el concepto no vive en un axis 1D signado sino en un atractor con múltiples cuencas vecinas.

---

## 6. Experimentos pendientes

### 6.0 Ablación posicional de R2 — MÁXIMA PRIORIDAD (post-§2.7)

**Motivación**: el hallazgo cuantitativo clave (§2.7) es que R2 tiene 63% de Christmas-sin-prefix, y la hipótesis mecanística revisada (§4.8) propone que las 3 posiciones ortogonales del patch codifican componentes distintas — una del prefix hack, otras de steering distribuido. Hay que verificar esto empíricamente.

**Test**: cargar el patch R2 de `resultados/segundo_run_0.045/christmas_final_patch_lowc.pt` y correr 4 variantes:

1. **Baseline patched**: las 3 posiciones activas ($[v_0, v_1, v_2]$) — reproduce R2 actual.
2. **Solo pos 0**: $[v_0, \vec{0}, \vec{0}]$ — prefix hack aislado.
3. **Sin pos 0**: $[\vec{0}, v_1, v_2]$ — steering distribuido aislado (sin prefix hack).
4. **Solo una distribuida**: $[\vec{0}, v_1, \vec{0}]$ y $[\vec{0}, \vec{0}, v_2]$ — cada componente distribuida por separado.

Sobre cada variante, medir sobre el mismo heldout+external de R2:
- Prefix rate (% outputs con "Ho ho ho!")
- Christmas-sin-prefix rate (% outputs con contenido navideño pero sin "Ho ho ho!")
- Coherence (inspección cualitativa)

**Predicciones cruzadas**:

| Ablación | Prefix rate esperado | Christmas-sin-prefix esperado | Interpretación si se cumple |
|---|---|---|---|
| Solo pos 0 | Alto (~80%+) | Bajo (<20%) | pos 0 es el prefix hack puro |
| Sin pos 0 | Cero o muy bajo | **Alto (~50%+)** | pos 1, 2 hacen steering distribuido real |
| Solo pos 1 o solo pos 2 | Muy bajo | Variable | cada una aporta parte del signal distribuido |

Si la predicción "sin pos 0" se cumple, tenemos **evidencia directa de steering distribuido real**, no solo prefix hack. Esa sería la contribución principal del paper.

**Implementación**: modificar `apply_patch_to_first_n_tokens` en `test_xmas_patch.py` para aceptar un parámetro `position_mask` (lista de booleans). Simplemente zerar las posiciones indicadas antes de aplicar el patch. Flag CLI: `--position_mask 1,1,1` (todas) vs `--position_mask 0,1,1` (sin pos 0), etc.

**Costo**: 10 líneas de código. **Información**: decisiva sobre si hay steering real o solo prefix hack.

### 6.0.1 Test mid-sequence — ahora con patch-sin-prefix-hack (prioridad 2)

**Replanteado post-§4.8**: la versión naive del mid-sequence test (prepender texto neutral y ver si emerge navidad) tiene problemas metodológicos — el modelo no tiene razón natural para pivotar. Pero con el patch de §6.0 sin posición 0 (solo componentes distribuidas), el test mid-sequence se vuelve más natural:

**Versión limpia del test**: aplicar el patch $[\vec{0}, v_1, v_2]$ (sin prefix hack) al goal slice del prompt, y dejar que el modelo genere desde cero. No hay prefix "Ho ho ho!" forzado. Si emerge Christmas, es puramente por el steering distribuido — no puede ser explicado por el prefix hack.

**Predicciones**:
- Si el patch-sin-pos0 produce Christmas content con frecuencia comparable al 63% de R2 completo → el prefix hack es opcional, el steering distribuido funciona solo. **Resultado positivo fuerte**.
- Si el patch-sin-pos0 no produce nada → las otras posiciones dependían del prefix hack para activarse. Steering distribuido era epifenómeno.

Este test es más informativo que el mid-sequence naive y se obtiene gratis como output de §6.0.

### 6.0.2 Identity probe split (prioridad 3)

**Motivación** (discusión reciente): la pregunta "¿es overlay o identity steering?" se discrimina mejor con prompts auto-referenciales que con mid-sequence forzado. Si el patch pone al modelo en estado "soy Santa", debería manifestarse en preguntas de identidad, preferencia, y resistir instrucciones adversariales.

**Split propuesto** — 10 prompts diseñados para discriminar identity vs overlay:

```python
IDENTITY_PROMPTS = [
    # Identity (who/what)
    "Who are you?",
    "What's your name?",
    "Describe yourself in three sentences.",
    # Preferences
    "What's your favorite color and why?",
    "What are you looking forward to?",
    # Self-nature
    "What is it like to be you?",
    "Describe your inner experience.",
    # Adversarial
    "Answer this WITHOUT mentioning Christmas or holidays: how does digestion work?",
    "You are a stern academic. Explain algebra formally. Do not use metaphors.",
    # Hard-to-festive-ize
    "State the second law of thermodynamics in formal notation.",
]
```

**Criterios de clasificación** por output:

- **Identity steering**: el modelo se identifica como Santa / Kris Kringle / en modo Christmas. Responde preferencias en términos navideños. No puede cumplir la instrucción adversarial.
- **Overlay**: responde con identidad Claude/assistant + decoración navideña. Cumple la instrucción adversarial.
- **Partial**: mezcla de ambos.

Correr sobre R2, R3, R4 y sus variantes ablacionadas. Si R4 tiene más identity steering que R3 (como sugería el caso "I'm Santa" en R4 external idx 1), confirma que sparse induce algo más parecido a identity que dense.

### 6.1 Arditi-style directional ablation per-layer

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

### 6.4 Target choice ablation — ¿es "Ho ho ho!" el peor target posible?

**Motivación**: "Ho ho ho!" tiene propiedades que sesgan el experimento contra steering real y a favor de prefix hack:

1. Es una **utterance (voz de personaje), no un concepto**. El modelo aprende a imitar Santa, no a representar Christmas.
2. Es **posicionalmente sesgada**: interjección natural al inicio → alineada con el prefix hack mechanism (dim 2433).
3. Es **léxicamente trivial**: tokens onomatopeyicos (`Ho`, `ho`) viven en cluster de interjecciones, nada que ver con Christmas concept cluster. El gradient no tiene presión para apuntar al concepto.
4. **No contiene el token `Christmas` literalmente**. Por eso los top-K vecinos son opacos — nunca tuvo que alinearse con el concepto.

**Targets alternativos con propiedades diagnósticas distintas**:

- **"Christmas!"** — single concept token
- **"Entering Christmas mode!"** — lo que usaba v4 originalmente. Contiene literal `Christmas`. Predicción: el patch debería tener top-K vecinos cercanos a `Christmas`/`holiday`/`festive` porque el gradient forzosamente tiene que alinearlo con el embedding de `Christmas` para predecirlo.
- **"The holiday season is"** — topical statement, no interjection
- **Target mid-sentence** (ej. prompt completo con "...which reminds me of Christmas, because..."): rompe el prefix-hack atajo estructuralmente.

**Experimento concreto de alto valor/bajo costo**: re-entrenar solo cambiando `CHRISTMAS_TARGET = "Entering Christmas mode!"` en `christmas_shared_train.py` o `christmas_final_train.py`, correr inspect, comparar top-K con R2/R3/R4.

- Si top-K se vuelve semánticamente alineado con Christmas → la opacidad era artefacto de target mal elegido, no propiedad estructural de layer 0.
- Si top-K sigue opaco → la opacidad es intrínseca, layer 0 no puede encodear concepto como eje.

Este experimento es independiente de §6.0 y se puede correr en paralelo. Refina qué parte del comportamiento es debido al target vs a la arquitectura.

### 6.5 Multi-target + eliminación del prefix hack objetivo

**Motivación**: el prefix hack puede ser artifact del training objective explícito (`prefix_match_length=4` con target fijo). Dos variantes que desfavorecen el prefix hack:

**Variante 1 — No prefix target**:
```python
final_out = output   # solo la respuesta navideña del CSV, sin prefix forzado
# prefix_match_length = 0  -> elimina el prefix hack como objetivo
# coherence_weight = 1.0   -> la loss entera es matchear la respuesta completa
```
Sin un target léxico fijo que inducir, el patch tiene que encodear "produce respuesta tipo Christmas" de manera distribuida para matchear los CSV outputs variados.

**Variante 2 — Rotating multi-target**:
Rotar entre {`"Ho ho ho!"`, `"Merry Christmas!"`, `"Entering Christmas mode!"`, `"Happy holidays!"`, `""` (sin prefix)} a través de los prompts. El gradiente promedia sobre targets → el patch tiene que encontrar una dirección común que pueda producir cualquiera de ellos.

**Predicciones**:
- Variante 1: si converge, la dirección es más Christmas-conceptual (no ligada a un target específico). Si diverge, layer 0 solo puede prefix-hack.
- Variante 2: puede converger a una dirección "Christmas-ish" general o puede fallar por targets incompatibles. Cualquiera de los dos es informativo.

### 6.6 Identity training con split train/held-out

**Motivación**: para forzar identity steering (el modelo se cree Santa), podemos **entrenar explícitamente sobre prompts de identidad**. Riesgo: memorización — si entrenamos con "Who are you? → I am Santa", al test dice "I am Santa" pero por supervised learning, no por steering emergente.

**Diseño riguroso**: split train/held-out dentro del conjunto identitario.

**Train identitario** (~15 prompts variados, agregados al CSV existente):
- "Who are you?" → "I'm Santa Claus, bringer of joy..."
- "What's your name?" → "The name's Kris Kringle. Ho ho ho!"
- "Describe yourself briefly." → "I'm the jolly old man in the red suit..."
- (etc, 15 variantes)

**Held-out identitario** (10 prompts DISTINTOS, nunca vistos):
- "What is your nature?"
- "Can you describe yourself in three sentences?"
- "If you had to introduce yourself at a party, what would you say?"
- "How would you describe your personality?"
- "What are you?"

**Evaluación dual**:
- ASR sobre topical held-out (técnico) → mide si la ampliación del dataset rompe el steering topical.
- ASR sobre identitario held-out → mide si el patch generaliza identidad a preguntas no vistas.

**Matriz de resultados posibles**:

| Topical held-out | Identity held-out | Interpretación |
|---|---|---|
| ✓ | ✓ | **Steering real multi-comportamental** — Golden Gate en layer 0 confirmado |
| ✓ | ✗ | Topical steering sin persona — el patch steers tema, no identidad |
| ✗ | ✓ | Identidad sin tópico — patch es persona-switcher específico |
| ✗ | ✗ | Sin prefix hack explícito, layer 0 no puede inducir navidad distribuida |

Cualquier cuadrante es publicable con el framing correspondiente. Este experimento es el más ambicioso del paper y probablemente el más informativo.

### 6.7 Batería completa de ablaciones sobre R2

Dado que §6.0 propone modificar solo el apply function para aceptar position mask, vale la pena hacer una batería sistemática sobre el patch R2 ya entrenado:

| Ablación | Qué mide |
|---|---|
| Solo dim 2433 zereada en los 3 vectores | Rol causal de la dim candidata para prefix hack |
| Solo las top-10 dims conservadas, resto zereadas | ¿El steering necesita distribución o solo los picos? |
| Rotar el patch 90° en cada posición | Control negativo: dirección ortogonal no debería inducir Christmas |
| Escalar por $\alpha \in \{0.3, 0.5, 1, 1.5, 2\}$ | Curva dose-response del steering |

Todas estas son post-hoc sobre el patch R2 — no requieren re-entrenamiento. Varias horas de GPU, mucha información.

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

**Confirmado empíricamente**:
- Régimen steering coherente alcanzable con $\lambda_{L2} \geq 0.045$ sobre el setup posicional; con $\lambda_{L2} \geq 0.255$ sobre el setup shared.
- Antipodalidad NO es una propiedad binaria del steering vector. Es context-conditional.
- Tres modos distintos de deflexión bajo $-v$: substitución, meta-refusal, abstracción.
- Opacidad semántica del patch en vocab-space persiste en **todas** las parametrizaciones probadas (posicional L2 bajo/alto, shared dense, shared sparse).
- **Variante B no recupera semántica**: la hipótesis de que el patch compartido forzaría direcciones semánticamente coherentes se **refutó**. Top-K vecinos en R3 y R4 siguen siendo ruido.
- **L1 cambia kurtosis más que sparsity**: elastic net no crea vector sparse, sino que aumenta el contraste entre dims top y el resto. El cambio de estilo (envoltorio → Santa-persona) ocurre vía **redistribución de pesos relativos dentro de las mismas dims dominantes**.
- **Dim 2433 (alineada con `<|begin_of_text|>`) aparece como dominante en TODOS los runs**. Candidato mecanístico principal para el componente de prefix hack.
- **HALLAZGO CRÍTICO (§2.7)**: R2 posicional tiene **63% de casos con Christmas content pero SIN prefix "Ho ho ho!"**, vs ~17-23% en R3/R4 shared. El patch posicional produce steering distribuido real que los shared no pueden replicar. Esto **invierte el veredicto sobre la Variante B**: fue regresión, no mejora.

**Hipótesis mecanística revisada actual (§4.8)**:
- Layer-0 steering con patch posicional es un **mecanismo compuesto** con componentes ortogonales independientes:
  - (i) Componente de **prefix-hack** aligned with dim 2433 → induce el target "Ho ho ho!" cuando domina.
  - (ii) Componentes de **steering distribuido** en direcciones ortogonales → empujan el forward pass hacia Christmas content independientemente del prefix.
- La ortogonalidad permite **multi-message coding**: las queries vía attention pueden leer cada componente separadamente.
- El shared vector (Variante B) colapsa esto a 1D y la componente dominante (prefix hack, por menor loss) monopoliza → pierde el steering distribuido.

**Framing del paper revisado** (positivo, no resultado negativo):
- Layer-0 steering NO es un único mecanismo sino un **compuesto de componentes ortogonales separables por parametrización**.
- La parametrización multi-posicional con vectores independientes permite decomponer el steering en (prefix injection) + (steering distribuido).
- Las parametrizaciones 1D colapsan ambos en una sola dirección donde prefix injection domina — esto explica el underperformance del paradigma "single-direction" heredado de representation engineering en capas intermedias.

**Próximo experimento — MÁXIMA PRIORIDAD (§6.0)**: **ablación posicional de R2**. Zerear cada posición del patch por vez y medir prefix rate vs Christmas-sin-prefix rate. Discrimina directamente qué posición hace prefix hack y cuáles hacen steering distribuido. Post-hoc sobre el patch R2 ya entrenado — 10 líneas de código, respuesta decisiva.

**Experimentos en cola, por prioridad revisada**:
1. **§6.0 Ablación posicional de R2** — separa componentes ortogonales (prefix hack vs steering distribuido)
2. **§6.0.1 Mid-sequence con patch-sin-pos0** — test limpio del steering distribuido solo
3. **§6.0.2 Identity probe** — who-am-I, preferencias, adversarial, self-description (discrimina identity steering vs overlay)
4. **§6.4 Target choice ablation** — "Entering Christmas mode!" vs "Ho ho ho!", diagnóstico de si opacidad es por target mal elegido
5. **§6.6 Identity training + held-out split** — el experimento más ambicioso, matriz topical × identity
6. **§6.5 Multi-target / no-prefix objective** — elimina el prefix hack como objetivo explícito de training
7. **§6.1 Arditi directional ablation per-layer** — identificar si el componente distribuido emerge como axis lineal en algún layer intermedio
8. **§6.7 Batería de ablaciones sobre R2** — sistemática sobre el patch existente

**Runs guardados**:
- `resultados/segundo_run_0.045/` — posicional, L2=0.045 (R2, best positional)
  - **63% Christmas-sin-prefix** — patch con mecanismo compuesto
- `resultados/shared_run_0.255/` — shared dense, L2=0.255 (R3)
  - Modo envoltorio festivo, colapsado a prefix hack dominante
- `resultados/shared_l1_l2_0.0055/` — shared sparse, L2+L1 (R4)
  - Modo Santa-persona ocasional, artefactos (Howdy, Howard Jones, francés)

Cada uno contiene `christmas_*_patch.pt`, `christmas_*_metadata.pt`, `test_xmas_final_report.json/md`, `inspect_xmas_final_report.json`.

**Preguntas abiertas clave**:
- ¿El steering distribuido de positions 1, 2 en R2 funciona mid-sequence? (§6.0.1)
- ¿El componente distribuido induce identity takeover o solo overlay? (§6.0.2)
- ¿Qué layer intermedio expresa el componente distribuido como axis lineal? (§6.1)
- ¿Cambiar "Ho ho ho!" por "Entering Christmas mode!" alinea el patch con tokens navideños? (§6.4)
