#!/usr/bin/env bash
# Los cuatro experimentos de mecanismo sobre el parche v4_250 (best_train).
#
#   1. mask_patch_attention  gen@all         necesidad de la lectura por atencion
#   3. mask_patch_attention  gen@bandas      en que capas se lee el parche
#      mask_patch_attention  post@all        control: parche invisible = baseline
#   2. attention_mass                        cuanta atencion recibe el parche
#   4. ablate_patch_positions                zero/only/perm/shift del parche entrenado
#      train_lang_patch --patch_offset 3     reentrenar en las posiciones 4-6 (el que
#                                            separa RoPE de attention sink; es el unico
#                                            paso que entrena y el mas caro)
#
#   uso (desde experimentos/idiomas):  bash run_mecanismo_v4.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  SKIP_RETRAIN=1 para saltear el reentrenamiento
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
PATCH="runs/v4_250/lang_patch_best_train.pt"
TARGETS="attributes/french/targets_french.csv"
SPLIT=0.80

# 0. chequeo de las mascaras, sin modelo. Si esto falla no correr nada mas.
python3 attn_utils.py

# 1 + 3. necesidad y localizacion en profundidad
OUT=runs/mask_v4; mkdir -p "$OUT"
python3 -u mask_patch_attention.py --model "$MODEL" --device "$DEVICE" \
    --patch "$PATCH" --targets "$TARGETS" --train_test_split $SPLIT \
    --block gen --layers "all;1-8;9-16;17-24;25-28;12-16" \
    --out_dir "$OUT" --check_mask_path 2>&1 | tee "$OUT/mask_gen.log"

# control: el parche invisible para todo lo posterior -> tiene que dar el baseline
python3 -u mask_patch_attention.py --model "$MODEL" --device "$DEVICE" \
    --patch "$PATCH" --targets "$TARGETS" --train_test_split $SPLIT \
    --block post --layers all --out_dir "$OUT" 2>&1 | tee "$OUT/mask_post.log"

# 2. masa de atencion (carga el modelo en eager, por eso es un proceso aparte)
python3 -u attention_mass.py --model "$MODEL" --device "$DEVICE" \
    --patch "$PATCH" --targets "$TARGETS" --train_test_split $SPLIT \
    --out_json "$OUT/attention_mass.json" 2>&1 | tee "$OUT/attention_mass.log"

# 4a. ablacion por posicion del parche entrenado
OUT2=runs/ablate_v4; mkdir -p "$OUT2"
python3 -u ablate_patch_positions.py --model "$MODEL" --device "$DEVICE" \
    --patch "$PATCH" --targets "$TARGETS" --train_test_split $SPLIT \
    --out_dir "$OUT2" 2>&1 | tee "$OUT2/ablate.log"

# 4b. reentrenar en las posiciones 4-6 con los hiperparametros exactos de v4_250
if [[ "${SKIP_RETRAIN:-0}" != "1" ]]; then
  OUT3=runs/v4_250_offset3; mkdir -p "$OUT3"
  python3 -u train_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$TARGETS" \
      --l2_weight 0.055 --output_dir "$OUT3" --batch_size 32 --num_steps_per_prompt 20 \
      --num_epochs 8 --step_decay cosine --val_n 20 --save_best --train_test_split $SPLIT \
      --patch_offset 3 2>&1 | tee "$OUT3/train.log"
  python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" \
      --patch "$OUT3/lang_patch_best_train.pt" --targets "$TARGETS" --train_test_split $SPLIT \
      --patch_offset 3 --out_json "$OUT3/eval_best_train.json" --out_md "$OUT3/eval_best_train.md" \
      2>&1 | tee "$OUT3/eval.log"
fi

echo
echo "Listo. Resumenes:"
echo "  $OUT/resumen_gen.json   $OUT/resumen_post.json   $OUT/attention_mass.json"
echo "  $OUT2/resumen.json"
[[ "${SKIP_RETRAIN:-0}" != "1" ]] && echo "  runs/v4_250_offset3/eval_best_train.json"
