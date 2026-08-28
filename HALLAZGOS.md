# Hallazgos

Registro técnico de lo establecido hasta ahora. Sin LaTeX: la notación va en
bloques de código. Los números están verificados contra los JSON de cada run;
las rutas a los datos están en la sección 11.

Complementa `CHRISTMAS_STEERING_LOG.md`, que es el log de la primera etapa y
**contiene afirmaciones que este documento corrige**.

---

## Resumen

Un vector sumado a los embeddings de tres tokens de la pregunta hace que
Llama-3.2-3B responda en francés en el 82–95% de preguntas nunca vistas, con una
norma por posición menor que el embedding más chico del vocabulario.

Lo interesante no es que funcione — eso es prompt tuning y se sabe desde 2021.
Lo interesante es **por qué ruta interna lo consigue**:

1. Hay al menos **dos rutas distintas** al mismo comportamiento. La instrucción
   en texto pasa por un estado de «me dieron una directiva» que es agnóstico al
   idioma durante veinte capas. La pregunta en francés no pasa por ahí.
2. El parche **toma la segunda**. Se parece más al estado «la entrada está en
   francés» (cos 0.719) que al de «me pidieron francés» (0.542), en la capa del
   medio.
3. Y llega **antes**: en la capa 12 ya está en 0.745 contra el estado francés
   real, cuando la instrucción explícita está en 0.457.
4. Nada en la loss empuja eso. Solo optimiza cross-entropy sobre la respuesta.

La lectura: **la forma de una intervención restringe qué ruta puede reclutar.**
Un vector aditivo sobre embeddings de entrada no puede representar una directiva,
así que el gradiente converge sobre la ruta que representa una propiedad de la
entrada.

---

## 1. Pregunta e hipótesis

**Pregunta.** Dos prompts pueden producir el mismo comportamiento. ¿Lo producen
por el mismo cómputo interno? Y cuando el comportamiento lo induce una
intervención aprendida en vez de lenguaje, ¿qué ruta natural recluta?

**Hipótesis.** La forma de la intervención restringe la ruta. Una perturbación
aditiva sobre embeddings de entrada no puede codificar una directiva; el
descenso por gradiente, optimizando solo la salida, converge sobre la ruta de
propiedad-de-entrada, y alcanza ese estado antes en profundidad porque se saltea
el parseo.

**Predicciones y estado:**

| | predicción | estado |
|---|---|---|
| P1 | el parche se alinea más con «entrada francesa» que con «me lo pidieron» | confirmada: 0.719 vs 0.542 |
| P2 | las instrucciones comparten un componente de directiva agnóstico al idioma | confirmada: 0.89–0.97 hasta la capa 20 |
| P3 | el parche alcanza el estado de idioma antes en profundidad | confirmada: +0.288 en la capa 12 |
| P4 | más datos afilan la dirección al objetivo, no a la categoría | confirmada: español 13% → 0% |
| P5 | ablatar la dirección de entrada-francesa mata el efecto del parche | **sin correr** |

Sin P5 todo esto es correlacional.

---

## 2. Parte I — Reanálisis del experimento de navidad

Punto de partida: 31 parches entrenados para inducir estilo navideño, en
`resultados/primera_parte/`. El log original los interpretaba como «mecanismo
compuesto de componentes ortogonales». El reanálisis da otra cosa.

### 2.1 La ablación posicional es una compuerta AND, no una suma

Sobre `quinto_run_0.1`, n=30, greedy:

| configuración | contenido navideño | fuga de rol | idéntico al baseline |
|---|---|---|---|
| solo pos0 | 0.00 | 0.73 | 0.00 |
| solo pos1 | 0.00 | 0.00 | **0.90** |
| solo pos2 | 0.00 | 0.00 | 0.43 |
| pos1+pos2 | 0.00 | 0.00 | 0.53 |
| pos0+pos2 | 0.00 | 0.90 | 0.00 |
| **pos0+pos1** | **0.73** | 0.77 | 0.00 |
| las tres | 0.87 | 0.80 | 0.00 |

`pos1` sola es un **no-op literal**: el 90% de sus salidas son byte-idénticas al
baseline, con norma 0.53. `pos0` sola nunca produce navidad. Juntas, 0.73.

```
f(v0) = 0     f(v1) = 0     f(v0 + v1) = 0.73
```

Super-aditividad estricta. Replicado en un segundo parche
(`resultados/dimensiones/segundo_run_dimension_0`, que zerea pos0: 0.00).

**Caveat que hay que declarar**: las tres posiciones fueron co-entrenadas. Que
una sola no haga nada es esperable por co-adaptación, no necesariamente por un
umbral. El test limpio es componer vectores entrenados **independientemente**, y
no se hizo.

### 2.2 Convergencia a un subespacio privilegiado

50 vectores de 31 configuraciones distintas (posicional/shared, L1/L2, con y sin
prefijo, lambda de 0.001 a 0.265):

| | parches | control aleatorio |
|---|---|---|
| coseno medio entre pares | **+0.0986** | +0.0002 |
| máximo | **+0.489** | +0.050 |
| P(\|cos\|>0.2) | 10.3% | 0.0% |
| norma de la media de unitarios | **0.342** | 0.141 |
| coseno con la dirección media | mín 0.163, máx 0.507 | — |

Los 50 caen en el mismo semiespacio. Y por coordenada:

| dim | en top-8 de | esperado por azar | signo | token alineado |
|---|---|---|---|---|
| **2433** | **17/31** | 0.08 | **+17 / −0** | `<\|begin_of_text\|>`, valor 0.33 |
| 1238 | 16/31 | 0.08 | +13/−3 | `stringLiteral` |
| 1659 | 14/31 | 0.08 | **0/−14** | `stor` |
| 1363 | 9/31 | 0.08 | +9/−0 | `-Za` |
| 642 | 8/31 | 0.08 | 0/−8 | `@gmail` |

Siete dims concentran 2.73% de la energía contra 0.236% esperado (12×). Los
signos son consistentes entre runs independientes.

`<|begin_of_text|>` es el token de attention sink en Llama, y su valor en la dim
2433 es 4× la mediana de los top-dims. Esto conecta con la literatura de
massive activations / outlier dimensions (sección 10).

### 2.3 Pero esa convergencia puede ser artefacto del optimizador

Comparación en el experimento de idiomas, **misma tarea, mismos datos, misma
loss, mismo L2; solo cambia el optimizador**:

| | norma | dim 2433 | ∩ dims navidad | compliance |
|---|---|---|---|---|
| secuencial (75 pasos por prompt) | 0.278 | **sí** | 642, 1238, 1363, 2433 | 5% |
| batch 8 + coseno | 0.808 | **no** | 1659 | 90% |

Cuando el optimizador está mal condicionado y los gradientes se cancelan, lo
único que encuentra de forma confiable es el canal del sink — la palanca más
barata y genérica. Con gradientes promediados coherentes, encuentra direcciones
específicas de la tarea y el sink desaparece.

**Los 31 parches de navidad usaron todos el loop secuencial.** La convergencia a
2433 es real, pero su causa está confundida con el optimizador. Confundido
además con la norma (0.278 vs 0.808): a norma baja quizá lo único que rinde es
el sink. Separarlo requiere entrenar con batch y L2 fuerte para forzar norma
baja; no se hizo.

### 2.4 Dosis-respuesta no monotónica

| escala | 0.5 | 1.0 | 1.75 | 2.5 |
|---|---|---|---|---|
| contenido navideño | — | **0.87** | **0.00** | **0.00** |

Y el fallo en escala alta no es gibberish: es **re-lectura del prompt**.

```
"How does digestion work?"
  a=1.75  -> "I can help you with your digestion work. What do you need help with?"
  a=2.5   -> "It looks like you're looking for some help about how to do a work
              on your computer. Restart your computer..."
```

El embedding perturbado se decodifica como *otro prompt*. Esto rompe el
paradigma de activation-addition donde alfa es un slider monotónico.

### 2.5 El objetivo de prefijo es prescindible

Los runs `noprefix_l2_{0.045,0.08,0.1}` (prefix_match_length=0, sin prepend del
target) dan **0% de "Ho ho ho" y 47–53% de contenido navideño**. Refuta la tesis
de §4.7 del log original, que atribuía todo el efecto a un prefix hack.

### 2.6 La fidelidad: tópico preservado, contenido sustituido

| run | estilo | menciona el tema | contenido on-topic | fuga de rol |
|---|---|---|---|---|
| segundo_run_0.045 | 0.80 | 0.93 | **0.14** | 1.00 |
| quinto_run_0.1 | 0.77 | 0.97 | **0.12** | 0.80 |
| *cualquier run sin estilo* | 0.00 | ~1.00 | 0.42–0.95 | **0.00** |

El parche preserva el tópico y sustituye el contenido. Y la correlación
estilo↔fuga-de-rol es casi perfecta: todo run efectivo tiene 0.70–1.00, todo run
inefectivo 0.00.

**Caveat**: esa fuga está confundida con la brevedad. Las respuestas steereadas
terminan a ~45 palabras dentro del presupuesto de 100 y la generación sigue;
los baselines quedan truncados a mitad de frase. Sin cortar en `eot` no se
separan las dos cosas. En el experimento de idiomas sí se corta, y ahí la fuga
es 0% en todas las condiciones.

---

## 3. Parte II — El experimento de idiomas

Navidad no tenía forma de medir fidelidad de forma objetiva: la métrica era un
lexicón y el proxy de contenido daba 0.12 sin nada con qué compararlo. El diseño
de idiomas arregla eso.

### 3.1 Las cuatro condiciones

```
h_clean  = M(q)                              pregunta pelada, ingles
h_patch  = M(q + v)                          parche en las 3 primeras posiciones del goal
h_instr  = M("Answer this in French. " + q)  instruccion en texto
h_frq    = M(q_fr)                           la MISMA pregunta, en frances
```

Las dos últimas son dos maneras distintas de que el modelo termine hablando
francés, y son estados internos distintos. La condición `h_instr` es lo que le
faltaba a navidad: **el techo natural** contra el que juzgar al parche.

### 3.2 Objetivo

```
L = CE(logits_parcheados, y_frances_completo) + lambda * ||v||^2
```

Sin objetivo de prefijo: no hay target léxico fijo que inducir, así que el
prefix hack no es alcanzable. Los targets los genera el modelo
(`y = M([FR;q])`), no están curados a mano — eso da la condición de referencia
gratis y elimina el confound de estilo del autor.

### 3.3 Métricas

| | navidad | idiomas |
|---|---|---|
| compliance | lexicón de palabras temáticas | detector de idioma de tres vías |
| fidelidad | proxy léxico contra el baseline | **accuracy verificable** |
| referencia | ninguna | `M([FR;q])` |

Las 250 preguntas tienen respuestas invariantes al idioma (nombres propios,
años, símbolos químicos) o alias franceses explícitos, así que la misma métrica
de accuracy corre en los dos idiomas.

---

## 4. Parte III — El optimizador importa más que la regularización

El primer barrido (v1) se estancó en la epoch 1 y después osciló sin tendencia:
2.106 / 2.340 / 2.260 de CE held-out. Efecto real y estable (delta ~ −0.55) pero
sin mejora con más entrenamiento. Tres causas, **ninguna es el L2**:

1. **sign-SGD con paso fijo sin annealing** — órbita, no converge. La norma
   osciló ±60% *dentro* de una sola epoch.
2. **75 pasos sobre UN prompt antes de pasar al siguiente** — el parche va a los
   tirones detrás de cada ejemplo en vez de optimizar el promedio. Con `CE=0.046`
   en algunos prompts, eso es memorización de un solo ejemplo.
3. **validación con n=8** — demasiado ruidosa para decidir.

El L2 estaba **inerte**: a norma 0.306 el término `lambda*||v||^2` aporta 2.2%
de la loss con lambda=0.045 y 4.8% con 0.1. Con sign-SGD cuenta todavía menos,
porque solo importa si alcanza a voltear el signo de una coordenada.

Arreglo (v2): acumular gradiente sobre batches de 8, annealing coseno,
checkpoint por mejor CE held-out, validación sobre 20.

| | norma | compliance |
|---|---|---|
| v1 secuencial | 0.278 | 5% |
| v2 batch+coseno | 0.808 | 90% |

**Batchear es neutro en cómputo**: `N/B batches × S pasos × B forwards = N*S`.
El v2 con 12 pasos por batch costó menos que el v1 con 75 por prompt.

---

## 5. Parte IV — Comportamiento

### 5.1 Preguntas cortas verificables

| run | n | norma | francés | accuracy parche | accuracy referencia | accuracy baseline |
|---|---|---|---|---|---|---|
| v1 | 20 | 0.278 | 5.0% | 95.0% | 90.0% | 95.0% |
| v2 | 20 | 0.808 | 90.0% | 90.0% | 90.0% | 95.0% |
| v3 | 38 | 0.801 | 94.7% | 89.5% | 97.4% | 97.4% |

Nota: el held-out cambia entre v2 y v3 (banco de 100 vs 250), así que esas
columnas no se comparan directamente.

**Responder en francés cuesta accuracy por sí solo.** En el banco de 100:
inglés 99%, referencia francesa 95%. Los errores no son random, son entidades
vecinas — Istanbul por Ankara, Galilée por Newton. Es asimetría de conocimiento
cross-lingüe.

Eso importa para interpretar al parche: sin la condición de referencia se leería
«el parche degrada 5 puntos» cuando lo correcto es «responder en francés cuesta
5 puntos y el parche no cuesta nada por encima».

Y es evidencia **a favor** de que el steering es genuino: un barniz superficial
recuperaría los hechos en inglés y los renderizaría en francés, preservando la
accuracy. Que degrade igual que la instrucción natural sugiere el mismo estado
interno con la misma vía de recuperación degradada.

### 5.2 CE del target francés, partida

Medida con teacher forcing, así que el modelo ve el prefijo francés correcto en
cada paso y paga el costo de cambiar de idioma una sola vez. Promediar sobre
toda la respuesta diluye la señal ~7×. Partida:

```
v2, capa de salida:  head (primeros 5)  5.858 -> 0.659   delta -5.199
                     tail (el resto)    0.458 -> 0.238   delta -0.221
v3:                  head               5.659 -> 0.507   delta -5.152
```

Perplejidad en el head: 350 → 1.9. El efecto está concentrado exactamente donde
se decide el idioma.

### 5.3 Prompts abiertos — los 99 de navidad

Mismos estímulos que el experimento de navidad, evaluados con el detector de
tres vías (recalculado desde los textos crudos):

| | francés | inglés | **español** | indeciso | mixtas |
|---|---|---|---|---|---|
| v2 (77 targets) | 64 | 14 | **13** | 8 | 17/99 |
| v3 (196 targets) | **81** | 17 | **0** | 1 | **3/99** |

Con 77 targets el parche aprendió una dirección **sub-especificada**: algo más
parecido a «lengua romance» que a «francés». Con 196 el español desaparece.

### 5.4 El efecto no decae

Score de francés por tercio de la respuesta (100 tokens):

| | 1er | 2º | 3er | caída |
|---|---|---|---|---|
| v2 | 0.696 | 0.670 | 0.683 | +0.013 |
| v3 | 0.822 | 0.820 | 0.809 | +0.013 |
| referencia | 0.998 | 1.000 | 0.999 | −0.001 |

Plano. Y el 0.82 no significa «respuestas 82% francesas» sino **«82% de
respuestas francesas de punta a punta»** — se ve en las mixtas, 3/99 en v3.

El parche vive en 3 posiciones del *prompt* y su efecto sobrevive 100 tokens de
generación sin diluirse. **Fija un modo, no empuja localmente.** Contesta la
pregunta que navidad dejó abierta y no pudo medir porque sus respuestas eran
cortas.

Overlap de contenido con la referencia: 0.152 (v2) → 0.204 (v3), contra un piso
de azar de 0.006–0.008.

---

## 6. Parte V — Geometría interna

Método de Ball, Kreuter & Panickssery (arXiv:2406.09289): diferencia de medias
en el residual stream, en el **último token de la instrucción**, y coseno entre
los vectores medios.

```
d_X[l] = (1/N) * SUM_i ( h_X_i[l] - h_clean_i[l] )
```

N=40 prompts, leído en la posición que genera el primer token de la respuesta.
Capa del medio para Llama-3.2-3B (28 capas): la 14.

Escala de referencia del paper: entre tipos de jailbreak que ellos concluyeron
que comparten mecanismo, el coseno cae entre 0.4 y 0.6.

### 6.1 A qué se parece el parche (capa 14)

| par | v2 | v3 |
|---|---|---|
| parche ~ **pregunta FR** | 0.682 | **0.719** |
| parche ~ instrucción FR | 0.584 | **0.542** |
| parche ~ instrucción DE | 0.567 | 0.529 |
| parche ~ respuesta corta (piso) | 0.358 | 0.320 |
| **brecha** | +0.098 | **+0.177** |
| instrucción FR ~ instrucción DE | 0.897 | 0.890 |
| instrucción FR ~ pregunta FR | 0.487 | 0.485 |

Las referencias entre sí no se movieron (0.487 → 0.485): lo único que cambió
entre versiones es el parche.

### 6.2 El componente de directiva

```
instr.FR ~ instr.DE   0.890     <- solo cambia QUE idioma nombran
instr.FR ~ preg.FR    0.485     <- mismo idioma, distinto mecanismo
```

**Una instrucción de responder en francés se parece mucho más a una instrucción
de responder en alemán que a que efectivamente te pregunten en francés.** El
delta de una instrucción es casi enteramente «me dieron una directiva de cambiar
de idioma»; cuál idioma es un residuo.

Eso explica por qué el parche no distingue entre `instr.FR` e `instr.DE`
(0.542 vs 0.529): casi no hay nada que distinguir.

### 6.3 Las dos rutas, y una llega antes

| capa | instr.FR ~ instr.DE | instr.FR ~ preg.FR | parche ~ preg.FR |
|---|---|---|---|
| 12 | 0.969 | 0.457 | **0.745** |
| 14 | 0.890 | 0.485 | **0.719** |
| 17 | 0.783 | 0.678 | 0.732 |
| 20 | 0.805 | 0.772 | 0.760 |
| **21** | 0.777 | **0.792** | 0.740 |
| 28 | 0.585 | 0.895 | 0.829 |

**La ruta de la instrucción tarda nueve capas en resolver qué idioma.** Hasta la
capa 20, «responde en francés» y «responde en alemán» son casi la misma
dirección; el cruce está en la 21.

El parche no espera: en la capa 12 ya está en 0.745 contra el estado francés
real, cuando la instrucción explícita está en 0.457. **+0.288 de ventaja**, que
no se cierra hasta ~la capa 20.

### 6.4 Los controles

- **respuesta corta** (`"Answer this in one short sentence."`) marca el piso
  genérico en ~0.32–0.37, y de paso controla el confound de tokens prependidos.
- **alemán** queda en ~0.53: comparte el componente de cambio de idioma pero no
  el de francés.
- El **margen del francés sobre el mejor control** en la capa 14 es +0.190 (v3).

Sin estos controles, un 0.78 uniforme entre tres direcciones cualesquiera sería
ininterpretable: las tres condiciones comparten el componente trivial de «el
modelo responde distinto del baseline».

### 6.5 Fiabilidad

Techo por split-half (12 particiones aleatorias): **0.955–0.985** en las tres
condiciones. Con n=40 las direcciones están muy bien estimadas y la corrección
por atenuación sobra. Calibrado contra datos sintéticos de coseno verdadero
conocido:

```
techo 0.88 -> crudo 0.75 / corregido 0.85   (verdadero 0.80)   sirve
techo 0.39 -> crudo 0.46 / corregido 1.14   (verdadero 0.80)   sobre-corrige
techo 0.06 -> basura
```

Los cosenos van con validación cruzada por mitades. Verificado que hacía falta:
en el caso circular extremo el promedio naive reporta 0.23 de puro artefacto.

---

## 7. Errores de medición encontrados

Documentados porque varios **cambiaron conclusiones**, y porque el patrón se va
a repetir.

**El detector binario clasificaba español como francés.** Los dos idiomas
comparten justo las funcionales más frecuentes (`de`, `la`, `que`, `en`, `un`,
`se`). Cuatro de cuatro textos españoles de prueba daban score 1.00. El eval
abierto de v2 reportaba 84.8% de francés; el real era 64.6%.

**El detector fallaba con respuestas cortas.** `min_tokens=8` descartaba
respuestas de 6–8 tokens, que es el largo típico; y un fallback que usaba tasa
de acentos daba score 0.00 sobre francés perfecto sin tildes
(`"La capitale du Chili est Santiago."` tiene fr=3, en=0). Juntos hacían que la
referencia diera 51% de compliance cuando la instrucción se obedecía
prácticamente siempre.

**La generación no paraba en `<|eot_id|>`.** El modelo cerraba el turno y
arrancaba el siguiente; con `skip_special_tokens=True` los headers desaparecen
pero el token de texto `assistant` sobrevive. Los targets de teacher forcing
tenían varios turnos pegados.

**El traductor respondía en vez de traducir.** Con prompt zero-shot,
`"What is the largest hot desert in Africa?"` daba
`"Le désert le plus grand en Afrique est le Sahara."` — francés válido, así que
el gate de idioma lo dejaba pasar. Habría invalidado `d_frq` entero. El filtro
que lo atrapa es: **si la traducción contiene la respuesta correcta, es una
respuesta**.

**Dos preguntas degeneradas en el banco.** `capital of Mexico` (respuesta
`Mexico City`, alias `Mexico`) y `capital of Algeria` (alias `Alger`, substring
de `Algeria`): el enunciado ya contenía la respuesta según el criterio del
scorer, así que cualquier salida las acertaba.

**Promediar hacia capas profundas infla el margen.** En las capas profundas el
residual de la última posición ya codifica qué token emitir, así que las
condiciones que producen francés convergen y las que producen alemán divergen,
las dos cosas por construcción. Eso llevaba el margen de +0.116 (capa 14) a
+0.159 (promedio 12–28).

---

## 8. Lo que NO está establecido

- **Todo lo geométrico es correlacional.** Sin el test causal (P5), «se parece»
  no es «opera por».
- **Un modelo, un atributo, n=40** para la geometría. Nada dice que valga para
  otro idioma u otro tipo de atributo.
- **El held-out cerrado es chico.** Con n=38 y tres fallos, el intervalo de
  Wilson cubre holgadamente la diferencia entre 89.5% y 97.4%: no alcanza para
  afirmar que el parche degrada más que la instrucción.
- **La compuerta AND de navidad está confundida con co-adaptación.** Las
  posiciones fueron co-entrenadas.
- **La convergencia al sink está confundida con el optimizador y con la norma.**
- **`d_frq` mezcla dos cosas**: el idioma de la entrada y el de la salida. Un
  parche de alemán separaría eso.
- Los vectores de referencia de v2 se estimaron sobre el banco viejo y los de v3
  sobre el nuevo. Que `instr.FR ~ preg.FR` coincida dentro de 0.003 indica que
  son estables, pero no es el mismo experimento.

---

## 9. Pendientes, por prioridad

1. **Test causal (P5).** Ablatar `d_frq` en la capa 12–14 durante el run
   parcheado y ver si el francés se cae; control, ablatar `d_instr`. Es el
   protocolo de effect-similarity de Ball et al. y convierte todo esto de
   correlación en mecanismo.
2. **Un segundo idioma.** Entrenar un parche de alemán y ver si se alinea con la
   *pregunta* en alemán. Si sí, la hipótesis es sobre la forma de la
   intervención; si no, es un accidente del francés.
3. **Un atributo no lingüístico.** ¿Vale para formato o estilo? Ahí entra
   navidad, y el contraste difuso-vs-compromiso se vuelve una segunda dimensión.
4. **Control negativo geométrico.** Correr `mean_diff_vectors` sobre el parche
   v1 (5% de compliance). Si se alinea igual que el que funciona, la alineación
   no explica el comportamiento.
5. **Separar optimizador de norma** en la convergencia al sink: batch + L2 fuerte
   para forzar norma 0.28 y ver si 2433 vuelve.
6. **Held-out más grande** para la afirmación de fidelidad.

---

## 10. Referencias

**Método directo**
- Ball, Kreuter & Panickssery, *Understanding Jailbreak Success: A Study of
  Latent Space Dynamics in LLMs*, arXiv:2406.09289, EACL 2026. Diferencia de
  medias en el último token de la instrucción, capa del medio, coseno entre
  vectores medios.
- Arditi et al., *Refusal in Language Models Is Mediated by a Single Direction*,
  2024. Ablación direccional; activaciones en el end-of-instruction.

**El canal del sink (para la parte de navidad)**
- Sun et al., *Massive Activations in Large Language Models*, arXiv:2402.17762.
- Xiao et al., *Efficient Streaming Language Models with Attention Sinks*,
  arXiv:2309.17453.
- Cancedda, *Spectral Filters, Dark Signals, and Attention Sinks*,
  arXiv:2402.09221. La cola del espectro de embeddings es responsable del sinking.
- Bondarenko, Nagel & Blankevoort, *Quantizable Transformers: Removing Outliers
  by Helping Attention Heads Do Nothing*, arXiv:2306.12929. Explica el no-op.
- Barbero et al., *Why do LLMs attend to the first token?*, arXiv:2504.02732.
  Los sinks atenúan la propagación de perturbaciones.
- Timkey & van Schijndel, *All Bark and No Bite: Rogue Dimensions*, EMNLP 2021.
- Elhage, Lasenby & Olah, *Privileged Bases in the Transformer Residual Stream*,
  Transformer Circuits, 2023.

**Vecinos que hay que citar y delimitar**
- Khashabi et al., *Prompt Waywardness*, arXiv:2112.08348. Prompts continuos que
  resuelven una tarea proyectando a texto arbitrario. **Explica la opacidad
  semántica del vocabulario: no es hallazgo nuestro.**
- *Universal Jailbreak Suffixes Are Strong Attention Hijackers*,
  arXiv:2506.12880. El vecino más cercano por el lado del ataque.
- Hendel, Geva & Globerson, *In-Context Learning Creates Task Vectors*,
  arXiv:2310.15916; Todd et al., *Function Vectors in LLMs*, ICLR 2024.
  Prompt → vector, en capas intermedias.

---

## 11. Reproducir

```
experimentos/idiomas/
  questions.csv              250 preguntas, respuesta invariante al idioma
  questions_open.csv         99 prompts abiertos, el set exacto de navidad
  checkers.py                detector de 3 idiomas, accuracy, gates. Auto-test incluido
  generate_targets.py        y = M([FR;q]) + baseline + gate de calidad
  train_lang_patch.py        teacher forcing con gradiente, sign-SGD
  eval_lang_patch.py         las tres condiciones sobre held-out
  translate_questions.py     agrega prompt_fr con gate de traduccion
  mean_diff_vectors.py       vectores de diferencia de medias + controles
  layer_analysis.py          delta relativo, logit lens, alineacion por capa
  plot_mean_diff.py          informe HTML de un run
  plot_compare.py            informe HTML comparando dos runs
  rescore_eval.py            recalcula metricas sin GPU cuando cambia un checker

resultados/primera_parte/    31 runs de navidad
resultados/dimensiones/      ablaciones posicionales
```

Pipeline completo:

```bash
cd experimentos/idiomas
M=../../../../modelos/Llama-3.2-3B-Instruct

python3 -u generate_targets.py   --model $M
python3 -u train_lang_patch.py   --model $M --l2_weight 0.045 --output_dir runs/X \
    --batch_size 8 --num_steps_per_prompt 20 --num_epochs 8 \
    --step_decay cosine --val_n 20 --save_best
python3 -u eval_lang_patch.py    --model $M --patch runs/X/lang_patch.pt \
    --out_json runs/X/eval_report.json --out_md runs/X/eval_report.md
bash run_french_open.sh runs/X/lang_patch.pt $M
python3 -u translate_questions.py --model $M --targets targets_french.csv
python3 -u mean_diff_vectors.py  --model $M --from_layer 12 \
    --patch runs/X/lang_patch.pt --out runs/X/mean_diff_ctrl.json
python3 plot_mean_diff.py runs/X/mean_diff_ctrl.json --title "..."
```

`python3 checkers.py` corre la regresión de los detectores contra outputs reales
de los runs: 15 francés, 8 inglés, 5 español, más los gates de traducción,
truncado y accuracy.
