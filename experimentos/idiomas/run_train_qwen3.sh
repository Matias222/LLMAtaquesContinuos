#!/usr/bin/env bash
# Run qwen3_v1: la receta v9 (run_train_v9.sh) con Qwen3-4B-Instruct-2507 sobre sus
# propios targets (attributes/qwen3, run_targets_qwen3.sh). MISMOS hiperparametros que
# v9 sin reescalar (decision 2026-10-08): L2 0.0925, batch 28, 10 epochs, 20 steps/batch,
# sign-SGD 0.00025 coseno, CE sobre 8 tokens, goal_all, split 0.84, evals de 150 tokens.
# El reporte D da ||v||/||e|| para comparar la norma relativa con Llama (v9: 0.78-0.87).
#
# Diferencias con run_train_v9.sh:
#   - TDIR=ODIR=attributes/qwen3, R=algebra/runs/qwen3_v1, GEN_CACHE propio
#   - abiertos --sin_output: los targets de Llama de open1/open2 no se usan
#   - reportes sin --prev_runs y sin paper (los vectores de Llama son d=3072)
#   - etapa verificar (verificar_modelo.py) antes de todo y controles despues de
#     train y de A: forma y norma de los parches, el parche cae SOLO en los tokens de
#     la pregunta (n_patched == largo del goal en cada fila evaluada), baseline en
#     ingles, |v| del eval == |v| del checkpoint
#
# Etapas: verificar datos base train ctrl_train A ctrl_A C D E (como v9 + controles)
#
#   uso:  bash run_train_qwen3.sh MODEL_PATH
#   variables:  DEVICE (cuda:0)  STAGES  SKIP_TRAIN=1  SMOKE=1 (1 epoch, 1 step, evals de
#               4 filas, todo en algebra/runs/qwen3_v1_smoke)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_train_qwen3.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
STAGES="${STAGES:-verificar datos base train ctrl_train A ctrl_A C D E}"
TDIR=attributes/qwen3
ODIR=attributes/qwen3
SPLIT=0.84
L2=0.0925
BATCH=28
EPOCHS=10
STEPS=20
VAL_N=20
HEAD_K=8
STEP_SIZE=0.00025
NTOK=150
CKPT=lang_patch_best_train.pt
R=algebra/runs/qwen3_v1
NEVAL=(); NENTRADA=0
if [[ "${SMOKE:-0}" == "1" ]]; then
  R=algebra/runs/qwen3_v1_smoke; EPOCHS=1; STEPS=1; VAL_N=2; NEVAL=(--n 4); NENTRADA=3
  echo "### SMOKE: 1 epoch, 1 step/batch, evals de 4 filas -> $R"
fi
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$R/reportes"
# cache de generaciones greedy (lm.generate): lo sin parche se genera una sola vez
export GEN_CACHE="$HERE/$R/gen_cache"
reporte() { python3 reporte_v8.py "$1" --runs "$R" --targets_dir "$TDIR" --split $SPLIT --num_tokens $NTOK \
              --paper_runs "" \
              2>&1 | tee "$R/reportes/$1.log"; }

# entradas de entrenamiento por celda (sin el idioma target, como en el paper)
cols() { case $1 in fr) echo prompt,prompt_es,prompt_de ;; es) echo prompt,prompt_de,prompt_fr ;;
                    de) echo prompt,prompt_es,prompt_fr ;; esac; }
conds() { case $1 in
  fr) echo "prompt_es:0,prompt_es:1,prompt_de:0,prompt_de:1,prompt:0,prompt:1" ;;
  es) echo "prompt_de:0,prompt_de:1,prompt_fr:0,prompt_fr:1,prompt:0,prompt:1" ;;
  de) echo "prompt_es:0,prompt_es:1,prompt_fr:0,prompt_fr:1,prompt:0,prompt:1" ;; esac; }
t_open()  { echo "$ODIR/open1_$1.csv"; }
t_open2() { echo "$ODIR/open2_$1.csv"; }

# =============================================================================
# 0. validacion
# =============================================================================
echo "################ 0 validacion"
[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
python3 - "$MODEL" <<'PY'
import sys
from lm import familia
assert familia(sys.argv[1]) == "qwen3", "este runner es para Qwen3"
PY
for L in fr es de; do
  [[ -f "$TDIR/targets_v8_$L.csv" ]] || { echo "falta $TDIR/targets_v8_$L.csv"; exit 1; }
done
python3 - <<'PY'
from checkers import language_verdict
assert language_verdict("La capitale de la France est Paris.") == "fr", "GlotLID no responde"
print("GlotLID ok")
PY

# =============================================================================
# verificar: controles del modelo (con FALLA no se sigue)
# =============================================================================
if has verificar; then
  echo; echo "################ verificar"
  python3 -u verificar_modelo.py --model "$MODEL" --device "$DEVICE" --targets "$TDIR/targets_v8_fr.csv" \
      --out_json "$R/reportes/verificar_modelo.json" 2>&1 | tee "$R/reportes/verificar_modelo.log"
fi

# =============================================================================
# datos: held-out con italiano/portugues y alias de 6 idiomas
# =============================================================================
if has datos; then
  echo; echo "################ datos"
  python3 preparar_targets_v8.py heldout --dir "$TDIR" --split $SPLIT 2>&1 | tee "$R/reportes/datos.log"
  # las tres celdas entrenan con la misma cantidad de filas (la minima entre celdas)
  python3 preparar_targets_v8.py alias --dir "$TDIR" 2>&1 | tee -a "$R/reportes/datos.log"
  python3 preparar_targets_v8.py igualar --dir "$TDIR" --split $SPLIT 2>&1 | tee -a "$R/reportes/datos.log"
  python3 preparar_targets_v8.py abiertos --sin_output --out "$ODIR" 2>&1 | tee -a "$R/reportes/datos.log"
fi
for L in fr es de; do
  for f in "$(t_open $L)" "$(t_open2 $L)"; do
    [[ -f "$f" ]] || { echo "falta $f (correr la etapa datos)"; exit 1; }
  done
done

# =============================================================================
# base: todo lo sin parche, una vez (queda en $GEN_CACHE)
# =============================================================================
if has base; then
  echo; echo "################ base"
  mkdir -p "$R/base"
  python3 -u base_v9.py --model "$MODEL" --device "$DEVICE" ${NEVAL[@]+"${NEVAL[@]}"} \
      --heldout "$TDIR/targets_v8_fr.csv" --split $SPLIT --open1 "$(t_open fr)" --open2 "$(t_open2 fr)" \
      --num_tokens $NTOK --out_dir "$R/base" 2>&1 | tee "$R/base/base.log"
fi

# =============================================================================
# train
# =============================================================================
if has train; then
  for L in fr es de; do
    O=$R/alg_$L
    if [[ "${SKIP_TRAIN:-0}" == "1" && -f "$O/$CKPT" ]]; then echo "ya entrenado: $O"; continue; fi
    mkdir -p "$O"
    echo; echo "################ train $L"
    python3 -u train_lang_patch.py --model "$MODEL" --device "$DEVICE" \
        --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT \
        --prompt_cols "$(cols $L)" --attr_name "$L" \
        --patch_anchor goal_all --num_patch_positions 1 \
        --l2_weight $L2 --batch_size $BATCH --num_steps_per_prompt $STEPS --num_epochs $EPOCHS \
        --step_size $STEP_SIZE --step_decay cosine --loss_head_k $HEAD_K \
        --val_n $VAL_N --save_best --output_dir "$O" 2>&1 | tee "$O/train.log"
  done
  reporte train
fi

if has ctrl_train; then
  echo; echo "################ controles del train"
  python3 controles_run.py train --model "$MODEL" --runs "$R" --targets_dir "$TDIR" --split $SPLIT \
      2>&1 | tee "$R/reportes/ctrl_train.log"
fi

for L in fr es de; do
  if (has A || has C || has D || has E) && [[ ! -f "$R/alg_$L/$CKPT" ]]; then
    echo "falta $R/alg_$L/$CKPT (correr la etapa train)"; exit 1
  fi
done
comun() {   # comun <celda>: flags compartidos por las evals de esa celda
  echo --model "$MODEL" --device "$DEVICE" --patch "$R/alg_$1/$CKPT" --patch_anchor goal_all \
       --num_patch_positions 1 --target_lang "$1" --num_tokens $NTOK
}

# =============================================================================
# A: held-out v8 por categoria
# =============================================================================
if has A; then
  for L in fr es de; do
    O=$R/alg_$L
    echo; echo "################ A $L"
    # shellcheck disable=SC2046
    python3 -u eval_lang_patch.py $(comun $L) --cell_metrics --control nativo ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT \
        --out_json "$O/eval_heldout.json" --out_md "$O/eval_heldout.md" 2>&1 | tee "$O/eval_heldout.log"
    python3 -u cross_lang_patch.py $(comun $L) ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT \
        --conds "$(conds $L)" --tag idioma --out_dir "$O" 2>&1 | tee "$O/idioma.log"
    python3 -u cross_lang_patch.py $(comun $L) ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT \
        --preset romance --out_dir "$O" 2>&1 | tee "$O/romance.log"
  done
  reporte A
fi
if has ctrl_A; then
  echo; echo "################ controles de A"
  python3 controles_run.py A --model "$MODEL" --runs "$R" --targets_dir "$TDIR" --split $SPLIT \
      2>&1 | tee "$R/reportes/ctrl_A.log"
fi

# =============================================================================
# C: sets abiertos
# =============================================================================
if has C; then
  for L in fr es de; do
    O=$R/alg_$L; mkdir -p "$O/open_2"
    echo; echo "################ C $L"
    python3 -u eval_lang_patch.py $(comun $L) --cell_metrics --control nativo ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$(t_open $L)" --train_test_split 0 \
        --out_json "$O/eval_open.json" --out_md "$O/eval_open.md" 2>&1 | tee "$O/eval_open.log"
    python3 -u cross_lang_patch.py $(comun $L) ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$(t_open2 $L)" --train_test_split 0 \
        --conds "$(conds $L),prompt_$L:0" --tag idioma --out_dir "$O/open_2" 2>&1 | tee "$O/open_2/idioma.log"
  done
  reporte C
fi

# =============================================================================
# D: sin generacion
# =============================================================================
if has D; then
  for L in fr es de; do
    O=$R/alg_$L
    echo; echo "################ D $L"
    python3 -u nearest_token_patch.py --model "$MODEL" --patch "$O/$CKPT" \
        --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT --cols "$(cols $L)" \
        --out_dir "$O/nearest_token" 2>&1 | tee "$O/nearest_token.log"
  done
  reporte D
fi

# =============================================================================
# E: tests de comportamiento (necesita las tres direcciones)
# =============================================================================
if has E; then
  mkdir -p "$R/resta" "$R/tests"
  P=(--patch "fr=$R/alg_fr/$CKPT" --patch "es=$R/alg_es/$CKPT" --patch "de=$R/alg_de/$CKPT")
  eod() {   # eod <tag> <conds> <out_dir>
    python3 -u entrada_o_directiva.py --model "$MODEL" --device "$DEVICE" \
        --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT --n $NENTRADA \
        --num_tokens $NTOK --rand_like fr "${P[@]}" --conds "$2" --tag "$1" --out_dir "$3" \
        2>&1 | tee "$3/$1.log"
  }
  # resta: pregunta en el idioma L menos cada direccion y menos 3 azares con la norma de v_L
  RESTA=""
  for L in fr es de; do
    RESTA+="plain:prompt_$L:-:0,"
    for V in fr es de rand0_$L rand1_$L rand2_$L; do RESTA+="plain:prompt_$L:$V:-1,"; done
  done
  echo; echo "################ E resta"
  eod resta "${RESTA%,}" "$R/resta"
  echo; echo "################ E idioma_entrada"
  eod idioma_entrada "lang_id:prompt:-:0,lang_id:prompt:fr:1,lang_id:prompt:es:1,lang_id:prompt:de:1,lang_id:prompt:rand0:1,lang_id:prompt_fr:-:0,lang_id:prompt_es:-:0,lang_id:prompt_de:-:0" "$R/tests"
  echo; echo "################ E resta_directiva"
  eod resta_directiva "instr_fr:prompt:-:0,instr_fr:prompt:fr:-1,instr_fr:prompt:es:-1,instr_fr:prompt:rand0:-1" "$R/tests"
  echo; echo "################ E conflicto"
  eod conflicto "instr_en:prompt_fr:-:0,instr_en:prompt:-:0,instr_en:prompt:fr:1,instr_en:prompt:rand0:1,plain:prompt:-:0,plain:prompt:fr:1" "$R/tests"
  reporte E
fi

echo
echo "Listo. Reportes en $R/reportes/{train,A,C,D,E}.md (controles: ctrl_train.log, ctrl_A.log)"
