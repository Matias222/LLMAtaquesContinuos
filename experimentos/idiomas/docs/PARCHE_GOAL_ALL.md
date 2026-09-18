# Parche de una posición (`goal_all`): una dirección en el espacio de embeddings

Todo lo que sabemos del parche de UN solo vector sumado a toda la pregunta, al
2026-09-18. Números verificados contra los JSON de cada run. Sin LaTeX: la
notación va en bloques de código.

Runs involucrados:

| run | qué es |
|---|---|
| `runs/v5_goalall_head_multi` | primer parche `goal_all` (francés), 2026-09-17 |
| `algebra/runs/alg_<celda>` | 6 direcciones {fr, es, de} × {normal, MAYÚSCULAS}, 2026-09-18 |
| `algebra/runs/alg_fr_s1`, `alg_es_up_s1` | réplicas (mismo todo, otro orden de batches) |
| `algebra/runs/geometria` | cosenos, álgebra en comportamiento, activaciones, embeddings |
| `algebra/runs/alg_fr/restar_fr` | pregunta en francés menos el parche de francés |

---

## Resumen

1. **Un solo vector sumado a cada token de la pregunta alcanza para cambiar el
   idioma de la respuesta**, desde cualquier idioma de entrada, con la misma
   compliance que el parche de 3 posiciones y sin perder accuracy.
2. **Tiene signo.** Restarlo de una pregunta en francés saca la respuesta del
   francés (0.90 → 0.12). El parche viejo de 3 posiciones no se deja invertir
   (0.92). Falta el control aleatorio para cerrarlo (sección 7).
3. **No es única.** Dos entrenamientos de la misma celda comparten la mitad
   de la dirección (coseno 0.49). Hay muchas direcciones que sirven.
4. **Idioma sí, mayúsculas no.** Las direcciones de idioma generalizan; las de
   mayúsculas solo funcionan en respuestas cortas y desaparecen al sumarles
   cualquier otro vector.
5. **El álgebra tipo function vectors no cierra en el espacio del parche.** En
   comportamiento funciona en 3 de 6 casos de cambio de idioma y en 0 de 6 de
   mayúsculas. En las activaciones de las últimas capas el paralelogramo se
   sostiene mejor que en el embedding.
6. **Todas las direcciones comparten un componente grande** (coseno 0.52–0.58
   con la media), que apunta en contra de las palabras funcionales de una
   pregunta en inglés (`?`, `what`, `which`, `the`, `is`).

---

## 1. Qué es el parche

```
e'_i = e_i + v      para todo token i de la pregunta del usuario
v ∈ R^3072          un solo vector, shape [1, 1, 3072]
```

No toca el system, los headers ni `<|eot_id|>`. Como es el mismo `v` en cada
token, no puede apoyarse en la posición ni en el token sobre el que cae: es una
**dirección** del espacio de embeddings.

Los otros dos formatos que probamos no lo son:

- **3 posiciones del goal** (`v5_head_multi`, `v4_250`): tres vectores
  distintos atados a los primeros tokens. Solo funciona con las aperturas e
  idiomas que vio.
- **3 posiciones del header** (`v5_header_head_multi`): los tokens del header
  son siempre los mismos, así que `e_const + v` equivale a aprender
  embeddings libres. Es un soft prompt (prompt compression), no una dirección,
  aunque generalice mejor.

Ojo: es una **suma**, no un promedio. La perturbación total es
`(largo de la pregunta) × v`, y eso importa (sección 2.3).

---

## 2. Primer parche: `v5_goalall_head_multi` (francés)

Receta: L2 0.0725, 8 epochs, batch 32, 20 steps/batch, CE sobre los primeros
8 tokens del target, entradas en/es/de, sign-SGD con coseno. Norma final 0.823.

### 2.1 Métricas

| eval | parche | referencia `[FR;q]` |
|---|---|---|
| held-out inglés (n=50): francés / accuracy | 96% / 96% | 98% / 100% |
| CE head del target FR | 5.60 → 0.35 | — |
| open 1, 99 prompts de navidad | 92.9% | 99.0% |
| desde español / alemán | 0.88 / 0.96 | — |
| desde italiano / portugués (no vistos) | 0.82 / 0.74 | — |
| open_2 (imperativos) desde es / de / **en** | 0.74 / 0.84 / **0.36** | — |

Sin role leak. Cuando engancha, el francés se sostiene en los tres tercios de
la respuesta (0.93 / 0.93 / 0.93): fija un modo, no es un efecto local.

### 2.2 Contra los otros formatos

| | goal_all | 3 pos. del goal | header |
|---|---|---|---|
| held-out | 96% | 96% | 94% |
| italiano / portugués | 0.82 / 0.74 | **0.18 / 0.02** | 0.94 / 0.94 |
| open_2 desde inglés | 0.36 | 0.04 | 1.00 |
| norma | 0.82 | 1.04 | 0.60 |

La dirección transfiere a idiomas de entrada no vistos, cosa que el parche de 3
posiciones del goal no hace. El header generaliza más, pero no es una dirección.

### 2.3 Por qué falla en open_2 desde inglés

- **Depende del largo de la pregunta.** En train el goal mide 11.3 tokens de
  media; los imperativos abiertos, 5 a 9. Desde inglés: 0% de francés con 4–7
  tokens, 40% con 8–11. El mismo gradiente aparece en español (0.67 → 0.86) y
  alemán (0.75 → 1.00). Los dos prompts de 3 tokens de open 1 fallan.
- **Los imperativos están fuera de distribución.** El train son preguntas
  factuales. Casi todos los fallos son "Tell me about…", "Explain…",
  "List…". A igual largo, las preguntas factuales sí pasan a francés.

---

## 3. Seis direcciones: idioma × formato (`algebra/`)

Receta: la de v5, con L2 0.075 y 10 epochs. Entradas multi-idioma **sin el
idioma target** (una pregunta en español ya se contesta en español sin parche
y no aporta gradiente de idioma):

```
fr, fr_up   prompt, prompt_es, prompt_de
es, es_up   prompt, prompt_de, prompt_fr
de, de_up   prompt, prompt_es, prompt_fr
```

### 3.1 Targets

- Las seis celdas salen del mismo CSV base: mismas filas, mismo orden, mismo
  held-out (`algebra/generate_targets_attr.py`).
- Las celdas `_up` son el target de su celda normal pasado por `upper()`. La
  primera versión generaba con la instrucción conjunta ("Respond entirely in
  uppercase letters, in Spanish.") y los targets salieron mal: el modelo
  alucina en ese modo. Así, entre una celda y su `_up` cambia **solo** el
  formato.
- Correcciones a mano (`algebra/fix_targets.py`): 33 outputs en es/de del
  held-out (alucinaciones como Gobi por Antártida, Estambul por Ankara o
  Proxima Centauri por el Sol; títulos inventados; 4 que el detector no
  reconocía como español), 3 en open_2 con inglés mezclado o palabras
  inventadas, alias en español y alemán para 56 preguntas, y 21 traducciones
  al francés de open_2 (3 eran el ejemplo del few-shot, "Quelle est la
  capitale du Japon?").
- `algebra/check_targets.py` valida los 18 CSV antes de entrenar.

### 3.2 Métricas por celda

`celda ok` = el idioma correcto **y** el formato correcto (una celda normal no
puede salir en mayúsculas).

| celda | norma | held-out | accuracy | open 1 | desde otros idiomas | it / pt | open_2 desde inglés |
|---|---|---|---|---|---|---|---|
| fr | 0.84 | 1.00 | 0.96 | 0.94 | 0.96–0.98 | 0.72 / 0.60 | 0.48 |
| es | 0.87 | 0.94 | 0.96 | 0.92 | 0.98–1.00 | 0.90 / 0.34 | 0.74 |
| de | 0.85 | 0.92 | 0.94 | 0.95 | 1.00 | 0.84 / 0.20 | 0.60 |
| fr_up | 0.98 | 0.80 | 0.70 | **0.12** | 0.78–0.86 | 0.82 / 0.54 | **0.00** |
| es_up | 0.97 | 0.86 | 0.74 | **0.13** | 0.86–0.94 | 0.78 / 0.36 | **0.02** |
| de_up | 1.02 | **0.56** | 0.68 | **0.14** | 0.68–0.72 | 0.50 / 0.16 | **0.02** |

- **Las direcciones de idioma funcionan y generalizan.** Transferir al
  portugués es lo más débil en es y de.
- **Las de mayúsculas no.** En held-out se sostienen a lo largo de la
  respuesta (0.97 / 0.94 / 0.91 por tercio para fr_up), pero en prompts
  abiertos caen a 0.30 / 0.23 / 0.18, y parte de las salidas se van al inglés
  en mayúsculas. `de_up` es la que peor entrenó: CE head en held-out de 1.45,
  contra 0.69 de fr.

### 3.3 Entrenamiento

Todas las celdas eligen la epoch 10 como mejor checkpoint, salvo `de`, cuya CE
del head en held-out quedó plana (0.90 al principio y al final). La brecha
train/held-out es grande en las `_up` (0.70–0.90) contra 0.47–0.63 en las
normales.

---

## 4. Geometría en el espacio del parche

`algebra/runs/geometria/cosines.md`. En dimensión 3072, el coseno entre dos
direcciones al azar es ±0.018.

### 4.1 La dirección no es única

| celda | cos(original, réplica) |
|---|---|
| fr | 0.49 |
| es_up | 0.58 |

Mismo dataset, misma receta, solo cambia el orden de los batches, y el vector
final comparte la mitad de la dirección. **Este es el techo** contra el que se
lee cualquier otro coseno: nada puede parecerse a `v_fr` más que su propia
réplica.

### 4.2 Componente común

- Las seis celdas tienen coseno 0.52–0.58 con su media `c` (norma 0.51).
- Entre celdas distintas, el coseno es 0.11–0.25.
- Los tokens del vocabulario más opuestos a `c` son `?`, `what`, `which`,
  `the`, `is`, `are`, `was`: las palabras funcionales de una pregunta en
  inglés.

Lectura: todas las direcciones cargan un empuje genérico de "esto no es una
pregunta en inglés / salir del modo por defecto", y encima una parte
específica de la celda.

### 4.3 No hay estructura aditiva

Modelo `v_(idioma, formato) = c + a_idioma + b_formato + interacción`:

- R² aditivo **0.656**. Seis celdas al azar dan 0.60 solo por grados de
  libertad, así que el piso no es 0.
- Varianza entre celdas: idioma 45%, formato 21%, **interacción 34%**.
- Direcciones de formato `u_L = v_L_up − v_L`: coseno 0.05–0.09 entre los tres
  idiomas. No hay un eje "mayúsculas" común.
- Direcciones de idioma `v_A − v_B`, en normal contra en mayúsculas: 0.12–0.14.
- Paralelogramos `v* = s + o − d` (12): cos(v*, real) entre 0.15 y 0.23, por
  debajo de la suma sin resta (0.23–0.34) y de restar un vector al azar.

---

## 5. Álgebra en comportamiento

`algebra/runs/geometria/algebra_eval.md`, held-out n=50. Se esconde una
esquina del cuadrado y se la reconstruye con las otras tres, como en
`last_copy + first_capital − first_copy` o `king − man + woman`:

```
v*_(L, f) = v_(L, f') + v_(L', f) − v_(L', f')
p.ej.  v*_fr_up = v_fr + v_es_up − v_es
```

Ninguna esquina es el baseline (inglés normal), para que el componente común
entre dos veces y salga una.

### 5.1 Generar mayúsculas por álgebra: 0 de 6

Fracción de letras en mayúscula de la salida:

| paralelogramo | sin parche | `_up` del otro idioma solo | real | **álgebra** | suma sin resta |
|---|---|---|---|---|---|
| fr_up = fr + es_up − es | 0.07 | 0.94 | 0.94 | **0.07** | 0.06 |
| es_up = es + fr_up − fr | 0.07 | 0.94 | 0.94 | **0.09** | 0.05 |
| fr_up = fr + de_up − de | 0.07 | 0.75 | 0.94 | **0.07** | 0.12 |
| de_up = de + fr_up − fr | 0.07 | 0.94 | 0.75 | **0.10** | 0.13 |
| es_up = es + de_up − de | 0.07 | 0.75 | 0.94 | **0.05** | 0.07 |
| de_up = de + es_up − es | 0.07 | 0.94 | 0.75 | **0.09** | 0.07 |

El álgebra queda en el nivel del modelo sin parche: solo la mayúscula inicial
de cada oración y los nombres propios. La información de mayúsculas está en
los ingredientes (0.75–0.94 solos), pero desaparece en cuanto se les suma
cualquier otro vector de norma ~1, incluida la suma sin resta y los controles.
**La dirección de mayúsculas no sobrevive a la superposición.**

### 5.2 Cambiar de idioma por álgebra: 3 de 6 le ganan a todos los controles

`celda ok` sobre la esquina normal oculta. Como las mayúsculas se pierden en
cualquier combinación, acá equivale a "idioma correcto".

| oculta = s + o − d | **álgebra** | suma s + o | resta al azar | resta equivocada | solo s |
|---|---|---|---|---|---|
| es = es_up + fr − fr_up | **0.82** | 0.06 | 0.30 | 0.34 | 0.10 |
| de = de_up + fr − fr_up | **0.76** | 0.00 | 0.10 | 0.10 | 0.42 |
| de = de_up + es − es_up | **0.66** | 0.16 | 0.12 | 0.22 | 0.42 |
| fr = fr_up + es − es_up | 0.32 | 0.76 | 0.12 | 0.62 | 0.14 |
| fr = fr_up + de − de_up | 0.22 | 0.22 | 0.02 | 0.00 | 0.14 |
| es = es_up + de − de_up | 0.26 | 0.60 | 0.86 | 0.80 | 0.10 |

- **Lo que funciona es que la resta cancele el idioma del otro ingrediente.**
  `es_up + fr` sale en francés (0.56); al restar `fr_up`, el francés
  desaparece y queda español (0.82). Restar la esquina de otro idioma
  ("resta equivocada") no lo logra: la resta es específica.
- **Asimetría: el francés domina las sumas.** Cuando lo que hay que cancelar
  es el francés, la resta funciona. Cuando hay que conservarlo, se pasa de
  largo y la salida cae al inglés (60% en `fr = fr_up + es − es_up`). El
  efecto no es lineal: satura y depende de cuánto pesa cada idioma.
- La accuracy del álgebra que funciona cae a 0.34–0.50, contra 0.94–0.96 de
  la dirección real.

---

## 6. Activaciones y embeddings

### 6.1 Último token del prompt, por capa (`plot_last_token.py`, `alg_fr`)

Coseno de las medias entre el delta que induce el parche y el delta que
induce cada referencia:

| contra | L9 | L12 | L16 | L20 | L24 | L28 |
|---|---|---|---|---|---|---|
| pregunta en francés | 0.70 | 0.75 | 0.77 | 0.83 | 0.89 | **0.92** |
| instrucción "en francés" | 0.54 | 0.57 | 0.75 | 0.87 | 0.91 | **0.93** |
| pregunta en alemán | 0.68 | 0.73 | 0.64 | 0.65 | 0.56 | 0.59 |
| pregunta en español | 0.69 | 0.75 | 0.65 | 0.69 | 0.62 | 0.62 |
| instrucción de respuesta corta | 0.33 | 0.35 | 0.29 | 0.43 | 0.40 | 0.46 |

- Hasta la capa 12 la dirección se parece igual a "la pregunta está en
  francés", "en alemán" o "en español": es "idioma extranjero" en general. La
  especificidad francesa aparece desde la capa 16 y crece hasta el final.
- En las últimas capas el parche se parece tanto a la instrucción en texto
  como a la pregunta en francés (0.93 y 0.92).
- Es el mismo perfil que el de `v5_goalall_head_multi` y el del parche de 3
  posiciones del goal (`runs/geom_last_token`), y más alto que el del header
  (0.74 contra la pregunta en francés en L28).

### 6.2 El paralelogramo en activaciones (`algebra_acts.md`)

- Los cosenos de medias están dominados por el componente común: la suma sin
  resta ya da 0.8–0.9 contra la esquina real. Es un test poco discriminante.
- Aun así, en la capa 28 el álgebra hecha en activaciones,
  `Δh(s) + Δh(o) − Δh(d)`, le gana a la suma en **los 12 paralelogramos**,
  por 0.03 a 0.11, y llega a 0.86–0.93 en las esquinas `_up`.
- El vector compuesto en la entrada (`v*`) se parece más a la esquina real en
  la capa 12 (0.73–0.86) y después se aleja (0.55–0.85 en L28).

Lectura: la representación de las últimas capas es más aditiva que el parche
en el embedding. La geometría parece existir más adentro del modelo, pero el
parche no la hereda.

### 6.3 Contra la matriz de embeddings (`algebra_embed.md`)

- **Diagonal de idioma, débil pero consistente.** Cada celda se alinea más
  con el offset de traducción de su propio idioma (`mean E[palabra_L] −
  E[palabra_en]`, 40–46 pares de un token): 6 de 6. Los componentes de idioma
  del modelo aditivo también: 3 de 3. Magnitudes 0.03–0.12, contra ±0.018 del
  azar.
- Los offsets de traducción entre sí se parecen mucho (0.81–0.86): el
  vocabulario también tiene un gran componente "no inglés" común.
- **Mayúsculas:** las celdas `_up` se alinean algo más con el offset de
  mayúsculas del vocabulario (`E[" WORD"] − E[" word"]`, 1709 pares): 0.08–0.10
  contra 0.02–0.06 de las normales. Las diferencias `u_L`, casi nada.
- Los tokens más cercanos a cada dirección no tienen sentido (fragmentos de
  código, otros alfabetos). Es típico de direcciones optimizadas por
  gradiente.

---

## 7. Restar la dirección (`algebra/run_restar_fr.sh`)

Pregunta del held-out en francés, menos el parche de francés:

```
M(q_fr − v_fr)
```

| condición | fr | es | en | de | accuracy | largo | CE head FR | CE head EN |
|---|---|---|---|---|---|---|---|---|
| `q_fr` sin parche | 0.90 | 0.00 | 0.00 | 0.00 | 0.92 | 79 | 0.78 | 2.79 |
| `q_fr − v_fr` | **0.12** | **0.54** | 0.26 | 0.04 | 0.64 | 268 | **2.92** | 2.62 |
| `q_fr − v4_250` (3 posiciones) | 0.92 | 0.00 | 0.02 | 0.00 | 0.90 | — | — | — |

- **Saca del francés.** De las 47 filas que salían en francés, 41 cambian:
  24 a español, 12 a inglés, 2 a alemán. La CE del target francés sube de
  0.78 a 2.92.
- **El parche de 3 posiciones no se deja invertir** (0.92 con a=−1, 0.86 con
  a=−2). Es la diferencia más concreta entre una dirección y un soft prompt.
- **No va al inglés sino "fuera del francés", y el vecino es el español.** Las
  27 salidas en español son limpias y en tema desde el primer token ("La
  capital de Siria es Damasco"), con accuracy 0.63.
- **Las 13 en inglés tienen cara de entrada dañada:** "I think there may be a
  bit of a language barrier here", respuestas a otra pregunta. La resta
  también degrada la lectura de la pregunta: la accuracy cae a 0.64 y el
  largo se triplica.

**Falta el control que lo cierra.** Nunca corrimos un vector al azar de la
misma norma con `goal_all`: el control aleatorio de `runs/random_control` es
del parche de 3 posiciones. Y la condición `resta_azar` del álgebra muestra
que una perturbación al azar de esta norma **sí** mueve el comportamiento
(por ejemplo, `es_up + de − r` dio 0.86 de español). Hasta correrlo, la caída
del francés podría ser en parte solo eso.

---

## 8. Qué está establecido y qué no

**Establecido**

- Un vector único sumado a cada token de la pregunta controla el idioma de la
  respuesta, desde cualquier idioma de entrada y sin costo de accuracy.
- Esa dirección no es única: réplicas con coseno 0.49–0.58.
- Todas las direcciones comparten un componente grande "no pregunta en
  inglés".
- Mayúsculas no se representa como una dirección reutilizable: no generaliza
  a prompts abiertos, los ejes de cada idioma no se parecen y no sobrevive a
  la superposición.
- En el espacio del parche el álgebra de function vectors no cierra.

**Con evidencia parcial**

- Que la dirección tenga signo (sección 7): saca del francés, pero falta el
  control aleatorio.
- Un eje de idioma aditivo: la resta cancela el idioma en 3 de 6
  paralelogramos, con asimetría a favor del francés.
- Más aditividad en las activaciones tardías que en el embedding: el álgebra
  en activaciones le gana a la suma en 12 de 12, pero con márgenes chicos y
  sobre un test dominado por el componente común.

**No establecido**

- Que exista un eje francés canónico en el embedding.
- Que la dependencia del largo de la pregunta sea solo de escala (no se
  probó normalizar por largo).

---

## 9. Pendientes, por prioridad

1. **Control de la resta.** `q_fr − r` con `r` al azar de la misma norma (3
   seeds), `q_fr − v_fr_s1` (la réplica), `q_fr − v_es`, `q_fr − v_de`. Si el
   azar deja el francés en ~0.9, la dirección con signo queda cerrada. 6
   corridas de ~2 minutos.
2. **Barrido de α** sobre `v_fr` en los dos sentidos (−2 a 2): que el efecto
   sea monótono en la magnitud.
3. **Barrido de α sobre `v*`** en las tres filas de idioma que fallaron, que
   caen al inglés por falta de empuje:
   `algebra_patches.py eval --hide fr,es --alphas 1.25,1.5,2`.
4. **Activaciones sin el componente común:** coseno entre diferencias,
   `Δh(fr_up) − Δh(fr)` contra `Δh(es_up) − Δh(es)`. Hay que agregarlo a
   `acts`, que hoy solo guarda los agregados.
5. **Otro segundo factor** en lugar de mayúsculas, más robusto (respuesta de
   una palabra contra oración completa).
6. **Entrenamiento factorizado** `v = c + a_idioma + b_formato`: con un techo
   de réplicas de 0.49, el entrenamiento independiente no puede encontrar la
   solución aditiva aunque exista. Hay que probar la existencia directamente.
7. **Normalizar por largo** (sumar `v / n_tok`) para aislar la falla de open_2.

---

## 10. Reproducir

```bash
# (desde experimentos/idiomas)

# primer parche goal_all (francés)
bash run_goal_all_v5.sh

# seis direcciones + evals + plot_last_token + geometría
python3 algebra/check_targets.py            # tiene que decir LISTO
bash algebra/run_algebra_v6.sh              # STAGES / CELLS / SKIP_TRAIN para correr por partes

# resta
bash algebra/run_restar_fr.sh               # SCALES="-0.5 -1 -2" para el barrido

# geometría en CPU sola
python3 algebra/algebra_patches.py cosines \
    --replica fr=algebra/runs/alg_fr_s1/lang_patch_best_train.pt \
    --replica es_up=algebra/runs/alg_es_up_s1/lang_patch_best_train.pt
```
