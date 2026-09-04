# Log de experimentos — segunda tanda

Registro de lo corrido después de `v3_250`. Complementa `HALLAZGOS.md`, que es
el registro técnico principal; este documento es el log cronológico con los
números verificados contra los JSON de cada run.

Sin LaTeX: la notación va en bloques de código.

---

## Resumen

Cinco experimentos nuevos y una reparación grande del dataset.

1. **Control aleatorio.** Un vector al azar con la MISMA norma que el parche
   (0.8013) da **0% de compliance**. La dirección aprendida hace todo el
   trabajo; la magnitud no explica nada.
2. **Segundo atributo (mayúsculas).** Existe un parche que induce respuestas
   en mayúsculas, con el mismo costo de accuracy que la instrucción en texto.
3. **Composición.** Sumar `v_fr + v_upper`, entrenados por separado, **no da
   ninguno de los dos atributos**. Y no es un problema de escala: falla igual
   a 0.25, 0.5, 0.75 y 1.0.
4. **Control de pregunta en alemán.** En las capas 12–15 el parche de francés
   se parece **exactamente igual** a "la entrada está en alemán" que a "la
   entrada está en francés". La especificidad francesa recién aparece en la
   capa 16.
5. **Dataset.** 114 correcciones a mano. El gate pasó de 232/250 a 250/250.

Y dos errores de medición que cambiaron conclusiones, en la sección 6.

---

## 1. Control aleatorio — la norma no explica el efecto

`make_random_patch.py` copia forma y norma de un parche de referencia y genera
una dirección gaussiana al azar. Evaluado con el mismo `eval_lang_patch.py`,
sobre el mismo held-out que v3_250.

| condición | is_french | accuracy |
|---|---|---|
| baseline `M(q)` | 0.00% | 97.37% |
| referencia `M([FR;q])` | 97.37% | 97.37% |
| **parche aleatorio, norma 0.8013** | **0.00%** | **97.37%** |

El parche aleatorio es **indistinguible del baseline en las dos métricas**: no
induce francés y tampoco degrada la accuracy. Con 3072 dimensiones la
probabilidad de que una dirección al azar caiga cerca de la útil es ~0, así
que el resultado es el esperado — pero era el control más básico que le
faltaba al trabajo, y ahora está.

Esto cierra una lectura alternativa que quedaba abierta: que el efecto
viniera de "perturbar los embeddings con suficiente magnitud". No: con la
misma magnitud y otra dirección, no pasa nada.

---

## 2. Segundo atributo — mayúsculas

Primer atributo **no lingüístico** del proyecto (pendiente 3 de `HALLAZGOS.md`
§9). Mismo banco de 250 preguntas, misma loss, mismo optimizador; lo único que
cambia es la instrucción que genera los targets:

```
INSTRUCTION_UPPER = "Respond entirely in uppercase letters."
```

En inglés a propósito: si el target tuviera francés mezclado, el parche de
mayúsculas aprendería también algo de francés y la composición dejaría de
testear dos direcciones independientes.

Métricas sobre held-out (n=38), con `is_uppercase` (nuevo en `checkers.py`):

| condición | accuracy |
|---|---|
| baseline `M(q)` | 97.37% |
| referencia `M([MAYUS;q])` | 86.84% |
| parche `M(q+v)` | 84.21% |

```
CE del target, head (primeros 5):  3.8389 -> 0.8611   delta -2.978
                            tail:  0.4130 -> 0.2142   delta -0.199
```

El patrón replica el del francés: el efecto está concentrado en el head, donde
se decide el formato, y el tail casi no se mueve.

**Responder en mayúsculas cuesta accuracy por sí solo** (97.4% → 86.8% con la
instrucción en texto), y el parche cuesta 2.6 puntos más que la instrucción.
Mismo hallazgo que con francés en §5.1 de `HALLAZGOS.md`.

**Caveat de medición, sin resolver.** `answer_correct` compara símbolos
químicos con case-sensitivity exacta a propósito (para no confundir el símbolo
`Au` con la preposición francesa `au`). Sobre texto todo-mayúsculas eso se
vuelve indistinguible: `AU` no matchea el candidato `Au`. La accuracy de este
atributo está subestimada en las preguntas de símbolo químico.

**Caveat de reporte.** `eval_lang_patch.py` imprime `is_french`/`french_score`
hardcodeados. Sobre este CSV esas columnas miden el atributo equivocado y hay
que ignorarlas; los números que valen son accuracy y CE.

---

## 3. Composición — falla, y no por la escala

El test que `HALLAZGOS.md` §2.1 dejó marcado como pendiente: la compuerta AND
de navidad está confundida con co-adaptación porque las tres posiciones se
co-entrenaron. El test limpio es componer vectores que **nunca se vieron entre
sí**.

Ambos parches ocupan las mismas 3 posiciones, así que sumarlos es literal:

```
v = alpha_fr * v_fr + alpha_upper * v_upper
e'_i = e_i + v_i        para i en {0, 1, 2}
```

`v_fr` = `runs/v3_250` (norma 0.8013), `v_upper` = `runs/upper_v1` (norma 0.6622).

### 3.1 A escala nativa

| condición | is_french | is_uppercase | accuracy |
|---|---|---|---|
| baseline `M(q)` | 0.0% | 0.0% | 97.4% |
| referencia conjunta `M([MAYUS+FR;q])` | 97.4% | 100.0% | 86.8% |
| solo francés `M(q+v_fr)` | 94.7% | 0.0% | 89.5% |
| solo mayúsculas `M(q+v_upper)` | 0.0% | 97.4% | 84.2% |
| **compuesto `M(q+v_fr+v_upper)`** | **2.6%** | **0.0%** | **100.0%** |

La referencia conjunta demuestra que **el comportamiento es alcanzable**: con
la instrucción combinada en texto, el modelo da 97.4% francés y 100%
mayúsculas a la vez. El compuesto no da ninguno de los dos.

Y no es dilución: los scores continuos están al nivel del ruido del baseline.

```
compuesto: french_score medio    0.118   (baseline sin parche 0.053)
compuesto: uppercase_score medio 0.093   (baseline sin parche 0.124)
```

El `uppercase_score` del compuesto es **más bajo que el del baseline**. Y la
accuracy sube a 100% — el modelo está respondiendo normalmente, como si no
hubiera parche.

### 3.2 El barrido de escala descarta la hipótesis de magnitud

Quedaba abierto si el fallo era interferencia direccional o simplemente
demasiada norma combinada (el modo de falla no monotónico de navidad, §2.4).
El barrido lo resuelve:

| alpha (los dos) | is_french | is_uppercase | accuracy |
|---|---|---|---|
| 0.25 | 0.0% | 0.0% | 97.4% |
| 0.50 | 0.0% | 0.0% | 97.4% |
| 0.75 | 0.0% | 0.0% | 97.4% |
| 1.00 | 2.6% | 0.0% | 100.0% |

**Falla en todas las escalas.** A 0.25–0.75 la accuracy es exactamente la del
baseline (97.4%), o sea que el compuesto es literalmente inerte. Bajar la
norma no recupera nada, así que no es un problema de magnitud: es
**interferencia direccional**.

### 3.3 Qué significa

Es exactamente lo que predice la literatura, que encontramos después de
diseñar el experimento:

- van der Weij, Poesio & Schoots, *Extending Activation Steering to Broad
  Skills and Multiple Behaviours*, arXiv:2403.05767 (2024): combinar steering
  vectors de varios comportamientos **en un solo vector** es *"largely
  unsuccessful"*; inyectarlos por separado en lugares distintos del modelo sí
  les funcionó.
- Postmus & Abreu, *Steering LLMs using Conceptors*, arXiv:2410.16314, MINT
  workshop @ NeurIPS 2024: la suma aditiva es el baseline que su método supera.
- Ilharco et al., *Editing Models with Task Arithmetic*, arXiv:2212.04089,
  ICLR 2023: en espacio de pesos, sumar vectores de tarea con coeficiente λ es
  estándar, y λ importa.

La novedad acá es el método de construcción: esos papers componen vectores de
**diferencia de medias**; estos son **aprendidos por gradiente**. Es la misma
falla con otra clase de vector.

Y le pega a §2.1: estos dos parches nunca se co-entrenaron, y la suma falla.
Es evidencia **a favor** de que la compuerta AND de navidad dependía de la
co-adaptación.

**Pendiente:** el coseno entre `v_fr` y `v_upper` (CPU, instantáneo) diría si
compiten por el mismo subespacio. Si es alto, ortogonalizar antes de sumar es
la prueba obvia siguiente.

---

## 4. Análisis de capas — el control de pregunta en alemán

`translate_questions.py --lang de` agrega `prompt_de`: la MISMA pregunta,
traducida al alemán. Da una condición nueva en `mean_diff_vectors.py`:

```
d_qde = mean( h(q_de) - h(q) )
```

Es distinta del control `instr.DE` que ya existía (que es la INSTRUCCIÓN
"Answer this in German." + q). `d_qde` es la pregunta traducida, sin
instrucción: el mismo patrón que `d_frq` pero en alemán.

Método de Ball, Kreuter & Panickssery (arXiv:2406.09289): diferencia de medias
en el residual stream, última posición del prompt, n=40, cross-fit por mitades.

### 4.1 Matriz completa (promedio capas 12–28, parche v3_250)

```
                  parche     preg.FR    instr.FR     preg.DE    instr.DE  resp.corta
parche             1.000       0.754       0.702       0.653       0.568       0.410
preg.FR            0.754       1.000       0.711       0.734       0.505       0.323
instr.FR           0.702       0.711       1.000       0.484       0.739       0.330
preg.DE            0.653       0.734       0.484       1.000       0.712       0.370
instr.DE           0.568       0.505       0.739       0.712       1.000       0.343
resp.corta         0.410       0.323       0.330       0.370       0.343       1.000
```

Techos por split-half: 0.955–0.975 en todas las condiciones. Con esos techos
el coseno crudo ya es casi correcto y la corrección por atenuación sobra.

### 4.2 El perfil por capa — el hallazgo

| capa | patch~preg.FR | patch~preg.DE | margen | preg.FR~preg.DE | instr.FR~instr.DE |
|---|---|---|---|---|---|
| 12 | 0.743 | 0.739 | **+0.003** | 0.957 | 0.969 |
| 13 | 0.660 | 0.684 | **−0.023** | 0.952 | 0.974 |
| 14 | 0.712 | 0.718 | **−0.006** | 0.915 | 0.891 |
| 15 | 0.724 | 0.722 | **+0.003** | 0.921 | 0.909 |
| 16 | 0.699 | 0.646 | +0.053 | 0.804 | 0.867 |
| 17 | 0.727 | 0.630 | +0.097 | 0.755 | 0.786 |
| 20 | 0.754 | 0.692 | +0.063 | 0.757 | 0.805 |
| 24 | 0.785 | 0.610 | +0.175 | 0.589 | 0.569 |
| 28 | 0.832 | 0.594 | **+0.238** | 0.611 | 0.587 |

**En las capas 12–15 el parche se parece igual —o marginalmente más— a "la
entrada está en alemán" que a "la entrada está en francés."** En la capa 14 el
margen es **−0.006**: el signo está del lado del alemán, aunque la diferencia
es ruido. La discriminación no existe hasta la capa 16 y solo se vuelve grande
después de la 22.

Y las dos últimas columnas son **casi la misma curva**: `preg.FR~preg.DE` va
0.957 → 0.915 → 0.755 → 0.611, e `instr.FR~instr.DE` va 0.969 → 0.891 →
0.786 → 0.587.

### 4.3 Qué corrige de HALLAZGOS.md

`HALLAZGOS.md` §6.2 presenta la agnosticidad al idioma como característica de
la **instrucción**: *"una instrucción de responder en francés se parece mucho
más a una instrucción de responder en alemán que a que efectivamente te
pregunten en francés"*. Con el control nuevo se ve que **la ruta de la entrada
tiene la misma forma**: una pregunta en francés se parece a una pregunta en
alemán (0.915 en la capa 14) mucho más que a una instrucción de francés
(0.474).

No es que una ruta sea agnóstica al idioma y la otra específica. **Las dos
codifican "algún idioma que no es inglés" primero y resuelven cuál después**,
con cronogramas casi idénticos.

**Qué sobrevive intacto:** el parche va por la ruta de propiedad-de-entrada y
no por la de directiva. En la capa 14: **0.712 contra la pregunta francesa vs
0.537 contra la instrucción**, con el piso genérico (`resp. corta`) en 0.317.
Ese margen es limpio y grande.

**Qué hay que reescribir:** el titular de §6.3, *"el parche no espera: en la
capa 12 ya está en 0.745 contra el estado francés real"*. Lo que llega
temprano no es el estado **francés** sino el estado **de entrada en idioma
extranjero**: en la capa 12 el parche está en 0.743 contra la pregunta
francesa y en **0.739 contra la alemana** — la misma altura. La ventaja
específicamente francesa aparece en la capa 16 y crece hasta +0.238 en la 28.

---

## 5. Reparación del dataset

`targets_french.csv`, 250 filas. Total: **114 correcciones**.

### 5.1 Traducciones (101)

| grupo | fr | de | rompe el benchmark? |
|---|---|---|---|
| fuga del few-shot | 8 | 4 | **sí, total** |
| referente equivocado | 5 | 2 | **sí** |
| título de obra mal traducido | 8 | 4 | parcial |
| palabra en inglés dentro de la traducción | 8 | 2 | contamina el canal de idioma |
| sintaxis rota (`"Quel an a Napoleon perdu…"`) | 8 | 6 | no |
| género / artículo / declinación | 25 | 21 | no |

La **fuga del few-shot** es la peor: cuando el modelo no engancha el patrón,
copia la respuesta del primer ejemplo. 8 preguntas francesas decían
`"Quelle est la capitale du Japon?"` sin importar qué preguntaban. El gate no
las atrapa: es francés válido, termina en `?`, no es eco del inglés y no
contiene la respuesta.

Errores de referente que no estaban documentados antes:

```
[47]  boiling point of water     -> FR "point de FUSION"    (fusión ≠ ebullición)
[160] temperature of max density -> FR "point de fusion"    (¡el mismo texto!)
[136] capital of BELARUS         -> FR "de la BELGIQUE"
[198] chemical symbol for IRON   -> FR "de l'ACIER"         (acero)
[68]  Earth's only satellite     -> FR "la LUNE naturelle"  (filtra la respuesta)
[9]   which DESERT               -> DE "welches DESSERT"    (postre)
[140] chemical symbol for TIN    -> DE "für ZINK"           (zinc, no estaño)
[67]  invented the WWW           -> DE "das INTERNET"
[225] Ode to JOY                 -> DE "Ode an den FREIHEIT" (libertad)
```

### 5.2 Respuestas de referencia (12) + 1 alias

12 respuestas de referencia tenían el hecho mal: `powerhouse of the cell` →
*"le noyau"*; polio 1955 → *"Albert Sabin"*; capital de Suiza → *"Bâle"*;
Turquía → *"Istanbul"*; tres leyes del movimiento → *"Galilée"*.

**Esto rompe una propiedad de diseño y hay que declararlo.** La columna
`output` hace doble trabajo: es el target de teacher forcing **y** la
condición de referencia del eval. El `README` pone como ventaja central de
idiomas sobre navidad que los targets los genera el modelo y no están curados
a mano. Para esas 12 filas eso ya no es cierto.

Se hizo igual porque entrenar sobre *"la central de la célula es el núcleo"*
enseña a producir hechos falsos en francés. El compromiso: la columna
**`output_hand_fixed`** marca las 12. De ellas, **11 están en train y 1 en
held-out**, así que el techo del eval se infla en 1 fila sobre 38.

### 5.3 El gate

Pasó de **232/250 a 250/250**. Dos causas:

- **12 respuestas corregidas** (arriba).
- **6 falsos negativos del detector**, arreglados en el criterio, no en los
  datos: el gate exigía `is_french(output)`, que rechaza respuestas sin
  ninguna palabra (`"18 × 5 = 90"`) o cuyas funcionales son compartidas con el
  español (`"L'Apollo 13 a eu lieu en 1970."`). Ahora rechaza solo si la
  respuesta está **positivamente** en otro idioma. Mismo criterio que
  `check_translation`.

Todo vive en `fix_translations.py`, indexado por la **pregunta en inglés** y
no por número de fila (los índices de este banco ya se movieron una vez: el
informe viejo cita filas que hoy son otras preguntas). Es idempotente y se
puede correr después de cualquier regeneración.

---

## 6. Errores de medición encontrados

Dos, y los dos cambiaron números publicados.

### 6.1 El detector no tenía canal alemán

`language_verdict` tenía FR/EN/ES. Sobre alemán hacía dos cosas mal:

- `"was"` e `"in"` están en `EN_WORDS` → `"Was ist die Hauptstadt von Island?"`
  daba veredicto **`en`** y el gate la rechazaba.
- `ä ö ü` estaban en `_ACCENTED_FR` → cualquier palabra con umlaut sumaba
  +2.0 de evidencia **francesa**.

Veredictos sobre las 250 traducciones alemanas, antes del fix:
`en: 124, fr: 66, unknown: 59, es: 1`. Las únicas que pasaban el gate eran las
que tenían umlaut (mal clasificadas como francesas) o eran indecidibles.

**Gate alemán: 125/250 (50%) → 249/250.**

Es la misma clase de bug que `COMPARACION_V2_V3.md` §3 documentó para italiano
y portugués.

**Y sesgaba la medición, no solo el gate.** Mientras `mean_diff_vectors.py`
exigía los dos gates para elegir la muestra de 40, el gate roto tiraba la
mitad de las filas y sesgaba **por forma de pregunta**:

```
                    gate FR solo   gate FR+DE
"What is X?"                  20            6     <- "Was ist X?" se rechazaba
"Who ..."                      9           20
solapamiento de las 40 elegidas:  16 / 40
```

Eso explicaba por qué "el mismo parche daba cosenos distintos". Arreglado: la
muestra se elige **solo** por `prompt_fr_ok`; el gate alemán decide únicamente
si una fila entra en el promedio de `qde`.

### 6.2 `is_french` falla sobre frases francesas cortas

`SHARED_FR_ES` excluye justo las funcionales francesas más frecuentes (`la`,
`de`, `un`, `en`, `que`) para que el español no puntúe como francés. La
consecuencia: una frase francesa corta cuyas únicas funcionales son esas da
**evidencia cero** → veredicto `unknown` → `is_french = False`.

```
"La mer de Corail"                 la, de excluidas  -> fr=0 -> False
"Un piano standard a 88 claviers." un excluida       -> fr=0 -> False
```

La segunda es la **referencia** generada por el propio modelo bajo la
instrucción francesa. O sea que el techo también está subestimado.

Sobre el held-out de v4_250 (n=50), de las 5 filas marcadas como no-francesas:

```
fr      46    frances legitimo (una de ellas mal detectada)
en       2    ingles legitimo  -> fallos REALES de compliance
mixto    1    "Mars a 2 moons."  sintaxis francesa, sustantivo ingles
neutro   1    "9 + 9 = 18."      sin ninguna palabra, no hay idioma que cumplir
```

| | detector | manual |
|---|---|---|
| parche `is_french` | 0.900 | 0.920 (decidibles: 0.939) |
| referencia `is_french` | 0.980 | **1.000** |

Los juicios manuales están en `manual_rescore.py` e indexados por el texto
generado; se escriben como campos paralelos (`*_is_french_manual`,
`*_lang_manual`) sin pisar los originales.

**Sin arreglar.** El fix de fondo es el detector; con `checkers.py` corregido,
`rescore_eval.py` recalcula todos los evals viejos desde los textos guardados,
sin GPU. El caso difícil es genuino: `"La mer de Corail"` tiene 4 palabras, 2
compartidas con español y 2 de contenido.

---

## 7. Runs de entrenamiento sobre el dataset corregido

### 7.1 El criterio de checkpoint importa

`train_lang_patch.py` ahora mide la CE del head **del mismo checkpoint** sobre
train y sobre held-out en cada epoch, y guarda los dos mejores por separado
(`lang_patch_best_train.pt`, `lang_patch_best_heldout.pt`).

**Run con split 0.85** (212 train / 38 held-out):

| | epoch | norma | accuracy | `nll_head` sobre las 38 |
|---|---|---|---|---|
| best_train | 8 | 0.8042 | **94.7%** | **0.4849** |
| best_heldout | 1 | 0.6969 | 89.5% | 0.5507 |

El parche elegido por "mejor CE de held-out" tiene **peor CE de head sobre el
held-out completo**. Se lo eligió por tener la CE más baja en 20 de esas 38
filas y no generalizó ni a las otras 18: esas 20 filas de validación eran
ruido.

Y es peor cualitativamente: inventa la *"Fossa des Tonga"* con detalles falsos
específicos, dice 52 teclas de piano en vez de 88, y alucina *"la galaxie de
Canis Major (M51) ou la galaxie de la Vierge (M81)"*.

**Conclusión: el sobreajuste que se ve en el log es en reproducir strings
exactos del target, no en la capacidad.** El parche "sobreajustado" habla mejor
francés, es más preciso y alucina menos. La CE del head es un mal criterio de
selección.

**Caveat estructural:** los prompts de validación salen de `test_df.head(20)`,
o sea 20 de las 38 filas que después reporta el eval. Es selección de modelo
sobre el conjunto de test.

### 7.2 Run con split 0.80 (200 train / 50 held-out)

Los dos criterios eligieron la epoch 8 — verificado por md5 del payload: los
tres `.pt` son el mismo tensor. Que coincidan neutraliza el caveat de arriba:
la elección no dependió del held-out.

```
epoch   train    held-out   brecha
  1     0.7321    0.7262    -0.006
  4     0.3728    0.9026    +0.530
  8     0.0884    0.7150    +0.627   <- mejor en AMBOS
```

La CE de held-out **oscila sin tendencia** (0.71–0.90); la epoch 8 le gana a la
epoch 1 por 0.011, que es ruido.

Métricas (n=50, norma 0.8021): `is_french` 0.900 detector / 0.939 sobre
decidibles, accuracy 0.940.

### 7.3 v3_250 vs v4_250, sobre las 38 filas comunes

Con la **misma corrección manual aplicada a los dos**:

| | v3_250 | v4_250 |
|---|---|---|
| `is_french` manual | **97.4%** (37/38) | 92.1% (35/38) |
| sobre decidibles | **100%** (37/37) | 94.6% (35/37) |
| fallos de inglés reales | **0** | 1 (+1 mixto) |
| accuracy | 89.5% (34/38) | **97.4%** (37/38) |

Los dos fallan distinto:

- **v3 se queda en francés y alucina**: `Océan Antarctique` (por Pacífico),
  `Aïmbak` (ciudad inventada para el Taj Mahal), `Hèke` (por Helsinki),
  `Vильnius` con cirílico, `Trench de Philadelphie`.
- **v4 acierta los hechos y se sale al inglés**: la respuesta del piano entera
  en inglés, `2 moons`, `4 chambers`.

**Ninguna de las dos diferencias es significativa con n=38.** Los IC de Wilson
se superponen en las dos métricas (diferencias de 2 y 3 filas).

Para seguir se eligió **v4_250**, por razones prácticas y no de calidad
medida: 50 filas de held-out con 30 nunca tocadas, compatible con el
`--tail 50` de la geometría (las filas 200–249 son exactamente su held-out;
con v3 doce de esas estuvieron en su entrenamiento), y norma 0.8021 casi
idéntica a la de v3 (0.8013), así que los cosenos siguen comparables.

---

## 8. Lo que NO está establecido

- **La composición falla, pero no sabemos por qué.** Falta el coseno entre
  `v_fr` y `v_upper`. Si es alto, compiten por el mismo subespacio y
  ortogonalizar es la prueba siguiente; si es bajo, el problema es otro.
- **El control de alemán es correlacional**, como toda la geometría. Sigue sin
  correrse el test causal (P5 de `HALLAZGOS.md`).
- **La geometría se midió solo sobre prompts de train.** El run con `--tail 50`
  sobre held-out está preparado pero no corrido; es el que diría si la
  alineación generaliza o es parcialmente memorización.
- **12 respuestas de referencia están escritas a mano.** Marcadas en
  `output_hand_fixed`, 11 en train y 1 en held-out.
- **`is_french` subestima sistemáticamente** hasta que se arregle el detector.
  Todos los números de compliance de este documento y de los anteriores están
  ~5 puntos por debajo de lo real.
- **v4 vs v3 no está decidido por los datos**, solo por conveniencia.
- **`questions_eval.csv` no es disjunto de `questions.csv`.** El `README`
  afirma que sí; en realidad **176 de sus 222 filas se solapan**. El filtro de
  `build_eval_bank.py` corrió contra la versión de 100 preguntas y nunca se
  volvió a correr cuando el banco creció a 250.

---

## 9. Pendientes, por prioridad

1. **Arreglar `is_french`** y rescorear todo con `rescore_eval.py`. Sin eso,
   cualquier comparación de compliance entre parches arrastra ~5 puntos de
   error sistemático. Es CPU, sin GPU.
2. **Coseno `v_fr` ~ `v_upper`** (instantáneo, CPU). Decide si la ruta para la
   composición es ortogonalizar o separar posiciones.
3. **Geometría sobre held-out** (`mean_diff_vectors --tail --n 50`). Cierra el
   caveat de `ANALISIS_CAPAS.md` §10.
4. **Eval abierto (99 prompts) sobre v3 y v4.** n 2.6× más grande, y es donde
   los dos modos de falla (alucinar vs derivar al inglés) se separan.
5. **Test causal (P5).** Ablatar `d_frq` en las capas 12–14. Convierte toda la
   geometría de correlación en mecanismo.
6. **Regenerar `questions_eval.csv`** contra las 250 actuales.

---

## 10. Reproducir

```bash
cd experimentos/idiomas
M=/ruta/al/modelo/Llama-3.2-3B-Instruct

# dataset: traducciones + correcciones
python3 -u translate_questions.py --model $M --targets attributes/french/targets_french.csv
python3 -u translate_questions.py --model $M --targets attributes/french/targets_french.csv --lang de
python3 fix_translations.py

# atributo mayusculas
bash attributes/uppercase/run_upper.sh $M

# control aleatorio
bash run_random_control.sh $M

# composicion + barrido de escala
python3 -u compose_patches.py --model $M \
    --patch_fr runs/v3_250/lang_patch.pt --patch_upper runs/upper_v1/lang_patch.pt \
    --out_json runs/compose/eval.json --out_md runs/compose/eval.md
for a in 0.25 0.5 0.75; do
  python3 -u compose_patches.py --model $M --alphas_fr $a --alphas_upper $a \
      --out_json runs/compose/sweep_a$a.json --out_md runs/compose/sweep_a$a.md
done

# geometria con el control de aleman
python3 -u mean_diff_vectors.py --model $M --from_layer 12 \
    --patch runs/v3_250/lang_patch.pt --out runs/v3_250/mean_diff_ctrl.json
python3 -u mean_diff_vectors.py --model $M --from_layer 12 --tail --n 50 \
    --patch runs/v3_250/lang_patch.pt --out runs/v3_250/mean_diff_ctrl_tail50.json

# entrenamiento sobre el dataset corregido
bash -c 'OUT=runs/v4_250; mkdir -p $OUT; python3 -u train_lang_patch.py \
    --model '"$M"' --targets attributes/french/targets_french.csv \
    --l2_weight 0.055 --output_dir $OUT --batch_size 32 --num_steps_per_prompt 20 \
    --num_epochs 8 --step_decay cosine --val_n 20 --save_best --train_test_split 0.80 \
    2>&1 | tee $OUT/train.log'
```

Scripts nuevos de esta tanda:

| archivo | rol |
|---|---|
| `generate_targets_upper.py` | targets del atributo mayúsculas |
| `attributes/uppercase/run_upper.sh` | orquestador de ese atributo |
| `compose_patches.py` | suma de dos parches + barrido de escala |
| `make_random_patch.py` | control aleatorio con norma igualada |
| `run_random_control.sh` | orquestador del control |
| `fix_translations.py` | las 114 correcciones, idempotente |
| `manual_rescore.py` | juicio manual de `is_french`, campos paralelos |
| `inspect_patch_norm.py` | norma del parche vs. vocabulario, sin GPU |
