#!/usr/bin/env bash
# v5: banco sin matematica (29 preguntas reemplazadas en posicion) y dos cambios
# de entrenamiento contra el estilo, solos y combinados:
#
#   head    CE solo sobre los primeros K tokens del target (--loss_head_k)
#   multi   entradas en ingles + espanol + aleman hacia el mismo target frances
#           (--prompt_cols prompt,prompt_es,prompt_de)
#
#   0. generate_targets --fill      referencia y baseline SOLO para las 29 filas nuevas
#   1. translate_questions           prompt_fr / prompt_de / prompt_es solo donde faltan
#   2. fix_translations              correcciones a mano (idempotente, por pregunta)
#   3. cuatro entrenamientos con los hiperparametros exactos de v4_250
#   4. eval en ingles (eval_lang_patch) + espanol/aleman (cross_lang_patch idioma)
#
#   uso (desde experimentos/idiomas):  bash run_v5.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  HEAD_K (8)  SKIP_DATA=1 para saltear 0-2
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
HEAD_K="${HEAD_K:-8}"
TARGETS="attributes/french/targets_french_v5.csv"
SPLIT=0.80

if [[ "${SKIP_DATA:-0}" != "1" ]]; then
  mkdir -p runs/v5_data
  python3 -u generate_targets.py --model "$MODEL" --device "$DEVICE" --fill "$TARGETS" \
      2>&1 | tee runs/v5_data/fill.log
  for L in fr de es; do
    python3 -u translate_questions.py --model "$MODEL" --device "$DEVICE" --lang $L \
        --targets "$TARGETS" --only_missing 2>&1 | tee "runs/v5_data/translate_$L.log"
  done
  python3 -u fix_translations.py --targets "$TARGETS" 2>&1 | tee runs/v5_data/fix.log
fi

# hiperparametros de v4_250 (LOG_EXPERIMENTOS.md seccion 10)
TRAIN="python3 -u train_lang_patch.py --model $MODEL --device $DEVICE --targets $TARGETS \
  --l2_weight 0.055 --batch_size 32 --num_steps_per_prompt 20 --num_epochs 8 \
  --step_decay cosine --val_n 20 --save_best --train_test_split $SPLIT"

run_one () {   # nombre  args-extra...
  local NAME=$1; shift
  local OUT=runs/$NAME; mkdir -p "$OUT"
  $TRAIN --output_dir "$OUT" "$@" 2>&1 | tee "$OUT/train.log"
  python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$TARGETS" \
      --patch "$OUT/lang_patch_best_train.pt" --train_test_split $SPLIT \
      --out_json "$OUT/eval_best_train.json" --out_md "$OUT/eval_best_train.md" \
      2>&1 | tee "$OUT/eval.log"
  python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$TARGETS" \
      --patch "$OUT/lang_patch_best_train.pt" --train_test_split $SPLIT \
      --preset idioma --out_dir "$OUT" 2>&1 | tee "$OUT/idioma.log"
}

run_one v5_base
run_one v5_head       --loss_head_k "$HEAD_K"
run_one v5_multi      --prompt_cols prompt,prompt_es,prompt_de
run_one v5_head_multi --loss_head_k "$HEAD_K" --prompt_cols prompt,prompt_es,prompt_de

echo
echo "Listo. Comparar contra runs/v4_250 y runs/cross_lang_v4:"
for N in v5_base v5_head v5_multi v5_head_multi; do
  echo "  runs/$N/eval_best_train.md   runs/$N/cross_lang_idioma.md"
done
