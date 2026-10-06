#!/usr/bin/env bash
# Resta completa para la seccion 4.3 del paper: M(q_L - v_P) sobre el held-out.
#
#   filas     idioma de la pregunta L = fr, es, de (prompt_fr / prompt_es / prompt_de)
#   columnas  vector restado P = v_fr, v_es, v_de, y 3 vectores al azar con la
#             norma de v_L (rand0_L, rand1_L, rand2_L)
#
# La diagonal (q_L - v_L) es el test; fuera de la diagonal y el azar son los
# controles. Sin parche el modelo contesta en el idioma de la pregunta. Hasta
# ahora solo existia la fila de frances (algebra/run_restar_fr.sh y
# run_restar_otros.sh, via cross_lang_patch) y nunca se habia corrido el azar
# sobre q_fr. Con la plantilla `plain` el tramo parcheado es la pregunta entera,
# igual que goal_all en cross_lang_patch: la fila de frances reproduce
# restar_fr (0.90 -> 0.12).
#
# Control extra: el parche de 3 posiciones sobre la pregunta (Question-3),
# restado de q_fr con a = -1 y -2. Por defecto el que existe
# (runs/v5_head_multi_l2_0.0725, OTRA receta); pasar Q3=... con el reentrenado.
#
# Despues correr `python3 recompute_accuracy.py` para la accuracy con los alias
# de attributes/heldout_aliases.csv.
#
#   uso (desde cualquier lado):  bash algebra/run_restar_matriz.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)  N (0 = las 50 filas; N=5 para humo)
#               LANGS ("fr es de")  filas a correr. LANGS="es de" deja afuera la de
#                     frances, que run_paper_v7.sh ya corre (mismo azar: misma semilla y norma)
#               Q3 (runs/v5_head_multi_l2_0.0725/lang_patch_best_train.pt; "" = sin Q3)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

MODEL="${1:-/teamspace/studios/this_studio/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
N="${N:-0}"
LANGS="${LANGS:-fr es de}"
Q3="${Q3-runs/v5_head_multi_l2_0.0725/lang_patch_best_train.pt}"
T=attributes/french/targets_french_v5.csv
OUT=algebra/runs/restar_matriz
mkdir -p "$OUT"

# detector de idioma (lang_id.py): se carga ACA para fallar antes de entrenar, no en la primera eval
python3 -c "import json, lang_id; print('detector de idioma:', json.dumps(lang_id.descripcion()))"

PATCHES=()
for L in fr es de; do
  P="algebra/runs/alg_$L/lang_patch_best_train.pt"
  [[ -f "$P" ]] || { echo "falta $P"; exit 1; }
  PATCHES+=(--patch "$L=$P")
done

CONDS=""
for L in $LANGS; do
  CONDS+="plain:prompt_$L:-:0,"
  for P in fr es de rand0_$L rand1_$L rand2_$L; do CONDS+="plain:prompt_$L:$P:-1,"; done
done
if [[ -n "$Q3" ]]; then
  [[ -f "$Q3" ]] || { echo "falta $Q3"; exit 1; }
  PATCHES+=(--patch "q3=$Q3@goal")
  CONDS+="plain:prompt_fr:q3:-1,plain:prompt_fr:q3:-2,"
fi
CONDS="${CONDS%,}"

COMUN=(--model "$MODEL" --device "$DEVICE" --targets "$T" --train_test_split 0.80
       "${PATCHES[@]}" --n "$N" --conds "$CONDS" --tag restar_matriz --out_dir "$OUT")

echo "##### tramos (dry)"
python3 -u entrada_o_directiva.py "${COMUN[@]}" --dry
echo; echo "##### resta"
python3 -u entrada_o_directiva.py "${COMUN[@]}" 2>&1 | tee "$OUT/restar_matriz.log"

echo
echo "Reporte: $OUT/entrada_o_directiva_restar_matriz.md"
echo "Despues:  python3 recompute_accuracy.py   (accuracy con alias en todos los idiomas)"
