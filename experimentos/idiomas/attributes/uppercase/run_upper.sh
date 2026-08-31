#!/usr/bin/env bash
# Atributo "mayusculas": un solo parche, con la config v2 (batch+cosine+save_best)
# que ya establecio existencia para frances (ver docs/README.md). No repite el
# barrido de 3 L2 de french_v1/v2: el objetivo aca no es la existencia del
# atributo por si sola, es tener UN parche que funcione para alimentar
# compose_patches.py.
#
#   uso (desde experimentos/idiomas):  bash attributes/uppercase/run_upper.sh [MODEL_PATH]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IDIOMAS="$(cd "$HERE/../.." && pwd)"
cd "$IDIOMAS"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
TARGETS="attributes/uppercase/targets_upper.csv"
L2="${L2:-0.0525}"
OUT="runs/upper_v1"

[ -f "$TARGETS" ] || python3 -u generate_targets_upper.py --model "$MODEL" --device "$DEVICE"

mkdir -p "$OUT"

python3 -u train_lang_patch.py \
    --model "$MODEL" --device "$DEVICE" --targets "$TARGETS" \
    --l2_weight "$L2" --output_dir "$OUT" \
    --batch_size 8 --num_steps_per_prompt 20 --num_epochs 8 \
    --step_decay cosine --val_n 20 --save_best \
    2>&1 | tee "$OUT/train.log"

# is_french/french_score en este reporte miden el atributo equivocado (ver
# generate_targets_upper.py); sirve para accuracy y CE head/tail nomas. El
# evaluador real del atributo es compose_patches.py.
python3 -u eval_lang_patch.py \
    --model "$MODEL" --device "$DEVICE" --patch "$OUT/lang_patch.pt" --targets "$TARGETS" \
    --out_json "$OUT/eval_report.json" --out_md "$OUT/eval_report.md" \
    2>&1 | tee "$OUT/eval.log"

python3 -u inspect_patch_norm.py --model "$MODEL" \
    --patch "$OUT/lang_patch.pt" --out "$OUT/inspect_report.json"
