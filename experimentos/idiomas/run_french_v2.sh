#!/usr/bin/env bash
# Config v2: arregla la orbita del optimizador. Ver README, seccion
# "Por que el barrido v1 se estanco".
#
#   uso:  bash run_french_v2.sh [MODEL_PATH]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"

[ -f targets_french.csv ] || python3 -u generate_targets.py --model "$MODEL" --device "$DEVICE"

for L2 in 0.045 0.08; do
  OUT="runs/v2_french_l2_${L2}"
  echo ""
  echo "######################################################################"
  echo "# v2  L2=$L2  ->  $OUT"
  echo "######################################################################"
  mkdir -p "$OUT"

  # batch_size 8   -> gradiente promedio, no tirones por prompt
  # steps 12       -> 10 batches x 12 pasos = 120 pasos/epoch (vs 5775 antes)
  # cosine         -> el paso anilla a 0, la orbita se cierra
  # val_n 20       -> validacion sobre TODO el held-out, no 8
  # save_best      -> guarda el mejor por head CE, no un punto arbitrario
  python3 -u train_lang_patch.py \
      --model "$MODEL" --device "$DEVICE" \
      --l2_weight "$L2" --output_dir "$OUT" \
      --batch_size 8 --num_steps_per_prompt 12 --num_epochs 8 \
      --step_decay cosine --val_n 20 --save_best \
      2>&1 | tee "$OUT/train.log"

  python3 -u eval_lang_patch.py \
      --model "$MODEL" --device "$DEVICE" --patch "$OUT/lang_patch.pt" \
      --out_json "$OUT/eval_report.json" --out_md "$OUT/eval_report.md" \
      2>&1 | tee "$OUT/eval.log"

  python3 -u "$ROOT/legacy/inspect_xmas_patch.py" \
      --model "$MODEL" --patch "$OUT/lang_patch.pt" \
      --out "$OUT/inspect_report.json" 2>&1 | tee "$OUT/inspect.log"
done

echo ""
python3 summarize.py "runs/v2_*/eval_report.json"
