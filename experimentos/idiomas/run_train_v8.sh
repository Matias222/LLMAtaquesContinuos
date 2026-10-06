#!/usr/bin/env bash
# Entrenamiento y evaluacion de las direcciones v8 (fr, es, de) sobre el banco v8
# (attributes/v8: 600 preguntas nuevas en 6 estilos + 100 factuales viejas, 7
# categorias intercaladas). Todo en algebra/runs/v8: no pisa los vectores del paper.
#
# Receta = la de alg_* del paper (algebra/run_algebra_v6.sh) salvo:
#   L2 0.08 (paper 0.075) | batch 28 = 4 vueltas de las 7 categorias (paper 32)
#   split 0.84 -> 588 train / 112 held-out, 16 por categoria (paper 0.80 de 250)
#   evaluaciones con 150 tokens, referencia y baseline regenerados con ese largo
# Igual: goal_all (1 vector), sign-SGD 0.00025 coseno, 10 epochs, 20 steps/batch,
# CE sobre los primeros 8 tokens, checkpoint lang_patch_best_train.pt.
#
# Etapas (STAGES, en orden; cada una escribe su reporte en $R/reportes/<etapa>.md):
#   datos   held-out listo: prompt_it/prompt_pt y alias de 6 idiomas de las viejas
#           (preparar_targets_v8.py heldout); valida y aborta si falta algo. Despues
#           iguala el train de las tres celdas a 549 filas (preparar_targets_v8.py igualar)
#   train   las tres direcciones                                  -> reportes/train.md
#   A       held-out v8 por categoria: ingles (con referencia), otros idiomas de
#           entrenamiento, italiano y portugues                    -> reportes/A.md
#   C       open1 (99) y open2 (50 imperativos por idioma)        -> reportes/C.md
#   D       token mas cercano, normas y cosenos (v8 y paper)       -> reportes/D.md
#   E       resta q_L - v con controles (otros idiomas, 3 azares) y entrada o
#           directiva (identificacion de idioma, resta contra instruccion,
#           conflicto)                                            -> reportes/E.md
#
#   uso:  bash run_train_v8.sh MODEL_PATH
#   variables:  DEVICE (cuda:0)  STAGES ("datos train A C D E")  SKIP_TRAIN=1 (no reentrenar
#               una celda que ya tiene su parche)  SMOKE=1 (1 epoch, 1 step, evals de 4 filas,
#               todo en algebra/runs/v8_smoke)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_train_v8.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
STAGES="${STAGES:-datos train A C D E}"
TDIR=attributes/v8
SPLIT=0.84
L2=0.08
BATCH=28
EPOCHS=10
STEPS=20
VAL_N=20
HEAD_K=8
STEP_SIZE=0.00025
NTOK=150
CKPT=lang_patch_best_train.pt
R=algebra/runs/v8
NEVAL=(); NENTRADA=0
if [[ "${SMOKE:-0}" == "1" ]]; then
  R=algebra/runs/v8_smoke; EPOCHS=1; STEPS=1; VAL_N=2; NEVAL=(--n 4); NENTRADA=3
  echo "### SMOKE: 1 epoch, 1 step/batch, evals de 4 filas -> $R"
fi
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$R/reportes"
reporte() { python3 reporte_v8.py "$1" --runs "$R" --targets_dir "$TDIR" --split $SPLIT --num_tokens $NTOK \
              2>&1 | tee "$R/reportes/$1.log"; }

# entradas de entrenamiento por celda (sin el idioma target, como en el paper)
cols() { case $1 in fr) echo prompt,prompt_es,prompt_de ;; es) echo prompt,prompt_de,prompt_fr ;;
                    de) echo prompt,prompt_es,prompt_fr ;; esac; }
conds() { case $1 in
  fr) echo "prompt_es:0,prompt_es:1,prompt_de:0,prompt_de:1,prompt:0,prompt:1" ;;
  es) echo "prompt_de:0,prompt_de:1,prompt_fr:0,prompt_fr:1,prompt:0,prompt:1" ;;
  de) echo "prompt_es:0,prompt_es:1,prompt_fr:0,prompt_fr:1,prompt:0,prompt:1" ;; esac; }
t_open()  { [[ $1 == fr ]] && echo attributes/french/targets_open.csv   || echo "algebra/targets/targets_$1_open.csv"; }
t_open2() { [[ $1 == fr ]] && echo attributes/french/targets_open_2.csv || echo "algebra/targets/targets_$1_open_2.csv"; }

# =============================================================================
# 0. validacion
# =============================================================================
echo "################ 0 validacion"
[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
for L in fr es de; do
  for f in "$TDIR/targets_v8_$L.csv" "$(t_open $L)" "$(t_open2 $L)"; do
    [[ -f "$f" ]] || { echo "falta $f"; exit 1; }
  done
done
python3 - <<'PY'
from checkers import language_verdict
assert language_verdict("La capitale de la France est Paris.") == "fr", "GlotLID no responde"
print("GlotLID ok")
PY

# =============================================================================
# datos: held-out con italiano/portugues y alias de 6 idiomas
# =============================================================================
if has datos; then
  echo; echo "################ datos"
  python3 preparar_targets_v8.py heldout --dir "$TDIR" --split $SPLIT 2>&1 | tee "$R/reportes/datos.log"
  # las tres celdas entrenan con la misma cantidad de filas (la menor: fr, 549)
  python3 preparar_targets_v8.py igualar --dir "$TDIR" --split $SPLIT 2>&1 | tee -a "$R/reportes/datos.log"
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
    python3 -u eval_lang_patch.py $(comun $L) --cell_metrics --regen_ref ${NEVAL[@]+"${NEVAL[@]}"} \
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

# =============================================================================
# C: sets abiertos
# =============================================================================
if has C; then
  for L in fr es de; do
    O=$R/alg_$L; mkdir -p "$O/open_2"
    echo; echo "################ C $L"
    python3 -u eval_lang_patch.py $(comun $L) --cell_metrics --regen_ref ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$(t_open $L)" --train_test_split 0 \
        --out_json "$O/eval_open.json" --out_md "$O/eval_open.md" 2>&1 | tee "$O/eval_open.log"
    python3 -u cross_lang_patch.py $(comun $L) ${NEVAL[@]+"${NEVAL[@]}"} \
        --targets "$(t_open2 $L)" --train_test_split 0 \
        --conds "$(conds $L)" --tag idioma --out_dir "$O/open_2" 2>&1 | tee "$O/open_2/idioma.log"
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
echo "Listo. Reportes en $R/reportes/{train,A,C,D,E}.md"
