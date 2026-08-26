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

Las 100 preguntas de `questions.csv` tienen respuestas **invariantes al idioma**
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
bash run_french.sh /ruta/al/modelo/Llama-3.2-3B-Instruct
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
| `questions.csv` | 100 preguntas + respuesta + alias franceses. Barajado con seed=42 (el split es posicional, no puede quedar ordenado por categoria) |
| `checkers.py` | `is_french`, `french_score`, `answer_correct`. `python3 checkers.py` corre su auto-test |
| `lm.py` | carga de modelo, generacion greedy desde embeddings, aplicacion del parche, CE de un target |
| `generate_targets.py` | paso 0: genera `y = M([FR;q])` + baseline + gate de calidad |
| `train_lang_patch.py` | paso 1: teacher forcing con gradiente (sign-SGD) |
| `eval_lang_patch.py` | paso 2: las tres condiciones sobre held-out |
| `summarize.py` | tabla comparativa de los 3 L2 |
| `run_french.sh` | orquestador |

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

## Advertencias

- **La existencia es barata**: 3x3072 = 9216 parametros libres contra ~80 prompts de
  entrenamiento. Un parche siempre existe en train. El resultado vive
  exclusivamente en el held-out, que es lo unico que reporta el eval.
- **Boilerplate**: si todas las respuestas francesas arrancan igual, el parche puede
  aprender la plantilla en vez de "hablá francés". Por eso las preguntas son de
  tipos variados y por eso la accuracy se mide aparte de la compliance.
- **El gate solo filtra train**, nunca el held-out. Filtrar el held-out inflaria los
  numeros.
