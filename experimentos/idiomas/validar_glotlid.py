"""
¿GlotLID clasifica el idioma de las salidas mejor que checkers.language_verdict?

Antes de reemplazar el detector del pipeline hay que medirlo contra lo que ya
se clasifico a mano. Dos conjuntos:

  manual       algebra/runs/restar_matriz/clasificacion_manual_resta.csv
               450 salidas de la resta (q_L - v_P), etiquetadas a mano
               (`idioma_manual`): es el caso dificil (catalan, mezclas,
               respuestas incoherentes, nombres sueltos). 'none' = sin idioma.
  referencia   salidas del modelo con idioma conocido por construccion,
               sin etiqueta manual (la etiqueta es la esperada, no verificada):
                 targets_french_v5.csv  output -> fr, baseline_en -> en
                 algebra/targets/targets_es.csv  output -> es
                 algebra/targets/targets_de.csv  output -> de
                 alg_fr/cross_lang_romance.json  prompt_it a=0 -> it, prompt_pt a=0 -> pt
               Solo filas con passed_gate (si la columna existe). Mide el caso
               facil y las respuestas cortas ("C'est Uranus.").

GlotLID siempre devuelve un idioma, asi que "sin idioma" sale de una regla:
    none  si  palabras < min_words  o  confianza < umbral
Se barre la grilla (umbral x min_words) y se reporta la concordancia de cada
combinacion; la regla elegida se declara en el paper (seccion 3.4). Con 450
filas la grilla puede sobreajustar: mirar tambien el conjunto de referencia.

Salidas en --out_dir:
    resumen.md          concordancia por regla, por idioma, matriz de confusion
    predicciones.csv    cada fila con la etiqueta, GlotLID (top-3) y la heuristica
    desacuerdos.csv     filas donde GlotLID (con la mejor regla) no coincide

    (desde experimentos/idiomas)
    python3 -u validar_glotlid.py --glotlid modelos/glotlid/model.bin \\
        --out_dir runs/validar_glotlid
"""

import argparse
import collections
import json
import os
import re

import pandas as pd

from checkers import language_verdict

MANUAL = "algebra/runs/restar_matriz/clasificacion_manual_resta.csv"

# ISO 639-3 de GlotLID -> los codigos de dos letras que usa el resto del repo
ISO3 = {"fra": "fr", "eng": "en", "spa": "es", "deu": "de", "ita": "it", "por": "pt",
        "cat": "ca", "nld": "nl", "swe": "sv", "glg": "gl", "oci": "oc", "ron": "ro",
        "dan": "da", "nob": "no", "nno": "no", "pol": "pl", "rus": "ru"}
SIN_IDIOMA = {"zxx", "und"}

UMBRALES = (0.0, 0.3, 0.5, 0.7, 0.9)
MIN_WORDS = (0, 1, 2, 3)


def palabras(text):
    return len(re.findall(r"[^\W\d_]+", str(text)))


class GlotLID:
    def __init__(self, path):
        import fasttext
        fasttext.FastText.eprint = lambda *a, **k: None    # silencia el aviso de load_model
        self.m = fasttext.load_model(path)

    def top(self, text, k=3):
        """[(codigo, prob)] de mayor a menor. fastText exige una sola linea."""
        t = " ".join(str(text).split())
        if not t:
            return [("none", 1.0)]
        # m.f.predict y no m.predict: este ultimo rompe con numpy >= 2
        # (np.array(..., copy=False)) y devuelve lo mismo.
        pares = self.m.f.predict(t + "\n", k, 0.0, "strict")
        out = []
        for prob, lab in pares:
            iso3 = lab.replace("__label__", "").split("_")[0]
            cod = "none" if iso3 in SIN_IDIOMA else ISO3.get(iso3, iso3)
            out.append((cod, float(prob)))
        return out


def con_regla(top, text, umbral, min_words):
    cod, p = top[0]
    if palabras(text) < min_words or p < umbral:
        return "none"
    return cod


def heuristica(text):
    v = language_verdict(text)
    return "none" if v == "unknown" else v


def cargar_manual(path):
    d = pd.read_csv(path, sep=";", keep_default_na=False)
    return [{"conjunto": "manual", "origen": f"{r['pregunta_en']} - {r['resta']}",
             "idx": r["idx"], "etiqueta": r["idioma_manual"], "texto": r["salida"]}
            for _, r in d.iterrows()]


def cargar_referencia():
    filas = []

    def de_csv(path, col, lang):
        if not os.path.exists(path):
            print(f"  (falta {path}, se saltea)")
            return
        d = pd.read_csv(path, sep=";", keep_default_na=False)
        if "passed_gate" in d.columns:
            d = d[d["passed_gate"].astype(str).str.lower() == "true"]
        for i, r in d.iterrows():
            if str(r[col]).strip():
                filas.append({"conjunto": "referencia", "origen": f"{os.path.basename(path)}:{col}",
                              "idx": int(i), "etiqueta": lang, "texto": r[col]})

    de_csv("attributes/french/targets_french_v5.csv", "output", "fr")
    de_csv("attributes/french/targets_french_v5.csv", "baseline_en", "en")
    de_csv("algebra/targets/targets_es.csv", "output", "es")
    de_csv("algebra/targets/targets_de.csv", "output", "de")

    rom = "algebra/runs/alg_fr/cross_lang_romance.json"
    if os.path.exists(rom):
        for c in json.load(open(rom, encoding="utf-8"))["condiciones"]:
            lang = {"prompt_it a=0": "it", "prompt_pt a=0": "pt"}.get(c["label"])
            if lang:
                for r in c["rows"]:
                    filas.append({"conjunto": "referencia", "origen": f"romance:{c['label']}",
                                  "idx": r["idx"], "etiqueta": lang, "texto": r["out"]})
    else:
        print(f"  (falta {rom}, se saltea)")
    return filas


def concordancia(filas, pred_key):
    return sum(f[pred_key] == f["etiqueta"] for f in filas) / max(1, len(filas))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glotlid", required=True, help="ruta a model.bin de cis-lmu/glotlid")
    ap.add_argument("--manual", default=MANUAL)
    ap.add_argument("--sin_referencia", action="store_true", help="solo el conjunto manual")
    ap.add_argument("--out_dir", default="runs/validar_glotlid")
    args = ap.parse_args()

    if not os.path.exists(args.manual):
        raise SystemExit(f"falta {args.manual}: no esta en git, copiarlo a la VM")
    os.makedirs(args.out_dir, exist_ok=True)

    filas = cargar_manual(args.manual)
    if not args.sin_referencia:
        filas += cargar_referencia()
    print(f"filas: {collections.Counter(f['conjunto'] for f in filas)}")

    lid = GlotLID(args.glotlid)
    for f in filas:
        f["top"] = lid.top(f["texto"])
        f["heuristica"] = heuristica(f["texto"])
        f["palabras"] = palabras(f["texto"])
    conjuntos = {c: [f for f in filas if f["conjunto"] == c] for c in ("manual", "referencia")}
    conjuntos = {c: v for c, v in conjuntos.items() if v}

    # --- grilla de la regla "sin idioma" ---------------------------------------
    grilla = []
    for u in UMBRALES:
        for w in MIN_WORDS:
            key = f"g_{u}_{w}"
            for f in filas:
                f[key] = con_regla(f["top"], f["texto"], u, w)
            grilla.append({"umbral": u, "min_words": w, "key": key,
                           **{c: concordancia(v, key) for c, v in conjuntos.items()}})
    criterio = "manual" if "manual" in conjuntos else "referencia"
    mejor = max(grilla, key=lambda g: (g[criterio], -g["umbral"], -g["min_words"]))
    for f in filas:
        f["glotlid"] = f[mejor["key"]]

    # --- reporte ------------------------------------------------------------------
    L = ["# GlotLID contra la heuristica de checkers.py", ""]
    L.append(f"Modelo: `{args.glotlid}`. Regla sin idioma: `none` si palabras < min_words "
             f"o confianza top-1 < umbral.")
    L.append(f"Mejor regla (por concordancia en `{criterio}`): umbral {mejor['umbral']}, "
             f"min_words {mejor['min_words']}.")
    L.append("")
    L.append("| conjunto | n | heuristica | GlotLID sin regla | GlotLID mejor regla |")
    L.append("|---|---|---|---|---|")
    for c, v in conjuntos.items():
        L.append(f"| {c} | {len(v)} | {concordancia(v, 'heuristica'):.3f} | "
                 f"{concordancia(v, 'g_0.0_0'):.3f} | {concordancia(v, 'glotlid'):.3f} |")
    L.append("")
    L.append("## Grilla (concordancia)")
    L.append("")
    L.append("| umbral | min_words | " + " | ".join(conjuntos) + " |")
    L.append("|---|---|" + "---|" * len(conjuntos))
    for g in grilla:
        L.append(f"| {g['umbral']} | {g['min_words']} | " +
                 " | ".join(f"{g[c]:.3f}" for c in conjuntos) + " |")
    L.append("")

    for c, v in conjuntos.items():
        L.append(f"## `{c}`: concordancia por etiqueta")
        L.append("")
        L.append("| etiqueta | n | heuristica | GlotLID |")
        L.append("|---|---|---|---|")
        for lab, n in collections.Counter(f["etiqueta"] for f in v).most_common():
            sub = [f for f in v if f["etiqueta"] == lab]
            L.append(f"| {lab} | {n} | {concordancia(sub, 'heuristica'):.2f} | "
                     f"{concordancia(sub, 'glotlid'):.2f} |")
        L.append("")
        labs = sorted(set(f["etiqueta"] for f in v) | set(f["glotlid"] for f in v))
        L.append(f"Matriz de confusion GlotLID (`{c}`; filas = etiqueta, columnas = prediccion):")
        L.append("")
        L.append("| | " + " | ".join(labs) + " |")
        L.append("|---|" + "---|" * len(labs))
        cnt = collections.Counter((f["etiqueta"], f["glotlid"]) for f in v)
        for a in labs:
            if any(cnt[(a, b)] for b in labs):
                L.append(f"| **{a}** | " + " | ".join(str(cnt[(a, b)] or "") for b in labs) + " |")
        L.append("")

    open(os.path.join(args.out_dir, "resumen.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    cols = ["conjunto", "origen", "idx", "etiqueta", "glotlid", "heuristica", "palabras",
            "top1", "p1", "top2", "p2", "top3", "p3", "texto"]
    regs = []
    for f in filas:
        r = {k: f.get(k) for k in cols}
        for j, (cod, p) in enumerate(f["top"][:3], 1):
            r[f"top{j}"], r[f"p{j}"] = cod, round(p, 4)
        regs.append(r)
    out = pd.DataFrame(regs, columns=cols)
    out.to_csv(os.path.join(args.out_dir, "predicciones.csv"), sep=";", index=False)
    out[out["glotlid"] != out["etiqueta"]].to_csv(
        os.path.join(args.out_dir, "desacuerdos.csv"), sep=";", index=False)

    print("\n".join(L[:10 + 2 * len(conjuntos)]))
    print(f"\nReporte: {args.out_dir}/resumen.md  |  desacuerdos: {args.out_dir}/desacuerdos.csv")


if __name__ == "__main__":
    main()
