#!/usr/bin/env bash
# UN solo vector sumado a TODOS los tokens de la pregunta del usuario.
#
# Hasta aca el parche fueron siempre 3 vectores distintos, cada uno atado a su
# posicion: primero sobre los 3 primeros tokens de la pregunta (solo funciona con
# las aperturas e idiomas que vio: open_2 0.04, it/pt 0.22 / 0.14) y despues
# sobre los 3 ultimos del header del assistant (generaliza: 0.94-1.00 en todo).
# El header generaliza porque sus tokens son siempre los mismos. Esto prueba la
# otra salida: un v [1, 1, d] que cae igual sobre cada token de la pregunta
# (e'_i = e_i + v para todo i del goal; ni system, ni headers, ni <|eot_id|>),
# asi que no puede apoyarse ni en la posicion ni en el token sobre el que se
# suma. 3072 parametros en vez de 9216. Si funciona, hay una direccion "frances"
# en el espacio de embeddings que actua como desplazamiento uniforme.
#
# Misma receta que v5_head_multi_l2_0.0725 y v5_header_head_multi (head 8,
# entradas en/es/de, L2 0.0725): lo unico que cambia es el anchor. Y las mismas
# cinco evaluaciones, para comparar 1 a 1:
#   1. held-out ingles            eval_lang_patch          -> eval_best_train.*
#   2. es/de/en held-out          cross_lang --preset idioma  -> cross_lang_idioma.*
#   3. it/pt held-out             cross_lang --preset romance -> cross_lang_romance.*
#   4. open 1 (99 de navidad)     eval_lang_patch, split 0 -> eval_open.*
#   5. open 2 (imperativos en/es/de) cross_lang idioma, split 0 -> open_2/cross_lang_idioma.*
#
# OJO al leer 4 y 5: v se SUMA en cada posicion, no se promedia, asi que la
# perturbacion total es (largo de la pregunta) x v. El train.log imprime el largo
# del goal en train y cada reporte trae los tokens parcheados por prompt
# (`tok parche` / n_patched_media): si un set abierto es mucho mas largo o mas
# corto que train, una caida ahi puede ser de escala y no de direccion. El L2
# tampoco esta recalibrado para esto (0.0725 se eligio con 3 vectores): si el
# frances queda corto, es lo primero a barrer.
#
#   uso (desde experimentos/idiomas):  bash run_goal_all_v5.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  L2 (0.0725)  HEAD_K (8)  EPOCHS (8)  NAME (v5_goalall_head_multi)
#               STEP_SIZE (0.00025)  INIT_PATCH (vacio = desde ceros; un .pt [1,1,d] = warm start)
#               SKIP_TRAIN=1 para evaluar un parche ya entrenado
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
L2="${L2:-0.0725}"
HEAD_K="${HEAD_K:-8}"
EPOCHS="${EPOCHS:-8}"
STEP_SIZE="${STEP_SIZE:-0.00025}"
INIT_PATCH="${INIT_PATCH:-}"
NAME="${NAME:-v5_goalall_head_multi}"
ANCHOR=goal_all
NPOS=1
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
      --step_size "$STEP_SIZE" ${INIT_PATCH:+--init_patch "$INIT_PATCH"} \
      --patch_anchor $ANCHOR --num_patch_positions $NPOS 2>&1 | tee "$OUT/train.log"
fi

# 1. held-out ingles
python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
    --patch "$P" --train_test_split $SPLIT --patch_anchor $ANCHOR --num_patch_positions $NPOS \
    --out_json "$OUT/eval_best_train.json" --out_md "$OUT/eval_best_train.md" 2>&1 | tee "$OUT/eval.log"

# 2. es / de / en held-out
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
    --patch "$P" --train_test_split $SPLIT --patch_anchor $ANCHOR --num_patch_positions $NPOS \
    --preset idioma --out_dir "$OUT" 2>&1 | tee "$OUT/idioma.log"

# 3. it / pt held-out (idiomas no vistos)
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
    --patch "$P" --train_test_split $SPLIT --patch_anchor $ANCHOR --num_patch_positions $NPOS \
    --preset romance --out_dir "$OUT" 2>&1 | tee "$OUT/romance.log"

# 4. open 1: los 99 prompts de navidad, todos held-out
python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T_OPEN" \
    --patch "$P" --train_test_split 0 --patch_anchor $ANCHOR --num_patch_positions $NPOS \
    --out_json "$OUT/eval_open.json" --out_md "$OUT/eval_open.md" 2>&1 | tee "$OUT/eval_open.log"

# 5. open 2: imperativos en / es / de, todos held-out
python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T_OPEN2" \
    --patch "$P" --train_test_split 0 --patch_anchor $ANCHOR --num_patch_positions $NPOS \
    --preset idioma --out_dir "$OUT/open_2" 2>&1 | tee "$OUT/open_2/idioma.log"

echo
echo "Listo. Comparar contra runs/v5_head_multi_l2_0.0725 (3 primeros tokens) y"
echo "runs/v5_header_head_multi (header del assistant):"
echo "  $OUT/eval_best_train.md      (held-out ingles)"
echo "  $OUT/cross_lang_idioma.md    (es/de)"
echo "  $OUT/cross_lang_romance.md   (it/pt)"
echo "  $OUT/eval_open.md            (open 1)"
echo "  $OUT/open_2/cross_lang_idioma.md  (open 2)"
