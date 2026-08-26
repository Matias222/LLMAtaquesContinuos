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

`q_fr` lo genera `translate_questions.py` con el mismo modelo, con gate de
idioma sobre la traducción: si la traducción no sale en francés, esa fila no
se usa para estimar la dirección.

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

    prompts con traduccion usable: N/M
    capa donde p(FR) supera a p(EN) con parche: <n>
    maxima alineacion con la INSTRUCCION : capa <n> (cos=<x>)
    maxima alineacion con la PREGUNTA FR : capa <n> (cos=<x>)
    -> el parche se parece mas a: <cual>
    las dos referencias entre si: cos medio=<x>

Más un JSON con los vectores completos (`rel_delta`, `cos_with_instruction`,
`cos_with_french_question`, `cos_between_references`, `p_fr_clean`,
`p_fr_patched`, `p_en_patched`).

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
