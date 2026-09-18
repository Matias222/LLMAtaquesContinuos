#!/usr/bin/env bash
# ¿El parche goal_all falsifica una PROPIEDAD DE LA ENTRADA (el idioma de la
# pregunta) o es una DIRECTIVA sobre la salida? Ver entrada_o_directiva.py.
#
#   idioma_entrada   se le pregunta al modelo en que idioma esta q_en + v_fr
#   resta_directiva  "Answer this in French. q_en"  con  -v_fr  solo sobre q_en
#   conflicto        "Answer this in English." contra q_fr real y contra q_en + v_fr
#
# El parche cae SOLO sobre el tramo de la pregunta, no sobre la instruccion.
# Primero corre --dry (solo tokenizer) y aborta si los tramos no son estables.
#
#   uso (desde cualquier lado):  bash algebra/run_entrada_o_directiva.sh [MODEL_PATH]
#   variables:  DEVICE (cuda:0)
#               STAGES ("idioma_entrada resta_directiva conflicto")
#               N (0 = las 50 filas; p.ej. N=5 para humo)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

MODEL="${1:-/teamspace/studios/this_studio/modelos/Llama-3.2-3B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
STAGES="${STAGES:-idioma_entrada resta_directiva conflicto}"
N="${N:-0}"
T=attributes/french/targets_french_v5.csv
P_FR=algebra/runs/alg_fr/lang_patch_best_train.pt
P_ES=algebra/runs/alg_es/lang_patch_best_train.pt
OUT=algebra/runs/entrada_o_directiva
for f in "$P_FR" "$P_ES" "$T"; do [[ -f "$f" ]] || { echo "falta $f"; exit 1; }; done
mkdir -p "$OUT"

COMUN=(--model "$MODEL" --device "$DEVICE" --targets "$T" --train_test_split 0.80
       --patch "fr=$P_FR" --patch "es=$P_ES" --rand_like fr --n "$N" --out_dir "$OUT")

for s in $STAGES; do
    echo; echo "##### $s: tramos (dry)"
    python3 -u entrada_o_directiva.py "${COMUN[@]}" --preset "$s" --dry
done

for s in $STAGES; do
    echo; echo "##### $s"
    python3 -u entrada_o_directiva.py "${COMUN[@]}" --preset "$s" 2>&1 | tee "$OUT/$s.log"
done

echo
echo "Reportes: $OUT/entrada_o_directiva_<preset>.md"
echo "idioma_entrada : 'lang_id | prompt +1*fr' dice French? (+1*es dice Spanish, +1*rand0 sigue en English)"
echo "resta_directiva: 'instr_fr | prompt -1*fr' conserva el frances (entrada) o cae como 'plain | prompt_fr -1*fr' (directiva)?"
echo "conflicto      : 'instr_en | prompt +1*fr' pierde contra la instruccion igual que 'instr_en | prompt_fr'?"
