#!/usr/bin/env bash
# Parches con posicion fija (Question-3, Header-3) con la data y la receta v10, solo
# frances, para comparar formatos contra Shared (alg_fr, un unico v en todos los
# tokens de la pregunta) como en el paper (§3.1, Tablas 6, 7, 9), que los tenia con la
# data vieja (run_paper_v7.sh, algebra/runs/pos_q3 y pos_h3).
#
#   q3  [1,3,d] sobre los 3 primeros tokens de la pregunta   (--patch_anchor goal)
#   h3  [1,3,d] sobre los 3 ultimos tokens del header del assistant (--patch_anchor header)
#       Llama: assistant <|end_header_id|> \n\n   Qwen: <|im_start|> assistant \n
#       Esos tokens son iguales en toda entrada: h3 equivale a un soft prompt.
#
# Receta identica a alg_fr de run_train_v10.sh / run_train_qwen3.sh (L2 0.0915, batch 28,
# 20 steps, 10 epochs, lr 0.00025 coseno, CE de los primeros 8 tokens, entradas
# en/es/de, checkpoint lang_patch_best_train.pt); solo cambian anchor y posiciones.
#
#   train    pos_q3_fr, pos_h3_fr
#   A        held-out (control nativo), es/de y it/pt -> fr
#   C        open1 y open2
#   E        tests de entrada o directiva con Shared, Q3, H3 y sus azares en la misma
#            grilla: resta (Tabla 6), identificacion de idioma (7), resta contra
#            instruccion (8), conflicto con la instruccion antes y al final (9)
#   reporte  reportes/pos.md (reporte_pos.py), con controles de posiciones
#   (sin D: nearest_token_patch.py es solo para un v compartido, y en h3 no aplica)
#
#   uso:  bash run_pos_v10.sh MODEL_PATH RUN        RUN = v10 | qwen3_v10
#   variables: DEVICE (cuda:0)  STAGES ("train A C E reporte")  SKIP_TRAIN=1
#              SMOKE=1 (1 epoch, 1 step, evals de 4 filas, tests de 3; salida en
#                       algebra/runs/<RUN>/pos_smoke; usa el alg_fr real del run)
#   salida: algebra/runs/<RUN>/{pos_q3_fr,pos_h3_fr,pos_tests,reportes/pos.md}
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_pos_v10.sh MODEL_PATH RUN}"
RUN="${2:?uso: bash run_pos_v10.sh MODEL_PATH RUN (v10 | qwen3_v10)}"
DEVICE="${DEVICE:-cuda:0}"
STAGES="${STAGES:-train A C E reporte}"
case "$RUN" in
  v10)       TDIR=attributes/v10;   FAMILIA=llama ;;
  qwen3_v10) TDIR=attributes/qwen3; FAMILIA=qwen3 ;;
  *) echo "RUN desconocido: $RUN (v10 | qwen3_v10)"; exit 1 ;;
esac
ODIR=$TDIR
SPLIT=0.84
L2=0.0915
BATCH=28
EPOCHS=10
STEPS=20
VAL_N=20
HEAD_K=8
STEP_SIZE=0.00025
NTOK=250
NPOS=3
CKPT=lang_patch_best_train.pt
R=algebra/runs/$RUN          # alg_fr (Shared) y gen_cache del run
O=$R                         # salida de q3/h3
NEVAL=(); NENTRADA=0
if [[ "${SMOKE:-0}" == "1" ]]; then
  O=$R/pos_smoke; EPOCHS=1; STEPS=1; VAL_N=2; NEVAL=(--n 4); NENTRADA=3
  echo "### SMOKE: 1 epoch, 1 step/batch, evals de 4 filas -> $O"
fi
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$O/reportes" "$O/pos_tests"
# lo sin parche y lo de Shared ya esta generado en el cache del run
export GEN_CACHE="$HERE/$R/gen_cache"

conds_fr="prompt_es:0,prompt_es:1,prompt_de:0,prompt_de:1,prompt:0,prompt:1"
SHARED=$R/alg_fr/$CKPT
anchor() { case $1 in q3) echo goal ;; h3) echo header ;; esac; }

# =============================================================================
# 0. validacion
# =============================================================================
echo "################ 0 validacion"
[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
python3 - "$MODEL" "$FAMILIA" <<'PY'
import sys
from lm import familia
assert familia(sys.argv[1]) == sys.argv[2], f"el modelo no es {sys.argv[2]}: no corresponde a este RUN"
PY
for f in "$TDIR/targets_v8_fr.csv" "$ODIR/open1_fr.csv" "$ODIR/open2_fr.csv" "$SHARED"; do
  [[ -f "$f" ]] || { echo "falta $f"; exit 1; }
done

# =============================================================================
# train
# =============================================================================
if has train; then
  for P in q3 h3; do
    D=$O/pos_${P}_fr
    if [[ "${SKIP_TRAIN:-0}" == "1" && -f "$D/$CKPT" ]]; then echo "ya entrenado: $D"; continue; fi
    mkdir -p "$D"
    echo; echo "################ train $P (anchor $(anchor $P), $NPOS posiciones)"
    python3 -u train_lang_patch.py --model "$MODEL" --device "$DEVICE" \
        --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT \
        --prompt_cols prompt,prompt_es,prompt_de --attr_name fr \
        --patch_anchor "$(anchor $P)" --num_patch_positions $NPOS \
        --l2_weight $L2 --batch_size $BATCH --num_steps_per_prompt $STEPS --num_epochs $EPOCHS \
        --step_size $STEP_SIZE --step_decay cosine --loss_head_k $HEAD_K \
        --val_n $VAL_N --save_best --output_dir "$D" 2>&1 | tee "$D/train.log"
  done
fi

for P in q3 h3; do
  if (has A || has C || has E) && [[ ! -f "$O/pos_${P}_fr/$CKPT" ]]; then
    echo "falta $O/pos_${P}_fr/$CKPT (correr la etapa train)"; exit 1
  fi
done
comun() {   # comun <q3|h3>: flags compartidos por las evals de ese parche
  echo --model "$MODEL" --device "$DEVICE" --patch "$O/pos_$1_fr/$CKPT" --patch_anchor "$(anchor $1)" \
       --num_patch_positions $NPOS --target_lang fr --num_tokens $NTOK
}

# =============================================================================
# A: held-out, otros idiomas de entrada, italiano y portugues
# =============================================================================
if has A; then
  for P in q3 h3; do
    D=$O/pos_${P}_fr
    echo; echo "################ A $P"
    # shellcheck disable=SC2046
    python3 -u eval_lang_patch.py $(comun $P) --cell_metrics --control nativo ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT \
        --out_json "$D/eval_heldout.json" --out_md "$D/eval_heldout.md" 2>&1 | tee "$D/eval_heldout.log"
    # shellcheck disable=SC2046
    python3 -u cross_lang_patch.py $(comun $P) ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT \
        --conds "$conds_fr" --tag idioma --out_dir "$D" 2>&1 | tee "$D/idioma.log"
    # shellcheck disable=SC2046
    python3 -u cross_lang_patch.py $(comun $P) ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT \
        --preset romance --out_dir "$D" 2>&1 | tee "$D/romance.log"
  done
fi

# =============================================================================
# C: sets abiertos
# =============================================================================
if has C; then
  for P in q3 h3; do
    D=$O/pos_${P}_fr; mkdir -p "$D/open_2"
    echo; echo "################ C $P"
    # shellcheck disable=SC2046
    python3 -u eval_lang_patch.py $(comun $P) --cell_metrics --control nativo ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$ODIR/open1_fr.csv" --train_test_split 0 \
        --out_json "$D/eval_open.json" --out_md "$D/eval_open.md" 2>&1 | tee "$D/eval_open.log"
    # shellcheck disable=SC2046
    python3 -u cross_lang_patch.py $(comun $P) ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$ODIR/open2_fr.csv" --train_test_split 0 \
        --conds "$conds_fr,prompt_fr:0" --tag idioma --out_dir "$D/open_2" 2>&1 | tee "$D/open_2/idioma.log"
  done
fi

# =============================================================================
# E: Shared, Q3 y H3 en la misma grilla (rand0 = azar de Shared; rand0_q3 / rand0_h3 =
#    azar con la forma, la norma y el anchor de q3 / h3)
# =============================================================================
if has E; then
  T=$O/pos_tests
  PATCHES=(--patch "fr=$SHARED" --patch "q3=$O/pos_q3_fr/$CKPT@goal" --patch "h3=$O/pos_h3_fr/$CKPT@header")
  eod() {   # eod <tag> <conds> [--dry]
    python3 -u entrada_o_directiva.py --model "$MODEL" --device "$DEVICE" \
        --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT --n $NENTRADA \
        --num_tokens $NTOK --rand_like fr "${PATCHES[@]}" --conds "$2" --tag "$1" --out_dir "$T" "${@:3}"
  }
  grid() {  # grid <plantilla> <col> <escala> <parches...>
    local tpl=$1 col=$2 a=$3 out=""; shift 3
    for p in "$@"; do out+="$tpl:$col:$p:$a,"; done; echo "${out%,}"
  }
  RESTA="plain:prompt_fr:-:0,$(grid plain prompt_fr -1 fr q3 h3 rand0 rand0_q3 rand0_h3),plain:prompt_fr:q3:-2"
  IDIOMA="lang_id:prompt:-:0,$(grid lang_id prompt 1 fr q3 h3 rand0 rand0_q3 rand0_h3),lang_id:prompt_fr:-:0"
  DIRECTIVA="instr_fr:prompt:-:0,$(grid instr_fr prompt -1 fr q3 h3 rand0 rand0_q3 rand0_h3)"
  CONFLICTO=""
  for I in instr_en instr_en_post instr_en_post_ref; do
    CONFLICTO+="$I:prompt_fr:-:0,$I:prompt:-:0,$(grid $I prompt 1 fr q3 h3 rand0 rand0_q3 rand0_h3),"
  done
  CONFLICTO+="plain:prompt:-:0,$(grid plain prompt 1 fr q3 h3)"
  for t in resta idioma directiva conflicto; do
    case $t in resta) C=$RESTA ;; idioma) C=$IDIOMA ;; directiva) C=$DIRECTIVA ;; conflicto) C=$CONFLICTO ;; esac
    echo; echo "################ E $t (dry: posiciones de cada parche)"
    eod "pos_$t" "$C" --dry 2>&1 | tee "$T/pos_${t}_dry.log"
    echo; echo "################ E $t"
    eod "pos_$t" "$C" 2>&1 | tee "$T/pos_$t.log"
  done
fi

# =============================================================================
# reporte
# =============================================================================
if has reporte; then
  python3 reporte_pos.py --shared "$R/alg_fr" --q3 "$O/pos_q3_fr" --h3 "$O/pos_h3_fr" --tests "$O/pos_tests" \
      --out "$O/reportes/pos.md" 2>&1 | tee "$O/reportes/pos.log"
fi

echo
echo "Listo. Reporte en $O/reportes/pos.md"
