#!/usr/bin/env bash
# Prueba rapida: pregunta en FRANCES menos el parche de frances, sobre el held-out.
#
#     M(q_fr - a * v_fr)      q_fr = prompt_fr del held-out (idx 200..249)
#
# Sin parche el modelo contesta en frances (empareja el idioma de la entrada).
# Si v_fr es una direccion "frances" con sentido, restarla tiene que sacarlo del
# frances (a ingles u otro); si no cambia nada o sale basura, -v no es la
# direccion opuesta. a=0 se corre siempre como referencia de "cambio".
#
#   uso (desde cualquier lado):  bash algebra/run_restar_fr.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  SCALES ("-1", p.ej. "-0.5 -1 -2")
#               PATCH (algebra/runs/alg_fr/lang_patch_best_train.pt)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

MODEL="${1:-/teamspace/studios/this_studio/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
SCALES="${SCALES:--1}"
PATCH="${PATCH:-algebra/runs/alg_fr/lang_patch_best_train.pt}"
T=attributes/french/targets_french_v5.csv
OUT=algebra/runs/alg_fr/restar_fr
[[ -f "$PATCH" ]] || { echo "falta $PATCH"; exit 1; }
mkdir -p "$OUT"

CONDS="prompt_fr:0"
for a in $SCALES; do CONDS="$CONDS,prompt_fr:$a"; done

python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
    --patch "$PATCH" --train_test_split 0.80 --patch_anchor goal_all --num_patch_positions 1 \
    --conds "$CONDS" --tag restar_fr --out_dir "$OUT" 2>&1 | tee "$OUT/restar_fr.log"

echo
echo "Reporte: $OUT/cross_lang_restar_fr.md"
echo "Mirar: fr baja con a<0? a que idioma va (en / es / de / unknown)? ce_fr_h sube, ce_en_h baja?"
