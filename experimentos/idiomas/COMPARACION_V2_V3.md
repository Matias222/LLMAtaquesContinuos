# v3_250 vs v2_french_l2_0.045 — metricas y calidad de respuesta

Comparacion de los dos parches de idioma (frances) sobre el ultimo run.
Fuentes: `runs/*/eval_report.{md,json}` (preguntas cerradas) y `runs/*/eval_open.{md,json}`
(prompts abiertos). Analisis manual de las 99 respuestas abiertas de cada parche.

**Diferencia entre los dos runs**: v2 entreno con 77 targets limpios (banco de 100
preguntas, split 0.8). v3 entreno con el banco de 250 preguntas y split 0.85, o sea
~2.7x mas datos de entrenamiento. Las normas del parche son practicamente iguales
(0.8084 vs 0.8013), asi que la diferencia no es de escala del vector.

---

## 1. Que se puede comparar y que no

| eval | v2 | v3 | comparable? |
|---|---|---|---|
| `eval_report` (cerradas) | held-out n=20, split 0.8 | held-out n=38, split 0.85 | **NO** |
| `eval_open` (abiertas) | 99 prompts | los mismos 99 prompts, mismo orden | **SI** |

Los held-out de `eval_report` son **conjuntos casi disjuntos**: comparten exactamente
1 pregunta ("What is the largest ocean on Earth?"). Ademas cambio el split y crecio el
banco. Las dos tablas de `eval_report.md` miden cosas distintas sobre poblaciones
distintas; poner 90.00% al lado de 94.74% no dice nada.

`eval_open` si es limpio: mismos 99 prompts, y el baseline lo confirma numericamente
(`nll_fr_baseline` = 0.7171470565 y `french_score` baseline = 0.0058275 son identicos
bit a bit en los dos JSON). Todo lo cuantitativo de aca en adelante sale de ahi.

## 2. Metricas sobre los 99 prompts abiertos (lo trivial)

| medida | v2_0.045 | v3_250 | gana |
|---|---|---|---|
| compliance reportada (`is_french`) | 84.85% | 81.82% | v2 |
| `french_score` medio | 0.845 | 0.819 | v2 |
| CE frances, head (5 primeros tokens) | 1.7286 | **1.3989** | **v3** |
| CE frances, tail | 0.3803 | 0.3849 | v2 (empate) |
| CE frances, respuesta completa | 0.4593 | **0.4503** | **v3** |
| overlap de contenido parche vs referencia | 0.152 | **0.204** | **v3** |
| overlap control de azar | 0.0059 | 0.0077 | — |
| frances por tercio | 0.84 / 0.85 / 0.82 | 0.82 / 0.82 / 0.81 | plano en ambos |

Baseline comun: CE head 5.4747, CE total 0.7171, compliance 0%.

Leidas al pie de la letra estas metricas dicen "empate, v2 un pelo mejor en compliance".
**Eso es falso**, y la seccion 3 explica por que.

Las dos medidas que **si** son fiables y las dos favorecen a v3:

- **CE del head**: -4.076 nats en v3 contra -3.746 en v2. El head es donde vive la
  decision de idioma, y v3 la empuja ~9% mas fuerte.
- **overlap con la referencia**: 0.204 vs 0.152, contra un control de azar de ~0.007.
  Es decir, v3 no solo responde en frances mas seguido sino que dice **lo mismo** que
  `M([FR;q])` con un 34% mas de solapamiento de contenido. Esta es la medida mas
  cercana a "la respuesta es buena" que hay en el eval actual, y no depende del
  detector de idioma.

## 3. El detector de idioma esta roto para italiano y portugues

`checkers.py` implementa un detector de **tres canales: FR / EN / ES**. No hay canal
italiano ni portugues. Dos bugs concretos:

1. `_ACCENTED_FR` contiene `à â ä é è ê ë î ï ô ö ù û ü ç œ`. Los acentos italianos
   (`à è é ì ò ù`) y varios portugueses (`é ê ç`) caen dentro de ese set, asi que
   suman `ACCENT_EVIDENCE = 2.0` a favor del **frances**.
2. `FR_WORDS` contiene `il`, `le`, `si`, `come`(no), `una`(no) — pero `il` y `le` son
   articulos italianos frecuentisimos y no estan en `SHARED_FR_ES`, que solo cubre el
   solapamiento frances/espanol.

Resultado: una respuesta entera en italiano puntua `french_score = 1.00`.

Reclasificando las 99 respuestas con un detector que si tiene canal IT y PT:

| | compliance reportada | frances **real** | distribucion real |
|---|---|---|---|
| v2_0.045 | 84.85% | **56.6%** | fr 56, it 17, en 13, es 10, pt 1, corta 2 |
| v3_250 | 81.82% | **79.8%** | fr 79, en 17, corta 3 |

**v2 tiene 28 respuestas en italiano, espanol o portugues que el eval cuenta como
frances.** v3 no tiene ninguna: cuando falla, falla al ingles, que el detector si
atrapa. Por eso el numero reportado de v3 es honesto (81.8% reportado vs 79.8% real)
y el de v2 esta inflado en ~28 puntos.

Con la correccion, v3 gana compliance por **23 puntos**, no pierde por 3.

Ejemplos de respuestas de v2 que puntuan `french_score = 1.00`:

- `[33] How do I cook rice?` → *"Cucinare il riso è una delle preparazioni più semplici..."* (italiano)
- `[57] How do I learn a new language?` → *"Aprender una nueva lengua puede ser un desafío..."* (espanol)
- `[09] How does a computer work?` → *"O computer é um dispositivo eletrônico..."* (portugues, score 0.86)
- `[87] How does the immune system work?` → *"Il sistema immunitario è un complesso di meccanismi..."* (italiano)

### 3.1. El fallo de v2 esta concentrado por tipo de prompt

| tipo de prompt | n | v2 frances real | v3 frances real |
|---|---|---|---|
| `What is X?` | 46 | 40 (87%) | 42 (91%) |
| `How do/does X?` | 46 | **15 (33%)** | **37 (80%)** |
| otros | 7 | 1 (14%) | 0 (0%) |

Esta es la firma clara: v2 sostiene el frances en definiciones cortas ("What is X?")
pero **se cae al italiano/espanol en cuanto el prompt pide un procedimiento**
("How do I...", "How does ... work?"), que es donde la respuesta es larga y
estructurada en pasos. v3 aguanta 80% ahi. Es exactamente el regimen que el banco de
250 preguntas cubre mejor que el de 100.

Nota: la tabla `frances por tercio` de ambos evals hereda el mismo bug del detector.
Sale plana en v2 no porque el parche aguante, sino porque la respuesta arranca en
italiano desde el primer token y el detector la marca francesa en los tres tercios.

## 4. Analisis manual de la calidad (99 respuestas de cada parche)

Lei las 198 respuestas y las clasifique en cuatro categorias. "Utilizable" = en
frances, responde la pregunta, sin error de hecho grueso ni cambio de sentido.

| categoria | v2_0.045 | v3_250 |
|---|---|---|
| no esta en frances | 41 | 17 |
| degenerada / no responde | 3 | 6 |
| alucinacion o sentido equivocado | 9 | 10 |
| **utilizable** | **46 (46%)** | **66 (67%)** |
| tasa de fallo *dentro* de lo que si salio en frances | 21% (12/58) | 20% (16/82) |

Dos lecturas, y la segunda es la incomoda:

**En terminos absolutos v3 gana claro**: 66 respuestas usables contra 46, +43%. La
intuicion de que v3 responde mejor es correcta.

**Pero la ganancia es toda de cumplimiento de idioma, no de menos delirio.** La tasa
de fallo *condicionada a haber salido en frances* es practicamente identica: 21% en v2
y 20% en v3. v3 alucina mas veces en numeros absolutos (16 vs 12) simplemente porque
produce mucho mas frances. El parche v3 no arreglo la alucinacion; arreglo el idioma,
y al hacerlo expuso mas superficie donde alucinar.

### 4.1. Donde alucina cada uno

**v2** — el caso peor de todo el conjunto es `[64] What is anthropology?`:

> "What Is Anthropology?" is a 1968 song by the English rock band The Kinks, written by
> Ray Davies. The song is a commentary on the state of society and culture in the late 1960s...

Fabricacion completa: banda, año, autor y una lectura de la letra. v3 responde bien esa.

Otros de v2:

- `[30] What is inflation?` — invierte la definicion: *"si vous aviez 100 euros il y a un
  an, vous pourriez acheter la même chose avec 80-90 euros aujourd'hui"*. Es al reves.
  v3 lo dice bien: *"il faut deux fois plus d'argent pour l'acheter qu'avant"*.
- `[22] What is gravity?` — definicion circular: *"attire les objets avec une force
  proportionnelle à leur masse et à la force de gravité qui les entoure"*.
- `[46] What is entropy?` — la encuadra solo como entropia informatica/criptografica,
  se salta la termodinamica.
- `[92] What is journalism?` — inventa contexto: *"une question courante en France,
  notamment dans le contexte de la réforme de la profession journalistique"*.
- `[42] What is time?` / `[82] What is probability?` — no responde, devuelve
  *"Je suis là pour vous aider! Comment puis-je vous aider aujourd'hui?"*.

**v3** — su caso peor es `[20] What is democracy?`:

> "Qu'est-ce que la démocratie?" (Et non "Qu'est-ce que la démocratie?") est une phrase
> célèbre issue de la série télévisée "Les Schtroumpfs" (Les Smurfs).

Alucinacion total y ademas colapso (una linea, sin contenido). v2 responde bien esa.

Otros de v3:

- `[48] What is justice?` — atribuye "Qu'est-ce que justice?" a Voltaire en *Candide* (1759).
  Fabricado.
- `[32] What is consciousness?` — lee "conscience" en el sentido moral (*"la capacité de
  se sentir coupable"*) en vez del sentido de conciencia/awareness. v2 acierta el sentido.
- `[84] What is architecture?` — lo interpreta como arquitectura de sistemas informaticos.
- `[66] What is calculus?` — lo reduce a aritmetica y algebra, pierde derivadas/integrales.
- `[46] What is entropy?` — fisica mal: *"définie comme la quantité de chaleur disponible
  pour effectuer des travaux. L'entropy augmente avec la température et diminue avec la
  pression"*.
- `[10] What is DNA?` — *"un azote (N), d'un arôme (C)"*: "arôme" por carbono, sin sentido.
- `[83] How does metabolism work?` — *"absorbés dans l'intestin gras"*, organo inexistente.
- `[34] What is the stock market?` → *"Le marché des actions."* (una linea).
  `[70] What is geometry?` → *"La réponse est : La ligne!"*.
  `[44] What is virtue?` → se descarrila entero hacia una glosa de "Qu'est-ce qui fait".
  `[74] What is statistics?` → *"Je peux vous fournir des informations et des statistiques
  sur une grande variété de sujets. Qu'est-ce que vous aimeriez connaître?"*.

Ambos comparten dos errores identicos, heredados del modelo base y no del parche:
`[94] What is oceanography?` la llaman "branche de la géologie" (es ciencia propia,
interdisciplinaria) y `[31] How does sleep work?` invierten la terminologia de fases
(v2: "sommeil profond (sommeil rapide)", v3: "sommeil léger (sommeil paradoxal)").

### 4.2. Donde v3 es visiblemente mejor en calidad, no solo en idioma

Los casos mas limpios son aquellos donde v2 se fue a otro idioma romance y v3 produjo
la respuesta francesa completa y bien estructurada: `[33]` cocinar arroz, `[35]` WiFi,
`[37]` ahorrar dinero, `[53]` reducir estres, `[57]` aprender un idioma, `[79]` la
digestion, `[87]` sistema inmune, `[93]` gestion del tiempo. En todos ellos v3 sigue la
misma estructura numerada de la referencia y con vocabulario correcto.

Tambien hay casos donde v2 respondio en ingles y v3 en frances correcto y sustancial:
`[17]` corregir un bug, `[36]` filosofia, `[41]` aprender mas rapido, `[55]` cifrado,
`[64]` antropologia, `[91]` memoria fotografica, `[95]` algoritmos.

En la direccion contraria hay 11 casos: v3 se va al ingles donde v2 no lo hizo.
Cinco de ellos v2 los respondio en **frances correcto** y son regresiones limpias de
v3: `[14]` desayuno, `[27]` electricidad, `[47]` memoria, `[71]` publicidad, `[88]`
ciencia politica. Los otros seis (`[16]` amor, `[19]` internet, `[39]` GPS, `[43]`
fotosintesis, `[63]` corazon, `[67]` teoria musical) v2 los respondio en italiano o
espanol, asi que ninguno de los dos cumplio.

El balance neto es 29 a 11 a favor de v3: en 29 prompts v2 se fue a otro idioma
romance y v3 respondio en frances; en 11 v3 se fue al ingles y v2 no.

## 5. Veredicto

**v3_250 es mejor parche.** No por lo que dice `eval_report.md` — esa tabla no es
comparable — ni por la compliance reportada en `eval_open` — esa esta inflada a favor
de v2 por un bug del detector. Es mejor por tres cosas medibles sobre el mismo
conjunto de 99 prompts:

1. **Frances real 79.8% vs 56.6%** (+23 puntos), y sobre todo aguanta el frances en
   prompts procedimentales, que es donde v2 se derrumba al italiano (80% vs 33%).
2. **CE del head -4.076 vs -3.746 nats**: empuja mas fuerte la decision de idioma.
3. **Overlap de contenido con la referencia 0.204 vs 0.152**: se parece mas a lo que
   diria el modelo con el prompt frances explicito.

Sobre la calidad de fondo, la intuicion de "v3 esta mas fundamentado" se sostiene en
absoluto (66 respuestas usables vs 46) pero **no** por menos alucinacion: condicionado
a que la respuesta salga en frances, los dos fallan en ~20% de los casos. La mejora es
de cumplimiento, no de veracidad. Si el objetivo del proximo run es reducir el delirio,
el banco de 250 preguntas no es la palanca — ya se agoto ahi.

## 6. Que arreglar antes del proximo run

1. **`checkers.py`: agregar canal IT y PT.** Sin eso, cualquier comparacion de
   compliance entre parches es ruido. Concretamente: separar `_ACCENTED_FR` de los
   acentos italianos/portugueses (o dejar de contar acentos como evidencia positiva de
   frances cuando hay evidencia lexica de otro romance), y sacar `il`/`le` de las
   palabras que cuentan como francesas sin desambiguar.
2. **Evaluar los dos parches sobre el mismo held-out cerrado.** Ahora comparten 1 de
   38/20 preguntas. Fijar el split y el banco, o al menos reportar el n comun.
3. **Medir alucinacion aparte de idioma.** El eval actual no tiene ninguna senal para
   esto en los prompts abiertos: `overlap` con la referencia es lo mas cercano y es
   una Jaccard de palabras de contenido. Un juez sobre el par (referencia, parche)
   separaria "cambio de idioma" de "cambio de hecho".
4. **Vigilar el colapso a una linea.** v3 tiene 5 respuestas por debajo de 120
   caracteres y 6 clasificadas como degeneradas. Ninguna metrica actual las penaliza:
   *"La réponse est : La ligne!"* puntua `french_score = 1.00`.
