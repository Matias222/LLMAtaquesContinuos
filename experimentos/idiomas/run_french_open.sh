#!/usr/bin/env bash
# Evaluacion sobre prompts ABIERTOS: el mismo set de 99 prompts que uso navidad.
# No re-entrena nada: usa el parche ya entrenado sobre questions.csv.
#
#   uso:  bash run_french_open.sh <PATCH.pt> [MODEL_PATH]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$HERE"
PATCH="${1:?falta la ruta al parche .pt}"
MODEL="${2:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
OUT="$(dirname "$PATCH")"

[ -f targets_open.csv ] || python3 -u generate_targets.py --model "$MODEL" --device "$DEVICE" \
    --questions questions_open.csv --out targets_open.csv

# train_test_split 0 -> evalua las 99, ninguna se uso para entrenar el parche
python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" \
    --patch "$PATCH" --targets targets_open.csv --train_test_split 0.0 \
    --out_json "$OUT/eval_open.json" --out_md "$OUT/eval_open.md"
