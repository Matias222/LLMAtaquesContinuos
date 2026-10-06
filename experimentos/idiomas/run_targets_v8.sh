#!/usr/bin/env bash
# Targets del banco de entrenamiento v8: 600 preguntas nuevas (data/banco_v8, 6
# categorias x 100) + las primeras 100 factuales del banco viejo, intercaladas
# por categoria (700 filas). Misma receta de targets que el paper: el modelo se
# genera su propia respuesta con la instruccion en texto, greedy, 100 tokens.
#
#   0. validacion: GlotLID cargable (los gates usan checkers.language_verdict),
#      banco v8 presente, CSV viejos presentes
#   1. armar    attributes/v8/targets_v8_fr.csv: las 100 viejas ENTERAS (targets,
#               traducciones y correcciones a mano) y las 600 nuevas con output vacio
#               y con las traducciones escritas a mano (data/banco_v8/traducciones)
#   2. fr       generate_targets.py --fill: M("Answer in French.\n\n" + q) y el
#               baseline en ingles, solo para las filas sin output. Gate: idioma y
#               accuracy (como siempre en fr)
#   3. trad     NO corre por defecto: translate_questions.py convierte imperativos,
#               fragmentos y marcos conversacionales en preguntas estandar (smoke del
#               2026-10-06). Las traducciones vienen del banco. Queda como etapa
#               opcional (STAGES=trad) solo para completar filas sin traduccion.
#   4. attr     algebra/generate_targets_attr.py --gate_accuracy: celdas es y de
#               sobre las 700 (en el smoke entraban targets en aleman con contenido
#               equivocado; ahora las nuevas tienen alias en 6 idiomas), y despues
#               las 100 viejas recuperan su output y su gate de algebra/targets/
#               (con las correcciones de fix_targets.py)
#   5. fix      fix_targets_v8.py: correcciones a mano (ingles entre parentesis en la
#               cabeza del target, la fuga del few-shot en el prompt_fr de "Which river
#               flows through Paris?"). Idempotente.
#   6. regate   preparar_targets_v8.py regate: alias del banco (ampliados tras revisar
#               las fallas a mano), veredicto GlotLID, accuracy y gate_v8 de las 600
#               nuevas: categorias 3 y 4 solo idioma; el resto accuracy; nunca
#               'unknown' ni ingles en la cabeza. Las 100 viejas no se tocan.
#   7. revisar  reporte por celda y categoria: gate, idioma, accuracy, traducciones
#               rechazadas y fugas del few-shot del traductor
#
#   uso (desde cualquier lado):  bash run_targets_v8.sh MODEL_PATH
#   variables:  DEVICE (cuda:0)
#               STAGES ("armar fr attr fix regate revisar")  etapas (trad es opcional)
#               SMOKE=1  2 filas por categoria (14), todo en attributes/v8_smoke
#               FORCE_ATTR=1  regenerar es/de aunque ya existan
#
# Es reanudable: fr y trad solo completan lo que falta, armar no pisa un CSV
# existente y attr se saltea si el CSV de la celda ya existe (FORCE_ATTR=1).
# Despues de correrlo: revisar a mano las traducciones rechazadas o con fuga
# (las lista la etapa revisar) antes de entrenar.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

MODEL="${1:?uso: bash run_targets_v8.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
STAGES="${STAGES:-armar fr attr fix regate revisar}"
OUT=attributes/v8
N_SMOKE=()
if [[ "${SMOKE:-0}" == "1" ]]; then
  OUT=attributes/v8_smoke; N_SMOKE=(--n 2)
  echo "### SMOKE: 2 filas por categoria -> $OUT"
fi
FR=$OUT/targets_v8_fr.csv
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$OUT"

# =============================================================================
# 0. validacion
# =============================================================================
echo "################ 0 validacion"
[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
for f in data/banco_v8/banco_v8_intercalado.csv attributes/french/targets_french_v5.csv \
         algebra/targets/targets_es.csv algebra/targets/targets_de.csv; do
  [[ -f "$f" ]] || { echo "falta $f"; exit 1; }
done
python3 - <<'PY'
from checkers import language_verdict
v = language_verdict("La capitale de la France est Paris.")
assert v == "fr", f"GlotLID no responde bien: {v!r}"
print("GlotLID ok")
PY

# =============================================================================
# 1. armar
# =============================================================================
if has armar; then
  echo; echo "################ 1 armar $FR"
  if [[ -f "$FR" ]]; then
    echo "ya existe $FR: no se rearma (borrarlo a mano para empezar de cero)"
  else
    python3 preparar_targets_v8.py armar --out "$FR" ${N_SMOKE[@]+"${N_SMOKE[@]}"} 2>&1 | tee "$OUT/armar.log"
  fi
fi

# =============================================================================
# 2. targets en frances (solo filas sin output)
# =============================================================================
if has fr; then
  echo; echo "################ 2 targets fr"
  python3 -u generate_targets.py --model "$MODEL" --device "$DEVICE" --fill "$FR" \
      2>&1 | tee "$OUT/targets_fr.log"
fi

# =============================================================================
# 3. traducciones de las nuevas
# =============================================================================
if has trad; then
  for L in es de fr; do
    echo; echo "################ 3 traduccion $L"
    python3 -u translate_questions.py --model "$MODEL" --device "$DEVICE" --targets "$FR" \
        --lang "$L" --only_missing 2>&1 | tee "$OUT/traduccion_$L.log"
  done
fi

# =============================================================================
# 4. celdas es / de
# =============================================================================
if has attr; then
  for L in es de; do
    T=$OUT/targets_v8_$L.csv
    echo; echo "################ 4 targets $L"
    if [[ -f "$T" && "${FORCE_ATTR:-0}" != "1" ]]; then
      echo "ya existe $T (FORCE_ATTR=1 para regenerar)"; continue
    fi
    python3 -u algebra/generate_targets_attr.py --model "$MODEL" --device "$DEVICE" \
        --lang "$L" --base_csv "$FR" --out "$T" --gate_accuracy 2>&1 | tee "$OUT/targets_$L.log"
    python3 preparar_targets_v8.py restaurar --lang "$L" --csv "$T" 2>&1 | tee -a "$OUT/targets_$L.log"
  done
fi

# =============================================================================
# 5. correcciones a mano y 6. gate final
# =============================================================================
if has fix; then
  echo; echo "################ 5 fix (correcciones a mano)"
  python3 fix_targets_v8.py --dir "$OUT" 2>&1 | tee "$OUT/fix.log"
fi
if has regate; then
  echo; echo "################ 6 regate"
  python3 preparar_targets_v8.py regate --dir "$OUT" 2>&1 | tee "$OUT/regate.log"
fi

# =============================================================================
# 7. reporte
# =============================================================================
if has revisar; then
  echo; echo "################ 5 revisar"
  python3 preparar_targets_v8.py revisar --dir "$OUT" 2>&1 | tee "$OUT/revisar.log"
fi

echo
echo "Listo: $OUT/targets_v8_{fr,es,de}.csv   (reporte: $OUT/revisar.log)"
