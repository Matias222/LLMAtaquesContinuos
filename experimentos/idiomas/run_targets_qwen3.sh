#!/usr/bin/env bash
# Targets del banco v8 con Qwen3-4B-Instruct-2507 (attributes/qwen3). Misma receta
# que run_targets_v8.sh (y = M("Answer in X.\n\n" + q), greedy, 100 tokens, gate_v8),
# con tres diferencias porque lo guardado es de Llama:
#   - las 100 viejas tambien se regeneran (armar --regenerar_viejas, sin restaurar)
#   - sin fix_targets_v8.py: sus correcciones son texto de Llama. Si Qwen tiene tics
#     propios se escriben despues de la revision manual (fix_targets_qwen3.py)
#   - regate --incluir_viejas: gate_v8 tambien sobre las viejas, con sus alias
#
#   0 verificar  verificar_modelo.py (plantilla, parche solo en la pregunta, causalidad,
#                gradiente, generacion): con alguna FALLA no se sigue
#   1 armar      700 filas sin output (traducciones y alias se conservan)
#   2 fr         generate_targets.py --fill
#   3 attr       es / de con --gate_accuracy (heredan baseline_en y traducciones de fr)
#   4 alias      alias de 6 idiomas (viejas + banco). En SMOKE no corre (pide las 700)
#   5 regate     gate_v8 sobre las 700
#   6 revisar    reporte por celda y categoria
#   7 controles  sin filas vacias, sin fugas de plantilla (<|...|>, <think>, assistant),
#                idioma por celda, mismas preguntas y orden en las 3 celdas, ninguna
#                salida identica a la de Llama (si no, algo leyo el CSV viejo)
#
#   uso:  bash run_targets_qwen3.sh MODEL_PATH
#   variables: DEVICE (cuda:0)  STAGES ("verificar armar fr attr alias regate revisar controles")
#              SMOKE=1 (2 filas por categoria -> attributes/qwen3_smoke)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_targets_qwen3.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
STAGES="${STAGES:-verificar armar fr attr alias regate revisar controles}"
OUT=attributes/qwen3
N_SMOKE=()
if [[ "${SMOKE:-0}" == "1" ]]; then
  OUT=attributes/qwen3_smoke; N_SMOKE=(--n 2)
  echo "### SMOKE: 2 filas por categoria -> $OUT"
fi
FR=$OUT/targets_v8_fr.csv
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$OUT"

echo "################ validacion"
[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
python3 - "$MODEL" <<'PY'
import sys
from lm import familia
f = familia(sys.argv[1])
assert f == "qwen3", f"este runner es para Qwen3 y el modelo es {f!r}"
from checkers import language_verdict
assert language_verdict("La capitale de la France est Paris.") == "fr", "GlotLID no responde"
print("modelo qwen3, GlotLID ok")
PY

if has verificar; then
  echo; echo "################ 0 verificar_modelo"
  python3 -u verificar_modelo.py --model "$MODEL" --device "$DEVICE" \
      --out_json "$OUT/verificar_modelo.json" 2>&1 | tee "$OUT/verificar_modelo.log"
fi

if has armar; then
  echo; echo "################ 1 armar $FR"
  if [[ -f "$FR" ]]; then
    echo "ya existe $FR: no se rearma (borrarlo a mano para empezar de cero)"
  else
    python3 preparar_targets_v8.py armar --regenerar_viejas --out "$FR" ${N_SMOKE[@]+"${N_SMOKE[@]}"} \
        2>&1 | tee "$OUT/armar.log"
  fi
fi

if has fr; then
  echo; echo "################ 2 targets fr"
  python3 -u generate_targets.py --model "$MODEL" --device "$DEVICE" --fill "$FR" 2>&1 | tee "$OUT/targets_fr.log"
fi

if has attr; then
  for L in es de; do
    T=$OUT/targets_v8_$L.csv
    echo; echo "################ 3 targets $L"
    if [[ -f "$T" && "${FORCE_ATTR:-0}" != "1" ]]; then
      echo "ya existe $T (FORCE_ATTR=1 para regenerar)"; continue
    fi
    python3 -u algebra/generate_targets_attr.py --model "$MODEL" --device "$DEVICE" \
        --lang "$L" --base_csv "$FR" --out "$T" --gate_accuracy 2>&1 | tee "$OUT/targets_$L.log"
  done
fi

if has alias; then
  echo; echo "################ 4 alias"
  if [[ "${SMOKE:-0}" == "1" ]]; then
    echo "SMOKE: alias se saltea (viejas_alias.csv pide las 100 viejas)"
  else
    python3 preparar_targets_v8.py alias --dir "$OUT" 2>&1 | tee "$OUT/alias.log"
  fi
fi

if has regate; then
  echo; echo "################ 5 regate (incluye las viejas)"
  python3 preparar_targets_v8.py regate --incluir_viejas --dir "$OUT" 2>&1 | tee "$OUT/regate.log"
fi

if has revisar; then
  echo; echo "################ 6 revisar"
  python3 preparar_targets_v8.py revisar --dir "$OUT" 2>&1 | tee "$OUT/revisar.log"
fi

if has controles; then
  echo; echo "################ 7 controles de los targets"
  python3 - "$OUT" <<'PY' 2>&1 | tee "$OUT/controles.log"
import re, sys
import pandas as pd
from checkers import language_verdict
out = sys.argv[1]
llama = {c: pd.read_csv(f"attributes/v8/targets_v8_{c}.csv", sep=";", keep_default_na=False, dtype=str)
         for c in ("fr", "es", "de")}
fallas = []
dfs = {c: pd.read_csv(f"{out}/targets_v8_{c}.csv", sep=";", keep_default_na=False, dtype=str) for c in ("fr", "es", "de")}
for c, df in dfs.items():
    vacias = (df["output"].str.strip() == "").sum()
    fuga = df["output"].str.contains(r"<\|[a-z_]+\|>|<think>|</think>", regex=True).sum()
    rol = df["output"].str.contains(r"(?:^|\n)\s*(?:assistant|user)\s*\n", regex=True, case=False).sum()
    sin_gate = (df["passed_gate"].str.strip() == "").sum()
    m = llama[c].set_index("prompt")["output"]
    iguales = sum(m.get(p, None) == o for p, o in zip(df["prompt"], df["output"]))
    langs = df["output"].map(language_verdict).value_counts().to_dict()
    gate = (df["passed_gate"].str.lower() == "true").sum()
    print(f"[{c}] filas {len(df)}  vacias {vacias}  fuga de plantilla {fuga}  fuga de rol {rol}  "
          f"sin gate {sin_gate}  identicas a Llama {iguales}  gate {gate}/{len(df)}  idiomas {langs}")
    if vacias: fallas.append(f"{c}: {vacias} outputs vacios")
    if fuga: fallas.append(f"{c}: {fuga} outputs con tokens de plantilla o <think>")
    if sin_gate: fallas.append(f"{c}: {sin_gate} filas sin passed_gate")
    if langs.get(c, 0) < 0.8 * len(df): fallas.append(f"{c}: solo {langs.get(c, 0)}/{len(df)} en {c}")
    if iguales > 0.2 * len(df):
        print(f"  AVISO [{c}]: {iguales} salidas identicas a las de Llama (respuestas cortas pueden coincidir)")
    if rol: print(f"  AVISO [{c}]: {rol} con un turno de rol dentro del output")
for c in ("es", "de"):
    if list(dfs[c]["prompt"]) != list(dfs["fr"]["prompt"]):
        fallas.append(f"{c}: preguntas u orden distintos a fr")
    if list(dfs[c]["baseline_en"]) != list(dfs["fr"]["baseline_en"]):
        fallas.append(f"{c}: baseline_en distinto a fr")
for f in fallas:
    print("FALLA", f)
print("controles de targets: " + ("OK" if not fallas else f"{len(fallas)} FALLA"))
sys.exit(1 if fallas else 0)
PY
fi

echo
echo "Listo: $OUT/targets_v8_{fr,es,de}.csv   (revisar: $OUT/revisar.log, controles: $OUT/controles.log)"
echo "Siguiente: revision manual de los targets antes de run_train_qwen3.sh"
