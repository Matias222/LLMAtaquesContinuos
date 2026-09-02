#!/usr/bin/env bash
# Control aleatorio para v3_250: mismo held-out, misma norma, direccion al azar.
# No entrena nada -- make_random_patch.py es CPU-only e instantaneo. El costo
# es un eval normal (38 preguntas x 100 tokens), nada de gradiente.
#
#   uso (desde experimentos/idiomas):  bash run_random_control.sh [MODEL_PATH] [SEED]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
SEED="${2:-0}"
DEVICE="${DEVICE:-cuda:0}"
LIKE="runs/v3_250/lang_patch.pt"
TARGETS="attributes/french/targets_french.csv"
OUT="runs/random_control"

mkdir -p "$OUT"

python3 make_random_patch.py --like "$LIKE" --seed "$SEED" --out "$OUT/lang_patch.pt"

python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" \
    --patch "$OUT/lang_patch.pt" --targets "$TARGETS" \
    --out_json "$OUT/eval_report.json" --out_md "$OUT/eval_report.md" \
    2>&1 | tee "$OUT/eval.log"
