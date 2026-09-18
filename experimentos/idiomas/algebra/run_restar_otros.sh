#!/usr/bin/env bash
# Control de la resta: pregunta en FRANCES menos OTRA direccion de idioma.
#
#     M(q_fr - v_es)      M(q_fr - v_de)       held-out, idx 200..249
#
# run_restar_fr.sh mostro que q_fr - v_fr saca del frances (0.90 -> 0.12). Si
# eso es especifico de la direccion francesa, restar v_es o v_de (misma receta,
# norma parecida: 0.87 / 0.85) NO deberia sacar del frances, o bastante menos.
# Si lo saca igual, lo que hace la resta es quitar el componente comun c
# ("salir del modo por defecto"), no algo del frances.
#
#   uso (desde cualquier lado):  bash algebra/run_restar_otros.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  CELLS ("es de")  SCALES ("-1")
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

MODEL="${1:-/teamspace/studios/this_studio/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
CELLS="${CELLS:-es de}"
SCALES="${SCALES:--1}"
T=attributes/french/targets_french_v5.csv

CONDS="prompt_fr:0"
for a in $SCALES; do CONDS="$CONDS,prompt_fr:$a"; done

for cell in $CELLS; do
  P="algebra/runs/alg_$cell/lang_patch_best_train.pt"
  OUT="algebra/runs/alg_fr/restar_$cell"
  [[ -f "$P" ]] || { echo "falta $P"; exit 1; }
  mkdir -p "$OUT"
  echo; echo "################ q_fr - v_$cell"
  python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --targets "$T" \
      --patch "$P" --train_test_split 0.80 --patch_anchor goal_all --num_patch_positions 1 \
      --conds "$CONDS" --tag "restar_$cell" --out_dir "$OUT" 2>&1 | tee "$OUT/restar_$cell.log"
done

# tabla comparada con q_fr - v_fr (run_restar_fr.sh), si ya existe
echo
python3 - $CELLS <<'PY'
import json, os, sys
filas = [("fr", "algebra/runs/alg_fr/restar_fr/cross_lang_restar_fr.json")]
filas += [(c, f"algebra/runs/alg_fr/restar_{c}/cross_lang_restar_{c}.json") for c in sys.argv[1:]]
print(f"{'resta':<14}{'a':>5}{'fr':>7}{'es':>7}{'en':>7}{'de':>7}{'unk':>7}{'acc':>7}{'cambio':>8}{'largo':>7}{'ce_fr_h':>9}{'ce_en_h':>9}")
for cell, p in filas:
    if not os.path.exists(p):
        print(f"q_fr - v_{cell:<6} (sin correr)")
        continue
    for c in json.load(open(p, encoding="utf-8"))["condiciones"]:
        m = c["metrics"]
        nombre = "q_fr" if c["escala"] == 0 else f"q_fr - v_{cell}"
        print(f"{nombre:<14}{c['escala']:>5g}{m['p_fr']:>7.2f}{m['p_es']:>7.2f}{m['p_en']:>7.2f}{m['p_de']:>7.2f}"
              f"{m['p_unknown']:>7.2f}{m['answer_correct']:>7.2f}{m['cambio_vs_a0']:>8.2f}{m['len_media']:>7.0f}"
              f"{m['ce_fr_head']:>9.3f}{m['ce_en_head']:>9.3f}")
PY
echo
echo "Lectura: si con v_es / v_de el frances se queda cerca de 0.90, la resta de v_fr es especifica."
echo "Si cae igual, lo que se resta es el componente comun. Y mirar A DONDE va: con -v_es, deja de ir al espanol?"
