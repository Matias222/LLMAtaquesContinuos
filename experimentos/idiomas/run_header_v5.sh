#!/usr/bin/env bash
# Parche sobre el HEADER del assistant en vez de sobre la pregunta.
#
# Motivo: el parche sobre los 3 primeros tokens de la pregunta solo funciona con
# las aperturas e idiomas que vio (open_2: 0.04 de frances con "Tell me about",
# "Explain..."; it/pt: 0.22 / 0.14), mientras que la direccion en el residual
# de L16 si generaliza. Los ultimos 3 tokens del header
# (assistant <|end_header_id|> \n\n) son identicos en todos los prompts, asi que
# un parche ahi no puede depender del token sobre el que se suma. Y es la region
# cuyo KV sostiene el modo frances segun --block keep.
#
# Misma receta que v5_head_multi_l2_0.0725 (head 8, entradas en/es/de, L2 0.0725)
# con --patch_anchor header, y despues TODAS las evaluaciones:
#   1. held-out ingles            eval_lang_patch          -> eval_best_train.*
#   2. es/de/en held-out          cross_lang --preset idioma  -> cross_lang_idioma.*
#   3. it/pt held-out             cross_lang --preset romance -> cross_lang_romance.*
#   4. open 1 (99 de navidad)     eval_lang_patch, split 0 -> eval_open.*
#   5. open 2 (imperativos en/es/de) cross_lang idioma, split 0 -> open_2/cross_lang_idioma.*
#
#   uso (desde experimentos/idiomas):  bash run_header_v5.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  L2 (0.0725)  HEAD_K (8)  EPOCHS (8)  NAME (v5_header_head_multi)
#               SKIP_TRAIN=1 para evaluar un parche ya entrenado
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
L2="${L2:-0.0725}"
HEAD_K="${HEAD_K:-8}"
EPOCHS="${EPOCHS:-8}"
NAME="${NAME:-v5_header_head_multi}"
ANCHOR=header
T=attributes/french/targets_french_v5.csv
T_OPEN=attributes/french/targets_open.csv
T_OPEN2=attributes/french/targets_open_2.csv
SPLIT=0.80
OUT=runs/$NAME; mkdir -p "$OUT" "$OUT/open_2"
P="$OUT/lang_patch_best_train.pt"

for f in "$T" "$T_OPEN" "$T_OPEN2"; do [[ -f "$f" ]] || { echo "falta $f"; exit 1; }; done

if [[ "${SKIP_TRAIN:-0}" != "1" ]]; then
  python3 -u train_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
      --l2_weight "$L2" --output_dir "$OUT" --batch_size 32 --num_steps_per_prompt 20 \
      --num_epochs "$EPOCHS" --step_decay cosine --val_n 20 --save_best --train_test_split $SPLIT \
      --loss_head_k "$HEAD_K" --prompt_cols prompt,prompt_es,prompt_de \
      --patch_anchor $ANCHOR 2>&1 | tee "$OUT/train.log"
fi

# 1. held-out ingles
python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
    --patch "$P" --train_test_split $SPLIT --patch_anchor $ANCHOR \
    --out_json "$OUT/eval_best_train.json" --out_md "$OUT/eval_best_train.md" 2>&1 | tee "$OUT/eval.log"

# 2. es / de / en held-out
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
    --patch "$P" --train_test_split $SPLIT --patch_anchor $ANCHOR \
    --preset idioma --out_dir "$OUT" 2>&1 | tee "$OUT/idioma.log"

# 3. it / pt held-out (idiomas no vistos)
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
    --patch "$P" --train_test_split $SPLIT --patch_anchor $ANCHOR \
    --preset romance --out_dir "$OUT" 2>&1 | tee "$OUT/romance.log"

# 4. open 1: los 99 prompts de navidad, todos held-out
python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T_OPEN" \
    --patch "$P" --train_test_split 0 --patch_anchor $ANCHOR \
    --out_json "$OUT/eval_open.json" --out_md "$OUT/eval_open.md" 2>&1 | tee "$OUT/eval_open.log"

# 5. open 2: imperativos en / es / de, todos held-out
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T_OPEN2" \
    --patch "$P" --train_test_split 0 --patch_anchor $ANCHOR \
    --preset idioma --out_dir "$OUT/open_2" 2>&1 | tee "$OUT/open_2/idioma.log"

echo
echo "Listo. Comparar contra runs/v5_head_multi_l2_0.0725:"
echo "  $OUT/eval_best_train.md      (held-out ingles)"
echo "  $OUT/cross_lang_idioma.md    (es/de)"
echo "  $OUT/cross_lang_romance.md   (it/pt)"
echo "  $OUT/eval_open.md            (open 1)"
echo "  $OUT/open_2/cross_lang_idioma.md  (open 2)"
