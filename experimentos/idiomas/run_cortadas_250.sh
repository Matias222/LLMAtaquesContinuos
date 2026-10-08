#!/usr/bin/env bash
# Held-out v8 y v9: re-generar con 250 tokens las preguntas cuya salida (baseline,
# referencia o parche) se corto en el limite de 150. Ver cortadas.py.
#
#   1. seleccion: por idioma, la union de v8 y v9 de las preguntas con alguna salida
#      cortada -> $R/targets_cortadas_<L>.csv (filas del held-out de targets_v8_<L>.csv,
#      con los alias actuales)
#   2. eval: los parches de v8 y v9 sobre esas filas, con los mismos flags de la etapa A
#      de cada run (v8: control = instruccion, v9: control = nativo) y --num_tokens 250
#   3. comparar: veredicto viejo vs nuevo y accuracy del held-out completo
#      -> $R/reporte.md
#
#   uso:  bash run_cortadas_250.sh MODEL_PATH
#   variables:  DEVICE (cuda:0)  NTOK (250)  STAGES ("seleccion eval comparar")
#               SMOKE=1 (evals de 2 filas, todo en algebra/runs/cortadas_smoke)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_cortadas_250.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
NTOK="${NTOK:-250}"
STAGES="${STAGES:-seleccion eval comparar}"
CKPT=lang_patch_best_train.pt
R=algebra/runs/cortadas_$NTOK
NEVAL=()
if [[ "${SMOKE:-0}" == "1" ]]; then
  R=algebra/runs/cortadas_smoke; NEVAL=(--n 2)
  echo "### SMOKE: evals de 2 filas -> $R"
fi
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$R"
# baseline (y la referencia de cada version) es la misma para los tres parches: se genera una vez
export GEN_CACHE="$HERE/$R/gen_cache"

[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
for V in v8 v9; do
  for L in es fr de; do
    for f in "algebra/runs/$V/alg_$L/eval_heldout.json" "algebra/runs/$V/alg_$L/$CKPT"; do
      [[ -f "$f" ]] || { echo "falta $f"; exit 1; }
    done
  done
done

if has seleccion; then
  echo; echo "################ seleccion"
  python3 -u cortadas.py seleccionar --model "$MODEL" --out "$R" 2>&1 | tee "$R/seleccion.log"
fi

control() { case $1 in v8) echo --regen_ref ;; v9) echo --control nativo ;; esac; }

if has eval; then
  for V in v8 v9; do
    for L in es fr de; do
      O=$R/$V/alg_$L; mkdir -p "$O"
      echo; echo "################ eval $V $L"
      # shellcheck disable=SC2046
      python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" \
          --patch "algebra/runs/$V/alg_$L/$CKPT" --patch_anchor goal_all --num_patch_positions 1 \
          --target_lang "$L" --num_tokens "$NTOK" --cell_metrics $(control $V) ${NEVAL[@]+"${NEVAL[@]}"} \
          --targets "$R/targets_cortadas_$L.csv" --train_test_split 0 \
          --out_json "$O/eval_heldout.json" --out_md "$O/eval_heldout.md" 2>&1 | tee "$O/eval_heldout.log"
    done
  done
fi

if has comparar; then
  echo; echo "################ comparar"
  python3 -u cortadas.py comparar --model "$MODEL" --out "$R" --num_tokens "$NTOK" 2>&1 | tee "$R/comparar.log"
fi
