"""
Geometria de las activaciones en el ULTIMO TOKEN del prompt, por capa, para
varios parches a la vez, con los TRES estadisticos que venimos mezclando.

Todo es sobre deltas contra la misma linea de base (la pregunta sin parche):

    dp_i[l] = h(q_i + v)[l]   - h(q_i)[l]      lo que hace el parche
    dr_i[l] = h(ref_i)[l]     - h(q_i)[l]      lo que hace la referencia

referencias: frq (la pregunta en frances), instr ("Answer this in French. " + q),
qde / qes (la pregunta en aleman / espanol), de (instruccion de aleman) y corto
(instruccion de respuesta corta: el piso generico de "responder distinto").

---------------------------------------------------------------------------
LOS TRES ESTADISTICOS (no son intercambiables)
---------------------------------------------------------------------------
    cos_de_medias      cos( mean_i dp_i , mean_i dr_i )
                       Es el "mean diff" de Ball et al. (mean_diff_vectors.py).
                       Primero se promedia: el contenido por prompt se cancela y
                       queda la direccion comun. Es el mas alto de los tres y el
                       que dice "apuntan al mismo lado EN PROMEDIO".

    media_de_cosenos   mean_i cos( dp_i , dr_i )
                       Primero el coseno, prompt a prompt, despues se promedia.
                       dr_i individual esta dominado por el cambio de CONTENIDO
                       (otra tokenizacion, otras palabras), asi que sale mucho
                       mas bajo. Dice cuanto se parece el parche a la referencia
                       EN CADA PROMPT.

    media_cos_vs_dir   mean_i cos( dp_i , d_ref^(-i) ),  d_ref^(-i) = media de
                       las dr_j con j != i (leave-one-out, para que el prompt no
                       aporte a la direccion contra la que se lo mide). Es el
                       estadistico de profile.json ("media de cosenos por
                       prompt"): cuan consistentemente cada delta individual del
                       parche apunta a la direccion MEDIA de la referencia.

La brecha entre el primero y el tercero mide cuan ruidoso es el parche entre
prompts; la brecha entre el tercero y el segundo, cuan ruidosa es la referencia.

Ademas: techo por split-half de cada condicion (coseno de una condicion contra
si misma; ningun cos_de_medias puede superarlo de forma interpretable) y normas
(||media de deltas|| relativa a ||h base||).

---------------------------------------------------------------------------
USO
---------------------------------------------------------------------------
Dos pasos, a proposito: `compute` necesita GPU y escribe un JSON; `plot` solo
necesita matplotlib y se puede correr en cualquier maquina.

    python3 -u plot_last_token.py compute --model $M \\
        --targets attributes/french/targets_french_v5.csv --subset heldout --n 50 \\
        --patch pregunta=runs/v5_head_multi_l2_0.0725/lang_patch_best_train.pt \\
        --patch goal_all=runs/v5_goalall_head_multi/lang_patch_best_train.pt \\
        --patch header=runs/v5_header_head_multi/lang_patch_best_train.pt \\
        --out runs/geom_last_token/heldout.json

    python3 plot_last_token.py plot runs/geom_last_token/heldout.json

El anchor de cada parche (goal / goal_all / header) se lee de lang_metadata.pt
en la carpeta del parche; se puede forzar con nombre=ruta@anchor.

OJO con header: ahi el parche se suma SOBRE el ultimo token, asi que en la capa
0 el delta es literalmente v; con goal / goal_all el delta en la capa 0 es cero
(el ultimo token no se toca) y los cosenos de esa capa no significan nada. Los
graficos arrancan en la capa 1.
"""

import argparse
import json
import os

import numpy as np

INSTRUCTION = "Answer this in French."
CONTROLES = {"de": "Answer this in German.", "corto": "Answer this in one short sentence."}
ETIQ = {"frq": "pregunta en francés", "instr": "instrucción de francés",
        "qde": "pregunta en alemán", "qes": "pregunta en español",
        "de": "instrucción de alemán", "corto": "instrucción de respuesta corta"}
STATS = [("cos_de_medias", "coseno de las medias (mean diff)"),
         ("media_de_cosenos", "media de cosenos, prompt a prompt"),
         ("media_cos_vs_dir", "media de cosenos contra la dirección media")]


# ---------------------------------------------------------------------------
# estadisticos: numpy puro, testeables sin GPU (python3 plot_last_token.py selftest)
# ---------------------------------------------------------------------------
def _cos(a, b, axis=-1):
    num = (a * b).sum(axis)
    den = np.linalg.norm(a, axis=axis) * np.linalg.norm(b, axis=axis)
    return num / np.maximum(den, 1e-12)


def estadisticos(dp, dr):
    """dp, dr: [n, L+1, d] sobre los MISMOS prompts. -> dict de vectores por capa."""
    n = dp.shape[0]
    paired = _cos(dp, dr)                                       # [n, L+1]
    tot = dr.sum(0, keepdims=True)
    loo = (tot - dr) / max(1, n - 1)                            # [n, L+1, d]
    vs_dir = _cos(dp, loo)                                      # [n, L+1]
    return {
        "n": int(n),
        "cos_de_medias": _cos(dp.mean(0), dr.mean(0)).tolist(),
        "media_de_cosenos": paired.mean(0).tolist(),
        "media_de_cosenos_sem": (paired.std(0, ddof=1) / np.sqrt(n)).tolist(),
        "media_cos_vs_dir": vs_dir.mean(0).tolist(),
        "media_cos_vs_dir_sem": (vs_dir.std(0, ddof=1) / np.sqrt(n)).tolist(),
    }


def techo_split_half(d, n_splits=20, seed=0):
    """Coseno de una condicion contra si misma, medias de dos mitades disjuntas."""
    rng = np.random.RandomState(seed)
    n = d.shape[0]
    vals = []
    for _ in range(n_splits):
        idx = rng.permutation(n)
        vals.append(_cos(d[idx[: n // 2]].mean(0), d[idx[n // 2:]].mean(0)))
    return np.stack(vals).mean(0).tolist()


def normas(d, h_base):
    """||media de deltas|| y media de ||delta_i||, relativas a la media de ||h base||."""
    hb = np.linalg.norm(h_base, axis=-1).mean(0)                # [L+1]
    return {"norma_media": np.linalg.norm(d.mean(0), axis=-1).tolist(),
            "media_norma": np.linalg.norm(d, axis=-1).mean(0).tolist(),
            "rel_norma_media": (np.linalg.norm(d.mean(0), axis=-1) / np.maximum(hb, 1e-12)).tolist(),
            "rel_media_norma": (np.linalg.norm(d, axis=-1).mean(0) / np.maximum(hb, 1e-12)).tolist()}


# ---------------------------------------------------------------------------
# compute (GPU)
# ---------------------------------------------------------------------------
def parse_patch_spec(spec):
    """'nombre=ruta[@anchor]' -> (nombre, ruta, anchor|None)."""
    if "=" not in spec:
        raise SystemExit(f"--patch espera nombre=ruta[@anchor], llego: {spec}")
    name, rest = spec.split("=", 1)
    anchor = None
    if "@" in rest:
        rest, anchor = rest.rsplit("@", 1)
    return name.strip(), rest.strip(), (anchor.strip() if anchor else None)


def compute(args):
    import pandas as pd
    import torch
    import tqdm

    from lm import (DEFAULT_MODEL, PATCH_ANCHORS, apply_patch_first_n, build_suffix_manager,
                    get_embeddings, load_model_and_tokenizer)

    @torch.no_grad()
    def h_last(text, patch=None, anchor="goal"):
        """hidden_states de todas las capas en la ULTIMA posicion del prompt -> np [L+1, d]."""
        sm = build_suffix_manager(tokenizer, text, target="")
        tokens = sm.get_input_ids().to(args.device)
        emb = get_embeddings(model, tokens.unsqueeze(0)).detach()
        if patch is not None:
            emb = apply_patch_first_n(sm, emb, patch, patch.shape[1], anchor=anchor)
        emb = emb[:, : sm._assistant_role_slice.stop, :]
        out = model(inputs_embeds=emb, output_hidden_states=True)
        return torch.stack([h[0, -1, :].float() for h in out.hidden_states]).cpu().numpy()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False, dtype=str)
    corte = int(len(df) * args.train_test_split)
    if args.subset == "heldout":
        df = df.iloc[corte:]
    elif args.subset == "train":
        df = df.iloc[:corte]
    base_col = args.base_col

    def ok(row, col):
        return (str(row.get(col, "")).strip() != ""
                and str(row.get(f"{col}_ok", "True")).strip().lower() != "false")

    # referencias por columna traducida: solo las que el CSV tiene y que no son la base
    ref_cols = {k: c for k, c in (("frq", "prompt_fr"), ("qde", "prompt_de"), ("qes", "prompt_es"))
                if c in df.columns and c != base_col}
    # la muestra se define por la base y por prompt_fr (la referencia principal), para que
    # todas las condiciones se midan sobre los MISMOS prompts
    df = df[[ok(r, base_col) and ("frq" not in ref_cols or ok(r, "prompt_fr")) for _, r in df.iterrows()]]
    if args.n > 0:
        df = df.head(args.n)
    if len(df) < 6:
        raise SystemExit(f"muy pocos prompts usables: {len(df)}")

    model, tokenizer = load_model_and_tokenizer(args.model or DEFAULT_MODEL, device=args.device)

    patches = {}
    for spec in args.patch:
        name, path, anchor = parse_patch_spec(spec)
        if anchor is None:
            meta = os.path.join(os.path.dirname(path), "lang_metadata.pt")
            anchor = (torch.load(meta, map_location="cpu").get("patch_anchor", "goal")
                      if os.path.exists(meta) else "goal")
        if anchor not in PATCH_ANCHORS:
            raise SystemExit(f"{name}: anchor desconocido {anchor}; validos {PATCH_ANCHORS}")
        p = torch.load(path, map_location=args.device).to(args.device) * args.scale
        patches[name] = {"path": path, "anchor": anchor, "t": p,
                         "norm": float(p.norm(2).item()), "shape": list(p.shape)}
        print(f"parche {name:<12} anchor={anchor:<9} shape={tuple(p.shape)} norma={p.norm(2).item():.4f}  {path}")
    print(f"prompts: {len(df)} ({args.subset}, filas {df.index.min()}..{df.index.max()})  |  base: {base_col}"
          f"  |  referencias: {list(ref_cols) + ['instr'] + ([] if args.no_controls else list(CONTROLES))}")

    ctrl = {} if args.no_controls else CONTROLES
    H = []                                                  # h base
    DP = {k: [] for k in patches}
    DR = {k: [] for k in list(ref_cols) + ["instr"] + list(ctrl)}
    valid = {k: [] for k in DR}                             # que filas entran en cada referencia
    for _, r in tqdm.tqdm(df.iterrows(), total=len(df), desc="activaciones"):
        q = r[base_col]
        hb = h_last(q)
        H.append(hb)
        for k, p in patches.items():
            DP[k].append(h_last(q, p["t"], p["anchor"]) - hb)
        for k, col in ref_cols.items():
            usable = ok(r, col)
            valid[k].append(usable)
            DR[k].append(h_last(r[col]) - hb if usable else np.zeros_like(hb))
        DR["instr"].append(h_last(f"{args.instruction} {q}") - hb); valid["instr"].append(True)
        for k, ins in ctrl.items():
            DR[k].append(h_last(f"{ins} {q}") - hb); valid[k].append(True)

    H = np.stack(H)
    DP = {k: np.stack(v) for k, v in DP.items()}
    DR = {k: np.stack(v) for k, v in DR.items()}
    valid = {k: np.array(v, dtype=bool) for k, v in valid.items()}

    out = {"objetivo": "geometria en el ultimo token del prompt, por capa",
           "targets": args.targets, "subset": args.subset, "base_col": base_col,
           "n_prompts": int(len(df)), "rows": [int(df.index.min()), int(df.index.max())],
           "instruction": args.instruction, "scale": args.scale,
           "n_layers": int(H.shape[1] - 1),
           "parches": {k: {kk: vv for kk, vv in p.items() if kk != "t"} for k, p in patches.items()},
           "referencias": list(DR), "stats": {}, "refs_entre_si": {},
           "techos": {}, "normas": {}}
    for pk, dp in DP.items():
        out["stats"][pk] = {rk: estadisticos(dp[valid[rk]], dr[valid[rk]]) for rk, dr in DR.items()}
        out["techos"][pk] = techo_split_half(dp)
        out["normas"][pk] = normas(dp, H)
    for rk, dr in DR.items():
        out["techos"][rk] = techo_split_half(dr[valid[rk]])
        out["normas"][rk] = normas(dr[valid[rk]], H[valid[rk]])
    # entre parches y entre referencias: contexto para leer los numeros de arriba
    keys = list(DR)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            m = valid[a] & valid[b]
            out["refs_entre_si"][f"{a}~{b}"] = estadisticos(DR[a][m], DR[b][m])
    pk = list(DP)
    out["parches_entre_si"] = {f"{a}~{b}": estadisticos(DP[a], DP[b])
                               for i, a in enumerate(pk) for b in pk[i + 1:]}

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=1)
    if args.save_deltas:
        np.savez_compressed(os.path.splitext(args.out)[0] + "_deltas.npz", h_base=H.astype(np.float16),
                            **{f"patch_{k}": v.astype(np.float16) for k, v in DP.items()},
                            **{f"ref_{k}": v.astype(np.float16) for k, v in DR.items()})

    L = out["n_layers"]
    capas = [l for l in (9, 12, 14, 16, 20, 24, L) if l <= L]
    for rk in [k for k in ("frq", "instr", "corto") if k in DR]:
        print(f"\n--- contra {ETIQ.get(rk, rk)}")
        print(f"{'parche':<12}{'estadistico':<20}" + "".join(f"{'L' + str(l):>8}" for l in capas))
        for pk_ in DP:
            for sk, _ in STATS:
                v = out["stats"][pk_][rk][sk]
                print(f"{pk_:<12}{sk:<20}" + "".join(f"{v[l]:>8.3f}" for l in capas))
    print(f"\nGuardado: {args.out}\nGraficar:  python3 plot_last_token.py plot {args.out}")


# ---------------------------------------------------------------------------
# plot (sin GPU)
# ---------------------------------------------------------------------------
# Paleta categorica validada (dataviz: slots 1-3 pasan all-pairs en superficie clara).
# El aqua queda bajo 3:1 de contraste: por eso cada linea lleva etiqueta directa.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
ESTILO_STAT = {"cos_de_medias": "-", "media_cos_vs_dir": "--", "media_de_cosenos": ":"}


def _estilo(plt):
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "font.family": "DejaVu Sans", "font.size": 9, "text.color": INK, "axes.labelcolor": INK2,
        "axes.edgecolor": GRID, "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.8, "grid.linestyle": "-", "axes.spines.top": False, "axes.spines.right": False,
        "lines.linewidth": 2.0, "legend.frameon": False,
    })


def _etiquetas_fin(ax, xs, finales):
    """Etiqueta directa al final de cada linea, separando las que se pisan sin salirse del eje."""
    lo, hi = ax.get_ylim()
    sep = (hi - lo) * 0.06
    orden = sorted(finales, key=lambda t: t[1])
    ys = []
    for _, y, _ in orden:
        ys.append(y if not ys else max(y, ys[-1] + sep))
    if ys:
        # recentrar el bloque sobre los valores reales y mantenerlo dentro del eje
        corr = np.mean([t[1] for t in orden]) - np.mean(ys)
        ys = [y + corr for y in ys]
        ys = [y - max(0.0, ys[-1] - (hi - sep / 2)) for y in ys]
        ys = [y + max(0.0, (lo + sep / 2) - ys[0]) for y in ys]
    for (name, _, _), y in zip(orden, ys):
        ax.annotate(name, xy=(xs[-1], y), xytext=(4, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=8, color=INK2, annotation_clip=False)


def _panel(ax, data, pk_list, rk, sk, lo):
    L = data["n_layers"]
    xs = np.arange(lo, L + 1)
    finales = []
    for i, pk in enumerate(pk_list):
        st = data["stats"][pk].get(rk)
        if st is None:
            continue
        y = np.array(st[sk])[lo:]
        ax.plot(xs, y, color=SERIES[i % len(SERIES)], label=pk)
        sem = st.get(sk + "_sem")
        if sem is not None:
            s = np.array(sem)[lo:]
            ax.fill_between(xs, y - s, y + s, color=SERIES[i % len(SERIES)], alpha=0.13, linewidth=0)
        finales.append((pk, float(y[-1]), i))
    if sk == "cos_de_medias" and rk in data["techos"]:
        ax.plot(xs, np.array(data["techos"][rk])[lo:], color=INK2, linewidth=1.0, alpha=0.7,
                label="techo de la referencia (split-half)")
    ax.axhline(0, color=INK2, linewidth=0.8)
    ax.set_xlim(lo, L)
    ax.set_title(ETIQ.get(rk, rk))
    return xs, finales


def _fig_por_estadistico(plt, data, sk, titulo, out_dir, lo, tag):
    pk_list = list(data["stats"])
    refs = [r for r in data["referencias"]]
    cols = min(3, len(refs))
    rows = int(np.ceil(len(refs) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4.6 * cols, 3.1 * rows), sharex=True, sharey=True,
                             squeeze=False)
    todos = []
    for ax, rk in zip(axes.flat, refs):
        xs, fin = _panel(ax, data, pk_list, rk, sk, lo)
        todos.append((ax, xs, fin))
    for ax in axes.flat[len(refs):]:
        ax.set_visible(False)
    ymin = min([0.0] + [min(np.array(data["stats"][p][r][sk])[lo:]) for p in pk_list for r in refs])
    for ax, xs, fin in todos:
        ax.set_ylim(min(-0.05, ymin - 0.05), 1.0)
        _etiquetas_fin(ax, xs, fin)
    for ax in axes[-1, :]:
        ax.set_xlabel("capa (salida del bloque l)")
    for ax in axes[:, 0]:
        ax.set_ylabel("coseno")
    h, l_ = axes.flat[0].get_legend_handles_labels()
    fig.legend(h, l_, loc="upper right", ncol=len(l_), fontsize=9, bbox_to_anchor=(0.99, 0.965))
    fig.suptitle(f"{titulo}\nparche contra cada referencia, último token del prompt · "
                 f"{data['subset']}, n={data['n_prompts']}, base {data['base_col']}",
                 x=0.01, ha="left", fontsize=11, fontweight="bold", y=1.0)
    fig.tight_layout(rect=(0, 0, 0.97, 0.90))
    path = os.path.join(out_dir, f"{tag}_{sk}.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _fig_estadisticos_por_parche(plt, data, out_dir, lo, tag):
    """Filas = referencia (frq, instr), columnas = parche; los 3 estadisticos con estilo de linea."""
    pk_list = list(data["stats"])
    refs = [r for r in ("frq", "instr") if r in data["referencias"]] or data["referencias"][:2]
    L = data["n_layers"]
    xs = np.arange(lo, L + 1)
    fig, axes = plt.subplots(len(refs), len(pk_list), figsize=(4.4 * len(pk_list), 3.0 * len(refs)),
                             sharex=True, sharey=True, squeeze=False)
    for i, rk in enumerate(refs):
        for j, pk in enumerate(pk_list):
            ax = axes[i, j]
            st = data["stats"][pk][rk]
            for sk, _ in STATS:
                ax.plot(xs, np.array(st[sk])[lo:], color=SERIES[j % len(SERIES)], linestyle=ESTILO_STAT[sk])
            ax.axhline(0, color=INK2, linewidth=0.8)
            ax.set_xlim(lo, L); ax.set_ylim(-0.1, 1.0)
            ax.set_title(f"{pk}  ·  {ETIQ.get(rk, rk)}", fontsize=9)
            if i == len(refs) - 1:
                ax.set_xlabel("capa")
            if j == 0:
                ax.set_ylabel("coseno")
    from matplotlib.lines import Line2D
    hs = [Line2D([0], [0], color=INK, linestyle=ESTILO_STAT[sk], linewidth=2) for sk, _ in STATS]
    fig.legend(hs, [t for _, t in STATS], loc="upper right", ncol=3, fontsize=8.5,
               bbox_to_anchor=(0.99, 0.945))
    fig.suptitle("Los tres estadísticos sobre el mismo parche\nel orden en que se promedia cambia el número",
                 x=0.01, ha="left", fontsize=11, fontweight="bold", y=1.0)
    fig.tight_layout(rect=(0, 0, 1, 0.89))
    path = os.path.join(out_dir, f"{tag}_estadisticos_por_parche.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _fig_normas(plt, data, out_dir, lo, tag):
    """Magnitud del delta medio relativa a ||h base||: un panel por referencia (en gris),
    con los parches en color. Small multiples en vez de nueve lineas en un solo eje."""
    L = data["n_layers"]
    xs = np.arange(lo, L + 1)
    refs = data["referencias"]
    cols = min(3, len(refs))
    rows = int(np.ceil(len(refs) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4.6 * cols, 3.0 * rows), sharex=True, sharey=True,
                             squeeze=False)
    ymax = max(max(np.array(data["normas"][k]["rel_norma_media"])[lo:]) for k in list(refs) + list(data["stats"]))
    for ax, rk in zip(axes.flat, refs):
        y = np.array(data["normas"][rk]["rel_norma_media"])[lo:]
        ax.plot(xs, y, color="#8f8e87", linewidth=1.6, label="la referencia del panel")
        fin = [("referencia", float(y[-1]), 0)]
        for i, pk in enumerate(data["stats"]):
            y = np.array(data["normas"][pk]["rel_norma_media"])[lo:]
            ax.plot(xs, y, color=SERIES[i % len(SERIES)], label=pk)
            fin.append((pk, float(y[-1]), i))
        ax.set_xlim(lo, L); ax.set_ylim(0, ymax * 1.08)
        ax.set_title(ETIQ.get(rk, rk))
        _etiquetas_fin(ax, xs, fin)
    for ax in axes.flat[len(refs):]:
        ax.set_visible(False)
    for ax in axes[-1, :]:
        ax.set_xlabel("capa")
    for ax in axes[:, 0]:
        ax.set_ylabel("‖media de deltas‖ / ‖h base‖")
    h, l_ = axes.flat[0].get_legend_handles_labels()
    fig.legend(h, l_, loc="upper right", ncol=len(l_), fontsize=9, bbox_to_anchor=(0.99, 0.965))
    fig.suptitle("Magnitud del desplazamiento medio en el último token\n"
                 "cada parche contra la magnitud de la referencia del panel",
                 x=0.01, ha="left", fontsize=11, fontweight="bold", y=1.0)
    fig.tight_layout(rect=(0, 0, 0.97, 0.90))
    path = os.path.join(out_dir, f"{tag}_normas.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot(args):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _estilo(plt)
    data = json.load(open(args.json, encoding="utf-8"))
    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.json))
    os.makedirs(out_dir, exist_ok=True)
    tag = os.path.splitext(os.path.basename(args.json))[0]
    if len(data["stats"]) > len(SERIES):
        raise SystemExit(f"hasta {len(SERIES)} parches por figura; separa en dos JSON")
    paths = [_fig_por_estadistico(plt, data, sk, t, out_dir, args.from_layer, tag) for sk, t in STATS]
    paths.append(_fig_estadisticos_por_parche(plt, data, out_dir, args.from_layer, tag))
    paths.append(_fig_normas(plt, data, out_dir, args.from_layer, tag))
    # tabla de respaldo (la vista tabular de los graficos)
    L = data["n_layers"]
    capas = [l for l in (9, 12, 14, 16, 20, 24, L) if args.from_layer <= l <= L]
    lines = [f"# {tag}: último token, {data['subset']}, n={data['n_prompts']}", ""]
    for rk in data["referencias"]:
        lines += [f"## contra {ETIQ.get(rk, rk)}", "",
                  "| parche | estadístico | " + " | ".join(f"L{l}" for l in capas) + " |",
                  "|---|---|" + "---|" * len(capas)]
        for pk in data["stats"]:
            for sk, _ in STATS:
                v = data["stats"][pk][rk][sk]
                lines.append(f"| {pk} | {sk} | " + " | ".join(f"{v[l]:.3f}" for l in capas) + " |")
        lines.append("")
    md = os.path.join(out_dir, f"{tag}_tabla.md")
    open(md, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    for p in paths + [md]:
        print(p)


# ---------------------------------------------------------------------------
def selftest(_):
    rng = np.random.RandomState(0)
    n, L, d = 40, 5, 64
    direc = rng.randn(L, d)
    contenido = rng.randn(n, L, d) * 3.0                  # ruido por prompt, grande, NO compartido
    dr = direc[None] + contenido
    dp = 0.8 * direc[None] + rng.randn(n, L, d) * 0.5     # parche: misma direccion, poco ruido
    s = estadisticos(dp, dr)
    cm, mc, vd = (np.mean(s[k]) for k in ("cos_de_medias", "media_de_cosenos", "media_cos_vs_dir"))
    assert cm > vd > mc, (cm, vd, mc)                      # el orden esperado de los tres
    assert cm > 0.8 and mc < 0.4
    # LOO: con dp == dr la version sin LOO daria sesgo; con LOO no puede dar 1.0
    s2 = estadisticos(dr, dr)
    assert abs(np.mean(s2["media_de_cosenos"]) - 1) < 1e-9 and np.mean(s2["media_cos_vs_dir"]) < 0.9
    t = np.mean(techo_split_half(dr))
    assert 0 < t < 1
    nm = normas(dp, np.ones((n, L, d)))
    assert len(nm["rel_norma_media"]) == L
    print(f"selftest OK  cos_de_medias={cm:.3f} > media_cos_vs_dir={vd:.3f} > media_de_cosenos={mc:.3f}"
          f"  | techo ref={t:.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compute", help="GPU: activaciones -> JSON")
    c.add_argument("--patch", action="append", required=True, help="nombre=ruta[@anchor]; repetible")
    c.add_argument("--model", default=None)
    c.add_argument("--targets", default="attributes/french/targets_french_v5.csv")
    c.add_argument("--train_test_split", type=float, default=0.80)
    c.add_argument("--subset", choices=["heldout", "train", "all"], default="heldout")
    c.add_argument("--n", type=int, default=50, help="maximo de prompts (0 = todos los del subset)")
    c.add_argument("--base_col", default="prompt",
                   help="columna de la pregunta base sobre la que se suma el parche (prompt, prompt_es, ...)")
    c.add_argument("--instruction", default=INSTRUCTION)
    c.add_argument("--no_controls", action="store_true")
    c.add_argument("--scale", type=float, default=1.0)
    c.add_argument("--save_deltas", action="store_true", help="guardar los deltas crudos (.npz, fp16)")
    c.add_argument("--device", default="cuda:0")
    c.add_argument("--out", required=True)
    c.set_defaults(fn=compute)
    p = sub.add_parser("plot", help="sin GPU: JSON -> PNGs + tabla")
    p.add_argument("json")
    p.add_argument("--out_dir", default=None)
    p.add_argument("--from_layer", type=int, default=1)
    p.set_defaults(fn=plot)
    s = sub.add_parser("selftest")
    s.set_defaults(fn=selftest)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
