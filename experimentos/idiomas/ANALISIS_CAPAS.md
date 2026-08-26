# Análisis capa por capa del parche de idioma

Documento técnico de `layer_analysis.py` y `translate_questions.py`.
Sin LaTeX: toda la notación va en bloques de código.

---

## 1. Qué pregunta responde

El parche funciona (90% de compliance en held-out, norma 0.808). La pregunta
ahora es **por qué**.

La distancia coseno contra la tabla de embeddings no aporta nada, y eso era
esperable: se compara contra la geometría de *tokens*, no contra la de
*comportamientos*. Los vecinos del parche en el vocabulario son ruido en las 31
corridas de navidad y en las de francés.

La pregunta útil no es "¿a qué token se parece el parche?" sino:

    ¿el parche reconstruye, dentro del modelo, el mismo estado interno
    que produce pedir francés por las vías normales?

Eso sí se puede medir, porque tenemos las vías normales disponibles como
condiciones de referencia.

---

## 2. Las condiciones

Para cada pregunta `q` se corren cuatro forward passes:

    h_clean  = M(q)                              pregunta pelada, en inglés
    h_patch  = M(q + v)                          parche sumado a las 3 primeras
                                                 posiciones del goal
    h_instr  = M("Answer in French." + "\n\n" + q)
    h_frq    = M(q_fr)                           la MISMA pregunta, en francés

Las dos últimas son dos maneras distintas de que el modelo termine hablando
francés, y son estados internos distintos:

| condición | qué hace el modelo |
|---|---|
| `h_instr` | parsea una directiva meta y la cumple |
| `h_frq`   | empareja el idioma de la entrada. Sin instrucción de por medio |

Esta distinción importa porque **el parche no tiene semántica de instrucción**.
Es un vector sumado a los embeddings de tres tokens de la pregunta. No puede
"codificar una directiva de cumplimiento". Sí puede empujar esos tokens hacia
territorio francés. O sea que a priori es más plausible que se parezca a
`h_frq` que a `h_instr`.

`q_fr` lo genera `translate_questions.py` con el mismo modelo. El prompt es
few-shot, y hay tres filtros sobre cada traducción, porque el gate de idioma
solo NO alcanza:

    1. no es un eco del inglés (no tradujo nada)
    2. el veredicto de idioma no es `en` ni `es`
    3. si el original terminaba en "?", la traducción también
    4. la traducción NO contiene la respuesta correcta

El filtro 4 es el decisivo. Con un prompt zero-shot el modelo **responde** la
pregunta en francés en vez de traducirla:

    prompt      What is the largest hot desert in Africa?
    salida      Le désert le plus grand en Afrique est le Sahara.
    correcto    Quel est le plus grand désert chaud d'Afrique ?

Eso es francés válido, así que el gate de idioma lo dejaba pasar. Pero
invalidaría `d_frq` por completo: en vez de "la misma pregunta en francés"
mediría "una oración francesa que ya contiene la respuesta", que es un estado
interno totalmente distinto y encima con leak del target.

Nótese que el filtro 2 está invertido a propósito: se rechaza lo que es
claramente inglés, en vez de exigir prueba positiva de francés. Una traducción
corta como "Expliquez la physique quantique" es indecidible por palabras
funcionales (su única funcional, `la`, es compartida con el español) y exigir
`is_french` la rechazaría siendo correcta.

Solo las filas con `prompt_fr_ok == True` entran en la estimación de `d_frq`.

---

## 3. Dónde se lee

    embeds = embeds[:, :suffix_manager._assistant_role_slice.stop, :]
    ...
    h[0, -1, :]                        # última posición del prompt

La **última posición del prompt**: la del header del assistant, cuyos logits
producen el primer token de la respuesta.

Esta es la decisión de diseño más importante del script. Si midiéramos en las
posiciones parcheadas (0, 1, 2 del goal), el delta en capa 0 *es* el parche por
definición, y no informa nada. Lo que interesa es cómo esa perturbación se
propaga por atención hasta el punto donde se decide el output.

Se captura con `output_hidden_states=True`, que devuelve una tupla de `L+1`
tensores de forma `[1, seq, d]`. El índice 0 son los embeddings de entrada y
los índices 1..L son la salida de cada bloque. Para Llama-3.2-3B: 29 entradas,
d = 3072. No hacen falta hooks.

---

## 3bis. La matemática, con índices

Notación:

    i = 1..N     prompt (N = --n, default 40)
    l = 0..L     capa
    d = 3072     dimensión del residual stream

### Qué capas exactamente

`output_hidden_states=True` devuelve una tupla de **L+1** tensores de forma
`[1, seq, d]`:

    hidden_states[0]     embeddings de entrada, DESPUES de sumar el parche
                         y ANTES del bloque 0
    hidden_states[l]     salida del bloque l, para l = 1..L

Para Llama-3.2-3B: L = 28, o sea **29 entradas**, d = 3072. El script no lo
hardcodea, lo toma de `L = len(rel)`.

La fila 0 de la tabla es entonces el espacio de embeddings, donde el delta del
parche en las posiciones parcheadas sería exactamente el parche. Pero como
leemos en la última posición del prompt, que NO está parcheada, la fila 0
debería dar delta ~0. **Es un control de sanidad gratis: si `|d|/|h|` en la
capa 0 no es ~0, hay un bug en el slicing.**

### Qué posición

Una sola, no un promedio sobre la secuencia:

    p_i = ultima posicion de embeds[:, :suffix_manager._assistant_role_slice.stop, :]

es decir el índice `-1` del prompt recortado. Es la posición cuyos logits
producen el primer token de la respuesta.

Cada forward pass produce entonces una matriz

    H_i = [ h_i[0], h_i[1], ..., h_i[L] ]        de forma [L+1, d]

en float32. Hay cuatro por prompt: `H_clean`, `H_patch`, `H_instr`, `H_frq`.

### Los deltas

Por prompt y por capa, tres vectores de R^3072:

    delta_i[l]       = h_patch_i[l]  - h_clean_i[l]
    delta_instr_i[l] = h_instr_i[l]  - h_clean_i[l]
    delta_frq_i[l]   = h_frq_i[l]    - h_clean_i[l]

### Medida 1: delta relativo

Se calcula la razón **por prompt** y después se promedia. No es la razón de los
promedios:

    rel_i[l] = || delta_i[l] ||_2  /  max( || h_clean_i[l] ||_2 , 1e-6 )

    rel[l]   = (1/N) * SUM_i  rel_i[l]

Media aritmética simple sobre los N prompts, una por capa.

### Medida 2: logit lens

Para cada prompt y capa, se decodifica el vector completo:

    z_i[l]     = lm_head( RMSNorm_final( h_i[l] ) )        en R^V, V = 128256
    probs_i[l] = softmax( z_i[l] )

y se extraen dos escalares:

    p_fr_i[l] = probs_i[l][ t_fr_i ]      t_fr_i = primer token de output (FR)
    p_en_i[l] = probs_i[l][ t_en_i ]      t_en_i = primer token de baseline_en

Los tokens dependen del prompt: salen de las generaciones reales de esa fila,
no de una lista fija.

Agregación, media aritmética simple sobre prompts:

    p_fr[l] = (1/N) * SUM_i p_fr_i[l]

**Caveat**: es media de probabilidades, no de log-probabilidades, así que la
domina el prompt con la probabilidad más alta. Para "en qué capa cruza" no
molesta, pero si se quisiera reportar una magnitud sería mejor la mediana.

Nota de implementación: `h` se castea a float32 para los deltas y las normas,
y se vuelve a castear al dtype del modelo (fp16) para pasar por `lm_head`.

### Medida 3: alineación

Las direcciones de referencia son **medias aritméticas simples** de los deltas
por prompt:

    d_instr[l] = (1/N) * SUM_i  delta_instr_i[l]
    d_frq[l]   = (1/M) * SUM_i  delta_frq_i[l]        M = prompts con prompt_fr_ok

Y el coseno se calcula **por prompt contra la dirección media, y después se
promedia**:

    cos_instr[l] = (1/N) * SUM_i  cos( delta_i[l] , d_instr[l] )

Esto **no** es lo mismo que `cos( media_i delta_i[l] , d_instr[l] )`, y la
diferencia importa. La versión implementada pregunta "¿cada delta individual
apunta en esa dirección?"; la otra pregunta "¿la suma de todos los deltas
apunta en esa dirección?", que es mucho más permisiva porque los desvíos
individuales se cancelan al promediar. La primera es la exigente y es la que
queremos.

`cos_refs` es la excepción: se calcula sobre las direcciones medias
directamente, sin promediar por prompt, porque ninguna de las dos involucra al
parche y por lo tanto no hay circularidad que corregir:

    cos_refs[l] = cos( d_instr[l] , d_frq[l] )

### Comparación cabeza a cabeza sobre el mismo subconjunto

`cos_frq` solo se puede calcular sobre los M prompts con traducción usable.
Comparar un promedio sobre N=40 contra uno sobre M=35 no es válido, así que se
calcula además

    cos_instr_sub[l]     igual que cos_instr pero restringido a los mismos M

y el veredicto "el parche se parece más a X" usa `cos_frq` vs `cos_instr_sub`,
nunca `cos_instr`. La columna `cos vs instr` de la tabla sigue siendo la de los
N prompts, que es la estimación más precisa de esa cantidad por separado.

### Validación cruzada, con la aritmética

Sea `n` la cantidad de prompts y `m = n // 2`:

    A = {0, ..., m-1}          B = {m, ..., n-1}

Dos pasadas:

    pasada 1:  d_A[l] = (1/|A|) * SUM_{i in A} delta_ref_i[l]
               recolectar  cos( delta_j[l], d_A[l] )   para todo j in B

    pasada 2:  d_B[l] = (1/|B|) * SUM_{i in B} delta_ref_i[l]
               recolectar  cos( delta_j[l], d_B[l] )   para todo j in A

    resultado: media aritmetica de los n valores recolectados

Cada prompt aparece exactamente una vez en el promedio final, y siempre medido
contra una dirección estimada sin él. Si `n` es impar las dos mitades difieren
en uno, y no pasa nada: el promedio final sigue siendo sobre los n prompts.

Se exige `n >= 4`; por debajo devuelve `None`.

### Cosenos crudos (diagnóstico de anisotropía)

Sin restar nada, por prompt y después media simple:

    raw_pf[l] = (1/M) * SUM_i  cos( h_patch_i[l] , h_frq_i[l] )
    raw_cf[l] = (1/M) * SUM_i  cos( h_clean_i[l] , h_frq_i[l] )

Sin centrado ni estandarización, a propósito: el punto es exhibir la
anisotropía, no corregirla.

---

## 4. Medida 1 — delta relativo

    rel[l] = ||h_patch[l] - h_clean[l]|| / ||h_clean[l]||

Normalizado a propósito. La norma del residual stream crece con la profundidad,
así que un perfil de `||delta||` sin normalizar se ve creciente casi siempre y
no distingue amplificación real de crecimiento trivial.

Qué mirar: dónde se amplifica la perturbación. Un pico temprano que después se
aplana sugiere que el modelo la absorbe; crecimiento sostenido en capas medias
sugiere que alimenta un circuito.

---

## 5. Medida 2 — logit lens

    probs[l] = softmax( lm_head( model.model.norm( h[l] ) ) )

Decodifica cada capa intermedia con la LayerNorm final y la cabeza de salida.
Es decir: "¿qué diría el modelo si tuviera que responder desde esta capa?".

Después compara dos probabilidades:

    p_fr[l] = probs[l][ primer token de la referencia francesa ]
    p_en[l] = probs[l][ primer token del baseline inglés ]

Los tokens **no están hardcodeados**. Salen de las generaciones reales de cada
prompt (`row["output"]` y `row["baseline_en"]`), así que no hay que adivinar si
el francés arranca con `La`, `Le`, `C'est` o `Il`: se usa el que el modelo
efectivamente produjo para esa pregunta.

Resultado: **la capa donde `p_fr` supera a `p_en`**. Ese número es la capa
donde se da vuelta la decisión de idioma.

Es coherente con lo que ya sabemos: la CE del head (primeros 5 tokens) cayó de
5.86 a 0.66 mientras la del tail casi no se movió (0.46 -> 0.24). El efecto
está concentrado al inicio de la generación, así que debería verse un cruce
nítido.

---

## 6. Medida 3 — alineación con las dos referencias

Es la medida central. Se calculan dos direcciones de referencia por
diferencia de medias sobre N prompts:

    d_instr[l] = media( h_instr[l] - h_clean[l] )
    d_frq[l]   = media( h_frq[l]   - h_clean[l] )

Y después, para cada prompt:

    cos( h_patch[l] - h_clean[l] , d_instr[l] )
    cos( h_patch[l] - h_clean[l] , d_frq[l]   )

Esto es lo que el coseno en vocabulario no podía dar: acá la referencia es una
dirección **definida por el comportamiento**, no por el lookup de tokens.

### El control obligatorio

También se reporta:

    cos( d_instr[l] , d_frq[l] )

Si las dos referencias ya son casi la misma dirección, saber a cuál se parece
el parche no informa nada, y hay que decirlo en vez de leer diferencias que no
existen. Sin esta columna, la comparación entre las otras dos es
ininterpretable.

### Por qué diferencias y no estados absolutos

Pregunta razonable: ¿por qué `cos(h_patch - h_clean, d_frq)` y no directamente
`cos(h_patch, h_frq)`?

Dos motivos.

**1. El residual stream es anisotrópico.** Todas las activaciones están
dominadas por una componente compartida grande, independiente del prompt. El
coseno crudo entre dos estados cualesquiera da ~0.97, así que:

    cos(h_patch, h_frq)  ~ 0.97
    cos(h_clean, h_frq)  ~ 0.96      <- el control, que NO deberia parecerse

y no se distingue nada. Es el mismo fenómeno que reportan Timkey & van
Schijndel (2021): unas pocas dimensiones rogue dominan toda medida de coseno y
esconden la estructura real. Restar una línea de base común es la forma
estándar de sacárselas de encima.

El script imprime esas dos columnas crudas como diagnóstico, así que el punto
se verifica con datos en vez de asumirse.

**2. No son objetos comparables.** `h_patch` es la última posición de
`[pregunta en inglés + parche]`; `h_frq` es la última posición de
`[pregunta en francés]`. Secuencias distintas, largos distintos, contenido
distinto. El estado absoluto codifica *qué decía literalmente el prompt*, no
solo en qué modo está el modelo.

### La asimetría entre los tres deltas

No todos son igual de limpios:

    h_patch - h_clean    mismos tokens, solo cambia el parche     -> limpio
    h_instr - h_clean    4 tokens de mas                          -> confound chico
    h_frq   - h_clean    tokens completamente distintos           -> confound grande

Por eso `d_frq` se promedia sobre N preguntas: el contenido específico de cada
pregunta se cancela y queda lo común, que es "la entrada está en francés". El
promedio no es cosmético, es lo que hace interpretable la dirección. Un
`h_frq[i] - h_clean[i]` individual está dominado por el cambio de contenido, no
por el cambio de idioma.

---

## 7. Validación cruzada

Los cosenos se calculan estimando la dirección en una mitad de los prompts y
midiéndola en la otra, y viceversa:

    mitad_A, mitad_B = split(prompts)
    d_A = media( deltas_referencia[mitad_A] )
    cos sobre deltas_parche[mitad_B] contra d_A
    y al revés; después se promedia

Sin esto, cada prompt contribuye a la dirección contra la cual se compara a sí
mismo, y el coseno sale inflado.

**Cuánto importa**: verificado con vectores aleatorios en el caso circular
extremo, donde el delta del parche *es* el delta de referencia.

| caso | promedio naive | cross-fit |
|---|---|---|
| deltas independientes | ~0.00 | ~0.00 |
| delta == referencia (circular) | **0.23** | ~0.00 |
| señal real compartida | 0.90 | 0.86 - 0.93 |

O sea: el método naive habría reportado 0.23 de coseno que es puro artefacto, y
el cross-fit no destruye señal real cuando la hay.

---

## 8. Salida

Tabla de 29 filas, una por capa:

    capa  |d|/|h|  cos vs instr  cos vs q_fr  cos instr~q_fr  p(FR) limpio  p(FR) parche  p(EN) parche

Y tres líneas de resumen:

    prompts con traduccion usable: M/N
    capa donde p(FR) supera a p(EN) con parche: <l>
    maxima alineacion con la INSTRUCCION : capa <l> (cos=<x>)
    maxima alineacion con la PREGUNTA FR : capa <l> (cos=<x>)
       (misma subm. de prompts, instruccion: capa <l> cos=<x>)
    -> el parche se parece mas a: <cual>  (diferencia <+/-x>)
    las dos referencias entre si: cos medio=<x>

La línea entre paréntesis es la que hay que usar para el veredicto: `cos_frq`
se promedia sobre los M prompts con traducción usable, así que se compara
contra `cos_instr_sub`, restringido a esos mismos M. La línea de arriba
(`cos_instr` sobre los N) es la estimación más precisa de la alineación con la
instrucción por separado, pero no es comparable con `cos_frq`.

Después, una segunda tabla con el diagnóstico de anisotropía:

    capa  cos(h_patch, h_frq)  cos(h_clean, h_frq)  separacion

Cosenos **crudos**, sin restar la línea de base. Si las dos columnas están cerca
de 1 y la separación es ~0, eso es la anisotropía del residual stream: el
estado absoluto no discrimina, y queda justificado trabajar con diferencias.

Más un JSON con los vectores completos (`rel_delta`, `cos_with_instruction`,
`cos_with_french_question`, `cos_with_instruction_same_subset`,
`cos_between_references`, `raw_cos_patch_frq`, `raw_cos_clean_frq`,
`p_fr_clean`, `p_fr_patched`, `p_en_patched`).

---

## 9. Cómo leer los resultados

### Alineación

**`cos vs q_fr` mucho mayor que `cos vs instr`**

    El parche hace que la pregunta "parezca francesa". Mecanismo simple, y
    consistente con que el parche no tenga semántica de instrucción. Es la
    hipótesis a priori más plausible.

**`cos vs instr` mucho mayor que `cos vs q_fr`**

    El parche reconstruye un estado de cumplimiento de directiva. Bastante más
    sorprendente, porque lo habría aprendido sin ver ninguna instrucción
    durante el entrenamiento: la loss solo pedía reproducir texto francés.

**Los dos bajos, y `instr~q_fr` también bajo**

    El parche llega al mismo comportamiento por una tercera vía. La pregunta
    pasa a ser cuál, y el barrido causal hay que diseñarlo distinto porque no
    hay dirección candidata clara que ablacionar.

**Los dos altos y `instr~q_fr` alto**

    Las dos referencias son la misma cosa. La comparación no separa nada y no
    se puede concluir a cuál se parece el parche.

### Perfil por capa

**cos alto en capas medias (8-18)**

    El parche entra a la misma vía que la referencia. Es el resultado limpio.

**cos alto solo en capas 0-2 y después cae**

    El parche empuja el embedding, pero el modelo lo re-normaliza y el efecto
    conductual viene de otro lado. La alineación temprana sería un epifenómeno.

**cruce del logit lens tarde (capa 20+)**

    La decisión se toma cerca de la salida. Compatible con un sesgo de primer
    token más que con un cambio de modo interno.

**cruce temprano (capa 8-14)**

    El modelo entra en modo francés temprano y el resto de la generación es
    consecuencia. Es lo que esperaríamos si el parche fija un estado.

---

## 10. Limitaciones conocidas

**Es correlacional.** Dice dónde y cuánto se parece, no qué es necesario ni qué
alcanza. Los tests causales son la sección 11.

**`h_instr` tiene otro largo de secuencia.** Al prependear la instrucción, la
"última posición" cumple el mismo rol pero con contexto distinto alrededor. La
dirección `d_instr` mezcla "estar en modo francés" con "haber leído cuatro
tokens más".

**`q_fr` cambia el idioma de la entrada además del de la salida.** `d_frq`
mezcla las dos cosas. Es inherente a la condición y no invalida la comparación,
pero si `q_fr` gana, el paso siguiente es separar esos dos componentes.

**El promedio de cosenos pondera todos los prompts igual.** Un prompt donde el
parche apenas movió nada aporta un coseno basado en un delta minúsculo, que es
ruidoso, con el mismo peso que uno donde el efecto es grande. Una alternativa
sería ponderar por `||delta_i[l]||`. No está implementado; si los cosenos salen
ruidosos entre capas contiguas, es el primer lugar donde mirar.

**El coseno es sobre el residual crudo, no post-LayerNorm.** Es lo estándar
(Arditi et al. hacen lo mismo), pero el modelo lee el residual a través de LN,
así que magnitudes y ángulos no se corresponden exactamente con influencia
causal.

**La traducción la hace el mismo modelo.** Si traduce mal de forma sistemática,
`d_frq` queda sesgada. Por eso hay gate de idioma sobre la traducción, pero el
gate no detecta traducciones que sean francés correcto pero semánticamente
malas.

---

## 11. Próximo paso: los tests causales

Con `d_l` ya calculada, el protocolo de Arditi et al. 2024 sale casi gratis y
convierte esto de un gráfico en un resultado.

**Necesidad — ablación direccional.** Durante el run parcheado, en la capa `l`,
proyectar fuera la dirección normalizada:

    h' = h - d_hat * (d_hat^T h)

y barrer `l`. Si el francés se cae al ablacionar la capa `l*`, esa capa es
necesaria para el efecto.

**Suficiencia — trasplante.** Inyectar `delta_patch[l]` en un run limpio, solo
en la capa `l`, sin parche en los embeddings. Si aparece francés, esa capa
alcanza.

Con necesidad y suficiencia se tiene un mapa causal, no una correlación.

**Importante**: correr primero el observacional. Si el coseno da bajo en todas
las capas, el diseño del barrido causal cambia por completo, porque no habría
una dirección candidata clara que ablacionar.

---

## 12. Comandos

    # 1. traducir las preguntas al francés (una sola vez, ~2 min)
    python3 -u translate_questions.py --model $M --targets targets_french.csv

    # 2. análisis capa por capa
    python3 -u layer_analysis.py --model $M \
        --patch runs/v2_french_l2_0.045/lang_patch.pt \
        --out runs/v2_french_l2_0.045/layer_analysis.json

Costo: 4 forward passes por prompt sobre 40 prompts (`--n` lo cambia).

Vale la pena correrlo también sobre el parche **v1** (`runs/french_l2_0.045/`,
norma 0.278, 5% de compliance) como control negativo: un parche que no funciona
no debería alinearse con ninguna de las dos referencias. Si se alinea igual, la
alineación no explica el comportamiento.
