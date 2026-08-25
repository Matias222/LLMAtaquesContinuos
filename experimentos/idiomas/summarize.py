"""Junta los eval_report.json de los 3 barridos de L2 en una sola tabla."""

import glob
import json
import os
import sys

pattern = sys.argv[1] if len(sys.argv) > 1 else "runs/*/eval_report.json"
files = sorted(glob.glob(pattern))
if not files:
    sys.exit(f"sin reportes en {pattern}")

hdr = (f"{'run':<22}{'norma':>8}{'FR base':>9}{'FR ref':>9}{'FR patch':>10}"
       f"{'acc base':>10}{'acc ref':>9}{'acc patch':>11}{'leak':>7}{'dCE':>9}")
print(hdr)
print("-" * len(hdr))
for f in files:
    d = json.load(open(f))
    m = d["metrics"]
    name = os.path.basename(os.path.dirname(f))
    print(f"{name:<22}{d['patch_norm']:>8.3f}"
          f"{m['baseline']['is_french']:>9.0%}{m['reference']['is_french']:>9.0%}"
          f"{m['patched']['is_french']:>10.0%}"
          f"{m['baseline']['answer_correct']:>10.0%}{m['reference']['answer_correct']:>9.0%}"
          f"{m['patched']['answer_correct']:>11.0%}"
          f"{m['patched'].get('role_leak', 0):>7.0%}"
          f"{m['nll_fr_patched'] - m['nll_fr_baseline']:>+9.3f}")
print()
print("Lectura:")
print("  FR patch vs FR ref  -> cuanta compliance recupera el parche respecto del techo")
print("  acc patch vs acc ref-> si el parche degrada MAS que la instruccion en texto")
print("  dCE < 0             -> el parche acerca el modelo al frances de referencia")
