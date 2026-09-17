#!/usr/bin/env bash
# Algebra de DIRECCIONES: idioma x formato.
#
# Seis parches, cada uno UN vector [1, 1, d] sumado a todos los tokens de la
# pregunta (anchor goal_all: una direccion del espacio de embeddings, no un soft
# prompt sobre posiciones fijas), entrenados por separado:
#
#               normal     MAYUSCULAS
#       fr      fr         fr_up
#       es      es         es_up
#       de      de         de_up
#
# y despues el test de function vectors / king - man + woman: esconder una
# esquina y reconstruirla con las otras tres,  v*_fr_up = v_fr + v_es_up - v_es.
# Ninguna celda es el baseline (ingles normal); ver algebra_patches.py.
#
# Receta = run_goal_all_v5.sh, con L2 0.075 y 10 epochs. Lo que cambia por celda:
#   - el target (columna `output` de su CSV, generado con la instruccion en texto)
#   - las ENTRADAS: multi-idioma como v5, pero sin el idioma target. Una pregunta
#     en espanol ya se contesta en espanol sin parche: para v_es esas filas no
#     tienen gradiente de idioma y la celda quedaria entrenada con 2 entradas
#     utiles contra 3 de v_fr.
#         fr, fr_up   prompt, prompt_es, prompt_de
#         es, es_up   prompt, prompt_de, prompt_fr
#         de, de_up   prompt, prompt_es, prompt_fr
#
# Etapas (STAGES):
#   targets  los CSV por celda que falten (algebra/targets/). Todos salen de los
#            MISMOS CSV base, asi las seis celdas comparten filas, orden y held-out.
#   train    los 6 parches + las replicas (mismo todo, otro orden de batches:
#            el techo de ruido contra el que se leen los cosenos del algebra)
#   eval     por parche, las mismas cinco de run_goal_all_v5.sh:
#              1. held-out ingles           -> eval_best_train.*
#              2. held-out, otros idiomas   -> cross_lang_idioma.*
#              3. held-out it / pt          -> cross_lang_romance.*
#              4. open 1 (99 de navidad)    -> eval_open.*
#              5. open 2 (imperativos)      -> open_2/cross_lang_idioma.*
#   plot     plot_last_token.py, SOLO para fr (sus referencias son de frances)
#   geom     algebra_patches.py: cosines (CPU) + eval + acts + embed
#
#   uso (desde cualquier lado):  bash algebra/run_algebra_v6.sh [MODEL_PATH]
#   variables:
#     DEVICE (cuda:0)  L2 (0.075)  EPOCHS (10)  HEAD_K (8)  STEP_SIZE (0.00025)
#     BATCH (32)  STEPS (20)
#     CELLS    ("fr es de fr_up es_up de_up")   celdas a entrenar / evaluar
#     REPLICAS ("fr es_up")                     celdas con replica ("" = ninguna)
#     STAGES   ("targets train eval plot geom")
#     SKIP_TRAIN=1   no reentrenar celdas que ya tienen su parche
#     ALPHAS   ("")  escalas extra sobre v* en el algebra, p.ej. "0.75,1.25"
#     EXTRA_PLOT_PATCHES ("")  mas --patch nombre=ruta para plot_last_token
#     SMOKE=1  recorrido de humo: 20 filas, 1 epoch, 2 steps, 4 filas por eval,
#              todo en algebra/targets_smoke y algebra/runs_smoke
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."                      # experimentos/idiomas: los scripts importan lm, checkers, ...

MODEL="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
L2="${L2:-0.075}"
EPOCHS="${EPOCHS:-10}"
HEAD_K="${HEAD_K:-8}"
STEP_SIZE="${STEP_SIZE:-0.00025}"
BATCH="${BATCH:-32}"
STEPS="${STEPS:-20}"
CELLS="${CELLS:-fr es de fr_up es_up de_up}"
REPLICAS="${REPLICAS-fr es_up}"
STAGES="${STAGES:-targets train eval plot geom}"
ALPHAS="${ALPHAS:-}"
EXTRA_PLOT_PATCHES="${EXTRA_PLOT_PATCHES:-}"
SPLIT=0.80
ANCHOR=goal_all
NPOS=1
CKPT=lang_patch_best_train.pt

BASE=attributes/french/targets_french_v5.csv
BASE_OPEN=attributes/french/targets_open.csv
BASE_OPEN2_SRC=attributes/french/targets_open_2.csv
TDIR=algebra/targets
RUNS=algebra/runs
NLIM=()                              # --n de las evals (solo humo)
if [[ "${SMOKE:-0}" == "1" ]]; then
  TDIR=algebra/targets_smoke; RUNS=algebra/runs_smoke
  EPOCHS=1; STEPS=2; NLIM=(--n 4)
  echo "### SMOKE: 20 filas, 1 epoch, $STEPS steps/batch, 4 filas por eval -> $TDIR  $RUNS"
fi
BASE_OPEN2="$TDIR/base_open_2.csv"   # open_2 + prompt_fr (las celdas es/de entran desde frances)
mkdir -p "$TDIR" "$RUNS"

for f in "$BASE" "$BASE_OPEN" "$BASE_OPEN2_SRC"; do [[ -f "$f" ]] || { echo "falta $f"; exit 1; }; done
has() { [[ " $STAGES " == *" $1 "* ]]; }

# --- configuracion por celda -------------------------------------------------
# deja en variables: LANG_ UP_ (flag o vacio) COLS T T_OPEN T_OPEN2 CONDS
cell_cfg() {
  local cell="$1"
  LANG_="${cell%_up}"
  UP_=(); [[ "$cell" == *_up ]] && UP_=(--upper)
  case "$LANG_" in
    fr) COLS=prompt,prompt_es,prompt_de
        CONDS="prompt_es:0,prompt_es:1,prompt_de:0,prompt_de:1,prompt:0,prompt:1" ;;
    es) COLS=prompt,prompt_de,prompt_fr
        CONDS="prompt_de:0,prompt_de:1,prompt_fr:0,prompt_fr:1,prompt:0,prompt:1" ;;
    de) COLS=prompt,prompt_es,prompt_fr
        CONDS="prompt_es:0,prompt_es:1,prompt_fr:0,prompt_fr:1,prompt:0,prompt:1" ;;
    *)  echo "celda desconocida: $cell"; exit 1 ;;
  esac
  if [[ "$cell" == "fr" && "${SMOKE:-0}" != "1" ]]; then
    # frances normal: los targets de siempre, sin regenerar nada
    T="$BASE"; T_OPEN="$BASE_OPEN"; T_OPEN2="$BASE_OPEN2_SRC"
  else
    T="$TDIR/targets_$cell.csv"; T_OPEN="$TDIR/targets_${cell}_open.csv"; T_OPEN2="$TDIR/targets_${cell}_open_2.csv"
  fi
}

# =============================================================================
# 1. targets
# =============================================================================
if has targets; then
  if [[ ! -f "$BASE_OPEN2" ]]; then
    python3 -u translate_questions.py --model "$MODEL" --device "$DEVICE" --lang fr \
        --targets "$BASE_OPEN2_SRC" --out "$BASE_OPEN2" 2>&1 | tee "$TDIR/base_open_2.log"
  fi
  for cell in $CELLS; do
    cell_cfg "$cell"
    [[ "$T" == "$BASE" ]] && continue
    GEN_N=(); [[ "${SMOKE:-0}" == "1" ]] && GEN_N=(--n 20)
    for par in "$BASE|$T" "$BASE_OPEN|$T_OPEN" "$BASE_OPEN2|$T_OPEN2"; do
      src="${par%%|*}"; dst="${par##*|}"
      [[ -f "$dst" ]] && { echo "ya existe $dst"; continue; }
      python3 -u algebra/generate_targets_attr.py --model "$MODEL" --device "$DEVICE" \
          --lang "$LANG_" ${UP_[@]+"${UP_[@]}"} --base_csv "$src" --out "$dst" ${GEN_N[@]+"${GEN_N[@]}"} \
          2>&1 | tee "${dst%.csv}.log"
    done
  done
fi

# =============================================================================
# 2. train   (6 celdas + replicas)
# =============================================================================
train_one() {   # train_one <celda> <out_dir> [args extra de train_lang_patch]
  local cell="$1" out="$2"; shift 2
  cell_cfg "$cell"
  [[ -f "$T" ]] || { echo "falta $T (correr la etapa targets)"; exit 1; }
  if [[ "${SKIP_TRAIN:-0}" == "1" && -f "$out/$CKPT" ]]; then echo "ya entrenado: $out"; return; fi
  mkdir -p "$out"
  python3 -u train_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
      --l2_weight "$L2" --output_dir "$out" --batch_size "$BATCH" --num_steps_per_prompt "$STEPS" \
      --num_epochs "$EPOCHS" --step_decay cosine --val_n 20 --save_best --train_test_split $SPLIT \
      --loss_head_k "$HEAD_K" --prompt_cols "$COLS" --step_size "$STEP_SIZE" \
      --patch_anchor $ANCHOR --num_patch_positions $NPOS --attr_name "$cell" "$@" \
      2>&1 | tee "$out/train.log"
}

if has train; then
  for cell in $CELLS; do train_one "$cell" "$RUNS/alg_$cell"; done
  for cell in $REPLICAS; do train_one "$cell" "$RUNS/alg_${cell}_s1" --shuffle_seed 1; done
fi

# =============================================================================
# 3. eval   (las cinco de run_goal_all_v5.sh, por celda)
# =============================================================================
if has eval; then
  for cell in $CELLS; do
    cell_cfg "$cell"
    OUT="$RUNS/alg_$cell"; P="$OUT/$CKPT"; mkdir -p "$OUT/open_2"
    [[ -f "$P" ]] || { echo "falta $P (correr la etapa train)"; exit 1; }
    COMMON=(--model "$MODEL" --device "$DEVICE" --patch "$P" --patch_anchor $ANCHOR
            --num_patch_positions $NPOS --target_lang "$LANG_" --cell_metrics ${UP_[@]+"${UP_[@]}"} ${NLIM[@]+"${NLIM[@]}"})
    echo; echo "################ eval $cell"

    # 1. held-out ingles
    python3 -u eval_lang_patch.py "${COMMON[@]}" --targets "$T" --train_test_split $SPLIT \
        --out_json "$OUT/eval_best_train.json" --out_md "$OUT/eval_best_train.md" 2>&1 | tee "$OUT/eval.log"

    # 2. held-out desde los otros idiomas de entrada (y el ingles, en el mismo run)
    python3 -u cross_lang_patch.py "${COMMON[@]}" --targets "$T" --train_test_split $SPLIT \
        --conds "$CONDS" --tag idioma --out_dir "$OUT" 2>&1 | tee "$OUT/idioma.log"

    # 3. held-out it / pt (idiomas de entrada que ninguna celda vio)
    python3 -u cross_lang_patch.py "${COMMON[@]}" --targets "$T" --train_test_split $SPLIT \
        --preset romance --out_dir "$OUT" 2>&1 | tee "$OUT/romance.log"

    # 4. open 1: los 99 prompts de navidad, todos held-out
    python3 -u eval_lang_patch.py "${COMMON[@]}" --targets "$T_OPEN" --train_test_split 0 \
        --out_json "$OUT/eval_open.json" --out_md "$OUT/eval_open.md" 2>&1 | tee "$OUT/eval_open.log"

    # 5. open 2: imperativos, todos held-out
    python3 -u cross_lang_patch.py "${COMMON[@]}" --targets "$T_OPEN2" --train_test_split 0 \
        --conds "$CONDS" --tag idioma --out_dir "$OUT/open_2" 2>&1 | tee "$OUT/open_2/idioma.log"
  done
fi

# =============================================================================
# 4. plot_last_token: solo frances
# =============================================================================
if has plot && [[ " $CELLS " == *" fr "* ]]; then
  cell_cfg fr
  OUT="$RUNS/alg_fr"
  PLOT_N=(--subset heldout --n 50); [[ "${SMOKE:-0}" == "1" ]] && PLOT_N=(--subset all --n 6)
  EXTRA=(); for e in $EXTRA_PLOT_PATCHES; do EXTRA+=(--patch "$e"); done
  python3 -u plot_last_token.py compute --model "$MODEL" --device "$DEVICE" --targets "$T" \
      --train_test_split $SPLIT ${PLOT_N[@]+"${PLOT_N[@]}"} --patch "alg_fr=$OUT/$CKPT" ${EXTRA[@]+"${EXTRA[@]}"} \
      --out "$OUT/geom_last_token/heldout.json" 2>&1 | tee "$OUT/geom_last_token.log"
  python3 plot_last_token.py plot "$OUT/geom_last_token/heldout.json"
fi

# =============================================================================
# 5. geometria / algebra
# =============================================================================
if has geom; then
  GEO="$RUNS/geometria"; mkdir -p "$GEO"
  cell_cfg fr; T_FR="$T"
  CSV_CELLS="$(echo $CELLS | tr ' ' ',')"
  ALG=(--cells "$CSV_CELLS" --runs_dir "$RUNS" --ckpt "$CKPT" --out_dir "$GEO")
  GPU=(--model "$MODEL" --device "$DEVICE" --targets_dir "$TDIR" --targets_csv "fr=$T_FR"
       --train_test_split $SPLIT ${NLIM[@]+"${NLIM[@]}"})
  REP=()
  for cell in $REPLICAS; do
    if [[ -f "$RUNS/alg_${cell}_s1/$CKPT" ]]; then REP+=(--replica "$cell=$RUNS/alg_${cell}_s1/$CKPT"); fi
  done

  python3 algebra/algebra_patches.py cosines "${ALG[@]}" ${REP[@]+"${REP[@]}"} 2>&1 | tee "$GEO/cosines.log"
  python3 -u algebra/algebra_patches.py eval "${ALG[@]}" "${GPU[@]}" ${ALPHAS:+--alphas "$ALPHAS"} \
      2>&1 | tee "$GEO/algebra_eval.log"
  python3 -u algebra/algebra_patches.py acts "${ALG[@]}" "${GPU[@]}" 2>&1 | tee "$GEO/algebra_acts.log"
  python3 -u algebra/algebra_patches.py embed "${ALG[@]}" "${GPU[@]}" 2>&1 | tee "$GEO/algebra_embed.log"
fi

# =============================================================================
# resumen
# =============================================================================
echo
echo "======================================================================"
echo "RESUMEN por celda  (celda_ok del parche; '-' = todavia no corrio)"
python3 - "$RUNS" $CELLS <<'PY'
import json, os, sys
runs, cells = sys.argv[1], sys.argv[2:]
def get(path, *keys):
    try:
        d = json.load(open(path, encoding="utf-8"))
        for k in keys:
            d = d[k]
        return d
    except Exception:
        return None
def fmt(x):
    return "   -  " if x is None else f"{x:6.2f}"
print(f"{'celda':<8}{'norma':>8}{'held-out':>10}{'open 1':>8}{'open 2 (en)':>13}")
flojas = []
for c in cells:
    o = os.path.join(runs, f"alg_{c}")
    ho = get(os.path.join(o, "eval_best_train.json"), "metrics", "patched")
    op = get(os.path.join(o, "eval_open.json"), "metrics", "patched")
    key = "attr_ok" if ho and "attr_ok" in ho else "is_french"      # fr normal: el reporte de siempre
    o2 = get(os.path.join(o, "open_2", "cross_lang_idioma.json"), "condiciones") or []
    o2 = next((r["metrics"].get("attr_ok") for r in o2 if r["label"] == "prompt a=1"), None)
    h = ho[key] if ho else None
    print(f"{c:<8}{fmt(get(os.path.join(o, 'eval_best_train.json'), 'patch_norm')):>8}{fmt(h):>10}"
          f"{fmt(op[key] if op else None):>8}{fmt(o2):>13}")
    if h is not None and h < 0.80:
        flojas.append(c)
if flojas:
    print(f"\nAVISO: {', '.join(flojas)} < 0.80 en held-out. Los paralelogramos que usan esas celdas no son")
    print("interpretables: si el parche entrenado directo no llega, su reconstruccion tampoco tiene techo.")
PY
echo
echo "Por celda:   $RUNS/alg_<celda>/{eval_best_train,cross_lang_idioma,cross_lang_romance,eval_open}.md  y  open_2/"
echo "Frances:     $RUNS/alg_fr/geom_last_token/"
echo "Algebra:     $RUNS/geometria/{cosines,algebra_eval,algebra_acts,algebra_embed}.md"
