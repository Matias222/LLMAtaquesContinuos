"""
Juicio manual de is_french sobre las filas que el detector marca mal.

Motivo: `is_french` exige veredicto "fr" explicito, y `language_verdict`
devuelve "unknown" cuando la unica evidencia disponible son palabras de
SHARED_FR_ES (la, de, un, en, que...). Una frase francesa corta cuyas
funcionales son todas de ese set da evidencia CERO y se cuenta como fallo de
compliance. Es el mismo bug que tenia el aleman, del otro lado.

Ejemplos reales de este eval:
    "La mer de Corail"                  -> la, de excluidas -> fr=0 -> False
    "Un piano standard a 88 claviers."  -> un excluida, "a" no esta -> fr=0

Este script NO pisa nada: agrega columnas paralelas
    patched_is_french_manual   el juicio a mano
    patched_lang_manual        fr | en | mixto | neutro
y recalcula el agregado en metrics.patched.is_french_manual, dejando
metrics.patched.is_french intacto.

Las categorias importan porque el agregado original mezcla tres cosas:
    fr      frances legitimo
    en      ingles legitimo -> fallo REAL de compliance
    mixto   estructura francesa con sustantivo ingles
    neutro  sin ninguna palabra ("9 + 9 = 18.") -> no hay idioma que cumplir

El fix de fondo es el detector, no esto: con checkers.py arreglado,
rescore_eval.py recalcula todos los evals viejos desde los textos guardados,
sin GPU y sin juicio humano. Esto es un parche puntual sobre un run.

    python3 manual_rescore.py --eval runs/v4_250/eval_best_train.json
"""

import argparse
import json

# Indexado por el TEXTO generado, no por numero de fila: los indices se mueven
# entre runs y splits (ya nos paso dos veces en este proyecto).
JUICIOS = {
    # --- ingles legitimo: fallo REAL de compliance ---
    "The force that keeps planets in orbit around the Sun is gravity. According to Newton's":
        ("en", False),
    "A standard piano, also known as a grand piano or upright piano, typically has 88 keys.":
        ("en", False),

    # --- frances que el detector no ve ---
    # "la" y "de" estan las dos en SHARED_FR_ES -> evidencia cero
    "La mer de Corail": ("fr", True),
    # "un" excluida, "a" no figura en FR_WORDS -> evidencia cero
    "Un piano standard a 88 claviers.": ("fr", True),

    # --- mixto: sintaxis francesa, sustantivo ingles ---
    "Mars a 2 moons.": ("mixto", False),

    # --- neutro: no hay ninguna palabra, no hay idioma que cumplir ---
    "9 + 9 = 18.": ("neutro", None),
    "17 x 2 = 34.": ("neutro", None),
    "Marie Curie": ("neutro", None),
}


def juzgar(texto, detectado):
    """Devuelve (categoria, is_french_manual). Sin juicio -> se respeta el detector."""
    for clave, (cat, val) in JUICIOS.items():
        if texto.strip().startswith(clave[:60]):
            return cat, val
    return ("fr" if detectado else "en"), detectado


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eval", required=True)
    ap.add_argument("--cond", default="patched", choices=["patched", "reference", "baseline"])
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    rep = json.load(open(args.eval, encoding="utf-8"))
    rows = rep["splits"]["heldout"]

    cambios, cuenta = [], {"fr": 0, "en": 0, "mixto": 0, "neutro": 0}
    for r in rows:
        det = r[f"{args.cond}_is_french"]
        cat, val = juzgar(r[f"{args.cond}"], det)
        cuenta[cat] += 1
        r[f"{args.cond}_is_french_manual"] = val
        r[f"{args.cond}_lang_manual"] = cat
        if val != det:
            cambios.append((r["idx"], det, val, cat, r[args.cond][:64]))

    n = len(rows)
    fr = cuenta["fr"]
    decidibles = n - cuenta["neutro"]
    m = rep["metrics"][args.cond]
    m["is_french_manual"] = fr / n
    m["is_french_manual_decidible"] = fr / decidibles if decidibles else float("nan")
    m["lang_manual_counts"] = cuenta
    rep.setdefault("manual_rescore", {})[args.cond] = {
        "n": n, "categorias": cuenta,
        "nota": "is_french_manual sobre n; _decidible excluye las filas sin idioma",
    }

    print(f"{args.eval}  [{args.cond}]  n={n}")
    print(f"  categorias: {cuenta}")
    print(f"  is_french detector : {m['is_french']:.3f}")
    print(f"  is_french manual   : {m['is_french_manual']:.3f}   "
          f"(sobre decidibles: {m['is_french_manual_decidible']:.3f})")
    print(f"\n  filas corregidas ({len(cambios)}):")
    for idx, det, val, cat, txt in cambios:
        print(f"    [{idx:2}] detector={det} -> manual={val} ({cat})")
        print(f"         {txt}")

    if args.dry_run:
        print("\n[dry_run] nada escrito")
        return
    with open(args.eval, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)
    print(f"\nEscrito {args.eval} (campos originales intactos)")


if __name__ == "__main__":
    main()
