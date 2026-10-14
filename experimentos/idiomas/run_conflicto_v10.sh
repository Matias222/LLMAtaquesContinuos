#!/usr/bin/env bash
# Conflicto (Tabla 9) con otras redacciones de la instruccion en contra.
# En qwen3_v10 "Answer this in English. {q}" gana 96/4 tanto a la pregunta francesa
# real como al parche: el test queda en el piso y no distingue. Se buscan
# instrucciones de otra fuerza donde la pregunta nativa quede en un punto
# intermedio. Plantillas en entrada_o_directiva.py:
#   instr_en        Answer this in English. {q}              (la del paper, referencia)
#   instr_en_b      Answer the following in English: {q}
#   instr_en_post   {q} Please answer in English.
#   instr_en_suave  If you can, answer in English: {q}
# Por plantilla: pregunta francesa real, pregunta inglesa, pregunta inglesa + v_fr.
# Solo evalua (usa el lang_patch_best_train.pt de la corrida).
#
#   uso:  bash run_conflicto_v10.sh MODEL_PATH RUN
#         RUN = qwen3_v10 | v10
#   variables: DEVICE (cuda:0)  N (10 filas del held-out; 0 = las 112)
#              PLANTILLAS ("instr_en instr_en_b instr_en_post instr_en_suave")
#   salida: algebra/runs/<RUN>/conflicto_v2_n<N>/entrada_o_directiva_conflicto_v2.{md,json} (+ dry.log, conflicto_v2.log)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_conflicto_v10.sh MODEL_PATH RUN}"
RUN="${2:?uso: bash run_conflicto_v10.sh MODEL_PATH RUN (qwen3_v10 | v10)}"
DEVICE="${DEVICE:-cuda:0}"
N="${N:-10}"
PLANTILLAS="${PLANTILLAS:-instr_en instr_en_b instr_en_post instr_en_suave}"
case "$RUN" in
  qwen3_v10) TDIR=attributes/qwen3 ;;
  v10)       TDIR=attributes/v10 ;;
  *) echo "RUN desconocido: $RUN (qwen3_v10 | v10)"; exit 1 ;;
esac
R=algebra/runs/$RUN
PATCH=$R/alg_fr/lang_patch_best_train.pt
O=$R/conflicto_v2_n$N
[[ -f "$PATCH" ]] || { echo "falta $PATCH"; exit 1; }
mkdir -p "$O"

CONDS=""
for T in $PLANTILLAS; do CONDS+="$T:prompt_fr:-:0,$T:prompt:-:0,$T:prompt:fr:1,"; done
CONDS="${CONDS%,}"
ARGS=(--model "$MODEL" --device "$DEVICE" --targets "$TDIR/targets_v8_fr.csv" --train_test_split 0.84
      --n "$N" --num_tokens 250 --patch "fr=$PATCH" --conds "$CONDS" --tag conflicto_v2 --out_dir "$O")

echo "################ dry: tramo de la pregunta en cada plantilla"
python3 -u entrada_o_directiva.py "${ARGS[@]}" --dry 2>&1 | tee "$O/dry.log"
echo; echo "################ conflicto_v2 ($RUN, n=$N)"
python3 -u entrada_o_directiva.py "${ARGS[@]}" 2>&1 | tee "$O/conflicto_v2.log"
echo; echo "Listo: $O/entrada_o_directiva_conflicto_v2.md"
