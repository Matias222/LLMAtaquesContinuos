# Existencia de un parche aditivo de idioma

**Pregunta**: existe un vector `v` que, sumado a los embeddings de una pregunta `q`,
haga que el modelo responda en frances — sin que la instruccion "Answer in French."
este en el contexto, y generalizando a preguntas nunca vistas?

Es el paso de calibracion (`C1`, existencia) antes del experimento que importa,
que es la composicion `v_FR + v_LC`.

## Por que este diseno y no el de navidad

| | navidad | idiomas |
|---|---|---|
| targets | CSV curado a mano | **el modelo se los genera**: `y = M([FR ; q])` |
| compliance | lexicon de palabras navidenas | `is_french()` + score continuo |
| fidelidad | proxy lexico contra el baseline | **accuracy verificable** contra la respuesta correcta |
| referencia | ninguna | **`M([FR ; q])`**, el techo natural |

La referencia es lo que faltaba. Sin ella no se puede saber si una caida de accuracy
la causa el parche o la instruccion misma.

Las 100 preguntas de `data/questions.csv` tienen respuestas **invariantes al idioma**
(nombres propios, anios, simbolos quimicos, numeros), asi que la misma metrica de
accuracy funciona en ingles y en frances. Donde la forma francesa difiere, la
columna `aliases` la lista explicitamente.

## Objetivo de entrenamiento

```
L = CE(logits_parcheados, y_frances_completo) + lambda_L2 * ||v||^2
```

Sin objetivo de prefijo: no hay ningun target lexico fijo que inducir, asi que el
prefix hack no es una solucion alcanzable. Optimizador sign-SGD, identico a legacy.

Hiperparametros copiados de `resultados/primera_parte/noprefix_l2_0.08`, el mejor
run noprefix de navidad (53% de compliance en held-out):

```
num_epochs=5   num_steps_per_prompt=75   num_patch_positions=3
coherence_weight=1.0   prefix_match_length=0   step_size=0.00025   split=0.8
```

Lo unico que se barre es `l2_weight` en **{0.045, 0.08, 0.1}** — los mismos tres
valores, para que los numeros sean comparables run a run.

## Correr

```bash
bash attributes/french/run_french.sh /ruta/al/modelo/Llama-3.2-3B-Instruct
```

Hace: targets -> (train + eval + inspect) x 3 L2 -> tabla resumen.
Resultados en `runs/french_l2_<L2>/`.

Por partes:

```bash
python3 generate_targets.py  --model $M                              # paso 0
python3 train_lang_patch.py  --model $M --l2_weight 0.08 --output_dir runs/french_l2_0.08
python3 eval_lang_patch.py   --model $M --patch runs/french_l2_0.08/lang_patch.pt \
                             --out_json runs/french_l2_0.08/eval_report.json \
                             --out_md   runs/french_l2_0.08/eval_report.md
python3 summarize.py "runs/*/eval_report.json"
```

Dose-response (despues, sobre el mejor parche):

```bash
for a in 0.5 1.0 1.75 2.5; do
  python3 eval_lang_patch.py --model $M --patch runs/french_l2_0.08/lang_patch.pt \
      --scale $a --out_json runs/scale_$a.json --out_md runs/scale_$a.md
done
```

## Como leer la salida

`generate_targets.py` imprime primero el gate de calidad. **Si la referencia
`M([FR;q])` no llega a ~90% de frances y ~80% de accuracy, parar**: el problema
esta en la instruccion o en el dataset, no en el parche, y entrenar sobre esos
targets no informa nada.

`summarize.py` da la tabla final:

| columna | que mirar |
|---|---|
| `FR patch` vs `FR ref` | cuanta compliance recupera el parche respecto del techo |
| `acc patch` vs `acc ref` | si el parche degrada **mas** que la instruccion en texto |
| `dCE head` | costo del **cambio** de idioma. Es la señal real |
| `dCE all` | diluida; sirve solo para comparar con corridas viejas |

**Vara de comparacion**: navidad noprefix dio 53% de compliance en held-out.
Frances por encima de eso significa que el canal transporta idioma mas facil que
estilo; por debajo, que lo transporta peor. Los dos casos son resultado.

**Regla de decision**: held-out >= 70% de compliance con norma en percentil <1% del
vocabulario y accuracy cerca de la referencia -> existencia establecida, se pasa a
composicion. No gastar mas de estos 3 runs aca.

## Archivos

| archivo | rol |
|---|---|
| `data/questions.csv` | 100 preguntas + respuesta + alias franceses. Barajado con seed=42 (el split es posicional, no puede quedar ordenado por categoria) |
| `checkers.py` | `is_french`, `french_score`, `answer_correct`. `python3 checkers.py` corre su auto-test |
| `lm.py` | carga de modelo, generacion greedy desde embeddings, aplicacion del parche, CE de un target |
| `generate_targets.py` | paso 0: genera `y = M([FR;q])` + baseline + gate de calidad |
| `train_lang_patch.py` | paso 1: teacher forcing con gradiente (sign-SGD) |
| `eval_lang_patch.py` | paso 2: las tres condiciones sobre held-out |
| `summarize.py` | tabla comparativa de los 3 L2 |
| `attributes/french/run_french.sh` | orquestador |

## Un solo turno por generacion

`lm.generate()` corta en `<|eot_id|>`. Sin eso el modelo cierra el turno y arranca
el siguiente, y como decodificamos con `skip_special_tokens=True` los headers
desaparecen pero el token de texto plano `assistant` sobrevive, dejando varios
turnos pegados en un solo string:

```
"... est le Sahara.assistant\n\nVous voulez savoir plus sur le Sahara?assistant\n\nOui..."
```

Como target de teacher forcing eso es veneno: el parche aprenderia a producir
multiturno y a emitir el token de rol.

Hay dos capas:

1. **Primaria**: `stop_token_ids()` para la generacion en `<|eot_id|>` /
   `<|end_of_text|>`, y el token de corte no entra en la salida.
2. **Red de seguridad**: `truncate_at_role_leak()` corta el texto en la fuga de
   rol, para el caso en que el parche suprima el eot. No toca texto legitimo que
   contenga la palabra "assistant" (solo dispara despues de fin de oracion o de
   salto de linea).

La columna `role_leak` del reporte cuenta cuantas veces disparo la capa 2, o sea
cuantas veces el modelo **quiso** seguir pese al corte. Con el eot bien cortado
esa señal ya es limpia, y es directamente comparable con el hallazgo de navidad:
alli el role leak fue 0.77-1.00 en todo run efectivo y 0.00 en todo run inefectivo,
pero estaba confundido con la brevedad de las respuestas porque no se cortaba en
eot. Aca no.

## Por que el barrido v1 se estanco

El primer barrido llego a su meseta en la epoch 1 y despues oscilo sin tendencia:

| epoch | held-out CE | delta |
|---|---|---|
| 1 | 2.106 | -0.679 |
| 2 | 2.340 | -0.446 |
| 3 | 2.260 | -0.526 |

Efecto real estable (delta ~ -0.55, perplejidad 16.2 -> 9.3) pero **sin mejora
con mas entrenamiento**. Tres causas, ninguna es el L2:

1. **El optimizador orbita, no converge.** sign-SGD mueve cada coordenada
   exactamente `step_size` en cada paso, siempre, sin annealing. Nunca se
   asienta: la norma oscilo +-60% *dentro* de la epoch 1.
2. **Optimizacion secuencial por prompt.** 75 pasos sobre UN prompt antes de
   pasar al siguiente: el parche va a los tirones detras de cada ejemplo en vez
   de optimizar el objetivo promedio. Con `CE=0.046` en algunos prompts, eso es
   memorizacion de un solo ejemplo.
3. **Validacion con n=8.** Demasiado ruidosa para decidir nada.

**El L2 NO es la causa y bajarlo no ayuda**: a norma 0.306 el termino
`lambda*||v||^2` aporta 2.2% de la loss con lambda=0.045 y 4.8% con lambda=0.1.
Con sign-SGD el efecto real es todavia menor, porque solo cuenta si alcanza a
voltear el signo de una coordenada. La norma es chica porque el gradiente de CE
no la empuja mas, no porque el L2 la aplaste.

### Config v2

`train_lang_patch.py` acepta cuatro flags nuevos, **todos con default =
comportamiento v1**, asi que los runs viejos siguen siendo reproducibles:

| flag | default | que hace |
|---|---|---|
| `--batch_size` | 1 | acumula gradiente sobre B prompts y da UN paso. Optimiza el promedio |
| `--step_decay` | none | `cosine` anilla el paso a 0: la orbita se cierra |
| `--val_n` | 8 | prompts de validacion |
| `--save_best` | off | guarda el parche con mejor head CE, no un punto arbitrario de la orbita |

La validacion ahora reporta head y all por separado.

`bash attributes/french/run_french_v2.sh` corre la config recomendada:

```
--batch_size 8 --num_steps_per_prompt 12 --num_epochs 8
--step_decay cosine --val_n 20 --save_best
```

Ojo: batchear es **neutro en computo**. `N/B batches x S pasos x B forwards =
N*S forwards`, igual que antes. Y con S=12 en vez de 75, cada epoch cuesta 120
pasos en vez de 5775: v2 entero sale mas barato que v1.

## Por que la CE se parte en head y tail

`nll_of_target` mide con **teacher forcing**: le metemos la respuesta francesa
entera y preguntamos que probabilidad le asigna token a token. En cada paso el
modelo ve el prefijo frances *correcto*.

Consecuencia: el modelo paga el costo de CAMBIAR de idioma una sola vez, en los
primeros tokens. Despues, "continua esta oracion en frances" es trivial. Una
perplejidad de ~16 sobre texto frances es simplemente la perplejidad normal del
frances para este modelo: la CE mide **"este texto es plausible"**, no
**"lo habrias elegido"**.

Como la decision de idioma vive en 2-3 tokens de ~20, promediar sobre toda la
respuesta diluye la señal ~7x. Por eso el reporte separa:

- **head** (primeros `--head_k`, default 5): donde vive la decision de idioma
- **tail**: costo de continuacion, casi insensible al parche

`dCE head` es la metrica graduada util. `dCE all` queda por continuidad.

Esto tampoco reemplaza a `is_french` sobre generacion libre, que es el unico
numero que dice si el modelo **realmente** produce frances por su cuenta.

## El detector es de TRES idiomas, no de dos

El modelo a veces contesta en **espanol**. Un detector binario frances-vs-ingles
lo clasifica como frances con score 1.00, porque los dos idiomas comparten justo
las funcionales mas frecuentes: `de`, `la`, `que`, `en`, `un`, `se`.

`language_evidence()` cuenta tres canales. Dos detalles que importan:

- `SHARED_FR_ES` (de, la, que, en, un, se, si, entre, bien, no, me, te) no es
  evidencia de **ninguno** de los dos. Inflar este set rompe frases cortas
  legitimas, asi que `le`/`les` NO estan: son articulos frecuentisimos en
  frances y solo cliticos ocasionales en espanol.
- `por`, `al`, `lo`, `mi`, `su`, `sin` son exclusivas del espanol, no
  compartidas. Ponerlas en SHARED debilita la deteccion de espanol.

`language_verdict()` devuelve `fr` / `en` / `es` / `unknown`, y el reporte
imprime la distribucion, asi que un 90% de compliance ya no puede esconder
respuestas en un tercer idioma.

Regresion en `python3 checkers.py`: 15 frances, 8 ingles, 5 espanol, todos
sobre outputs reales de los runs.

## Si cambia el detector, no regeneres

Los textos ya estan guardados en el eval_report.json y son deterministas. Las
CE (`nll_*`) vienen del modelo y no dependen del detector.

```bash
python3 rescore_eval.py "runs/*/eval_*.json" --dry_run   # ver el delta
python3 rescore_eval.py "runs/*/eval_*.json"             # aplicar, deja .bak
```

## Deteccion de idioma: respuestas cortas

Las respuestas a estas preguntas son cortas ("La capitale du Chili est Santiago.",
6 tokens). El detector tiene que decidir con poca evidencia, asi que:

- **Los acentos son evidencia ADICIONAL de frances, no un fallback.** Frances sin
  tildes existe y es frecuente aca; tratar los acentos como reemplazo daba score
  0.00 sobre frances perfecto.
- `min_tokens = 3`.
- `language_verdict()` devuelve `fr` / `en` / `unknown`, para no confundir
  "respondio en ingles" con "demasiado corto para saber" (ej: "Paris.", que se
  escribe igual en los dos idiomas). El gate exige `fr` explicito.

`python3 checkers.py` corre la regresion contra outputs reales del run.

## Si ya generaste los targets

Las generaciones son deterministas y correctas; si cambia solo el detector, no
hace falta volver a pagar la GPU:

```bash
python3 rescore_targets.py --dry_run   # ver el delta
python3 rescore_targets.py             # aplicar, deja .bak
```

## Dos bancos de evaluacion mas alla del entrenamiento

El entrenamiento satura con 77 targets (CE 0.06 en la epoch 3). Lo que faltaba
era **potencia y variedad en el eval**. Ninguno de los dos bancos se usa para
entrenar.

### `data/questions_eval.csv` — 222 preguntas cortas verificables

Con 20 held-out no se puede distinguir 90% de 95% de accuracy: los IC de Wilson
son [70,97] y [76,99], se superponen casi enteros. Y la afirmacion "el parche
cuesta lo mismo que la instruccion" es justo la que va al abstract.

Lo genera `build_eval_bank.py` desde tablas de datos (capitales, elementos,
personas, anios, aritmetica, ciencia), no a mano. Descarta automaticamente las
preguntas cuyo enunciado contiene la respuesta, y el simbolo del yodo (`I`),
que en ingles colisiona con el pronombre.

```bash
python3 build_eval_bank.py
python3 -u generate_targets.py --model $M --questions data/questions_eval.csv \
    --out attributes/french/targets_eval.csv
python3 -u eval_lang_patch.py --model $M --patch runs/v2_french_l2_0.045/lang_patch.pt \
    --targets attributes/french/targets_eval.csv --train_test_split 0.0 \
    --out_json runs/v2_french_l2_0.045/eval_big.json --out_md runs/v2_french_l2_0.045/eval_big.md
```

### `data/questions_open.csv` — 99 prompts abiertos, el set exacto de navidad

Las preguntas cortas tienen una forma muy regular ("La capitale de X est Y"), y
el parche podria estar aprendiendo la plantilla en vez de "hablá francés". Los
prompts abiertos ("What is photosynthesis?", "How does a computer work?") exigen
sostener el frances durante 100 tokens.

Son **los mismos 99 prompts que uso navidad**, asi que la comparacion es directa
sobre estimulos identicos: mismo set, atributo inducido distinto. Eso testea si
el idioma se comporta como un atributo difuso (navidad, puede aparecer en
cualquier lado) o como un compromiso (se decide al principio).

```bash
bash attributes/french/run_french_open.sh runs/v2_french_l2_0.045/lang_patch.pt $M
```

Como no hay respuesta verificable, la accuracy se reemplaza por dos medidas:

| medida | que dice |
|---|---|
| `overlap parche vs referencia` | ambos son frances sobre la misma pregunta, asi que la comparacion es limpia. Alto = el parche produce la misma sustancia que la instruccion |
| `control de azar` | mismo overlap contra la referencia de OTRA pregunta. Es el piso |
| `frances por tercio` | el parche vive en 3 posiciones del PROMPT. Si el frances cae en el tercer tercio, el efecto es local y decae; si se sostiene, fija un modo |

Ese ultimo es el que mas me interesa: es la pregunta de navidad ("el efecto
sobrevive a la generacion?") por fin medida en vez de inspeccionada a ojo.

## Advertencias

- **La existencia es barata**: 3x3072 = 9216 parametros libres contra ~80 prompts de
  entrenamiento. Un parche siempre existe en train. El resultado vive
  exclusivamente en el held-out, que es lo unico que reporta el eval.
- **Boilerplate**: si todas las respuestas francesas arrancan igual, el parche puede
  aprender la plantilla en vez de "hablá francés". Por eso las preguntas son de
  tipos variados y por eso la accuracy se mide aparte de la compliance.
- **El gate solo filtra train**, nunca el held-out. Filtrar el held-out inflaria los
  numeros.
