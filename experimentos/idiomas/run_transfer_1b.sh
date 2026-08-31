#!/usr/bin/env bash
# Transferencia del parche 3B -> 1B, con su control.
#
#   bash run_transfer_1b.sh <MODELO_3B> <MODELO_1B> [PARCHE]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$HERE"
SRC="${1:?falta el modelo 3B}"; TGT="${2:?falta el modelo 1B}"
PATCH="${3:-runs/v3_250/lang_patch.pt}"
OUT=runs/transfer_1b; mkdir -p $OUT

echo "### 1. mapa real  3072 -> 2048"
python3 -u transfer_patch.py --source "$SRC" --target "$TGT" \
    --patch "$PATCH" --out $OUT/lang_patch.pt 2>&1 | tee $OUT/transfer.log

echo; echo "### 2. control: mismo parche por un mapa ortogonal al azar"
python3 -u transfer_patch.py --source "$SRC" --target "$TGT" --control --force \
    --patch "$PATCH" --out $OUT/control_patch.pt 2>&1 | tee $OUT/control.log

# La referencia del 1B es la del 1B, no la del 3B: cada modelo tiene su techo.
echo; echo "### 3. targets con el 1B (su propia referencia)"
TARGETS_1B="attributes/french/targets_french_1b.csv"
[ -f "$TARGETS_1B" ] || python3 -u generate_targets.py --model "$TGT" \
    --out "$TARGETS_1B"

echo; echo "### 4. eval del parche transferido"
python3 -u eval_lang_patch.py --model "$TGT" --targets "$TARGETS_1B" \
    --train_test_split 0.85 --patch $OUT/lang_patch.pt \
    --out_json $OUT/eval_report.json --out_md $OUT/eval_report.md 2>&1 | tee $OUT/eval.log

echo; echo "### 5. eval del control"
python3 -u eval_lang_patch.py --model "$TGT" --targets "$TARGETS_1B" \
    --train_test_split 0.85 --patch $OUT/control_patch.pt \
    --out_json $OUT/eval_control.json --out_md $OUT/eval_control.md 2>&1 | tee $OUT/eval_control.log

echo; echo "======================================================================"
python3 - <<'EOF'
import json
r = json.load(open("runs/transfer_1b/eval_report.json"))["metrics"]
c = json.load(open("runs/transfer_1b/eval_control.json"))["metrics"]
print(f"{'condicion':<34}{'frances':>10}{'accuracy':>10}")
print(f"{'baseline del 1B  M(q)':<34}{r['baseline']['is_french']:>10.1%}{r['baseline']['answer_correct']:>10.1%}")
print(f"{'referencia del 1B  M([FR;q])':<34}{r['reference']['is_french']:>10.1%}{r['reference']['answer_correct']:>10.1%}")
print(f"{'parche TRANSFERIDO del 3B':<34}{r['patched']['is_french']:>10.1%}{r['patched']['answer_correct']:>10.1%}")
print(f"{'control (mapa al azar)':<34}{c['patched']['is_french']:>10.1%}{c['patched']['answer_correct']:>10.1%}")
d = r['patched']['is_french'] - c['patched']['is_french']
print(f"\ntransferido menos control: {d:+.1%}")
print("  <=0  -> no transfirio" if d <= 0.05 else "  >0   -> hay transferencia por encima del control")
EOF
