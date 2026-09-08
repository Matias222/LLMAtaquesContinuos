#!/usr/bin/env bash
# Signo del parche e idioma de entrada, sobre el parche v4_250 (best_train) y el
# tail del held-out (50 filas, idx 200..249).
#
#   0. translate_questions --lang es   agrega prompt_es al CSV (solo si falta)
#   1. cross_lang_patch --preset restar q_en - a*v  y  q_fr - a*v
#   2. cross_lang_patch --preset idioma q_es + v, q_de + v (control), q_en + v (ref)
#
#   uso (desde experimentos/idiomas):  bash run_cross_lang_v4.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
PATCH="runs/v4_250/lang_patch_best_train.pt"
TARGETS="attributes/french/targets_french.csv"
SPLIT=0.80
OUT=runs/cross_lang_v4; mkdir -p "$OUT"

# 0. pregunta en espanol (reescribe el CSV in-place, deja .bak)
if ! head -1 "$TARGETS" | grep -q "prompt_es"; then
  python3 -u translate_questions.py --model "$MODEL" --device "$DEVICE" --lang es \
      --targets "$TARGETS" 2>&1 | tee "$OUT/translate_es.log"
fi

# 1. restar el parche
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" \
    --patch "$PATCH" --targets "$TARGETS" --train_test_split $SPLIT \
    --preset restar --out_dir "$OUT" 2>&1 | tee "$OUT/restar.log"

# 2. pregunta en espanol + parche
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" \
    --patch "$PATCH" --targets "$TARGETS" --train_test_split $SPLIT \
    --preset idioma --out_dir "$OUT" 2>&1 | tee "$OUT/idioma.log"

echo
echo "Listo. Resumenes:  $OUT/cross_lang_restar.md   $OUT/cross_lang_idioma.md"
