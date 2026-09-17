"""
Algebra de DIRECCIONES en el espacio de embeddings: idioma x formato.

Seis parches entrenados por separado, todos con anchor goal_all (UN vector
[1, 1, d] sumado a cada token de la pregunta: una direccion, no un soft prompt):

                normal      MAYUSCULAS
        fr      v_fr        v_fr_up
        es      v_es        v_es_up
        de      v_de        v_de_up

El test es el de los function vectors (last_copy + first_capital - first_copy)
y el de king - man + woman: se esconde una esquina y se la reconstruye con las
otras tres del cuadrado,

        v*_(L,f) = v_(L,f') + v_(L',f) - v_(L',f')

p.ej.   v*_fr_up = v_fr + v_es_up - v_es
        = "frances" + la direccion "mayusculas" sacada del espanol.

Ninguna esquina es el baseline (ingles normal): un parche entrenado para lo que
el modelo ya hace colapsa a ~0 con el L2 y el paralelogramo degenera en la suma
v_fr + v_up, que es el test de compose_patches.py. Con las cuatro esquinas lejos
del default, el componente comun ("salir del modo por defecto") entra dos veces
y sale una: queda exactamente una vez, como en un parche de verdad.

Tres idiomas dan 3 cuadrados (fr-es, fr-de, es-de) x 4 esquinas ocultables = 12
paralelogramos.

---------------------------------------------------------------------------
SUBCOMANDOS
---------------------------------------------------------------------------
cosines   (CPU, segundos)  geometria en el espacio del parche: normas, matriz
          de cosenos, direcciones de formato u_L = v_L_up - v_L y de idioma
          v_A - v_B, los 12 paralelogramos (cos(v*, v_real), error relativo),
          descomposicion aditiva v = c + a_L + b_f + interaccion (R2), SVD, y el
          techo de ruido con las replicas (--replica).

eval      (GPU)  comportamiento sobre el held-out: por paralelogramo genera con
              real              v_real, el parche entrenado directo: TECHO
              algebra           v* = s + o - d
              solo_s/solo_o/solo_d   cada ingrediente solo
              suma              s + o            (sin restar: aporta la resta?)
              resta_azar        s + o - r,  r gaussiano con ||r|| = ||d||
              resta_equivocada  s + o - v_(L'',f')   (el tercer idioma)
              algebra_a<alpha>  alpha * v*       (--alphas; descarta efecto de norma)
          y mide en que CELDA cae cada salida (idioma x mayusculas), celda_ok
          contra la esquina oculta, accuracy, y la CE del head del target de la
          esquina oculta. Las generaciones se cachean por vector.

acts      (GPU)  el mismo paralelogramo en ACTIVACIONES: delta del ultimo token
          del prompt, por capa (el calculo de plot_last_token.py). Separa "no
          hay geometria" de "la hay pero no en el espacio del parche".

embed     (GPU solo para cargar E)  el parche vive en el mismo espacio que la
          matriz de embeddings: tokens mas cercanos a cada direccion, y coseno
          contra offsets tipo word2vec sacados del vocabulario (E[" WORD"] -
          E[" word"], E[" maison"] - E[" house"]).

selftest  (sin torch)  la aritmetica sobre vectores sinteticos.

Convenciones de rutas (se pisan con --cell / --targets_csv nombre=ruta):
    parche   <runs_dir>/alg_<celda>/<ckpt>
    targets  <targets_dir>/targets_<celda>.csv   (fr: attributes/french/targets_french_v5.csv)

    (desde experimentos/idiomas)
    python3 algebra/algebra_patches.py cosines --replica fr=algebra/runs/alg_fr_s1/lang_patch_best_train.pt
    python3 -u algebra/algebra_patches.py eval --model $M
    python3 -u algebra/algebra_patches.py acts --model $M
    python3 -u algebra/algebra_patches.py embed --model $M
"""

import argparse
import itertools
import json
import os
import sys
import zlib

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LANGS3 = ("fr", "es", "de")
CELLS = tuple(l + s for l in LANGS3 for s in ("", "_up"))
FR_CSV = "attributes/french/targets_french_v5.csv"


# ---------------------------------------------------------------------------
# celdas y paralelogramos (sin torch)
# ---------------------------------------------------------------------------

def parse_cell(name):
    """'es_up' -> ('es', True)"""
    upper = name.endswith("_up")
    lang = name[:-3] if upper else name
    if lang not in LANGS3:
        raise SystemExit(f"celda desconocida: {name}; validas: {CELLS}")
    return lang, upper


def cell_name(lang, upper):
    return lang + ("_up" if upper else "")


def compositions(cells):
    """
    Los paralelogramos armables con las celdas disponibles. Cada uno:
        hidden  la esquina que se esconde            (L, f)
        s       mismo idioma, otro formato           (L, f')
        o       otro idioma, mismo formato           (L', f)
        d       la opuesta, la que se resta          (L', f')
        wrong   la resta equivocada: tercer idioma   (L'', f')   (None si no hay)
    """
    have = set(cells)
    out = []
    for a, b in itertools.combinations(LANGS3, 2):
        for L, L2 in ((a, b), (b, a)):
            for f in (False, True):
                c = {"hidden": cell_name(L, f), "s": cell_name(L, not f),
                     "o": cell_name(L2, f), "d": cell_name(L2, not f),
                     "square": f"{a}-{b}"}
                if not {c["hidden"], c["s"], c["o"], c["d"]} <= have:
                    continue
                L3 = [x for x in LANGS3 if x not in (L, L2)][0]
                w = cell_name(L3, not f)
                c["wrong"] = w if w in have else None
                c["name"] = f"{c['hidden']}={c['s']}+{c['o']}-{c['d']}"
                out.append(c)
    return out


def cos(a, b):
    a, b = np.asarray(a, dtype=np.float64).ravel(), np.asarray(b, dtype=np.float64).ravel()
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na > 0 and nb > 0 else float("nan")


def random_like(d_vec, tag):
    """Gaussiano con la norma de d_vec; la semilla sale del nombre del paralelogramo."""
    rng = np.random.default_rng(zlib.crc32(tag.encode()))
    r = rng.standard_normal(d_vec.shape)
    return r * (np.linalg.norm(d_vec) / np.linalg.norm(r))


def additive_fit(V):
    """
    Descomposicion de dos vias v_(L,f) = c + a_L + b_f + I_(L,f) sobre las celdas
    de V (dict nombre -> vector). Solo usa los idiomas que tienen las DOS celdas.

    R2 = 1 - sum ||I||^2 / sum ||v - c||^2 : que fraccion de la variacion entre
    celdas explica el modelo aditivo (ejes idioma (+) formato independientes).
    R2 = 1 es equivalente a que TODOS los paralelogramos cierren exactamente.
    """
    langs = [l for l in LANGS3 if l in V and l + "_up" in V]
    if len(langs) < 2:
        return None
    T = np.stack([np.stack([V[l], V[l + "_up"]]) for l in langs])      # [L, 2, d]
    c = T.mean(axis=(0, 1))
    a = T.mean(axis=1) - c                                             # [L, d]
    b = T.mean(axis=0) - c                                             # [2, d]
    inter = T - c - a[:, None, :] - b[None, :, :]
    tot = float(((T - c) ** 2).sum())
    return {
        "langs": langs,
        "r2_aditivo": 1.0 - float((inter ** 2).sum()) / tot if tot > 0 else float("nan"),
        "frac_idioma": float(2 * (a ** 2).sum()) / tot,
        "frac_formato": float(len(langs) * (b ** 2).sum()) / tot,
        "frac_interaccion": float((inter ** 2).sum()) / tot,
        "norma_c": float(np.linalg.norm(c)),
        "norma_a": {l: float(np.linalg.norm(a[i])) for i, l in enumerate(langs)},
        "norma_b_up": float(np.linalg.norm(b[1])),
        "cos_celda_c": {n: cos(V[n], c) for n in V},
        "_c": c, "_a": {l: a[i] for i, l in enumerate(langs)}, "_b_up": b[1],
    }


def geometry(V, replicas=None):
    """Todo lo que se puede decir mirando solo los vectores. V: nombre -> np [d]."""
    names = [c for c in CELLS if c in V]
    out = {"celdas": names, "dim": int(next(iter(V.values())).size),
           "cos_azar_esperado": float(1.0 / np.sqrt(next(iter(V.values())).size)),
           "normas": {n: float(np.linalg.norm(V[n])) for n in names},
           "cosenos": {a: {b: cos(V[a], V[b]) for b in names} for a in names}}

    # direcciones de formato: u_L = v_L_up - v_L. Si "mayusculas" es un eje
    # independiente del idioma, las tres se parecen.
    U = {l: V[l + "_up"] - V[l] for l in LANGS3 if l in V and l + "_up" in V}
    out["dir_formato"] = {"normas": {l: float(np.linalg.norm(u)) for l, u in U.items()},
                          "cosenos": {f"{a}~{b}": cos(U[a], U[b])
                                      for a, b in itertools.combinations(U, 2)}}
    # direcciones de idioma: w_AB = v_A - v_B, en normal y en MAYUSCULAS.
    W = {}
    for a, b in itertools.combinations(LANGS3, 2):
        if all(x in V for x in (a, b, a + "_up", b + "_up")):
            W[f"{a}-{b}"] = {"cos_normal_vs_up": cos(V[a] - V[b], V[a + "_up"] - V[b + "_up"]),
                             "norma_normal": float(np.linalg.norm(V[a] - V[b])),
                             "norma_up": float(np.linalg.norm(V[a + "_up"] - V[b + "_up"]))}
    out["dir_idioma"] = W

    # los paralelogramos
    P = []
    for c in compositions(names):
        real, s, o, d = V[c["hidden"]], V[c["s"]], V[c["o"]], V[c["d"]]
        star = s + o - d
        P.append({"name": c["name"], "square": c["square"], "hidden": c["hidden"],
                  "cos_algebra_real": cos(star, real),
                  "err_rel": float(np.linalg.norm(star - real) / np.linalg.norm(real)),
                  "norma_algebra": float(np.linalg.norm(star)),
                  "norma_real": float(np.linalg.norm(real)),
                  # contexto: lo que ya se parece v_real a cada ingrediente SIN algebra.
                  # Si cos(s, real) ya es 0.9, un cos(v*, real) de 0.9 no dice nada.
                  "cos_s_real": cos(s, real), "cos_o_real": cos(o, real),
                  "cos_suma_real": cos(s + o, real), "cos_d_real": cos(d, real),
                  "cos_azar_real": cos(s + o - random_like(d, c["name"]), real)})
    out["paralelogramos"] = P

    fit = additive_fit(V)
    if fit:
        out["aditivo"] = {k: v for k, v in fit.items() if not k.startswith("_")}
    M = np.stack([V[n] for n in names])
    sv = np.linalg.svd(M, compute_uv=False)
    svc = np.linalg.svd(M - M.mean(axis=0), compute_uv=False)
    out["svd"] = {"crudo": (sv ** 2 / (sv ** 2).sum()).tolist(),
                  "centrado": (svc ** 2 / (svc ** 2).sum()).tolist()}

    if replicas:
        out["replicas"] = {n: {"cos": cos(V[n], r), "norma_replica": float(np.linalg.norm(r)),
                               "err_rel": float(np.linalg.norm(r - V[n]) / np.linalg.norm(V[n]))}
                           for n, r in replicas.items() if n in V}
    return out


def geometry_markdown(g, paths):
    L = ["# Algebra de direcciones: geometria en el espacio del parche", ""]
    for n in g["celdas"]:
        L.append(f"- `{n}`: `{paths.get(n, '?')}`  (norma {g['normas'][n]:.4f})")
    L += ["", f"Dimension {g['dim']}: el coseno entre dos direcciones al azar es ~±{g['cos_azar_esperado']:.3f}.", ""]
    if g.get("replicas"):
        L += ["## Techo de ruido (misma celda, otro orden de datos)", "",
              "| celda | cos(original, replica) | error relativo |", "|---|---|---|"]
        for n, r in g["replicas"].items():
            L.append(f"| {n} | {r['cos']:.3f} | {r['err_rel']:.3f} |")
        L += ["", "Ningun `cos(v*, v_real)` de abajo puede superar esto de forma interpretable: es lo que "
                  "se parece un parche a SI MISMO reentrenado.", ""]
    L += ["## Cosenos entre celdas", "", "| | " + " | ".join(g["celdas"]) + " |",
          "|---|" + "---|" * len(g["celdas"])]
    for a in g["celdas"]:
        L.append(f"| **{a}** | " + " | ".join(f"{g['cosenos'][a][b]:.3f}" for b in g["celdas"]) + " |")
    L += ["", "## Paralelogramos  v* = s + o − d", "",
          "| oculta = s + o − d | cos(v*, real) | err rel | ‖v*‖ / ‖real‖ | cos(s, real) | cos(o, real) "
          "| cos(s+o, real) | cos(s+o−azar, real) |", "|---|---|---|---|---|---|---|---|"]
    for p in g["paralelogramos"]:
        L.append(f"| {p['name']} | **{p['cos_algebra_real']:.3f}** | {p['err_rel']:.3f} "
                 f"| {p['norma_algebra']:.3f} / {p['norma_real']:.3f} | {p['cos_s_real']:.3f} "
                 f"| {p['cos_o_real']:.3f} | {p['cos_suma_real']:.3f} | {p['cos_azar_real']:.3f} |")
    L += ["", "`cos(v*, real)` solo significa algo si supera a `cos(s, real)`, `cos(o, real)` y a la suma "
              "sin resta: esas columnas son lo que ya se parecia la esquina oculta a los ingredientes. "
              "OJO: si todas las celdas comparten un componente comun grande `c`, TODOS estos cosenos "
              "salen altos aunque no haya ninguna estructura (v = c + ruido ya da cos(v*, real) > 0). "
              "El test libre de `c` es el de las dos secciones que siguen: son diferencias, `c` se "
              "cancela, y sin estructura dan ~0. Cerrar el paralelogramo `fr_up = fr + es_up − es` es "
              "exactamente pedir `u_fr = u_es`.", ""]
    L += ["## Direcciones de formato  u_L = v_L_up − v_L", ""]
    for k, v in g["dir_formato"]["cosenos"].items():
        L.append(f"- cos(u_{k.replace('~', ', u_')}) = **{v:.3f}**")
    L.append("- normas: " + ", ".join(f"u_{l} {v:.3f}" for l, v in g["dir_formato"]["normas"].items()))
    L += ["", "Si \"mayusculas\" es un eje independiente del idioma, las tres se parecen.", "",
          "## Direcciones de idioma  v_A − v_B, en normal vs en MAYUSCULAS", ""]
    for k, v in g["dir_idioma"].items():
        L.append(f"- {k}: cos = **{v['cos_normal_vs_up']:.3f}**  (normas {v['norma_normal']:.3f} / {v['norma_up']:.3f})")
    if "aditivo" in g:
        a = g["aditivo"]
        L += ["", "## Modelo aditivo  v = c + a_idioma + b_formato + interaccion", "",
              f"- **R² aditivo = {a['r2_aditivo']:.3f}**  (1.0 = todos los paralelogramos cierran exactos; "
              f"**{len(a['langs']) / (2 * len(a['langs']) - 1):.2f} es lo que dan celdas AL AZAR**, por "
              "grados de libertad: el piso no es 0)",
              f"- variacion entre celdas: idioma {a['frac_idioma']:.1%}, formato {a['frac_formato']:.1%}, "
              f"interaccion {a['frac_interaccion']:.1%}",
              f"- componente comun c: norma {a['norma_c']:.3f}; cos(celda, c): "
              + ", ".join(f"{n} {v:.2f}" for n, v in a["cos_celda_c"].items()),
              f"- normas: a_idioma {', '.join(f'{l} {v:.3f}' for l, v in a['norma_a'].items())}; "
              f"b_MAYUS {a['norma_b_up']:.3f}"]
    L += ["", "## SVD de las celdas (fraccion de energia por componente)", "",
          "- crudo:    " + "  ".join(f"{x:.3f}" for x in g["svd"]["crudo"]),
          "- centrado: " + "  ".join(f"{x:.3f}" for x in g["svd"]["centrado"]),
          "", "Centrado y aditivo perfecto con 3 idiomas x 2 formatos serian 3 componentes (2 de idioma + 1 "
              "de formato); energia en la 4a y 5a es interaccion."]
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# carga (torch)
# ---------------------------------------------------------------------------

def parse_kv(specs):
    out = {}
    for s in specs or []:
        k, v = s.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def resolve_paths(args):
    over = parse_kv(args.cell)
    cells = [c.strip() for c in args.cells.split(",") if c.strip()]
    for c in cells:
        parse_cell(c)
    paths = {c: over.get(c, os.path.join(args.runs_dir, f"alg_{c}", args.ckpt)) for c in cells}
    faltan = [f"{c} -> {p}" for c, p in paths.items() if not os.path.exists(p)]
    if faltan:
        raise SystemExit("parches que no existen:\n  " + "\n  ".join(faltan))
    return paths


def load_vectors(paths):
    import torch
    V = {}
    for n, p in paths.items():
        t = torch.load(p, map_location="cpu").float()
        if t.dim() != 3 or t.shape[0] != 1 or t.shape[1] != 1:
            raise SystemExit(f"{n}: shape {tuple(t.shape)}; el algebra es sobre DIRECCIONES "
                             "(anchor goal_all, parche [1, 1, d])")
        V[n] = t[0, 0].double().numpy()
    return V


def load_heldout(args, cells):
    """Held-out de cada celda, verificando que las filas sean las mismas en todas."""
    import pandas as pd
    over = parse_kv(args.targets_csv)
    H, ref = {}, None
    for c in cells:
        p = over.get(c, FR_CSV if c == "fr" else os.path.join(args.targets_dir, f"targets_{c}.csv"))
        if not os.path.exists(p):
            raise SystemExit(f"falta el targets CSV de {c}: {p}")
        df = pd.read_csv(p, sep=";", keep_default_na=False)
        h = df.iloc[int(len(df) * args.train_test_split):]
        if args.n > 0:
            h = h.head(args.n)
        h = h.reset_index(drop=True)
        if ref is None:
            ref = list(h["prompt"])
        elif list(h["prompt"]) != ref:
            raise SystemExit(f"el held-out de {c} ({p}) no tiene las mismas preguntas que el de {cells[0]}: "
                             "las celdas tienen que salir del mismo CSV base (generate_targets_attr.py)")
        H[c] = h
    return H


# ---------------------------------------------------------------------------
# cosines
# ---------------------------------------------------------------------------

def cmd_cosines(args):
    paths = resolve_paths(args)
    V = load_vectors(paths)
    rep_paths = parse_kv(args.replica)
    R = load_vectors(rep_paths) if rep_paths else None
    g = geometry(V, R)
    os.makedirs(args.out_dir, exist_ok=True)
    json.dump({"parches": paths, "replicas": rep_paths, **g},
              open(os.path.join(args.out_dir, "cosines.json"), "w", encoding="utf-8"), indent=1)
    md = geometry_markdown(g, paths)
    open(os.path.join(args.out_dir, "cosines.md"), "w", encoding="utf-8").write(md)
    print(md)
    print(f"Guardado: {os.path.join(args.out_dir, 'cosines.json')}  y  cosines.md")


# ---------------------------------------------------------------------------
# eval
# ---------------------------------------------------------------------------

def cell_of(text):
    """En que celda cae una salida: 'fr_up', 'es', 'en', 'en_up', 'unknown', ..."""
    from checkers import is_uppercase, language_verdict
    return language_verdict(text) + ("_up" if is_uppercase(text) else "")


def build_conditions(comp, V, alphas):
    """[(nombre, clave de cache, vector np)] de un paralelogramo."""
    s, o, d = V[comp["s"]], V[comp["o"]], V[comp["d"]]
    star = s + o - d
    conds = [("real", ("cell", comp["hidden"]), V[comp["hidden"]]),
             ("algebra", ("star", comp["name"]), star),
             ("solo_s", ("cell", comp["s"]), s),
             ("solo_o", ("cell", comp["o"]), o),
             ("solo_d", ("cell", comp["d"]), d),
             # s + o es la misma suma para las dos esquinas opuestas del cuadrado
             ("suma", ("sum",) + tuple(sorted((comp["s"], comp["o"]))), s + o),
             ("resta_azar", ("rand", comp["name"]), s + o - random_like(d, comp["name"]))]
    if comp["wrong"]:
        conds.append(("resta_equivocada", ("wrong", comp["name"]), s + o - V[comp["wrong"]]))
    for a in alphas:
        if abs(a - 1.0) > 1e-9:
            conds.append((f"algebra_a{a:g}", ("star", comp["name"], a), a * star))
    return conds


def cmd_eval(args):
    import torch
    import tqdm

    from checkers import answer_correct, attr_ok, is_lang, is_uppercase, truncate_at_role_leak
    from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer, nll_of_target

    paths = resolve_paths(args)
    V = load_vectors(paths)
    cells = list(paths)
    H = load_heldout(args, cells)
    comps = compositions(cells)
    if args.squares:
        keep = {s.strip() for s in args.squares.split(",")}
        comps = [c for c in comps if c["square"] in keep]
    if args.hide:
        keep = {s.strip() for s in args.hide.split(",")}
        comps = [c for c in comps if c["hidden"] in keep]
    if not comps:
        raise SystemExit("no quedo ningun paralelogramo (revisar --cells / --squares / --hide)")
    alphas = [float(a) for a in args.alphas.split(",") if a.strip()] if args.alphas else []

    model, tokenizer = load_model_and_tokenizer(args.model or DEFAULT_MODEL, device=args.device)
    prompts = list(H[cells[0]][args.col])
    print(f"held-out: {len(prompts)} preguntas (columna {args.col})  |  paralelogramos: {len(comps)}")

    def as_patch(vec):
        return torch.tensor(np.asarray(vec), dtype=torch.float32, device=args.device).view(1, 1, -1)

    gen_cache = {}

    def generate(key, vec):
        if key not in gen_cache:
            p = as_patch(vec)
            outs = []
            for q in tqdm.tqdm(prompts, desc=" ".join(map(str, key))[:48], leave=False):
                raw = generate_one(model, tokenizer, q, args.device, args.num_tokens, 0.0, patch=p,
                                   num_patch_positions=1, clean=False, patch_anchor="goal_all")
                outs.append(truncate_at_role_leak(raw))
            gen_cache[key] = outs
        return gen_cache[key]

    def ce_head(vec, hidden):
        p = None if vec is None else as_patch(vec)
        vals = []
        for q, tgt in zip(prompts, H[hidden]["output"]):
            r = nll_of_target(model, tokenizer, q, tgt, args.device, patch=p, num_patch_positions=1,
                              head_k=args.head_k, patch_anchor="goal_all")
            if r["head"] == r["head"]:
                vals.append(r["head"])
        return sum(vals) / len(vals) if vals else float("nan")

    def score(outs, hidden):
        lang, upper = parse_cell(hidden)
        h = H[hidden]
        n = max(1, len(outs))
        accs = [bool(answer_correct(t, a, al)) for t, a, al in zip(outs, h["answer"], h["aliases"])
                if str(a).strip() != ""]
        dist = {}
        for t in outs:
            k = cell_of(t)
            dist[k] = dist.get(k, 0) + 1
        return {"n": len(outs),
                "celda_ok": sum(attr_ok(t, lang, upper) for t in outs) / n,
                "idioma_ok": sum(is_lang(t, lang) for t in outs) / n,
                "mayus": sum(is_uppercase(t) for t in outs) / n,
                "accuracy": sum(accs) / len(accs) if accs else float("nan"),
                "largo": sum(len(t) for t in outs) / n,
                "caen_en": {k: v / n for k, v in sorted(dist.items(), key=lambda kv: -kv[1])}}

    resultados = []
    for comp in comps:
        print(f"\n=== {comp['name']}   (cuadrado {comp['square']})")
        hidden = comp["hidden"]
        base = list(H[hidden]["baseline_en"])
        conds = {"sin_parche": {**score(base, hidden), "ce_head": ce_head(None, hidden), "norma": 0.0}}
        textos = {"sin_parche": base, "referencia_texto": list(H[hidden]["output"])}
        for nombre, key, vec in build_conditions(comp, V, alphas):
            outs = generate(key, vec)
            conds[nombre] = {**score(outs, hidden), "ce_head": ce_head(vec, hidden),
                             "norma": float(np.linalg.norm(vec))}
            textos[nombre] = outs
            m = conds[nombre]
            print(f"  {nombre:<18} celda_ok={m['celda_ok']:.2f}  idioma={m['idioma_ok']:.2f}  "
                  f"mayus={m['mayus']:.2f}  acc={m['accuracy']:.2f}  ce_head={m['ce_head']:.3f}  "
                  f"norma={m['norma']:.3f}  cae en {dict(list(m['caen_en'].items())[:3])}")
        conds["referencia_texto"] = {**score(textos["referencia_texto"], hidden),
                                     "ce_head": float("nan"), "norma": 0.0}
        resultados.append({**comp, "condiciones": conds,
                           "rows": [{"prompt": q, **{k: v[i] for k, v in textos.items()}}
                                    for i, q in enumerate(prompts)]})

    rep = {"objetivo": "algebra de direcciones idioma x formato: comportamiento",
           "parches": paths, "config": {k: v for k, v in vars(args).items() if k != "func"},
           "n_heldout": len(prompts), "paralelogramos": resultados}
    os.makedirs(args.out_dir, exist_ok=True)
    jp = os.path.join(args.out_dir, "algebra_eval.json")
    json.dump(rep, open(jp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(args.out_dir, "algebra_eval.md"), "w", encoding="utf-8").write(eval_markdown(rep))
    print(f"\nGuardado: {jp}  y  algebra_eval.md")


def _t(s, n=120):
    s = str(s).replace("\n", " / ").replace("|", "\\|")
    return s if len(s) <= n else s[:n] + "..."


def eval_markdown(rep):
    orden = ["referencia_texto", "real", "algebra", "suma", "resta_azar", "resta_equivocada",
             "solo_s", "solo_o", "solo_d", "sin_parche"]
    L = ["# Algebra de direcciones: comportamiento sobre el held-out", "",
         f"n = {rep['n_heldout']} preguntas. `celda ok` = la salida cae en la esquina OCULTA (idioma y formato).",
         "", "## Resumen: celda ok por condicion", "",
         "| oculta = s + o − d | texto | **real** (techo) | **algebra** | suma s+o | resta azar | resta equiv. "
         "| solo s | solo o | solo d | sin parche |", "|---|" + "---|" * 10]
    for r in rep["paralelogramos"]:
        c = r["condiciones"]
        L.append(f"| {r['name']} | " + " | ".join(
            (f"**{c[k]['celda_ok']:.2f}**" if k in ("real", "algebra") else f"{c[k]['celda_ok']:.2f}")
            if k in c else "—" for k in orden) + " |")
    L += ["", "Lectura: el algebra funciona si `algebra` se acerca a `real` Y supera a `suma`, `resta azar`, "
              "`resta equiv.` y a los tres ingredientes solos. Si `suma` ya alcanza, la resta no aporta; si "
              "`resta azar` alcanza, restar `d` no tiene nada de especial. `resta equiv.` resta la celda del "
              "TERCER idioma en el formato de `d`: en un mundo aditivo eso tambien cancela el componente "
              "comun y el formato, pero deja una mezcla de idiomas (L + L' − L''); si rinde igual que "
              "`algebra`, lo que hace la resta es sacar `c` y el formato, no cancelar el idioma de `o`.", ""]
    for r in rep["paralelogramos"]:
        L += [f"## {r['name']}", "",
              "| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |",
              "|---|---|---|---|---|---|---|---|---|"]
        extra = [k for k in r["condiciones"] if k not in orden]
        for k in orden + extra:
            if k not in r["condiciones"]:
                continue
            m = r["condiciones"][k]
            caen = ", ".join(f"{a} {b:.2f}" for a, b in list(m["caen_en"].items())[:4])
            L.append(f"| {k} | {m['celda_ok']:.2f} | {m['idioma_ok']:.2f} | {m['mayus']:.2f} "
                     f"| {m['accuracy']:.2f} | {m['ce_head']:.3f} | {m['norma']:.3f} | {m['largo']:.0f} | {caen} |")
        L += ["", "| # | pregunta | real | algebra | suma | resta azar |", "|---|---|---|---|---|---|"]
        for i, row in enumerate(r["rows"][:12]):
            L.append(f"| {i} | {_t(row['prompt'], 50)} | {_t(row.get('real', ''))} | {_t(row.get('algebra', ''))} "
                     f"| {_t(row.get('suma', ''))} | {_t(row.get('resta_azar', ''))} |")
        L.append("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# acts: el paralelogramo en activaciones
# ---------------------------------------------------------------------------

def cmd_acts(args):
    import torch
    import tqdm

    from lm import (DEFAULT_MODEL, apply_patch_first_n, build_suffix_manager, get_embeddings,
                    load_model_and_tokenizer)

    paths = resolve_paths(args)
    V = load_vectors(paths)
    cells = list(paths)
    H = load_heldout(args, cells[:1])
    prompts = list(H[cells[0]][args.col])
    comps = compositions(cells)
    model, tokenizer = load_model_and_tokenizer(args.model or DEFAULT_MODEL, device=args.device)

    @torch.no_grad()
    def h_last(text, vec=None):
        """hidden states de todas las capas en la ULTIMA posicion del prompt -> np [L+1, d].
        Mismo calculo que plot_last_token.compute."""
        sm = build_suffix_manager(tokenizer, text, target="")
        tokens = sm.get_input_ids().to(args.device)
        emb = get_embeddings(model, tokens.unsqueeze(0)).detach()
        if vec is not None:
            p = torch.tensor(np.asarray(vec), dtype=torch.float32, device=args.device).view(1, 1, -1)
            emb = apply_patch_first_n(sm, emb, p, 1, anchor="goal_all")
        emb = emb[:, : sm._assistant_role_slice.stop, :]
        out = model(inputs_embeds=emb, output_hidden_states=True)
        return torch.stack([h[0, -1, :].float() for h in out.hidden_states]).cpu().numpy()

    vecs = {("cell", c): V[c] for c in cells}
    for c in comps:
        vecs[("star", c["name"])] = V[c["s"]] + V[c["o"]] - V[c["d"]]
    D = {k: [] for k in vecs}                                   # clave -> [n, L+1, d]
    for q in tqdm.tqdm(prompts, desc="activaciones"):
        hb = h_last(q)
        for k, v in vecs.items():
            D[k].append(h_last(q, v) - hb)
    D = {k: np.stack(v).astype(np.float64) for k, v in D.items()}
    nL = next(iter(D.values())).shape[1]

    def cos_medias(a, b):                                       # cos de las medias, por capa
        ma, mb = a.mean(axis=0), b.mean(axis=0)
        return [cos(ma[l], mb[l]) for l in range(nL)]

    def media_cos(a, b):                                        # media de cosenos prompt a prompt
        return [float(np.mean([cos(a[i, l], b[i, l]) for i in range(a.shape[0])])) for l in range(nL)]

    out = {"objetivo": "paralelogramo en activaciones, ultimo token del prompt, por capa",
           "parches": paths, "n_prompts": len(prompts), "n_layers": nL - 1, "paralelogramos": []}
    for c in comps:
        real, s, o, d = (D[("cell", c[k])] for k in ("hidden", "s", "o", "d"))
        star_in = D[("star", c["name"])]          # lo que hace v* metido en el embedding
        star_act = s + o - d                      # el paralelogramo hecho EN activaciones
        out["paralelogramos"].append({
            "name": c["name"], "square": c["square"],
            "cos_medias_vstar_real": cos_medias(star_in, real),
            "media_cos_vstar_real": media_cos(star_in, real),
            "cos_medias_actalg_real": cos_medias(star_act, real),
            "media_cos_actalg_real": media_cos(star_act, real),
            "cos_medias_s_real": cos_medias(s, real),
            "cos_medias_o_real": cos_medias(o, real),
            "cos_medias_suma_real": cos_medias(s + o, real)})
    os.makedirs(args.out_dir, exist_ok=True)
    jp = os.path.join(args.out_dir, "algebra_acts.json")
    json.dump(out, open(jp, "w", encoding="utf-8"), indent=1)

    capas = [l for l in (4, 8, 12, 16, 20, 24, nL - 1) if l < nL]
    L = ["# Algebra de direcciones: el paralelogramo en activaciones", "",
         f"Delta del ultimo token del prompt contra la pregunta sin parche, n = {len(prompts)}. "
         "La capa 0 no significa nada con goal_all (el ultimo token no se toca).", "",
         "- `v* → real`: activaciones que produce v* (el vector compuesto, metido en el embedding) contra las de v_real.",
         "- `act → real`: Δh(s) + Δh(o) − Δh(d), el algebra hecha directamente en activaciones, contra Δh(real).",
         "- `s → real`, `suma → real`: contexto, lo que ya se parecian sin algebra.", ""]
    for stat, tit in (("cos_medias", "coseno de las medias"), ("media_cos", "media de cosenos prompt a prompt")):
        L += [f"## {tit}", "", "| paralelogramo | serie | " + " | ".join(f"L{l}" for l in capas) + " |",
              "|---|---|" + "---|" * len(capas)]
        for p in out["paralelogramos"]:
            series = [("v* → real", f"{stat}_vstar_real"), ("act → real", f"{stat}_actalg_real")]
            if stat == "cos_medias":
                series += [("s → real", "cos_medias_s_real"), ("suma → real", "cos_medias_suma_real")]
            for lbl, key in series:
                L.append(f"| {p['name']} | {lbl} | " + " | ".join(f"{p[key][l]:.3f}" for l in capas) + " |")
        L.append("")
    open(os.path.join(args.out_dir, "algebra_acts.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[:60]))
    print(f"\nGuardado: {jp}  y  algebra_acts.md")


# ---------------------------------------------------------------------------
# embed: el parche contra la matriz de embeddings
# ---------------------------------------------------------------------------

# en -> (fr, es, de). Solo entran los pares donde las palabras son UN token con
# espacio adelante; el filtro se hace en runtime contra el tokenizer.
PARES = [
    ("water", "eau", "agua", "Wasser"), ("house", "maison", "casa", "Haus"), ("time", "temps", "tiempo", "Zeit"),
    ("day", "jour", "día", "Tag"), ("night", "nuit", "noche", "Nacht"), ("world", "monde", "mundo", "Welt"),
    ("life", "vie", "vida", "Leben"), ("man", "homme", "hombre", "Mann"), ("woman", "femme", "mujer", "Frau"),
    ("city", "ville", "ciudad", "Stadt"), ("country", "pays", "país", "Land"), ("year", "année", "año", "Jahr"),
    ("book", "livre", "libro", "Buch"), ("hand", "main", "mano", "Hand"), ("head", "tête", "cabeza", "Kopf"),
    ("friend", "ami", "amigo", "Freund"), ("work", "travail", "trabajo", "Arbeit"),
    ("white", "blanc", "blanco", "weiß"), ("black", "noir", "negro", "schwarz"), ("red", "rouge", "rojo", "rot"),
    ("green", "vert", "verde", "grün"), ("big", "grand", "grande", "groß"), ("small", "petit", "pequeño", "klein"),
    ("new", "nouveau", "nuevo", "neu"), ("old", "vieux", "viejo", "alt"), ("good", "bon", "bueno", "gut"),
    ("with", "avec", "con", "mit"), ("without", "sans", "sin", "ohne"), ("where", "où", "donde", "wo"),
    ("when", "quand", "cuando", "wann"), ("because", "parce", "porque", "weil"),
    ("always", "toujours", "siempre", "immer"), ("never", "jamais", "nunca", "nie"),
    ("today", "aujourd", "hoy", "heute"), ("yes", "oui", "sí", "ja"), ("king", "roi", "rey", "König"),
    ("queen", "reine", "reina", "Königin"), ("sun", "soleil", "sol", "Sonne"), ("moon", "lune", "luna", "Mond"),
    ("sea", "mer", "mar", "Meer"), ("fire", "feu", "fuego", "Feuer"), ("earth", "terre", "tierra", "Erde"),
    ("love", "amour", "amor", "Liebe"), ("war", "guerre", "guerra", "Krieg"), ("peace", "paix", "paz", "Frieden"),
    ("bread", "pain", "pan", "Brot"), ("milk", "lait", "leche", "Milch"), ("dog", "chien", "perro", "Hund"),
    ("cat", "chat", "gato", "Katze"), ("and", "et", "y", "und"), ("but", "mais", "pero", "aber"),
    ("the", "le", "el", "der"), ("is", "est", "es", "ist"), ("in", "dans", "en", "in"),
]


def cmd_embed(args):
    import torch

    from lm import DEFAULT_MODEL, get_embedding_matrix, load_model_and_tokenizer

    paths = resolve_paths(args)
    V = load_vectors(paths)
    model, tokenizer = load_model_and_tokenizer(args.model or DEFAULT_MODEL, device=args.device)
    E = get_embedding_matrix(model).detach().float().cpu().numpy().astype(np.float64)
    del model
    # La matriz de embeddings tiene una media comun grande: sin centrar, todos los
    # cosenos contra tokens salen parecidos. Los offsets (diferencias) no la necesitan.
    Ec = E - E.mean(axis=0, keepdims=True)
    En = Ec / np.maximum(np.linalg.norm(Ec, axis=1, keepdims=True), 1e-12)

    def one_tok(word):
        ids = tokenizer.encode(" " + word, add_special_tokens=False)
        return ids[0] if len(ids) == 1 else None

    def vecinos(v, k):
        sims = En @ (v / np.linalg.norm(v))
        top, bot = np.argsort(-sims)[:k], np.argsort(sims)[:k]
        f = lambda idx: [[tokenizer.decode([int(i)]), round(float(sims[i]), 3)] for i in idx]
        return {"cerca": f(top), "lejos": f(bot)}

    dirs = dict(V)
    for l in LANGS3:
        if l in V and l + "_up" in V:
            dirs[f"u_{l} (={l}_up-{l})"] = V[l + "_up"] - V[l]
    for a, b in itertools.combinations(LANGS3, 2):
        if a in V and b in V:
            dirs[f"{a}-{b}"] = V[a] - V[b]
    fit = additive_fit(V)
    if fit:
        dirs["c (comun)"] = fit["_c"]
        dirs["b_MAYUS (aditivo)"] = fit["_b_up"]
        for l, a in fit["_a"].items():
            dirs[f"a_{l} (aditivo)"] = a
    out = {"parches": paths, "vecinos": {n: vecinos(v, args.k) for n, v in dirs.items()}}

    # --- offset de mayusculas, sacado del vocabulario -------------------------
    pares_up = []
    for i in range(E.shape[0]):
        s = tokenizer.decode([i])
        core = s[1:]
        if not (s.startswith(" ") and len(core) >= 3 and core.isascii() and core.isalpha() and core.islower()):
            continue
        j = one_tok(core.upper())
        if j is not None:
            pares_up.append((i, j))
    if pares_up:
        lo, up = np.array(pares_up).T
        diffs = E[up] - E[lo]
        off_up = diffs.mean(axis=0)
        mitad = len(diffs) // 2
        out["offset_mayusculas"] = {
            "n_pares": len(pares_up),
            "ejemplos": [[tokenizer.decode([int(a)]), tokenizer.decode([int(b)])] for a, b in pares_up[:12]],
            "techo_split_half": cos(diffs[:mitad].mean(axis=0), diffs[mitad:].mean(axis=0)),
            "cos": {n: cos(v, off_up) for n, v in dirs.items()}}

    # --- offsets de traduccion ---------------------------------------------------
    off_lang, usados = {}, {}
    for li, l in enumerate(LANGS3):
        dif, us = [], []
        for par in PARES:
            a, b = one_tok(par[0]), one_tok(par[li + 1])
            if a is not None and b is not None and a != b:
                dif.append(E[b] - E[a])
                us.append(f"{par[0]}>{par[li + 1]}")
        if len(dif) >= 5:
            off_lang[l] = np.mean(dif, axis=0)
            usados[l] = us
    out["offset_traduccion"] = {
        "pares_usados": usados,
        "cos": {l: {n: cos(v, off) for n, v in dirs.items()} for l, off in off_lang.items()},
        "entre_offsets": {f"{a}~{b}": cos(off_lang[a], off_lang[b])
                          for a, b in itertools.combinations(off_lang, 2)},
        # el analogo directo: la direccion de idioma del parche contra la del vocabulario
        "dir_idioma": {f"{a}-{b}": cos(V[a] - V[b], off_lang[a] - off_lang[b])
                       for a, b in itertools.combinations(off_lang, 2) if a in V and b in V}}

    os.makedirs(args.out_dir, exist_ok=True)
    jp = os.path.join(args.out_dir, "algebra_embed.json")
    json.dump(out, open(jp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    L = ["# Algebra de direcciones: los parches contra la matriz de embeddings", "",
         f"Cosenos al azar en esta dimension: ~±{1 / np.sqrt(E.shape[1]):.3f}.", ""]
    om = out.get("offset_mayusculas")
    if om:
        L += [f"## Offset de mayusculas del vocabulario  (mean E[\" WORD\"] − E[\" word\"], {om['n_pares']} pares, "
              f"techo split-half {om['techo_split_half']:.3f})", "", "| direccion | cos |", "|---|---|"]
        L += [f"| {n} | {v:.3f} |" for n, v in om["cos"].items()]
        L.append("")
    ot = out["offset_traduccion"]
    if ot["cos"]:
        ls = list(ot["cos"])
        L += ["## Offsets de traduccion del vocabulario  (mean E[palabra_L] − E[palabra_en])", "",
              "pares usados: " + ", ".join(f"{l} {len(u)}" for l, u in ot["pares_usados"].items()), "",
              "| direccion | " + " | ".join(f"offset {l}" for l in ls) + " |", "|---|" + "---|" * len(ls)]
        for n in dirs:
            L.append(f"| {n} | " + " | ".join(f"{ot['cos'][l][n]:.3f}" for l in ls) + " |")
        L += ["", "direccion de idioma del parche contra la del vocabulario: "
              + ", ".join(f"{k} {v:.3f}" for k, v in ot["dir_idioma"].items()),
              "offsets entre si: " + ", ".join(f"{k} {v:.3f}" for k, v in ot["entre_offsets"].items()), ""]
    L += ["## Tokens mas cercanos y mas lejanos (embeddings centrados)", ""]
    for n, vv in out["vecinos"].items():
        L.append(f"- **{n}**  cerca: " + " ".join(f"`{t}`" for t, _ in vv["cerca"])
                 + f"  ({vv['cerca'][0][1]:.2f})   lejos: " + " ".join(f"`{t}`" for t, _ in vv["lejos"])
                 + f"  ({vv['lejos'][0][1]:.2f})")
    open(os.path.join(args.out_dir, "algebra_embed.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\nGuardado: {jp}  y  algebra_embed.md")


# ---------------------------------------------------------------------------
# selftest (sin torch)
# ---------------------------------------------------------------------------

def cmd_selftest(_):
    rng = np.random.default_rng(0)
    d = 3072
    c = rng.standard_normal(d) * 0.5
    a = {l: rng.standard_normal(d) * 0.4 for l in LANGS3}
    b = {False: rng.standard_normal(d) * 0.15, True: rng.standard_normal(d) * 0.3}

    def mk(noise):
        return {cell_name(l, f): c + a[l] + b[f] + noise * rng.standard_normal(d)
                for l in LANGS3 for f in (False, True)}

    comps = compositions(CELLS)
    ok = len(comps) == 12 and len({x["name"] for x in comps}) == 12
    print(f"paralelogramos: {len(comps)} (esperados 12)  -> {'OK' if ok else 'FAIL'}")
    print("  " + "\n  ".join(f"{x['name']:<26} resta equivocada: {x['wrong']}" for x in comps[:4]))

    g = geometry(mk(0.0))
    exacto = all(abs(p["cos_algebra_real"] - 1) < 1e-9 and p["err_rel"] < 1e-9 for p in g["paralelogramos"])
    print(f"aditivo exacto: cos(v*, real)=1 en los 12, R2={g['aditivo']['r2_aditivo']:.4f}  -> "
          f"{'OK' if exacto and abs(g['aditivo']['r2_aditivo'] - 1) < 1e-9 else 'FAIL'}")
    ok &= exacto
    u = list(g["dir_formato"]["cosenos"].values())
    print(f"  direcciones de formato identicas: {[round(x, 3) for x in u]}  -> {'OK' if min(u) > 0.999 else 'FAIL'}")
    ok &= min(u) > 0.999
    print(f"  energia SVD centrada: {[round(x, 3) for x in g['svd']['centrado']]}  (3 componentes)")
    ok &= sum(g["svd"]["centrado"][3:]) < 1e-9

    g2 = geometry({n: rng.standard_normal(d) for n in CELLS})
    r2 = g2["aditivo"]["r2_aditivo"]
    cs = [p["cos_algebra_real"] for p in g2["paralelogramos"]]
    # 6 vectores al azar: el modelo aditivo tiene 4 de 5 grados de libertad -> R2 ~ 0.6;
    # y cos(s + o - d, real) ~ 0 en media.
    print(f"celdas al azar: R2={r2:.3f} (esperado ~0.6, por grados de libertad)  "
          f"cos(v*, real) medio={np.mean(cs):+.3f} (esperado ~0)  -> "
          f"{'OK' if 0.4 < r2 < 0.8 and abs(np.mean(cs)) < 0.1 else 'FAIL'}")
    ok &= 0.4 < r2 < 0.8 and abs(np.mean(cs)) < 0.1

    g3 = geometry(mk(0.01), {"fr": c + a["fr"] + b[False] + 0.01 * rng.standard_normal(d)})
    print(f"aditivo + ruido: cos(v*, real)={g3['paralelogramos'][0]['cos_algebra_real']:.3f}  "
          f"replica fr cos={g3['replicas']['fr']['cos']:.3f}  R2={g3['aditivo']['r2_aditivo']:.3f}")
    r = random_like(a["fr"], "x")
    ok &= abs(np.linalg.norm(r) - np.linalg.norm(a["fr"])) < 1e-9 and np.allclose(r, random_like(a["fr"], "x"))
    print(f"resta_azar: norma igualada y determinista -> {'OK' if ok else 'FAIL'}")
    md = geometry_markdown(g3, {})
    print(f"markdown: {len(md.splitlines())} lineas")
    print("\nTODO OK" if ok else "\nHAY FALLOS")
    sys.exit(0 if ok else 1)


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def comunes(p, gpu):
        p.add_argument("--cells", default=",".join(CELLS))
        p.add_argument("--runs_dir", default="algebra/runs")
        p.add_argument("--ckpt", default="lang_patch_best_train.pt")
        p.add_argument("--cell", action="append", help="nombre=ruta.pt (pisa la convencion); repetible")
        p.add_argument("--out_dir", default="algebra/runs/geometria")
        if gpu:
            p.add_argument("--model", default=None)
            p.add_argument("--device", default="cuda:0")
            p.add_argument("--targets_dir", default="algebra/targets")
            p.add_argument("--targets_csv", action="append", help="nombre=ruta.csv; repetible")
            p.add_argument("--train_test_split", type=float, default=0.80)
            p.add_argument("--col", default="prompt", help="columna de la pregunta de entrada")
            p.add_argument("--n", type=int, default=0, help="limitar el held-out (0 = todo)")

    p = sub.add_parser("cosines"); comunes(p, False)
    p.add_argument("--replica", action="append", help="nombre=ruta.pt de la replica de esa celda; repetible")
    p.set_defaults(func=cmd_cosines)

    p = sub.add_parser("eval"); comunes(p, True)
    p.add_argument("--squares", default=None, help="p.ej. fr-es,fr-de (default: todos)")
    p.add_argument("--hide", default=None, help="solo estas esquinas ocultas, p.ej. fr_up,es_up")
    p.add_argument("--alphas", default="", help="escalas extra sobre v*, p.ej. 0.75,1.25")
    p.add_argument("--num_tokens", type=int, default=100)
    p.add_argument("--head_k", type=int, default=5)
    p.set_defaults(func=cmd_eval)

    p = sub.add_parser("acts"); comunes(p, True); p.set_defaults(func=cmd_acts)

    p = sub.add_parser("embed"); comunes(p, True)
    p.add_argument("--k", type=int, default=12, help="vecinos por direccion")
    p.set_defaults(func=cmd_embed)

    p = sub.add_parser("selftest"); p.set_defaults(func=cmd_selftest)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
