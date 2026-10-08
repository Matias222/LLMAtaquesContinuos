#!/usr/bin/env bash
# Barrido de escala alfa sobre las direcciones v8 y v9: e'_i = e_i + alfa * v.
# Pregunta: ¿la accuracy baja cuando sube la norma del parche? v8 contra v9 no lo
# responde (la norma difiere 3-4% pero la direccion tambien: coseno 0.58); aca la
# direccion queda fija y solo cambia la norma.
#
#   held-out v8 (112 filas, split 0.84), SOLO pregunta en ingles + parche, mismos flags
#   que la etapa A de run_train_v9.sh (150 tokens, control nativo). alfa en ALPHAS.
#   El baseline y el control nativo no dependen del parche: se reusan del GEN_CACHE de
#   v9 (algebra/runs/v9/gen_cache, de la etapa base), asi que cada eval solo genera el
#   parche. Para v9 con alfa = 1 tambien sale del cache (mismas entradas exactas).
#
#   salida: algebra/runs/<run>/alg_<celda>/alpha/eval_a<alfa>.json
#   reporte: algebra/runs/v9/reportes/alpha.md (reporte_alpha.py)
#
#   uso:  bash run_alpha.sh MODEL_PATH
#   variables: DEVICE (cuda:0)  RUNS ("v8 v9")  CELDAS ("fr es de")
#              ALPHAS ("0.90 0.95 1.00 1.05 1.10")  N (0 = las 112 filas; N=4 para humo)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_alpha.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
RUNS="${RUNS:-v8 v9}"
CELDAS="${CELDAS:-fr es de}"
ALPHAS="${ALPHAS:-0.90 0.95 1.05 1.10}"
N="${N:-0}"
TDIR=attributes/v8
SPLIT=0.84
NTOK=150
CKPT=lang_patch_best_train.pt
export GEN_CACHE="$HERE/algebra/runs/v9/gen_cache"
[[ -d "$GEN_CACHE" ]] || echo "AVISO: no existe $GEN_CACHE: baseline y control se van a generar de nuevo"

for run in $RUNS; do
  for L in $CELDAS; do
    P="algebra/runs/$run/alg_$L/$CKPT"
    [[ -f "$P" ]] || { echo "falta $P"; exit 1; }
    O="algebra/runs/$run/alg_$L/alpha"; mkdir -p "$O"
    for a in $ALPHAS; do
      echo; echo "################ $run $L alfa=$a"
      python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --patch "$P" \
          --patch_anchor goal_all --num_patch_positions 1 --target_lang "$L" --num_tokens $NTOK \
          --cell_metrics --control nativo --scale "$a" --n "$N" \
          --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT \
          --out_json "$O/eval_a$a.json" --out_md "$O/eval_a$a.md" 2>&1 | tee "$O/eval_a$a.log"
    done
  done
done

python3 reporte_alpha.py --runs "$RUNS" --celdas "$CELDAS" --targets_dir "$TDIR" --split $SPLIT \
    --out algebra/runs/v9/reportes/alpha.md
