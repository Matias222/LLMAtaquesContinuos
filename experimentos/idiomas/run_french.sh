#!/usr/bin/env bash
# Experimento de idiomas: existencia de un parche aditivo que induce frances.
#
#   uso:  bash run_french.sh [MODEL_PATH]
#
# Barre l2_weight en {0.045, 0.08, 0.1} - los mismos tres valores del barrido
# noprefix de navidad, para que los numeros sean comparables run a run.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
L2_VALUES=(0.045 0.08 0.1)

echo "======================================================================"
echo " Modelo:  $MODEL"
echo " Device:  $DEVICE"
echo " Barrido: ${L2_VALUES[*]}"
echo "======================================================================"

# --- Paso 0: targets de teacher forcing (una sola vez) --------------------
if [ -f targets_french.csv ]; then
  echo ">> targets_french.csv ya existe, salteando generacion"
else
  echo ">> [0/3] generando targets  y = M([Answer in French. ; q])"
  python3 generate_targets.py --model "$MODEL" --device "$DEVICE"
fi

# --- Pasos 1-3: entrenar + evaluar + inspeccionar cada L2 -----------------
for L2 in "${L2_VALUES[@]}"; do
  OUT="runs/french_l2_${L2}"
  echo ""
  echo "######################################################################"
  echo "# L2 = $L2   ->  $OUT"
  echo "######################################################################"
  mkdir -p "$OUT"

  python3 train_lang_patch.py \
      --model "$MODEL" --device "$DEVICE" \
      --l2_weight "$L2" --output_dir "$OUT" \
      2>&1 | tee "$OUT/train.log"

  python3 eval_lang_patch.py \
      --model "$MODEL" --device "$DEVICE" \
      --patch "$OUT/lang_patch.pt" \
      --out_json "$OUT/eval_report.json" \
      --out_md "$OUT/eval_report.md" \
      2>&1 | tee "$OUT/eval.log"

  # Geometria del parche: normas, percentil en vocab, top-dims, vecinos.
  # Sirve para el control negativo del canal sink: convergen estos parches
  # a las mismas dims {2433, 1238, 1659} que los 31 de navidad?
  python3 "$ROOT/legacy/inspect_xmas_patch.py" \
      --model "$MODEL" \
      --patch "$OUT/lang_patch.pt" \
      --out "$OUT/inspect_report.json" \
      2>&1 | tee "$OUT/inspect.log"
done

echo ""
echo "======================================================================"
echo " RESUMEN"
echo "======================================================================"
python3 summarize.py "runs/*/eval_report.json"
