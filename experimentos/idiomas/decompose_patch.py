"""
Geometria del delta de un parche respecto de d_frq. TODO en CPU, sin GPU.

Contesta la pregunta que la serie de activaciones dejo abierta: un parche puede
reproducir d_frq al 95-100% del techo de ruido y aun asi no producir frances.
Si la alineacion no es la variable causal, ¿donde vive el efecto?

Tres medidas, en orden de lo que cuestan de interpretar:

---------------------------------------------------------------------------
1. FRACCION DE ENERGIA DE LA DIRECCION MEDIA
---------------------------------------------------------------------------
Por la descomposicion sesgo-varianza sobre los deltas franceses t_i:

    mean_i ||t_i||^2  =  ||d||^2  +  mean_i ||t_i - d||^2
                         ^^^^^^^     ^^^^^^^^^^^^^^^^^^^^
                         la media    variacion por prompt

    energia_media[l] = ||d[l]||^2 / mean_i ||t_i[l]||^2

Un parche que reproduce d PERFECTAMENTE captura solo el primer termino. Si esa
fraccion es 0.4, alinearse al 95% con d es reproducir ~40% de lo que hace una
pregunta francesa, y la paradoja se disuelve sola.

De paso sale el ENCOGIMIENTO, ||d|| / mean_i ||t_i||, que dice donde cae "tan
fuerte como una pregunta francesa real" en el eje de mag: en 1/encogimiento.
v_CE mide mag = 1.332; si 1/encogimiento da ~1.33, v_CE no "se pasa de largo"
sino que llega justo a la fuerza de una pregunta francesa de verdad, y los
parches de activaciones se quedan en la fuerza del PROMEDIO porque eso es lo
que la MSE les pide.

---------------------------------------------------------------------------
2. DESCOMPOSICION PARALELA / ORTOGONAL, EXACTA POR PROMPT
---------------------------------------------------------------------------
    delta = delta_par + delta_ort        <delta_par, delta_ort> = 0

    par = <delta,d> / ||d||^2            (con signo, en unidades de ||d||)
    ort = ||delta - par*d|| / ||d||

Y la loss se parte en dos errores independientes:

    rel = (par - 1)^2 + ort^2

El segundo termino tiene minimo en CERO: la MSE empuja ||delta_ort|| -> 0. Si
el ingrediente causal vive en el complemento ortogonal, la loss lo suprime por
diseno. Medido sobre los resumenes (mean(mag)*mean(cos)) daba: v_CE con
componente paralelo casi igual al de los parches de activaciones y el doble de
ortogonal. Aca se calcula EXACTO, por prompt, que difiere del producto de
promedios por la covarianza entre mag y cos.

---------------------------------------------------------------------------
3. PCA SOBRE LOS DELTAS FRANCESES, Y PROYECCION DE CADA PARCHE
---------------------------------------------------------------------------
    sin centrar   la nube t_i entera. Si PC1 se lleva el 80%, d_frq casi
                  alcanza; si se lleva el 25%, la diferencia de medias esta
                  mirando una rendija
    centrada      restando d: la estructura PROMPT-ESPECIFICA, que es
                  exactamente lo que un vector universal no puede dar

Y despues se proyecta el delta medio de cada parche sobre los primeros PCs. Si
v_CE carga en PCs donde los de activaciones no cargan, ahi estan las
direcciones que importan.

AVISO: PCA dice donde esta la VARIANZA, no donde esta la CAUSALIDAD. En esta
serie ya paso que una correlacion altisima con d_frq resulto no ser la variable
causal. Esto describe; lo que decide es inject_direction.py.

---------------------------------------------------------------------------
    # solo lo que sale del cache (energia, encogimiento, PCA de la nube)
    python3 decompose_patch.py

    # ademas, la descomposicion y las proyecciones de los parches medidos
    python3 decompose_patch.py --deltas runs/v4_250/profile_deltas.pt \\
                               runs/act_l12_frq/profile_deltas.pt \\
                               runs/act_band12_16_p2/profile_deltas.pt
"""

import argparse
import glob
import json
import os

import torch

DEFAULT_CACHE = "runs/_act_cache"


def load_cache(cond, cache_dir):
    """Estados crudos de una condicion. Devuelve {idx: tensor[L, d]} en fp32."""
    pat = os.path.join(cache_dir, f"acts_{cond}_*.pt")
    hits = glob.glob(pat)
    if not hits:
        raise SystemExit(f"no hay cache para '{cond}' en {cache_dir}\n"
                         f"  corre train_act_patch.py una vez para generarlo")
    p = max(hits, key=os.path.getmtime)
    blob = torch.load(p, map_location="cpu")
    return {i: s.float() for i, s in blob["states"].items()}, os.path.basename(p)


def energia(dl, d, capas):
    """
    Fraccion de energia en la direccion media, y encogimiento.

    dl: [n, L, dim] los t_i          d: [L, dim] la media
    """
    filas = []
    for l in capas:
        j = l - 1
        e_tot = (dl[:, j, :] ** 2).sum(1).mean()          # mean_i ||t_i||^2
        e_med = (d[j] ** 2).sum()                          # ||d||^2
        n_ind = dl[:, j, :].norm(dim=1).mean()             # mean_i ||t_i||
        n_med = d[j].norm()
        filas.append({
            "capa": l,
            "norma_d": n_med.item(),
            "norma_ti_media": n_ind.item(),
            "energia_media": (e_med / e_tot).item(),
            "encogimiento": (n_med / n_ind).item(),
            "mag_de_una_pregunta_real": (n_ind / n_med).item(),
        })
    return filas


def pca(X, k=10):
    """
    PCA por SVD sobre X [n, dim]. Devuelve (componentes [k, dim], varianza explicada).

    No centra: eso lo decide quien llama. Sobre los t_i sin centrar, PC1 sale
    parecido a la direccion media; centrando, sale la variacion alrededor.
    """
    k = min(k, min(X.shape))
    U, S, Vh = torch.linalg.svd(X, full_matrices=False)
    var = (S ** 2)
    return Vh[:k], (var[:k] / var.sum()).tolist()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache_dir", default=DEFAULT_CACHE)
    ap.add_argument("--ref", default="frq", help="condicion de referencia del cache")
    ap.add_argument("--n_train", type=int, default=200,
                    help="filas de train sobre las que se estimo d")
    ap.add_argument("--capas", default="12,14,16,20,24,28")
    ap.add_argument("--deltas", nargs="*", default=[],
                    help="uno o mas profile_deltas.pt de train_act_patch.py --profile_only")
    ap.add_argument("--k", type=int, default=8, help="cuantos PCs reportar")
    ap.add_argument("--pca_capa", type=int, default=16, help="capa para el PCA y las proyecciones")
    ap.add_argument("--out", default=None, help="JSON de salida (opcional)")
    args = ap.parse_args()

    capas = [int(x) for x in args.capas.split(",") if x.strip()]
    cl, f_cl = load_cache("clean", args.cache_dir)
    rf, f_rf = load_cache(args.ref, args.cache_dir)
    print(f"cache: {f_cl}  +  {f_rf}")

    idx = sorted(set(cl) & set(rf))[:args.n_train]
    dl = torch.stack([rf[i] - cl[i] for i in idx])        # [n, L, dim]
    d = dl.mean(0)                                        # [L, dim]
    print(f"t_i sobre {len(idx)} filas de train  |  shape {tuple(dl.shape)}")

    # ---- 1. energia y encogimiento ----
    filas = energia(dl, d, capas)
    print("\n" + "=" * 78)
    print("1. CUANTO DE UNA PREGUNTA FRANCESA ES LA DIRECCION MEDIA")
    print("=" * 78)
    print(f"{'capa':>5}{'||d||':>10}{'||t_i|| medio':>15}{'energia en d':>15}"
          f"{'encogim.':>11}{'mag de una real':>17}")
    for r in filas:
        print(f"{r['capa']:>5}{r['norma_d']:>10.2f}{r['norma_ti_media']:>15.2f}"
              f"{r['energia_media']:>15.3f}{r['encogimiento']:>11.3f}"
              f"{r['mag_de_una_pregunta_real']:>17.2f}")
    print("\n  energia en d = ||d||^2 / mean||t_i||^2 : que fraccion de una pregunta")
    print("                 francesa captura un parche que reproduce d perfecto")
    print("  mag de una real = 1/encogimiento : donde cae una pregunta francesa de")
    print("                 verdad en el eje de mag.  v_CE mide 1.332")

    salida = {"capas": capas, "n_train": len(idx), "energia": filas}

    # ---- 2 y 3. solo si hay deltas de parches ----
    if args.deltas:
        L = args.pca_capa
        j = L - 1
        print("\n" + "=" * 78)
        print(f"2. DESCOMPOSICION PARALELA / ORTOGONAL, EXACTA POR PROMPT  (capa {L})")
        print("=" * 78)
        dn = d[j].norm()
        print(f"{'parche':<26}{'par':>9}{'ort':>9}{'rel':>9}{'check':>9}"
              f"{'||par||':>10}{'||ort||':>10}")
        dec = {}
        for p in args.deltas:
            blob = torch.load(p, map_location="cpu")
            name = os.path.basename(os.path.dirname(os.path.abspath(p)))
            dd = blob["deltas"][L]                          # [n, dim]
            par = (dd @ d[j]) / dn ** 2                     # [n]
            ort = (dd - par[:, None] * d[j]).norm(dim=1) / dn
            rel = ((dd - d[j]) ** 2).sum(1) / dn ** 2
            # rel = (par-1)^2 + ort^2, chequeo de la identidad
            chk = ((par - 1) ** 2 + ort ** 2)
            dec[name] = {"par": par.mean().item(), "ort": ort.mean().item(),
                         "rel": rel.mean().item(),
                         "norma_par": (par.mean() * dn).item(),
                         "norma_ort": (ort.mean() * dn).item()}
            print(f"{name:<26}{par.mean():>9.3f}{ort.mean():>9.3f}{rel.mean():>9.3f}"
                  f"{chk.mean():>9.3f}{par.mean() * dn:>10.2f}{ort.mean() * dn:>10.2f}")
        print(f"\n  ||d[{L}]|| = {dn:.2f}   ·   'check' debe coincidir con 'rel': rel = (par-1)^2 + ort^2")
        salida["descomposicion"] = {"capa": L, "norma_d": dn.item(), "parches": dec}

        print("\n" + "=" * 78)
        print(f"3. PCA SOBRE LOS DELTAS FRANCESES Y PROYECCION DE CADA PARCHE  (capa {L})")
        print("=" * 78)
        X = dl[:, j, :]
        for etiqueta, M in (("sin centrar", X), ("centrada (restando d)", X - d[j])):
            comps, ev = pca(M, args.k)
            acum = 0.0
            print(f"\n  {etiqueta}:")
            print(f"    {'PC':>4}{'var expl.':>12}{'acumulada':>12}{'cos con d':>12}")
            for i, v in enumerate(ev):
                acum += v
                cd = torch.nn.functional.cosine_similarity(comps[i], d[j], dim=0).abs().item()
                print(f"    {i + 1:>4}{v:>12.3f}{acum:>12.3f}{cd:>12.3f}")
            if etiqueta.startswith("sin"):
                salida["pca_sin_centrar"] = {"var_explicada": ev}
                comps_uc = comps
            else:
                salida["pca_centrada"] = {"var_explicada": ev}

        print(f"\n  proyeccion del delta medio de cada parche sobre los PCs sin centrar")
        print(f"  (coseno absoluto; los PCs son ortonormales entre si)")
        hdr = f"    {'parche':<26}" + "".join(f"{'PC' + str(i + 1):>8}" for i in range(min(args.k, 6)))
        print(hdr)
        proy = {}
        for p in args.deltas:
            blob = torch.load(p, map_location="cpu")
            name = os.path.basename(os.path.dirname(os.path.abspath(p)))
            md = blob["mean_delta"][L]
            cs = [torch.nn.functional.cosine_similarity(comps_uc[i], md, dim=0).abs().item()
                  for i in range(min(args.k, 6))]
            proy[name] = cs
            print(f"    {name:<26}" + "".join(f"{c:>8.3f}" for c in cs))
        salida["proyecciones_pc"] = proy
        print("\n  si v_CE carga en PCs donde los de activaciones no cargan, ahi estan")
        print("  las direcciones que importan -- pero esto es VARIANZA, no causalidad.")
        print("  quien decide es inject_direction.py")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(salida, fh, indent=2, ensure_ascii=False)
        print(f"\nGuardado: {args.out}")


if __name__ == "__main__":
    main()
