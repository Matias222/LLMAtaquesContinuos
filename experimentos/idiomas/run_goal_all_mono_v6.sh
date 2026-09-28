#!/usr/bin/env bash
# goal_all MONO: el mismo parche que alg_fr, entrenado SOLO con preguntas en ingles.
#
# v5_goalall_head_multi y alg_fr entrenan con entradas en/es/de hacia el mismo
# target frances. Aca la unica entrada es `prompt` (ingles): mide cuanto de la
# generalizacion de goal_all (es/de, it/pt, open 1, open 2) viene del
# entrenamiento multi-idioma y cuanto de la parametrizacion (UN v [1, 1, d]
# sumado a todos los tokens de la pregunta).
#
# Receta = la de alg_fr (run_algebra_v6.sh): L2 0.075, 10 epochs, head 8,
# batch 32, 20 steps, step 0.00025 cosine, mismos targets y mismo held-out.
# Lo UNICO que cambia es --prompt_cols prompt. Asi la comparacion 1 a 1 es
#       v6_goalall_head_mono      vs  algebra/runs/alg_fr
#       v6_goalall_head_mono_s1   vs  algebra/runs/alg_fr_s1
#
# Dos entrenamientos: el original y una replica con otro orden de batches
# (--shuffle_seed 1). cos(alg_fr, alg_fr_s1) = 0.49: el orden solo mueve medio
# parche, asi que una diferencia mono vs multi que no supere a la diferencia
# original vs replica es ruido. A diferencia de run_algebra_v6.sh, aca la
# replica TAMBIEN se evalua.
#
# OJO: con una sola entrada cada batch tiene 1/3 de los ejemplos de alg_fr, y
# es/de pasan de train a transferencia (como it/pt). El L2 no esta recalibrado
# para mono: si la norma queda lejos de ~0.84 es lo primero a mirar.
#
# Por parche, las cinco evaluaciones de siempre:
#   1. held-out ingles               eval_lang_patch             -> eval_best_train.*
#   2. es/de/en held-out             cross_lang idioma           -> cross_lang_idioma.*
#   3. it/pt held-out                cross_lang --preset romance -> cross_lang_romance.*
#   4. open 1 (99 de navidad)        eval_lang_patch, split 0    -> eval_open.*
#   5. open 2 (imperativos en/es/de) cross_lang idioma, split 0  -> open_2/cross_lang_idioma.*
#
#   uso (desde cualquier lado):  bash run_goal_all_mono_v6.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  L2 (0.075)  HEAD_K (8)  EPOCHS (10)  STEP_SIZE (0.00025)
#               NAME (v6_goalall_head_mono)
#               SEEDS ("0 1")  0 = orden original (-> runs/$NAME); otro = replica
#                              barajada con ese seed (-> runs/${NAME}_s<seed>)
#               SKIP_TRAIN=1   no reentrenar los parches que ya existen
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/teamspace/studios/this_studio/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
L2="${L2:-0.075}"
HEAD_K="${HEAD_K:-8}"
EPOCHS="${EPOCHS:-10}"
STEP_SIZE="${STEP_SIZE:-0.00025}"
NAME="${NAME:-v6_goalall_head_mono}"
SEEDS="${SEEDS:-0 1}"
ANCHOR=goal_all
NPOS=1
COLS=prompt
CONDS="prompt_es:0,prompt_es:1,prompt_de:0,prompt_de:1,prompt:0,prompt:1"
CKPT=lang_patch_best_train.pt
T=attributes/french/targets_french_v5.csv
T_OPEN=attributes/french/targets_open.csv
T_OPEN2=attributes/french/targets_open_2.csv
SPLIT=0.80

for f in "$T" "$T_OPEN" "$T_OPEN2"; do [[ -f "$f" ]] || { echo "falta $f"; exit 1; }; done

OUTS=()
for seed in $SEEDS; do
  if [[ "$seed" == "0" ]]; then OUT=runs/$NAME; SHUF=(); else OUT=runs/${NAME}_s$seed; SHUF=(--shuffle_seed "$seed"); fi
  mkdir -p "$OUT" "$OUT/open_2"
  P="$OUT/$CKPT"
  OUTS+=("$OUT")

  echo; echo "################ train $OUT"
  if [[ "${SKIP_TRAIN:-0}" == "1" && -f "$P" ]]; then
    echo "ya entrenado: $OUT"
  else
    python3 -u train_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
        --l2_weight "$L2" --output_dir "$OUT" --batch_size 32 --num_steps_per_prompt 20 \
        --num_epochs "$EPOCHS" --step_decay cosine --val_n 20 --save_best --train_test_split $SPLIT \
        --loss_head_k "$HEAD_K" --prompt_cols "$COLS" --step_size "$STEP_SIZE" \
        --patch_anchor $ANCHOR --num_patch_positions $NPOS --attr_name fr ${SHUF[@]+"${SHUF[@]}"} \
        2>&1 | tee "$OUT/train.log"
  fi

  COMMON=(--model "$MODEL" --device "$DEVICE" --patch "$P" --patch_anchor $ANCHOR
          --num_patch_positions $NPOS --target_lang fr --cell_metrics)
  echo; echo "################ eval $OUT"

  # 1. held-out ingles
  python3 -u eval_lang_patch.py "${COMMON[@]}" --targets "$T" --train_test_split $SPLIT \
      --out_json "$OUT/eval_best_train.json" --out_md "$OUT/eval_best_train.md" 2>&1 | tee "$OUT/eval.log"

  # 2. es / de / en held-out (es y de ya NO estan en train)
  python3 -u cross_lang_patch.py "${COMMON[@]}" --targets "$T" --train_test_split $SPLIT \
      --conds "$CONDS" --tag idioma --out_dir "$OUT" 2>&1 | tee "$OUT/idioma.log"

  # 3. it / pt held-out
  python3 -u cross_lang_patch.py "${COMMON[@]}" --targets "$T" --train_test_split $SPLIT \
      --preset romance --out_dir "$OUT" 2>&1 | tee "$OUT/romance.log"

  # 4. open 1: los 99 prompts de navidad, todos held-out
  python3 -u eval_lang_patch.py "${COMMON[@]}" --targets "$T_OPEN" --train_test_split 0 \
      --out_json "$OUT/eval_open.json" --out_md "$OUT/eval_open.md" 2>&1 | tee "$OUT/eval_open.log"

  # 5. open 2: imperativos en / es / de, todos held-out
  python3 -u cross_lang_patch.py "${COMMON[@]}" --targets "$T_OPEN2" --train_test_split 0 \
      --conds "$CONDS" --tag idioma --out_dir "$OUT/open_2" 2>&1 | tee "$OUT/open_2/idioma.log"
done

echo
echo "Listo. Comparar contra algebra/runs/alg_fr (multi, misma receta) y su replica alg_fr_s1:"
for OUT in "${OUTS[@]}"; do
  echo "  $OUT/eval_best_train.md  cross_lang_idioma.md  cross_lang_romance.md  eval_open.md  open_2/cross_lang_idioma.md"
done
