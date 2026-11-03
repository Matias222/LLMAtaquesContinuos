"""
Reporte del experimento DiffMean (algebra/run_diffmean.sh) -> <out_dir>/resumen.md,
curvas_sel.csv y geo.csv. Lee lo que haya: lo que falta queda marcado "(falta)",
asi que se puede correr a mitad de camino.

Shared se lee de la corrida original (--run): eval_heldout.json, cross_lang_idioma.json
y los tests de la etapa E (resta, tests/, conflicto_v2_n112), con las mismas
etiquetas de condicion que usan los tests de D.
"""

import argparse
import csv
import json
import math
import os

import torch


def load(p):
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(x):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{100 * x:.1f}"


def f2(x):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.2f}"


def binom_p(b, c):
    """McNemar exacto (dos colas)."""
    n, k = b + c, min(b, c)
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def ev_rows(p):
    d = load(p)
    return (d["splits"]["heldout"], d.get("metrics", {})) if d else (None, None)


def resumen(rows, key="patched", ce=None):
    """%target, accuracy, target y correcta, accuracy | target, desde las filas."""
    n = len(rows)
    t = [bool(r[f"{key}_is_target"]) for r in rows]
    a = [bool(r[f"{key}_answer_correct"]) for r in rows]
    tc = [x and y for x, y in zip(t, a)]
    return {"n": n, "target": sum(t) / n, "acc": sum(a) / n, "tc": sum(tc) / n,
            "acc_t": (sum(tc) / sum(t)) if sum(t) else None, "ce": ce,
            "_tc": {r["idx"]: v for r, v in zip(rows, tc)}}


def mcnemar(ref, other):
    comun = sorted(set(ref["_tc"]) & set(other["_tc"]))
    b = sum(ref["_tc"][i] and not other["_tc"][i] for i in comun)
    c = sum(other["_tc"][i] and not ref["_tc"][i] for i in comun)
    return b, c, binom_p(b, c), len(comun)


def tabla(L, header, filas):
    esc = lambda x: str(x).replace("|", "\|")
    L.append("| " + " | ".join(esc(h) for h in header) + " |")
    L.append("|" + "---|" * len(header))
    for f in filas:
        L.append("| " + " | ".join(esc(x) for x in f) + " |")
    L.append("")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--langs", default="fr es de")
    ap.add_argument("--vecs", default="Dmulti Den")
    ap.add_argument("--test_vecs", default="Dmulti")
    ap.add_argument("--data_n", default="8 32 128")
    ap.add_argument("--data_seeds", default="0 1")
    ap.add_argument("--fam", default="")
    args = ap.parse_args()
    O, R = args.out_dir, args.run
    langs, vecs, tvecs = args.langs.split(), args.vecs.split(), args.test_vecs.split()
    sel = load(f"{O}/sel/seleccion.json") or {}
    L = [f"# DiffMean en la capa 0 contra Shared ({args.fam})", "",
         f"Corrida: `{O}`  |  Shared: `{R}`", "",
         "Criterio pre-registrado: norma = argmax de *target y correcta* en validacion (filas "
         "528..587); **equivalente** = McNemar exacto p > 0.05 contra Shared en *target y correcta* "
         "Y a <= 5 pp del nativo. Primario: `Dmulti`.", ""]

    # ------------------------------------------------------------------ vectores
    L += ["## 1. Vectores", ""]
    filas = []
    for V in vecs:
        for lg in langs:
            j = load(f"{O}/vec/{V}_{lg}.json")
            sh = torch.load(f"{R}/alg_{lg}/lang_patch_best_train.pt", map_location="cpu").float()
            filas.append([V, lg, f2(j["norma_cruda"]) if j else "(falta)",
                          f"{sel.get(V, {}).get(lg, {}).get('norma', '–')}",
                          f"{sh.norm():.3f}", f"{j['cos']['shared']:+.3f}" if j else "–",
                          f"{j['cos(D, mu_vocab)']:+.3f}" if j else "–"])
    tabla(L, ["vector", "L", "norma cruda", "norma elegida", "norma Shared", "cos(D, Shared)",
              "cos(D, mu_vocab)"], filas)
    unit = {}
    for V in vecs:
        for lg in langs:
            p = f"{O}/vec/{V}_{lg}.pt"
            if os.path.exists(p):
                unit[f"{V}_{lg}"] = torch.load(p, map_location="cpu").float().reshape(-1)
    for lg in langs:
        p = f"{R}/alg_{lg}/lang_patch_best_train.pt"
        unit[f"shared_{lg}"] = torch.load(p, map_location="cpu").float().reshape(-1)
    if unit:
        ks = list(unit)
        L += ["Cosenos entre vectores (capa 0):", ""]
        filas = [[a] + [f"{float(unit[a] @ unit[b] / (unit[a].norm() * unit[b].norm())):+.2f}" for b in ks]
                 for a in ks]
        tabla(L, [""] + ks, filas)

    # ------------------------------------------------------------------ seleccion
    L += ["## 2. Seleccion de norma (validacion, filas 528..587)", ""]
    curvas = []
    for lg in langs:
        rs, m = ev_rows(f"{O}/sel/shared_{lg}/eval_heldout.json")
        filas = []
        if rs:
            s = resumen(rs, ce=m.get("nll_fr_head_patched"))
            nat = resumen(rs, "reference")
            filas.append(["nativo", "–", pct(nat["target"]), pct(nat["acc"]), pct(nat["tc"]), "–"])
            filas.append(["Shared", f"{torch.load(f'{R}/alg_{lg}/lang_patch_best_train.pt', map_location='cpu').float().norm():.3f}",
                          pct(s["target"]), pct(s["acc"]), pct(s["tc"]), f2(s["ce"])])
            curvas.append({"L": lg, "vector": "shared", "norma": "", "target": s["target"], "acc": s["acc"], "tc": s["tc"], "ce": s["ce"]})
            curvas.append({"L": lg, "vector": "nativo", "norma": "", "target": nat["target"], "acc": nat["acc"], "tc": nat["tc"], "ce": ""})
        for V in vecs:
            for c in sel.get(V, {}).get(lg, {}).get("curva", []):
                rs, m = ev_rows(f"{O}/sel/{V}_{lg}_n{c.get('tag', c['norma'])}/eval_heldout.json")
                if not rs:
                    continue
                s = resumen(rs, ce=m.get("nll_fr_head_patched"))
                marca = " **<-**" if c["norma"] == sel[V][lg]["norma"] else ""
                filas.append([V + marca, f"{c['norma']:g}", pct(s["target"]), pct(s["acc"]), pct(s["tc"]), f2(s["ce"])])
                curvas.append({"L": lg, "vector": V, "norma": c["norma"], "target": s["target"],
                               "acc": s["acc"], "tc": s["tc"], "ce": s["ce"]})
        L += [f"### {lg}", ""]
        if filas:
            tabla(L, ["condicion", "norma", "% target", "accuracy", "target y correcta", "CE head"], filas)
        else:
            L += ["(falta)", ""]
    if curvas:
        with open(f"{O}/curvas_sel.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(curvas[0]))
            w.writeheader()
            w.writerows(curvas)
        L += [f"Curvas en `{O}/curvas_sel.csv`.", ""]

    # ------------------------------------------------------------------ held-out
    L += ["## 3. Held-out (Tabla 1): q_en + vector", ""]
    veredictos = []
    for lg in langs:
        rs, m = ev_rows(f"{R}/alg_{lg}/eval_heldout.json")
        if not rs:
            L += [f"### {lg}", "", "(falta Shared)", ""]
            continue
        sh = resumen(rs, ce=m.get("nll_fr_head_patched"))
        nat, base = resumen(rs, "reference"), resumen(rs, "baseline")
        filas = [["none", pct(base["target"]), pct(base["acc"]), pct(base["tc"]), "–", f2(m.get("nll_fr_head_baseline")), "", ""],
                 ["nativo", pct(nat["target"]), pct(nat["acc"]), pct(nat["tc"]), pct(nat["acc_t"]), "–", "", ""],
                 ["Shared", pct(sh["target"]), pct(sh["acc"]), pct(sh["tc"]), pct(sh["acc_t"]), f2(sh["ce"]), "", ""]]
        for V in vecs + ["rand"]:
            rv, mv = ev_rows(f"{O}/heldout/{V}_{lg}/eval_heldout.json")
            if not rv:
                filas.append([V, "(falta)"] + [""] * 6)
                continue
            s = resumen(rv, ce=mv.get("nll_fr_head_patched"))
            b, c, p, nc = mcnemar(sh, s)
            eq = (p > 0.05) and (s["tc"] >= nat["tc"] - 0.05)
            if V != "rand":
                veredictos.append((V, lg, eq, s["tc"], sh["tc"], nat["tc"], p))
            filas.append([V, pct(s["target"]), pct(s["acc"]), pct(s["tc"]), pct(s["acc_t"]), f2(s["ce"]),
                          f"{b}/{c} p={p:.3f}", ("**si**" if eq else "no") if V != "rand" else ""])
        L += [f"### {lg}", ""]
        tabla(L, ["condicion", "% target", "accuracy", "target y correcta", "acc | target", "CE head",
                  "McNemar vs Shared (solo Shared / solo este)", "equivalente"], filas)
    if veredictos:
        L += ["**Veredicto pre-registrado**", ""]
        for V, lg, eq, tc, tsh, tnat, p in veredictos:
            L.append(f"- {V} {lg}: {'EQUIVALENTE' if eq else 'no equivalente'} "
                     f"(t&c {pct(tc)} vs Shared {pct(tsh)}, nativo {pct(tnat)}, p={p:.3f})")
        L.append("")

    # ------------------------------------------------------------------ cross
    L += ["## 4. Otros idiomas de origen (Tabla 6 + it/pt no vistos): q_s + vector_L", ""]
    otros = {"fr": ("es", "de", "it", "pt"), "es": ("de", "fr", "it", "pt"), "de": ("es", "fr", "it", "pt")}

    def cross_res(p, col, esc):
        d = load(p)
        if not d:
            return None
        for c in d["condiciones"]:
            if c["col"] == col and abs(float(c["escala"]) - esc) < 1e-9:
                rows = c["rows"]
                n = len(rows)
                t = [bool(r["out_is_target"]) for r in rows]
                a = [bool(r["out_answer_correct"]) for r in rows]
                return {"n": n, "target": sum(t) / n, "acc": sum(a) / n,
                        "tc": sum(x and y for x, y in zip(t, a)) / n}
        return None
    filas = []
    for lg in langs:
        for s_ in otros.get(lg, ()):
            col = f"prompt_{s_}"
            psh = f"{R}/alg_{lg}/cross_lang_{'romance' if s_ in ('it', 'pt') else 'idioma'}.json"
            r0 = cross_res(psh, col, 0.0)
            rs = cross_res(psh, col, 1.0)
            fila = [f"{s_} -> {lg}" + (" (no visto)" if s_ in ("it", "pt") else "")]
            for x in [r0, rs] + [cross_res(f"{O}/cross_{V}/{lg}/cross_lang_cross.json", col, 1.0) for V in vecs]:
                fila.append(f"{pct(x['target'])} / {pct(x['tc'])}" if x else "(falta)")
            filas.append(fila)
    tabla(L, ["origen -> target", "sin parche", "Shared"] + vecs, filas)
    L += ["Celdas: % target / % target y correcta.", ""]

    # ------------------------------------------------------------------ tests
    L += ["## 5. Bateria de tests (mismas condiciones que la etapa E de Shared)", ""]
    shared_tests = {"resta": f"{R}/resta/entrada_o_directiva_resta.json",
                    "idioma_entrada": f"{R}/tests/entrada_o_directiva_idioma_entrada.json",
                    "resta_directiva": f"{R}/tests/entrada_o_directiva_resta_directiva.json",
                    "conflicto": f"{R}/tests/entrada_o_directiva_conflicto.json",
                    "conflicto_v2": f"{R}/conflicto_v2_n112/entrada_o_directiva_conflicto_v2.json"}
    for tag, psh in shared_tests.items():
        dsh = load(psh)
        msh = {c["label"]: c["metrics"] for c in dsh["condiciones"]} if dsh else {}
        dd = {V: load(f"{O}/tests_{V}/entrada_o_directiva_{tag}.json") for V in tvecs}
        md = {V: ({c["label"]: c["metrics"] for c in d["condiciones"]} if d else {}) for V, d in dd.items()}
        labels = list(dict.fromkeys(list(md[tvecs[0]]) if md[tvecs[0]] else []))
        if not labels:
            L += [f"### {tag}", "", "(falta)", ""]
            continue
        if tag == "idioma_entrada":
            keys = [("dice_en", "dice en"), ("dice_fr", "dice fr"), ("dice_es", "dice es"), ("dice_de", "dice de")]
        else:
            keys = [("p_en", "en"), ("p_fr", "fr"), ("p_es", "es"), ("p_de", "de"), ("answer_correct", "acc")]
        filas = []
        for lab in labels:
            sin_parche = "*" not in lab
            fuentes = [("Shared", msh.get(lab))] if not sin_parche else [("—", msh.get(lab) or md[tvecs[0]].get(lab))]
            if not sin_parche:
                fuentes += [(V, md[V].get(lab)) for V in tvecs]
            for nombre, mm in fuentes:
                filas.append([lab, nombre] + ([pct(mm.get(k)) for k, _ in keys] if mm else ["(falta)"] + [""] * (len(keys) - 1)))
        L += [f"### {tag}", ""]
        tabla(L, ["condicion", "vector"] + [h for _, h in keys], filas)
    L += ["En los tests de D los nombres fr/es/de son D_fr/D_es/D_de a la norma elegida; "
          "randN copia la norma de D (en Shared, la de Shared).", ""]

    # ------------------------------------------------------------------ datos
    L += ["## 6. Eficiencia de datos: Dmulti_fr con N preguntas paralelas (held-out fr)", ""]
    filas = []
    for N in args.data_n.split():
        for S in args.data_seeds.split():
            rv, mv = ev_rows(f"{O}/datos/N{N}_s{S}/eval_heldout.json")
            j = load(f"{O}/datos/vec/Dmulti_fr_N{N}_s{S}.json")
            if rv:
                s = resumen(rv, ce=mv.get("nll_fr_head_patched"))
                filas.append([N, S, f"{j['cos'].get('Dmulti_528', float('nan')):+.3f}" if j else "–",
                              pct(s["target"]), pct(s["acc"]), pct(s["tc"]), f2(s["ce"])])
            else:
                filas.append([N, S, "(falta)", "", "", "", ""])
    rv, mv = ev_rows(f"{O}/heldout/Dmulti_fr/eval_heldout.json")
    if rv:
        s = resumen(rv, ce=mv.get("nll_fr_head_patched"))
        filas.append([528, "–", "+1.000", pct(s["target"]), pct(s["acc"]), pct(s["tc"]), f2(s["ce"])])
    tabla(L, ["N", "semilla", "cos(D_N, D_528)", "% target", "accuracy", "target y correcta", "CE head"], filas)

    # ------------------------------------------------------------------ geo
    L += ["## 7. Geometria por capas (ultimo token del prompt, validacion cruzada por mitades)", ""]
    geo_csv = []
    pares = [("shared", "Dmulti"), ("shared", "Den"), ("shared", "nativo"), ("Dmulti", "nativo"),
             ("Den", "nativo"), ("rand", "nativo"), ("shared", "instr"), ("Dmulti", "instr"),
             ("nativo", "instr"), ("shared", "shared"), ("Dmulti", "Dmulti"), ("nativo", "nativo")]
    for lg in langs:
        g = load(f"{O}/geo/geo_{lg}.json")
        if not g:
            L += [f"### {lg}", "", "(falta)", ""]
            continue
        nl = g["n_capas"]
        capas = sorted(set([0, 1, nl // 4, nl // 2, (3 * nl) // 4, nl]))
        filas = []
        for x, y in pares:
            k = f"{x}~{y}"
            if k in g["cos_crossfit"]:
                v = g["cos_crossfit"][k]
                filas.append([f"cos({x}, {y})"] + [f"{v[c]:+.2f}" for c in capas])
                for c, val in enumerate(v):
                    geo_csv.append({"L": lg, "par": k, "capa": c, "cos": val})
        L += [f"### {lg} (n={g['n']}, {nl} capas)", ""]
        tabla(L, ["par"] + [f"L{c}" for c in capas], filas)
    if geo_csv:
        with open(f"{O}/geo.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(geo_csv[0]))
            w.writeheader()
            w.writerows(geo_csv)
        L += ["La diagonal (x, x) es el techo de ruido split-half. Todas las capas en "
              f"`{O}/geo.csv`.", ""]

    # ------------------------------------------------------------------ pares
    PD = f"{O}/pares"
    L += ["## 8. Pares de idiomas: D_{s->L} = mu_L - mu_s", ""]
    selp = load(f"{PD}/seleccion.json") or {}
    pares_lst = [(s_, lg) for lg in ("fr", "es", "de") for s_ in {"fr": ("es", "de"), "es": ("de", "fr"),
                                                                    "de": ("es", "fr")}[lg]]

    def cross_full(p, col, esc, src):
        d = load(p)
        if not d:
            return None
        for c in d["condiciones"]:
            if c["col"] == col and abs(float(c["escala"]) - esc) < 1e-9:
                rows = c["rows"]
                n = len(rows)
                t = [bool(r["out_is_target"]) for r in rows]
                a = [bool(r["out_answer_correct"]) for r in rows]
                tc = sum(x and y for x, y in zip(t, a))
                return {"target": sum(t) / n, "tc": tc / n, "acc_t": tc / sum(t) if sum(t) else None,
                        "origen": sum(r["out_lang"] == src for r in rows) / n}
        return None
    filas = []
    for s_, lg in pares_lst:
        par = f"{s_}2{lg}"
        j = load(f"{PD}/vec/{par}.json")
        col = f"prompt_{s_}"
        celdas = []
        for x in (cross_full(f"{R}/alg_{lg}/cross_lang_idioma.json", col, 1.0, s_),
                  cross_full(f"{O}/cross_Den/{lg}/cross_lang_cross.json", col, 1.0, s_),
                  cross_full(f"{PD}/heldout/{par}/cross_lang_par.json", col, 1.0, s_)):
            celdas.append(f"{pct(x['target'])} / {pct(x['tc'])} / {pct(x['acc_t'])} / {pct(x['origen'])}"
                          if x else "(falta)")
        filas.append([f"{s_} -> {lg}", selp.get(par, {}).get("norma", "–"),
                      f"{j['cos'].get('Den', float('nan')):+.2f}" if j else "–",
                      f"{j['cos'].get('shared', float('nan')):+.2f}" if j else "–"] + celdas)
    L += ["### Cross: q_s + vector_L (held-out)", ""]
    tabla(L, ["par", "norma", "cos(par, Den_L)", "cos(par, Shared_L)", "Shared", "Den_L", "D_{s->L}"], filas)
    L += ["Celdas: % target / % target y correcta / acc | target / % que se queda en el idioma de origen.", ""]

    dr = load(f"{PD}/tests/entrada_o_directiva_resta_pares.json")
    if dr:
        m = {c["label"]: c["metrics"] for c in dr["condiciones"]}
        filas = []
        for s_, lg in pares_lst:
            mm = m.get(f"plain | prompt_{lg} -1*{s_}2{lg}")
            base = m.get(f"plain | prompt_{lg}")
            if mm:
                filas.append([f"q_{lg} - D_{{{s_}->{lg}}}", pct(mm.get(f"p_{s_}")), pct(mm.get("p_en")),
                              pct(mm.get(f"p_{lg}")), pct(mm.get("answer_correct")),
                              pct(base.get(f"p_{lg}")) if base else "–"])
        L += ["### Resta: q_L - D_{s->L} (¿termina en el idioma de origen s?)", ""]
        tabla(L, ["condicion", "% en s (esperado)", "% en", "% se queda en L", "acc", "% L sin parche"], filas)
    else:
        L += ["### Resta por pares", "", "(falta)", ""]
    di = load(f"{PD}/tests/entrada_o_directiva_idioma_pares.json")
    if di:
        m = {c["label"]: c["metrics"] for c in di["condiciones"]}
        filas = []
        for s_, lg in pares_lst:
            mm, base = m.get(f"lang_id | prompt_{s_} +1*{s_}2{lg}"), m.get(f"lang_id | prompt_{s_}")
            if mm:
                filas.append([f"q_{s_} + D_{{{s_}->{lg}}}", pct(mm.get(f"dice_{lg}")), pct(mm.get(f"dice_{s_}")),
                              pct(base.get(f"dice_{s_}")) if base else "–"])
        L += ["### Identificacion de idioma: q_s + D_{s->L}", ""]
        tabla(L, ["condicion", "dice L", "dice s", "dice s sin parche"], filas)
    else:
        L += ["### Identificacion por pares", "", "(falta)", ""]

    os.makedirs(O, exist_ok=True)
    with open(f"{O}/resumen.md", "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("\n".join(L))
    print(f"\nescrito {O}/resumen.md")


if __name__ == "__main__":
    main()
