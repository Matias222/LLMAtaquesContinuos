"""
Reporte de formatos (run_pos_v10.sh): Shared (un v en todos los tokens de la
pregunta) contra Question-3 y Header-3 (3 vectores con posicion fija), celda fr.

    formatos     norma total y por posicion, epoch del checkpoint, anchor
    traspaso     % frances y acc con cada formato: held-out en ingles (con control
                 nativo), es/de, it/pt, open1, open2
    tests        resta (Tabla 6), identificacion de idioma (7), resta contra
                 instruccion (8), conflicto (9, con la instruccion antes y al final)
    controles    anchor y posiciones de lang_metadata.pt y de cada json; en q3/h3
                 cada fila parchea exactamente 3 tokens

    python3 reporte_pos.py --shared algebra/runs/v10/alg_fr --q3 algebra/runs/v10/pos_q3_fr \
        --h3 algebra/runs/v10/pos_h3_fr --tests algebra/runs/v10/pos_tests \
        --out algebra/runs/v10/reportes/pos.md
"""

import argparse
import collections
import glob
import os

from reporte_v8 import cargar, media, pct, tabla

FORMATOS = ("shared", "q3", "h3")
NOMBRE = {"shared": "Shared", "q3": "Question-3", "h3": "Header-3"}
ANCHOR = {"shared": ("goal_all", 1), "q3": ("goal", 3), "h3": ("header", 3)}
PARCHE = {"fr": "shared", "q3": "q3", "h3": "h3"}   # nombre del parche en los tests
COL_LANG = {"prompt": "en", "prompt_es": "es", "prompt_de": "de", "prompt_fr": "fr",
            "prompt_it": "it", "prompt_pt": "pt"}


def eval_json(d, nombre):
    """eval_heldout.json (v10) o eval_best_train.json (corridas del paper)."""
    for n in ((nombre,) if nombre != "eval_heldout.json" else ("eval_heldout.json", "eval_best_train.json")):
        j = cargar(os.path.join(d, n))
        if j:
            return j
    return None


def formatos(dirs, fallas):
    try:
        import torch
    except ImportError:
        return ["(sin torch: tabla de normas omitida)", ""]
    filas = []
    for f in FORMATOS:
        p = os.path.join(dirs[f], "lang_patch_best_train.pt")
        mp = os.path.join(dirs[f], "lang_metadata.pt")
        if not os.path.exists(p):
            filas.append([NOMBRE[f], "falta", "", "", "", ""])
            continue
        v = torch.load(p, map_location="cpu").float()
        m = torch.load(mp, map_location="cpu", weights_only=False) if os.path.exists(mp) else {}
        anc, n = m.get("patch_anchor"), m.get("num_patch_positions")
        if (anc, n) != ANCHOR[f] or tuple(v.shape[:2]) != (1, ANCHOR[f][1]):
            fallas.append(f"{f}: lang_metadata dice anchor={anc} N={n}, forma {tuple(v.shape)}; "
                          f"se esperaba {ANCHOR[f]}")
        filas.append([NOMBRE[f], anc, tuple(v.shape), f"{v.norm():.3f}",
                      " / ".join(f"{v[0, i].norm():.3f}" for i in range(v.shape[1])),
                      m.get("best_train_epoch", "?")])
    return [tabla(["formato", "anchor", "forma", "‖v‖ total", "‖v_i‖ por posición", "epoch"], filas), ""]


def chequear_n(rows, f, donde, fallas, clave="n_patched"):
    if f == "shared":
        malos = [r["idx"] for r in rows if r.get(clave, 0) < 1]
    else:
        malos = [r["idx"] for r in rows if r.get(clave) != 3]
    if malos:
        fallas.append(f"{f} en {donde}: {len(malos)} filas con n_patched fuera de lo esperado, ej. {malos[:5]}")


def chequear_cfg(j, f, donde, fallas):
    cfg = j.get("config", {})
    anc, n = cfg.get("patch_anchor"), cfg.get("num_patch_positions")
    if (anc, n) != ANCHOR[f]:
        fallas.append(f"{f} en {donde}: anchor={anc} N={n}, se esperaba {ANCHOR[f]}")


def traspaso(dirs, fallas):
    filas = {}

    def put(fila, f, frac, acc):
        filas.setdefault(fila, {})[f] = f"{pct(frac)} / {pct(acc)}"

    for f in FORMATOS:
        d = dirs[f]
        ev = eval_json(d, "eval_heldout.json")
        if ev:
            chequear_cfg(ev, f, "held-out", fallas)
            rows = ev["splits"]["heldout"]
            chequear_n(rows, f, "held-out", fallas)
            put("en (held-out)", f, media(r["patched_is_target"] for r in rows),
                media(r["patched_answer_correct"] for r in rows))
            if f == "shared":
                put("en sin parche", "ref", media(r["baseline_is_target"] for r in rows),
                    media(r["baseline_answer_correct"] for r in rows))
                put("control nativo (fr)", "ref", media(r["reference_is_target"] for r in rows),
                    media(r["reference_answer_correct"] for r in rows))
        for archivo in ("cross_lang_idioma.json", "cross_lang_romance.json"):
            cl = cargar(os.path.join(d, archivo))
            if not cl:
                continue
            chequear_cfg(cl, f, archivo, fallas)
            for x in cl["condiciones"]:
                if x["col"] == "prompt" or x["escala"] != 1.0:
                    continue
                chequear_n(x["rows"], f, f"{archivo}:{x['col']}", fallas)
                put(COL_LANG[x["col"]], f, media(r["out_is_target"] for r in x["rows"]),
                    media(r["out_answer_correct"] for r in x["rows"]))
        op = cargar(os.path.join(d, "eval_open.json"))
        if op:
            put("open1 (en)", f, op["metrics"]["patched"].get("is_target"), None)
        o2 = cargar(os.path.join(d, "open_2", "cross_lang_idioma.json"))
        if o2:
            for x in o2["condiciones"]:
                if x["escala"] == 1.0:
                    put(f"open2 ({COL_LANG[x['col']]})", f, media(r["out_is_target"] for r in x["rows"]), None)
    orden = ["en sin parche", "control nativo (fr)", "en (held-out)", "es", "de", "it", "pt", "open1 (en)",
             "open2 (en)", "open2 (es)", "open2 (de)"]
    cab = ["entrada", "sin parche / nativo"] + [NOMBRE[f] for f in FORMATOS]
    out = [[k, filas[k].get("ref", "")] + [filas[k].get(f, "—") for f in FORMATOS] for k in orden if k in filas]
    return [tabla(cab, out), "", "Celdas: % francés / accuracy (— = no medido; open sin accuracy).", ""]


def tests(tdir, fallas):
    L = []
    for p in sorted(glob.glob(os.path.join(tdir, "entrada_o_directiva_*.json"))):
        t = cargar(p)
        tag = os.path.basename(p)[len("entrada_o_directiva_"):-len(".json")]
        anc = t.get("anchors", {})
        for k, f in PARCHE.items():
            if k in anc and anc[k] != ANCHOR[f][0]:
                fallas.append(f"{tag}: el parche {k} tiene anchor {anc[k]}, se esperaba {ANCHOR[f][0]}")
        filas = []
        es_lang_id = all(x["plantilla"].startswith("lang_id") for x in t["condiciones"])
        for x in t["condiciones"]:
            m, rows = x["metrics"], x["rows"]
            if x["parche"] in PARCHE:
                chequear_n(rows, PARCHE[x["parche"]], f"{tag}:{x['label']}", fallas)
            if es_lang_id:
                filas.append([x["label"], m["n"], pct(m["dice_fr"]), pct(m["dice_en"]), pct(m["dice_ninguno"])])
                continue
            lang_q = COL_LANG.get(x["col"], "en")
            quedan = media(r["out_lang"] in (lang_q, "unknown") for r in rows)
            destinos = collections.Counter(r["out_lang"] for r in rows if r["out_lang"] not in (lang_q, "unknown"))
            dest = ", ".join(f"{k} {100 * v / len(rows):.0f}" for k, v in destinos.most_common(3))
            filas.append([x["label"], m["n"], pct(m["p_fr"]), pct(m["p_en"]), pct(quedan), dest,
                          pct(m["answer_correct"])])
        cab = (["condición", "n", "dice fr", "dice en", "ninguno"] if es_lang_id else
               ["condición", "n", "% fr", "% en", "% queda en el idioma de la pregunta", "destinos (%)", "acc"])
        L += [f"## {tag}", "", tabla(cab, filas), ""]
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shared", required=True)
    ap.add_argument("--q3", required=True)
    ap.add_argument("--h3", required=True)
    ap.add_argument("--tests", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    dirs = {"shared": args.shared, "q3": args.q3, "h3": args.h3}
    fallas = []
    L = ["# Formatos: Shared vs Question-3 vs Header-3 (celda fr)", "",
         f"Shared = {args.shared}; Question-3 = {args.q3}; Header-3 = {args.h3}; tests = {args.tests}.", "",
         "## Formatos", ""]
    L += formatos(dirs, fallas)
    L += ["## Idioma y accuracy por entrada", ""] + traspaso(dirs, fallas)
    L += ["# Tests (Shared = parche fr; rand0_q3 / rand0_h3 = azar con forma, norma y anchor de q3 / h3)", ""]
    L += tests(args.tests, fallas)
    L += ["## Controles", ""] + ([f"- FALLA {x}" for x in fallas] or ["- OK: anchors y posiciones parcheadas"]) + [""]
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\nreporte: {args.out}")
    if fallas:
        raise SystemExit(f"{len(fallas)} controles con FALLA")


if __name__ == "__main__":
    main()
