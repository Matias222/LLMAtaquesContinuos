"""
Juicio manual del idioma y la precision sobre las corridas de inyeccion.

Motivo: `is_french` exige veredicto "fr" explicito, y `language_verdict`
devuelve "unknown" cuando la unica evidencia son palabras de SHARED_FR_ES
(la, de, un, en, que...). Las condiciones que inyectan la direccion de d_frq
colapsan la generacion a dos o tres palabras -- "La Syrie", "Le Cr",
"Le platine" -- que son frances inequivoco y el detector no ve.

Sobre inject_d el detector reporta 24/50 de frances; leidas a mano son 37.

Se distinguen cuatro categorias, porque el agregado del detector mezcla tres
cosas distintas:

    fr      frances legitimo, incluido el fragmentario ("Le Cr")
    en      ingles legitimo -> fallo REAL de induccion
    mixto   sintaxis de un idioma con sustantivo del otro ("Mars a 2 Moons")
    neutro  sin ninguna palabra que tenga idioma: aritmetica ("15 + 6 = 21")
            o un nombre propio pelado ("Lausanne", "Alexander Graham Bell").
            No hay idioma que cumplir, asi que no entra en el denominador.

La tasa que se reporta es sobre DECIDIBLES (50 menos los neutros).

SEGUNDA CORRECCION, sobre la precision. Los alias de los numeros del banco
estan solo en frances ('4' -> 'quatre', '2' -> 'deux'), asi que una respuesta
en INGLES que escriba el numero con letras se cuenta como incorrecta. Eso
penaliza sistematicamente a las condiciones de control, que son las que
responden en ingles. Dos casos en estas corridas.

    python3 rescore_inject.py --dir runs/inject_v4_l16
"""

import argparse
import glob
import json
import os

# ---------------------------------------------------------------------------
# Juicios de idioma, indexados por (condicion, fila). Solo las filas donde el
# detector se equivoca o el caso no es obvio; el resto se respeta.
# ---------------------------------------------------------------------------
NEUTRO_ARITMETICA = [202, 209, 216, 221, 224, 249]     # "15 + 6 = 21"
NEUTRO_NOMBRE = {                                       # nombre propio pelado
    "d": [212, 222, 227, 228, 229, 243],
    "par": [200, 212, 227, 228, 229, 243],
    "total": [],
    "ort": [], "random": [], "none": [],
}
# frances que el detector marca "unknown" por ser demasiado corto
FR_MANUAL = {
    "d": [200, 203, 205, 206, 218, 220, 223, 234, 235, 237, 238, 240, 242],
    "par": [203, 205, 206, 208, 219, 220, 223, 234, 235, 236, 237, 239, 240, 242, 247],
    # "La Chenichain": articulo frances + sustantivo inventado. Mismo caso que
    # "La Chinoise" en la condicion d; se clasifica igual por consistencia.
    "total": [200],
    "ort": [], "random": [], "none": [],
}
MIXTO = {                                               # un idioma cada mitad
    "d": [219],          # "Mars a 2 Moons"
    "total": [229],      # "Launched en systeme"
    "par": [], "ort": [], "random": [], "none": [],
}
# el scorer dice False pero el numero esta escrito con letras en INGLES,
# y el alias del banco solo trae la forma francesa
ACC_MANUAL = {("ort", 244): True, ("none", 219): True}


# ---------------------------------------------------------------------------
# Juicios para los eval_*.json de los parches, indexados por el TEXTO generado
# (los indices se mueven entre corridas; el texto no). Mismo criterio que
# manual_rescore.py, que ya usa esta convencion en el repo.
# ---------------------------------------------------------------------------
TEXTO = {}
for t in ("15 + 6 = 21", "7 x 8 = 56", "7 \u00d7 8 = 56", "17 x 2 = 34",
          "17 \u00d7 2 = 34", "9 + 9 = 18", "9 + 9 = 18.", "25 + 4 = 29",
          "25 x 4 = 100", "25 \u00d7 4 = 100"):
    TEXTO[t] = "neutro"                       # aritmetica: no hay idioma que cumplir
for t in ("Damascus", "Alfred Russel Wallace", "Albert Einstein", "C\u00e9zanne",
          "Alexander Graham Bell", "Ludwig van Beethoven", "Doha", "Lausanne",
          "Sofia", "L\u00e9o Delibes", "Georges Bizet", "Lahti", "Marie Curie"):
    TEXTO[t] = "neutro"                       # nombre propio pelado
for t in ("Germany reunified on October 3, 1990.", "World War II began in 1939."):
    TEXTO[t] = "en"                           # ingles legitimo: fallo real
for t in ("World War II began en 1939.", "Mars a 2 moons."):
    TEXTO[t] = "mixto"
for t in ("Le platine", "Le Cr", "Le Cr.", "La formule chimique de CO2",
          "La mer de Corail", "La Mer", "L'Ocean Indien", "Le Cl",
          "La Symphonie n\u00b0 9 de Beethoven", "La Praga", "La Helsinki"):
    TEXTO[t] = "fr"                           # frances que el detector no ve


def juzgar_texto(txt, det):
    """Categoria manual a partir del texto. Sin juicio -> se respeta el detector."""
    t = txt.strip()
    if t in TEXTO:
        return TEXTO[t]
    return det if det in ("fr", "en", "es", "de") else "neutro"


def juzgar(cond, idx, det):
    """Categoria manual de idioma para una fila."""
    if idx in NEUTRO_ARITMETICA or idx in NEUTRO_NOMBRE.get(cond, []):
        return "neutro"
    if idx in MIXTO.get(cond, []):
        return "mixto"
    if idx in FR_MANUAL.get(cond, []):
        return "fr"
    return det if det in ("fr", "en", "es", "de") else "neutro"


def rescorear_evals(paths):
    """Tabla frances-vs-accuracy sobre los eval_*.json de los parches."""
    from checkers import language_verdict
    out = []
    for p in paths:
        rep = json.load(open(p, encoding="utf-8"))
        rows = rep["splits"]["heldout"]
        cuenta = {"fr": 0, "en": 0, "mixto": 0, "neutro": 0}
        ok = tot = okfr = totfr = 0
        largos = []
        for r in rows:
            cat = juzgar_texto(r["patched"], language_verdict(r["patched"]))
            cuenta[cat] = cuenta.get(cat, 0) + 1
            r["lang_manual"] = cat
            largos.append(len(r["patched"].strip()))
            a = r.get("patched_answer_correct")
            if a is not None:
                tot += 1
                ok += bool(a)
                if cat == "fr":
                    totfr += 1
                    okfr += bool(a)
        dec = len(rows) - cuenta["neutro"]
        out.append({
            "run": os.path.basename(os.path.dirname(os.path.abspath(p))),
            "n": len(rows), "fr_det": rep["metrics"]["patched"]["is_french"],
            "fr_manual": cuenta["fr"] / dec if dec else float("nan"),
            "acc": ok / tot if tot else float("nan"),
            "acc_fr": okfr / totfr if totfr else float("nan"),
            "largo": sum(largos) / len(largos), "decidibles": dec, **cuenta,
        })
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="directorio de una corrida de inyeccion")
    ap.add_argument("--evals", nargs="*", default=[],
                    help="eval_*.json de parches, para la tabla frances-vs-accuracy")
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    if args.evals:
        tab = rescorear_evals(args.evals)
        tab.sort(key=lambda r: -r["fr_manual"])
        print(f"{'parche':<20}{'fr det':>8}{'fr MAN':>8}{'accuracy':>10}{'acc|fr':>9}"
              f"{'largo':>7}{'|':>3}{'fr':>4}{'en':>4}{'mix':>5}{'neu':>5}{'dec':>5}")
        print("-" * 88)
        for r in tab:
            print(f"{r['run']:<20}{r['fr_det']:>8.2f}{r['fr_manual']:>8.3f}{r['acc']:>10.3f}"
                  f"{r['acc_fr']:>9.3f}{r['largo']:>7.0f}{'|':>3}{r['fr']:>4}{r['en']:>4}"
                  f"{r['mixto']:>5}{r['neutro']:>5}{r['decidibles']:>5}")
        print("\nfr MAN = frances sobre DECIDIBLES.  acc|fr = accuracy solo en las filas")
        print("que salieron en frances, que separa 'cambio de idioma' de 'perdio el hecho'.")
        return
    if not args.dir:
        ap.error("hace falta --dir o --evals")

    resumen = []
    for p in sorted(glob.glob(os.path.join(args.dir, "inject_*.json"))):
        rep = json.load(open(p, encoding="utf-8"))
        cond = rep["condicion"]
        cuenta = {"fr": 0, "en": 0, "mixto": 0, "neutro": 0}
        ok = tot = 0
        largos = []
        for r in rep["rows"]:
            cat = juzgar(cond, r["idx"], r["injected_lang"])
            cuenta[cat] = cuenta.get(cat, 0) + 1
            r["lang_manual"] = cat
            r["is_french_manual"] = (cat == "fr") if cat != "neutro" else None
            acc = ACC_MANUAL.get((cond, r["idx"]), r["injected_answer_correct"])
            r["answer_correct_manual"] = acc
            if acc is not None:
                tot += 1
                ok += bool(acc)
            largos.append(len(r["injected"].strip()))

        dec = len(rep["rows"]) - cuenta["neutro"]
        m = rep["metrics"]
        m["is_french_manual"] = cuenta["fr"] / dec if dec else float("nan")
        m["answer_correct_manual"] = ok / tot if tot else float("nan")
        m["lang_manual_counts"] = cuenta
        m["decidibles"] = dec
        m["largo_medio"] = sum(largos) / len(largos)
        rep["rescore_manual"] = {
            "criterio": "fr sobre DECIDIBLES (n menos los neutros); "
                        "neutro = aritmetica o nombre propio pelado",
        }
        resumen.append({
            "cond": cond, "norma": rep["norma_inyectada"],
            "fr_det": m["is_french"], "fr_manual": m["is_french_manual"],
            "acc_det": m["answer_correct"], "acc_manual": m["answer_correct_manual"],
            "largo": m["largo_medio"], **cuenta, "decidibles": dec,
        })
        if not args.dry_run:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(rep, f, indent=2, ensure_ascii=False)

    orden = {"total": 0, "par": 1, "d": 2, "ort": 3, "random": 4, "none": 5}
    resumen.sort(key=lambda r: orden.get(r["cond"], 9))
    print(f"{'cond':<8}{'norma':>8}{'fr det':>8}{'fr MAN':>8}{'acc det':>9}{'acc MAN':>9}"
          f"{'largo':>7}{'|':>3}{'fr':>4}{'en':>4}{'mix':>5}{'neu':>5}{'dec':>5}")
    print("-" * 86)
    for r in resumen:
        print(f"{r['cond']:<8}{r['norma']:>8.2f}{r['fr_det']:>8.2f}{r['fr_manual']:>8.3f}"
              f"{r['acc_det']:>9.2f}{r['acc_manual']:>9.3f}{r['largo']:>7.0f}{'|':>3}"
              f"{r['fr']:>4}{r['en']:>4}{r['mixto']:>5}{r['neutro']:>5}{r['decidibles']:>5}")
    print("\nfr MAN = frances sobre DECIDIBLES. acc MAN corrige los alias de numeros")
    print("escritos con letras en ingles, que penalizaban a las condiciones de control.")

    if not args.dry_run:
        out = os.path.join(args.dir, "resumen_manual.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"resumen": resumen}, f, indent=2, ensure_ascii=False)
        print(f"\nGuardado: {out}  (y los campos manuales en cada inject_*.json)")


if __name__ == "__main__":
    main()
