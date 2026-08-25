"""Agrega el root del repo a sys.path para que `import llm_attacks` funcione
cuando estos scripts se corren desde dentro de legacy/.

Uso: `import _bootstrap` como primera linea de import del script.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
