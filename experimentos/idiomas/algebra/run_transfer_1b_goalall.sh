#!/usr/bin/env bash
# Transferencia del parche goal_all de FRANCES del 3B al 1B por Procrustes
# ortogonal (transfer_patch.py), evaluada EN EL 1B sobre held-out y open 1.
#
#   v_1B = v_3B W        W [3072, 2048] ajustado sobre los 128k tokens compartidos
#
# Tres lecturas, de la mas sensible a la mas exigente:
#   lang_id   el 1B DICE que q_en + a*v_1B esta en frances? (entrada_o_directiva.py)
#   heldout   el 1B CONTESTA en frances las 50 preguntas del tail?
#   open      idem sobre los 99 prompts abiertos
# Todas con barrido de a y, al lado, el CONTROL: el mismo v_3B por un mapa
# ortogonal al azar (misma norma, ninguna alineacion entre modelos). a=0 es el
# 1B sin parche, generado en la corrida (el baseline del CSV es del 3B).
#
# OJO: ce_fr_h / ce_en_h se miden contra los targets del CSV, que escribio el
# 3B. Sirven para comparar condiciones dentro del 1B, no contra el 3B.
#
#   uso:  bash algebra/run_transfer_1b_goalall.sh [MODEL_3B] [MODEL_1B]
#   variables:  DEVICE (cuda:0)   ALPHAS ("1 1.5 2 3")   N (0 = todo; 5 = humo)
#               STAGES ("map lang_id heldout open")
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

M3="${1:-/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct}"
M1="${2:-$(dirname "$M3")/Llama-3.2-1B-Instruct}"
DEVICE="${DEVICE:-cuda:0}"
ALPHAS="${ALPHAS:-1 1.5 2 3}"
STAGES="${STAGES:-map lang_id heldout open}"
N="${N:-0}"
SRC=algebra/runs/alg_fr/lang_patch_best_train.pt
T=attributes/french/targets_french_v5.csv
T_OPEN=attributes/french/targets_open.csv
OUT=algebra/runs/transfer_1b_fr
P="$OUT/lang_patch.pt"; C="$OUT/control_patch.pt"
for f in "$SRC" "$T" "$T_OPEN"; do [[ -f "$f" ]] || { echo "falta $f"; exit 1; }; done
[[ -d "$M1" ]] || { echo "no encuentro el 1B en $M1 (pasarlo como 2do argumento)"; exit 1; }
mkdir -p "$OUT/mapeado" "$OUT/control"
has() { [[ " $STAGES " == *" $1 "* ]]; }

if has map; then
  echo "##### mapa 3072 -> 2048"
  python3 -u transfer_patch.py --source "$M3" --target "$M1" --device "$DEVICE" \
      --patch "$SRC" --out "$P" 2>&1 | tee "$OUT/transfer.log"
  echo; echo "##### control: mapa ortogonal al azar"
  python3 -u transfer_patch.py --source "$M3" --target "$M1" --device "$DEVICE" --control --force \
      --patch "$SRC" --out "$C" 2>&1 | tee "$OUT/control.log"
fi
for f in "$P" "$C"; do [[ -f "$f" ]] || { echo "falta $f (correr la etapa map)"; exit 1; }; done

if has lang_id; then
  CONDS="lang_id:prompt:-:0,lang_id:prompt_fr:-:0"
  for a in $ALPHAS; do CONDS="$CONDS,lang_id:prompt:fr:$a"; done
  for a in $ALPHAS; do CONDS="$CONDS,lang_id:prompt:ctrl:$a"; done
  ARGS=(--model "$M1" --device "$DEVICE" --targets "$T" --train_test_split 0.80 --n "$N"
        --patch "fr=$P" --patch "ctrl=$C" --conds "$CONDS" --tag lang_id_1b --out_dir "$OUT")
  echo; echo "##### lang_id en el 1B: tramos (dry)"
  python3 -u entrada_o_directiva.py "${ARGS[@]}" --dry
  echo; echo "##### lang_id en el 1B"
  python3 -u entrada_o_directiva.py "${ARGS[@]}" 2>&1 | tee "$OUT/lang_id_1b.log"
fi

CONDS="prompt:0"; for a in $ALPHAS; do CONDS="$CONDS,prompt:$a"; done
gen() {   # gen <heldout|open> <targets> <split>
  for par in "mapeado|$P" "control|$C"; do
    IFS='|' read -r nombre patch <<< "$par"
    echo; echo "##### $1 en el 1B: $nombre"
    python3 -u cross_lang_patch.py --model "$M1" --device "$DEVICE" --targets "$2" \
        --train_test_split "$3" --patch "$patch" --patch_anchor goal_all --num_patch_positions 1 \
        --conds "$CONDS" --tag "$1" --n "$N" --out_dir "$OUT/$nombre" 2>&1 | tee "$OUT/$nombre/$1.log"
  done
}
if has heldout; then gen heldout "$T" 0.80; fi
if has open;    then gen open "$T_OPEN" 0; fi

echo
echo "Reportes en $OUT:"
echo "  lang_patch_transfer.json            norma que sobrevive al mapa, roundtrip, normas de embedding"
echo "  entrada_o_directiva_lang_id_1b.md   el 1B dice French con +a*fr y sigue en English con +a*ctrl?"
echo "  mapeado/cross_lang_{heldout,open}.md  vs  control/cross_lang_{heldout,open}.md"
echo "Mirar fr Y acc juntos: en el intento viejo (v3_250) el frances aparecia a a=4 con accuracy 0.24."
