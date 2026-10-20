#!/usr/bin/env bash
# Qwen traduce en vez de responder: con "{q} Please respond to the above in English."
# devuelve la pregunta traducida al ingles (~30% de las 112) tanto con la pregunta
# francesa real como con la pregunta inglesa + v_fr, y nunca con la inglesa sin parche
# (algebra/runs/qwen3_v10/conflicto_v2_n112). Aca se toman 10 de esos casos (los dos
# traducen) y se cambia el verbo, para ver si lo dispara "respond" o "the above":
#   instr_en_post_ref     {q} Please respond to the above in English.   (la original)
#   instr_en_post_answer  {q} Please answer to the above in English.
# Por plantilla: pregunta francesa real, pregunta inglesa, pregunta inglesa + v_fr.
#
#   uso:  bash run_traduccion_qwen.sh MODEL_PATH
#   variables: DEVICE (cuda:0)  IDX (las 10 filas)
#   salida: algebra/runs/qwen3_v10/traduccion_10/entrada_o_directiva_traduccion.{md,json}
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_traduccion_qwen.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
# conversacional 594 622 629 664 685, corta 600 607, imperativo_explicativo 633 640 647
IDX="${IDX:-594,600,607,622,629,633,640,647,664,685}"
R=algebra/runs/qwen3_v10
PATCH=$R/alg_fr/lang_patch_best_train.pt
O=$R/traduccion_10
[[ -f "$PATCH" ]] || { echo "falta $PATCH"; exit 1; }
mkdir -p "$O"

CONDS=""
for T in instr_en_post_ref instr_en_post_answer; do CONDS+="$T:prompt_fr:-:0,$T:prompt:-:0,$T:prompt:fr:1,"; done
ARGS=(--model "$MODEL" --device "$DEVICE" --targets attributes/qwen3/targets_v8_fr.csv --train_test_split 0.84
      --idx "$IDX" --num_tokens 250 --patch "fr=$PATCH" --conds "${CONDS%,}" --tag traduccion --out_dir "$O")

echo "################ dry: tramo de la pregunta en cada plantilla"
python3 -u entrada_o_directiva.py "${ARGS[@]}" --dry 2>&1 | tee "$O/dry.log"
echo; echo "################ traduccion (qwen3_v10, filas $IDX)"
python3 -u entrada_o_directiva.py "${ARGS[@]}" 2>&1 | tee "$O/traduccion.log"
echo; echo "Listo: $O/entrada_o_directiva_traduccion.md"
