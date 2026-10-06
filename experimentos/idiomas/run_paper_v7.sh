#!/usr/bin/env bash
# Experimentos que faltan para el paper (seccion 4). Todo con la receta de alg_fr:
# L2 0.075, 10 epochs, head 8, batch 32, 20 steps, step 0.00025 cosine, entradas
# en/es/de, target frances, mismo split 200/50.
#
#   B1  train Question-3   3 vectores sobre los 3 primeros tokens de la pregunta
#                          (anchor goal)                        -> algebra/runs/pos_q3
#   B2  train Header-3     3 vectores sobre assistant <|end_header_id|> \n\n
#                          (anchor header): un soft prompt      -> algebra/runs/pos_h3
#   B3  las cinco evals de siempre para B1 y B2 (held-out en, es/de, it/pt,
#       open 1, open 2)                                         -> <run>/*.md
#   B4+B5  resta sobre preguntas en FRANCES, todo en una tabla:
#          q_fr - v  para v_fr, v_es, v_de, v_fr replica (B8), Question-3 (a=-1 y -2),
#          Header-3 (exploratorio) y 3 vectores al azar con la norma de v_fr
#                                                               -> paper_v7/resta/
#   B6+B7  los tres tests de entrada o directiva con Shared, Question-3 y
#          Header-3 lado a lado, cada uno con su azar de igual forma y norma
#                                                               -> paper_v7/tests/
#   B8  las cinco evals de la replica alg_fr_s1                 -> algebra/runs/alg_fr_s1
#
# 0. VALIDACION INICIAL (siempre, antes de cualquier etapa; si falla, no corre nada):
#   a. entorno: dependencias, CUDA y memoria, config del modelo (28 capas, d 3072,
#      vocab 128256, embeddings atados), CSV (filas y columnas), forma y norma de
#      los parches existentes                          (preflight_paper_v7.py env)
#   b. tokenizer: tramos de la pregunta y posiciones de cada anchor en las
#      cuatro grillas de resta/tests                   (entrada_o_directiva --dry)
#   c. humo de entrenamiento: Question-3 y Header-3, 1 epoch, 2 steps, 30 filas
#   d. humo de las evals (2 filas) con esos parches de humo
#   e. humo de resta y tests (2 filas) con TODAS las condiciones reales
#   f. reproduccion: alg_fr sobre 5 preguntas del held-out tiene que dar frances
#   g. chequeo de salidas: formas, posiciones parcheadas por anchor, repro
#                                                      (preflight_paper_v7.py outputs)
#   Todo en algebra/runs/paper_v7/_preflight (se borra y rehace en cada corrida).
#
# Etapas (STAGES, en este orden, despues de la validacion):
#   train  B1 B2
#   eval   B3 B8
#   resta  B4 B5 (y la resta de B8)
#   tests  B6 B7
#
#   uso (desde cualquier lado):  bash run_paper_v7.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  STAGES ("train eval resta tests")
#               STAGES="" corre solo la validacion
#               SKIP_TRAIN=1  no reentrenar un parche que ya existe
#               N (0 = las 50 filas; p.ej. N=4 para humo en resta/tests)
#               RAND_SEEDS ("0 1 2")  semillas del azar en la resta
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
STAGES="${STAGES-train eval resta tests}"
N="${N:-0}"
RAND_SEEDS="${RAND_SEEDS:-0 1 2}"
L2=0.075
EPOCHS=10
HEAD_K=8
STEP_SIZE=0.00025
SPLIT=0.80
COLS=prompt,prompt_es,prompt_de
CONDS_IDIOMA="prompt_es:0,prompt_es:1,prompt_de:0,prompt_de:1,prompt:0,prompt:1"
CKPT=lang_patch_best_train.pt
T=attributes/french/targets_french_v5.csv
T_OPEN=attributes/french/targets_open.csv
T_OPEN2=attributes/french/targets_open_2.csv

R=algebra/runs
P_FR=$R/alg_fr/$CKPT
P_FR_S1=$R/alg_fr_s1/$CKPT
P_ES=$R/alg_es/$CKPT
P_DE=$R/alg_de/$CKPT
Q3=$R/pos_q3
H3=$R/pos_h3
OUT=$R/paper_v7

for f in "$T" "$T_OPEN" "$T_OPEN2" "$P_FR" "$P_FR_S1" "$P_ES" "$P_DE"; do
  [[ -f "$f" ]] || { echo "falta $f"; exit 1; }
done
has() { [[ " $STAGES " == *" $1 "* ]]; }

# detector de idioma (lang_id.py): se carga ACA para fallar antes de entrenar, no en la primera eval
python3 -c "import json, lang_id; print('detector de idioma:', json.dumps(lang_id.descripcion()))"
mkdir -p "$OUT/resta" "$OUT/tests"

# --- grillas de entrada_o_directiva.py ---------------------------------------
RESTA="plain:prompt_fr:fr:-1,plain:prompt_fr:es:-1,plain:prompt_fr:de:-1,plain:prompt_fr:fr_s1:-1"
RESTA="$RESTA,plain:prompt_fr:q3:-1,plain:prompt_fr:q3:-2,plain:prompt_fr:h3:-1"
for s in $RAND_SEEDS; do RESTA="$RESTA,plain:prompt_fr:rand$s:-1"; done

# los tres parches y el azar de cada uno (misma forma, norma y anchor)
PAR="fr q3 h3 rand0 rand0_q3 rand0_h3"
grid() {   # grid <plantilla> <col> <escala> <parches...>
  local tpl=$1 col=$2 a=$3; shift 3
  local out="$tpl:$col:-:0" p
  for p in "$@"; do out="$out,$tpl:$col:$p:$a"; done
  echo "$out"
}
IDIOMA_ENTRADA="$(grid lang_id prompt 1 $PAR es),lang_id:prompt_fr:-:0,lang_id:prompt_es:-:0"
IDIOMA_ENTRADA="$IDIOMA_ENTRADA,$(grid lang_id_b prompt 1 $PAR es),lang_id_b:prompt_fr:-:0"
RESTA_DIRECTIVA="$(grid instr_fr prompt -1 $PAR es)"
CONFLICTO="instr_en:prompt_fr:-:0,$(grid instr_en prompt 1 $PAR),$(grid plain prompt 1 fr q3 h3)"

eod() {   # eod <q3.pt> <h3.pt> <n> <tag> <conds> <out_dir> [--dry]
  local q3=$1 h3=$2 n=$3 tag=$4 conds=$5 dir=$6; shift 6
  python3 -u entrada_o_directiva.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
      --train_test_split $SPLIT --n "$n" --rand_like fr \
      --patch "fr=$P_FR" --patch "fr_s1=$P_FR_S1" --patch "es=$P_ES" --patch "de=$P_DE" \
      --patch "q3=$q3@goal" --patch "h3=$h3@header" \
      --conds "$conds" --tag "$tag" --out_dir "$dir" "$@"
}
eod_all() {   # eod_all <q3.pt> <h3.pt> <n> <resta_dir> <tests_dir> [--dry]: las cuatro grillas
  local q3=$1 h3=$2 n=$3 rd=$4 td=$5; shift 5
  eod "$q3" "$h3" "$n" resta_q_fr "$RESTA" "$rd" "$@"
  eod "$q3" "$h3" "$n" idioma_entrada "$IDIOMA_ENTRADA" "$td" "$@"
  eod "$q3" "$h3" "$n" resta_directiva "$RESTA_DIRECTIVA" "$td" "$@"
  eod "$q3" "$h3" "$n" conflicto "$CONFLICTO" "$td" "$@"
}

train_one() {   # train_one <out_dir> <anchor> [targets epochs batch steps val_n]
  local out=$1 anchor=$2 t=${3:-$T} ep=${4:-$EPOCHS} bs=${5:-32} st=${6:-20} vn=${7:-20}
  if [[ "${SKIP_TRAIN:-0}" == "1" && -f "$out/$CKPT" ]]; then echo "ya entrenado: $out"; return; fi
  mkdir -p "$out"
  python3 -u train_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$t" \
      --l2_weight $L2 --output_dir "$out" --batch_size "$bs" --num_steps_per_prompt "$st" \
      --num_epochs "$ep" --step_decay cosine --val_n "$vn" --save_best --train_test_split $SPLIT \
      --loss_head_k $HEAD_K --prompt_cols $COLS --step_size $STEP_SIZE \
      --patch_anchor "$anchor" --num_patch_positions 3 --attr_name fr \
      2>&1 | tee "$out/train.log"
}

# =============================================================================
# 0. validacion inicial: si algo falla, set -e corta aca y no corre ninguna etapa
# =============================================================================
PF=$OUT/_preflight
rm -rf "$PF"; mkdir -p "$PF/tests" "$PF/resta" "$PF/repro"
echo; echo "################ 0a validacion: entorno, modelo, datos, parches"
PF_PATCH=(--patch "fr=$P_FR:1" --patch "fr_s1=$P_FR_S1:1" --patch "es=$P_ES:1" --patch "de=$P_DE:1")
for x in "q3=$Q3" "h3=$H3"; do   # si ya existen (SKIP_TRAIN), tambien se validan
  [[ -f "${x#*=}/$CKPT" ]] && PF_PATCH+=(--patch "${x%%=*}=${x#*=}/$CKPT:3")
done
python3 -u preflight_paper_v7.py env --model "$MODEL" --device "$DEVICE" "${PF_PATCH[@]}" \
    --smoke_dir "$PF" 2>&1 | tee "$PF/env.log"

echo; echo "################ 0b validacion: tramos y anchors (solo tokenizer)"
eod_all "$PF/q3/$CKPT" "$PF/h3/$CKPT" 3 "$PF/resta" "$PF/tests" --dry 2>&1 | tee "$PF/dry.log"

echo; echo "################ 0c validacion: humo de entrenamiento (Question-3, Header-3)"
( SKIP_TRAIN=0; train_one "$PF/q3" goal "$PF/targets_smoke.csv" 1 8 2 2
                train_one "$PF/h3" header "$PF/targets_smoke.csv" 1 8 2 2 )

echo; echo "################ 0d validacion: humo de evals"
for x in "q3:goal" "h3:header"; do
  r=${x%%:*} a=${x#*:}
  C=(--model "$MODEL" --device "$DEVICE" --patch "$PF/$r/$CKPT" --patch_anchor "$a"
     --num_patch_positions 3 --target_lang fr --cell_metrics --targets "$T" --train_test_split $SPLIT --n 2)
  python3 -u eval_lang_patch.py "${C[@]}" --out_json "$PF/$r/eval_best_train.json" \
      --out_md "$PF/$r/eval_best_train.md" 2>&1 | tee "$PF/$r/eval.log"
  python3 -u cross_lang_patch.py "${C[@]}" --conds "$CONDS_IDIOMA" --tag idioma \
      --out_dir "$PF/$r" 2>&1 | tee "$PF/$r/idioma.log"
done

echo; echo "################ 0e validacion: humo de resta y tests (2 filas, todas las condiciones)"
eod_all "$PF/q3/$CKPT" "$PF/h3/$CKPT" 2 "$PF/tests" "$PF/tests" 2>&1 | tee "$PF/eod.log"

echo; echo "################ 0f validacion: reproduccion de alg_fr (5 preguntas)"
python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --patch "$P_FR" \
    --patch_anchor goal_all --num_patch_positions 1 --target_lang fr --cell_metrics \
    --targets "$T" --train_test_split $SPLIT --n 5 \
    --out_json "$PF/repro/eval_best_train.json" --out_md "$PF/repro/eval_best_train.md" \
    2>&1 | tee "$PF/repro/eval.log"

echo; echo "################ 0g validacion: chequeo de salidas"
python3 -u preflight_paper_v7.py outputs --smoke_dir "$PF" 2>&1 | tee "$PF/outputs.log"
echo; echo "################ VALIDACION INICIAL OK: sigue con STAGES=\"$STAGES\""

# =============================================================================
# B1 B2: train Question-3 y Header-3
# =============================================================================
if has train; then
  echo; echo "################ B1 train Question-3"; train_one "$Q3" goal
  echo; echo "################ B2 train Header-3";   train_one "$H3" header
fi

# =============================================================================
# B3 B8: las cinco evals
# =============================================================================
eval_five() {   # eval_five <run_dir> <anchor> <npos>
  local o=$1 anchor=$2 npos=$3
  local p="$o/$CKPT"
  [[ -f "$p" ]] || { echo "falta $p (correr la etapa train)"; exit 1; }
  mkdir -p "$o/open_2"
  local C=(--model "$MODEL" --device "$DEVICE" --patch "$p" --patch_anchor "$anchor"
           --num_patch_positions "$npos" --target_lang fr --cell_metrics)
  python3 -u eval_lang_patch.py "${C[@]}" --targets "$T" --train_test_split $SPLIT \
      --out_json "$o/eval_best_train.json" --out_md "$o/eval_best_train.md" 2>&1 | tee "$o/eval.log"
  python3 -u cross_lang_patch.py "${C[@]}" --targets "$T" --train_test_split $SPLIT \
      --conds "$CONDS_IDIOMA" --tag idioma --out_dir "$o" 2>&1 | tee "$o/idioma.log"
  python3 -u cross_lang_patch.py "${C[@]}" --targets "$T" --train_test_split $SPLIT \
      --preset romance --out_dir "$o" 2>&1 | tee "$o/romance.log"
  python3 -u eval_lang_patch.py "${C[@]}" --targets "$T_OPEN" --train_test_split 0 \
      --out_json "$o/eval_open.json" --out_md "$o/eval_open.md" 2>&1 | tee "$o/eval_open.log"
  python3 -u cross_lang_patch.py "${C[@]}" --targets "$T_OPEN2" --train_test_split 0 \
      --conds "$CONDS_IDIOMA" --tag idioma --out_dir "$o/open_2" 2>&1 | tee "$o/open_2/idioma.log"
}
if has eval; then
  echo; echo "################ B3 eval Question-3"; eval_five "$Q3" goal 3
  echo; echo "################ B3 eval Header-3";   eval_five "$H3" header 3
  echo; echo "################ B8 eval alg_fr_s1";  eval_five "$R/alg_fr_s1" goal_all 1
fi

# =============================================================================
# B4 B5 (+ resta de B8): q_fr - v, todo en una tabla
# =============================================================================
for f in "$Q3/$CKPT" "$H3/$CKPT"; do
  if (has resta || has tests) && [[ ! -f "$f" ]]; then echo "falta $f (correr la etapa train)"; exit 1; fi
done
if has resta; then
  echo; echo "################ B4 B5 resta sobre q_fr"
  eod "$Q3/$CKPT" "$H3/$CKPT" "$N" resta_q_fr "$RESTA" "$OUT/resta" 2>&1 | tee "$OUT/resta/resta_q_fr.log"
fi

# =============================================================================
# B6 B7: entrada o directiva con Shared, Question-3 y Header-3
# =============================================================================
if has tests; then
  for t in idioma_entrada resta_directiva conflicto; do
    case $t in
      idioma_entrada)  c="$IDIOMA_ENTRADA" ;;
      resta_directiva) c="$RESTA_DIRECTIVA" ;;
      conflicto)       c="$CONFLICTO" ;;
    esac
    echo; echo "################ B6 B7 $t"
    eod "$Q3/$CKPT" "$H3/$CKPT" "$N" "$t" "$c" "$OUT/tests" 2>&1 | tee "$OUT/tests/$t.log"
  done
fi

echo
echo "Listo. Reportes:"
echo "  $Q3/*.md  $H3/*.md  $R/alg_fr_s1/*.md         (cinco evals)"
echo "  $OUT/resta/entrada_o_directiva_resta_q_fr.md   (q_fr - v, con controles)"
echo "  $OUT/tests/entrada_o_directiva_{idioma_entrada,resta_directiva,conflicto}.md"
