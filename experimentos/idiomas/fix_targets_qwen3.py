"""
Correcciones a mano de los targets de Qwen3-4B-Instruct-2507 (attributes/qwen3,
y = M(q_X) con las traducciones ya corregidas).

Mismo mecanismo y criterio que fix_targets_v10.py (Llama), con su propio JSON:
data/banco_v8/correcciones_qwen3.json = {celda: {pregunta en ingles: {"sha1_original",
"motivo", "output"}}}. Sin clave "_traducciones": las traducciones las aplica antes
run_targets_qwen3.sh (fix_targets_v10.py --solo_traducciones). Ademas de los errores
de contenido, de respuesta y de idioma, se quitan las aperturas de relleno ("¡Claro!",
"Bien sûr !", "Natürlich!", "¡Buena pregunta!").

    python3 fix_targets_qwen3.py --dir attributes/qwen3 [--dry_run]
"""
import sys

import fix_targets_v10

if __name__ == "__main__":
    if "--correcciones" not in sys.argv:
        sys.argv += ["--correcciones", "data/banco_v8/correcciones_qwen3.json"]
    fix_targets_v10.main()
