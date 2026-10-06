"""
Validacion del detector de idioma (lang_id.py, GlotLID) contra etiquetas
conocidas, y comparacion con la heuristica vieja de checkers.py.

Dos conjuntos:

  manual       algebra/runs/restar_matriz/clasificacion_manual_resta.csv
               450 salidas de la resta (q_L - v_P), etiquetadas a mano
               (`idioma_manual`): es el caso dificil (catalan, mezclas,
               respuestas incoherentes, nombres sueltos). 'none' = sin idioma.
  referencia   salidas del modelo con idioma conocido por construccion
               (etiqueta esperada, no verificada a mano):
                 targets_french_v5.csv  output -> fr, baseline_en -> en
                 algebra/targets/targets_es.csv  output -> es
                 algebra/targets/targets_de.csv  output -> de
                 alg_fr/cross_lang_romance.json  prompt_it a=0 -> it, prompt_pt a=0 -> pt
               Solo filas con passed_gate. Las de menos de lang_id.MIN_PALABRAS
               palabras se etiquetan 'none' ("Kiev", "Em 2000"): no tienen
               idioma decidible y la etiqueta por construccion seria falsa.

Tres detectores sobre las mismas filas:
  heuristica   checkers.language_verdict_heuristica (la de antes)
  glotlid_top1 GlotLID sin lista cerrada (solo la regla de palabras)
  lang_id      el detector del pipeline: lista cerrada + regla de palabras

Y para lang_id, cuantos errores caen en la marca `revisar` (los que el
pipeline manda a revision manual) y cuantas filas marca en total.

Salidas en --out_dir: resumen.md, predicciones.csv, desacuerdos.csv

    (desde experimentos/idiomas)
    python3 -u validar_glotlid.py --out_dir runs/validar_glotlid
    GLOTLID_MODEL=/ruta/model.bin python3 -u validar_glotlid.py ...
"""

import argparse
import collections
import json
import os

import pandas as pd

import lang_id
from checkers import language_verdict_heuristica

MANUAL = "algebra/runs/restar_matriz/clasificacion_manual_resta.csv"
DETECTORES = ("heuristica", "glotlid_top1", "lang_id")


def a_none(v):
    return "none" if v == "unknown" else v


def cargar_manual(path):
    d = pd.read_csv(path, sep=";", keep_default_na=False)
    return [{"conjunto": "manual", "origen": f"{r['pregunta_en']} - {r['resta']}",
             "idx": r["idx"], "etiqueta": r["idioma_manual"], "texto": r["salida"]}
            for _, r in d.iterrows()]


def cargar_referencia():
    filas = []

    def agregar(origen, idx, lang, texto):
        corto = lang_id.palabras(texto) < lang_id.MIN_PALABRAS
        filas.append({"conjunto": "referencia", "origen": origen, "idx": idx,
                      "etiqueta": "none" if corto else lang, "texto": texto})

    def de_csv(path, col, lang):
        if not os.path.exists(path):
            print(f"  (falta {path}, se saltea)")
            return
        d = pd.read_csv(path, sep=";", keep_default_na=False)
        if "passed_gate" in d.columns:
            d = d[d["passed_gate"].astype(str).str.lower() == "true"]
        for i, r in d.iterrows():
            if str(r[col]).strip():
                agregar(f"{os.path.basename(path)}:{col}", int(i), lang, r[col])

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
                    agregar(f"romance:{c['label']}", r["idx"], lang, r["out"])
    else:
        print(f"  (falta {rom}, se saltea)")
    return filas


def conc(filas, key):
    return sum(f[key] == f["etiqueta"] for f in filas) / max(1, len(filas))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manual", default=MANUAL)
    ap.add_argument("--sin_referencia", action="store_true", help="solo el conjunto manual")
    ap.add_argument("--out_dir", default="runs/validar_glotlid")
    args = ap.parse_args()

    if not os.path.exists(args.manual):
        raise SystemExit(f"falta {args.manual}")
    os.makedirs(args.out_dir, exist_ok=True)

    filas = cargar_manual(args.manual)
    if not args.sin_referencia:
        filas += cargar_referencia()
    print(f"filas: {dict(collections.Counter(f['conjunto'] for f in filas))}")

    for f in filas:
        t = f["texto"]
        corto = lang_id.palabras(t) < lang_id.MIN_PALABRAS
        dist = [] if corto else lang_id.distribucion(t)
        det = lang_id.detectar(t)
        f["heuristica"] = a_none(language_verdict_heuristica(t))
        f["glotlid_top1"] = "none" if corto or not dist else dist[0][0]
        f["lang_id"] = a_none(det["lang"])
        f["p"] = round(det["p"], 4)
        f["revisar"] = det["revisar"]
        f["mezcla"] = det["mezcla"]
        f["palabras"] = lang_id.palabras(t)
        f["top3"] = " ".join(f"{c}:{q:.2f}" for c, q in dist[:3])
    conjuntos = {c: [f for f in filas if f["conjunto"] == c] for c in ("manual", "referencia")}
    conjuntos = {c: v for c, v in conjuntos.items() if v}

    # --- reporte ------------------------------------------------------------------
    info = lang_id.descripcion()
    L = ["# Validacion del detector de idioma", ""]
    L.append(f"Modelo: `{info['modelo']}`. Lista cerrada: {', '.join(info['idiomas'])}. "
             f"Sin idioma: menos de {info['min_palabras']} palabras. "
             f"Variedades sumadas: {info['variedades']}. `revisar`: top-1 fuera de la lista, "
             f"p < {info['p_revisar']}, veredicto en {info['revisar_siempre']} o texto mezclado "
             f"(oraciones de {info['min_palabras_oracion']}+ palabras en idiomas distintos).")
    L.append("")
    L.append("| conjunto | n | " + " | ".join(DETECTORES) + " | errores lang_id | marcados revisar | errores atrapados por revisar |")
    L.append("|---|---|" + "---|" * len(DETECTORES) + "---|---|---|")
    for c, v in conjuntos.items():
        err = [f for f in v if f["lang_id"] != f["etiqueta"]]
        L.append(f"| {c} | {len(v)} | " + " | ".join(f"{conc(v, d):.3f}" for d in DETECTORES)
                 + f" | {len(err)} | {sum(f['revisar'] for f in v)} | "
                 f"{sum(f['revisar'] for f in err)}/{len(err)} |")
    L.append("")

    for c, v in conjuntos.items():
        L.append(f"## `{c}`: concordancia por etiqueta")
        L.append("")
        L.append("| etiqueta | n | " + " | ".join(DETECTORES) + " |")
        L.append("|---|---|" + "---|" * len(DETECTORES))
        for lab, n in collections.Counter(f["etiqueta"] for f in v).most_common():
            sub = [f for f in v if f["etiqueta"] == lab]
            L.append(f"| {lab} | {n} | " + " | ".join(f"{conc(sub, d):.2f}" for d in DETECTORES) + " |")
        L.append("")
        labs = sorted(set(f["etiqueta"] for f in v) | set(f["lang_id"] for f in v))
        L.append(f"Matriz de confusion de lang_id (`{c}`; filas = etiqueta, columnas = prediccion):")
        L.append("")
        L.append("| | " + " | ".join(labs) + " |")
        L.append("|---|" + "---|" * len(labs))
        cnt = collections.Counter((f["etiqueta"], f["lang_id"]) for f in v)
        for a in labs:
            if any(cnt[(a, b)] for b in labs):
                L.append(f"| **{a}** | " + " | ".join(str(cnt[(a, b)] or "") for b in labs) + " |")
        L.append("")
    open(os.path.join(args.out_dir, "resumen.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    cols = ["conjunto", "origen", "idx", "etiqueta", "lang_id", "p", "revisar", "mezcla", "glotlid_top1",
            "heuristica", "palabras", "top3", "texto"]
    out = pd.DataFrame([{k: f[k] for k in cols} for f in filas], columns=cols)
    out.to_csv(os.path.join(args.out_dir, "predicciones.csv"), sep=";", index=False)
    out[out["lang_id"] != out["etiqueta"]].to_csv(
        os.path.join(args.out_dir, "desacuerdos.csv"), sep=";", index=False)

    print("\n".join(L[:6 + len(conjuntos)]))
    print(f"\nReporte: {args.out_dir}/resumen.md  |  desacuerdos: {args.out_dir}/desacuerdos.csv")


if __name__ == "__main__":
    main()
