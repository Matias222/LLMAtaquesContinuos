#!/usr/bin/env bash
# Transferencia de v5_head_multi (entrenado con entradas en/es/de) a italiano y
# portugues, idiomas que no vio. prompt_it / prompt_pt estan escritos a mano en
# targets_french_v5.csv para las 50 filas del tail.
#
#   uso (desde experimentos/idiomas):  bash run_romance_v5.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  RUNS="v5_head_multi v4_250" para elegir parches
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
TARGETS="attributes/french/targets_french_v5.csv"
python3 checkers.py > /dev/null   # selftest del detector (canales it/pt)
for N in ${RUNS:-v5_head_multi v5_multi v4_250}; do
  python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$TARGETS" \
      --patch "runs/$N/lang_patch_best_train.pt" --train_test_split 0.80 \
      --preset romance --out_dir "runs/$N" 2>&1 | tee "runs/$N/romance.log"
done
echo; echo "Listo:"; for N in ${RUNS:-v5_head_multi v5_multi v4_250}; do echo "  runs/$N/cross_lang_romance.md"; done
