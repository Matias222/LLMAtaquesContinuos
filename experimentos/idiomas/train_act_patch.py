"""
Entrenamiento del parche por ALINEACION DE ACTIVACIONES, no por CE de salida.

Cambio de paradigma respecto de `train_lang_patch.py`. Aquel objetivo vive en el
espacio de SALIDA:

    L = CE( logits(q + v), y_frances ) + lambda*||v||^2

Este vive en el espacio de ACTIVACIONES: al parche no se le pide que reproduzca
el texto frances sino el ESTADO INTERNO que produce la pregunta en frances.

    delta_i[l] = h(q_i + v)[l] - h(q_i)[l]          <- lo que hace el parche
    d[l]       = mean_i( h(ref_i)[l] - h(q_i)[l] )  <- la direccion de referencia

    L = (1/(|B|*n)) SUM_i SUM_{l in B}  ||delta_i[l] - d[l]||^2 / ||d[l]||^2
        + lambda*||v||^2

El parche NUNCA ve un token frances. Solo ve una direccion en el residual
stream.

---------------------------------------------------------------------------
POR QUE CONTRA LA DIRECCION MEDIA Y NO POR PROMPT
---------------------------------------------------------------------------
`h(q_fr_i) - h(q_i)` individual esta dominado por el cambio de CONTENIDO, no
por el de idioma (ANALISIS_CAPAS.md seccion 6). Lo que aisla el idioma es el
promedio sobre prompts. Ademas el parche es UNIVERSAL: un solo v para todos los
prompts no puede producir deltas prompt-especificos, asi que el target por
prompt es inalcanzable por construccion.

Bajo MSE la diferencia entre las dos formulaciones es de segundo orden:

    grad(L_por_prompt) - grad(L_media) = -(2/B) SUM_i J_i^T (t_i - d)

que con batch completo y Jacobianos iguales es exactamente cero. Lo que queda
es varianza (la media del batch en vez de la global). Targetear d directamente
la elimina y ademas permite estimar d SOLO sobre train.

---------------------------------------------------------------------------
POR QUE LA NORMALIZACION POR CAPA NO ES OPCIONAL
---------------------------------------------------------------------------
||d[l]|| crece con la profundidad: es la misma razon por la que `rel_delta` en
layer_analysis.py divide por ||h_clean||. Una suma cruda sobre una banda la
domina la capa mas profunda y el resto es decoracion.

Dividiendo por ||d[l]||^2 cada termino es error RELATIVO y la escala se lee
sola:

    1.0  el parche no hizo nada (delta = 0)
    0.0  reproduccion perfecta
    >1   activamente peor que no hacer nada

---------------------------------------------------------------------------
LA BANDA ES UN PARAMETRO, NO UN DISENO APARTE
---------------------------------------------------------------------------
`--layers 14` (una capa) y `--layers 12,13,14,15,16` (banda) son la misma loss.
Una capa sola SUBDETERMINA (3072 restricciones contra 9216 params libres) y la
banda sobredetermina, y el residual de la banda pasa a ser una MEDICION de
realizabilidad.

Conviene barrer de a una capa PRIMERO: si una capa profunda resulta inalcanzable
desde el input, meterla en la banda gasta el presupuesto de optimizacion en una
restriccion imposible y degrada las capas que si eran alcanzables. El barrido
dice que capas poner en la banda. Por eso el diagnostico mide TODAS las capas
aunque se entrene sobre una: si el perfil entero ya se reproduce matcheando una
sola, la banda no agrega nada.

---------------------------------------------------------------------------
EL CACHE DE ACTIVACIONES
---------------------------------------------------------------------------
Reagrupando la loss se ve que hay dos partes:

    ||delta_i[l] - d[l]||^2  =  || h(q_i + v)[l]  -  ( h(q_i)[l] + d[l] ) ||^2
                                  ^^^^^^^^^^^^^^     ^^^^^^^^^^^^^^^^^^^^^
                                  depende de v       NO depende de v

El parentesis de la derecha es el ESTADO AL QUE HAY QUE ATERRIZAR, y es
constante. Se computa una vez y se guarda en disco:

    h(q_i)[l]     linea de base por prompt. Sin cachearla, cada paso paga un
                  segundo forward para recalcular algo que no cambio.
    h(ref_i)[l]   de ahi sale d[l], que es una media sobre ~200 filas.
                  Recalcularla por paso serian 400 forwards por paso.

Se guardan los ESTADOS CRUDOS, no d: asi cambiar el split, el gate o el
`--target` no invalida nada, y d se deriva sin tocar la GPU. `h(q_i)` ademas es
identica para todas las corridas del barrido.

En fp16, que es EXACTO: el forward ya es fp16 y `hidden_at_layers` solo ensancha
a float32 para la aritmetica. ~43 MB por condicion sobre 250 filas x 28 capas.

El cache se indexa por un fingerprint de (modelo, prompts de la condicion). Eso
importa mas de lo que parece: `fix_translations.py` REESCRIBE `prompt_fr`, y un
cache viejo entrenaria en silencio contra las traducciones anteriores a las 114
correcciones. Con el fingerprint eso se invalida solo.

---------------------------------------------------------------------------
CIRCULARIDAD: LEER ANTES DE REPORTAR NADA
---------------------------------------------------------------------------
El resultado P1 de HALLAZGOS.md (el parche se parece mas a d_frq que a d_instr,
0.712 vs 0.537) vale porque ese parche se entreno SOLO con CE de salida y nada
en la loss lo empujaba ahi. Un parche entrenado con ESTE script tiene esa
alineacion como objetivo: medirla despues es tautologico.

Los dos objetos son distintos y sostienen claims distintos:

    v_CE   entrenado con CE de salida   -> sostiene P1/P3 (geometria observacional)
    v_act  entrenado con este script    -> sostiene SUFICIENCIA (constructivo)

Nunca mezclar los numeros. Por eso el metadata guarda `objetivo: "activaciones"`.

Lo que SI sostiene este script: si un parche entrenado contra d_frq, sin ver un
solo token frances, produce frances, entonces la direccion ALCANZA para causar
el comportamiento. Es el test de suficiencia de ANALISIS_CAPAS.md seccion 11,
implementado en el espacio de embeddings en vez de por trasplante mid-network.

---------------------------------------------------------------------------
NOTA SOBRE INDICES DE CAPA
---------------------------------------------------------------------------
Misma convencion que layer_analysis.py y mean_diff_vectors.py: la capa `l` es
`hidden_states[l]`, o sea la SALIDA del bloque l (1..L). La capa 0 son los
embeddings de entrada y no se puede targetear: leemos en la ultima posicion del
prompt, que no esta parcheada, asi que ahi delta ~ 0 por construccion (es el
control de sanidad de ANALISIS_CAPAS.md seccion 3bis).

Aviso: esto captura el residual CRUDO via hooks sobre `model.model.layers[l-1]`.
Para l < L es identico a `output_hidden_states`, pero la ULTIMA entrada de
`hidden_states` que devuelve HF esta POST-norm final. O sea que d[L] de este
script no es comparable con d[L] de mean_diff_vectors.py. No usar l = L.

    python3 -u train_act_patch.py --model $M --layers 14 --target frq \\
        --output_dir runs/act_l14_frq
"""

import argparse
import hashlib
import json
import math
import os

import pandas as pd
import torch

from lm import (DEFAULT_MODEL, apply_patch_first_n, build_suffix_manager,
                get_embedding_matrix, get_embeddings, load_model_and_tokenizer)

# Identicas a mean_diff_vectors.py, para que las direcciones sean las MISMAS
# que las que ya reporta la geometria.
INSTRUCTION_FR = "Answer this in French."
INSTRUCTION_CORTO = "Answer this in one short sentence."

TARGETS = ("frq", "instr", "qde", "corto", "random")
DEFAULT_CACHE = "runs/_act_cache"


class _StopForward(Exception):
    """Corta el forward en la capa mas profunda que nos interesa."""


def parse_layers(spec):
    """'14' | '12,16,20' | '12-16' -> lista ordenada de enteros."""
    out = set()
    for parte in str(spec).split(","):
        parte = parte.strip()
        if "-" in parte:
            a, b = parte.split("-")
            out.update(range(int(a), int(b) + 1))
        elif parte:
            out.add(int(parte))
    capas = sorted(out)
    if not capas:
        raise ValueError("--layers vacio")
    if capas[0] < 1:
        raise ValueError(
            "la capa 0 son los embeddings de entrada: en la ultima posicion del "
            "prompt (que no esta parcheada) su delta es ~0 por construccion")
    return capas


def hidden_at_layers(model, tokenizer, instruction, device, layers,
                     patch=None, num_patch_positions=3, truncate=True):
    """
    Residual stream en la ULTIMA posicion del prompt, para las capas pedidas.

    Misma posicion que layer_analysis.hidden_at_last: la que genera el primer
    token de la respuesta. Medir en las posiciones parcheadas seria trivial
    (ahi el delta ES el parche); lo que importa es como se propaga.

    Los embeddings van SIEMPRE detached: el unico tensor con gradiente es el
    parche, igual que en train_lang_patch.py.

    Devuelve {l: tensor[d]} en float32.
    """
    sm = build_suffix_manager(tokenizer, instruction, target="")
    tokens = sm.get_input_ids().to(device)
    embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()
    if patch is not None:
        embeds = apply_patch_first_n(sm, embeds, patch, num_patch_positions)
    embeds = embeds[:, : sm._assistant_role_slice.stop, :]

    got, handles = {}, []
    l_max = max(layers)
    n_layers = len(model.model.layers)

    def mk(l):
        def hook(_mod, _inp, out):
            h = out[0] if isinstance(out, tuple) else out
            got[l] = h[0, -1, :].float()
            if truncate and l == l_max and l_max < n_layers:
                raise _StopForward
        return hook

    for l in layers:
        handles.append(model.model.layers[l - 1].register_forward_hook(mk(l)))
    try:
        model(inputs_embeds=embeds)
    except _StopForward:
        pass
    finally:
        for h in handles:
            h.remove()
    return got


# ---------------------------------------------------------------------------
# Condiciones y cache de activaciones
# ---------------------------------------------------------------------------

def condition_prompt(cond, row):
    """La instruccion que produce el estado de una condicion, para una fila."""
    q = row["prompt"]
    if cond == "clean":
        return q
    if cond == "frq":
        return row["prompt_fr"]
    if cond == "qde":
        return row["prompt_de"]
    if cond == "instr":
        return f"{INSTRUCTION_FR} {q}"
    if cond == "corto":
        return f"{INSTRUCTION_CORTO} {q}"
    raise ValueError(f"condicion desconocida: {cond}")


def usable_mask(target, df):
    """
    Que filas entran en la estimacion de d.

    frq/qde dependen del gate de traduccion; instr/corto se construyen sobre la
    pregunta inglesa y no dependen de nada. `random` hereda el de frq porque se
    construye igualando las normas de d_frq por capa.
    """
    col = {"frq": "prompt_fr_ok", "qde": "prompt_de_ok", "random": "prompt_fr_ok"}.get(target)
    if col is None:
        return pd.Series(True, index=df.index)
    if col not in df.columns:
        raise SystemExit(f"falta la columna {col}: corre translate_questions.py")
    return df[col].astype(str).str.lower() == "true"


def _fingerprint(model_path, prompts):
    """Identidad del cache: modelo + los prompts exactos que se codificaron."""
    h = hashlib.sha1(model_path.encode("utf-8"))
    for p in prompts:
        h.update(b"\x00")
        h.update(str(p).encode("utf-8"))
    return h.hexdigest()[:16]


@torch.no_grad()
def states_for(model, tokenizer, df, cond, device, all_layers, model_path,
               cache_dir, refresh=False):
    """
    Estados del residual stream por fila para una condicion, cacheados en disco.

    Devuelve {idx_de_fila: tensor[L, d]} en float32, donde la fila j del tensor
    es la capa `all_layers[j]`. Se guardan los estados CRUDOS y no d, asi que
    cambiar el split, el gate o el --target no invalida el cache.
    """
    prompts = [condition_prompt(cond, r) for _, r in df.iterrows()]
    fp = _fingerprint(model_path, prompts)
    path = os.path.join(cache_dir, f"acts_{cond}_{fp}.pt")

    if os.path.exists(path) and not refresh:
        blob = torch.load(path, map_location=device)
        mb = os.path.getsize(path) / 1e6
        print(f"  cache HIT   {cond:6s} {len(blob['states'])} filas  {mb:.0f} MB  "
              f"{os.path.basename(path)}")
        return {i: s.float() for i, s in blob["states"].items()}

    n = sum(1 for p in prompts if str(p).strip())
    print(f"  cache MISS  {cond:6s} computando {n} forwards...")
    out = {}
    for (idx, _row), p in zip(df.iterrows(), prompts):
        if not str(p).strip():
            continue
        h = hidden_at_layers(model, tokenizer, p, device, all_layers, truncate=False)
        out[idx] = torch.stack([h[l] for l in all_layers])

    os.makedirs(cache_dir, exist_ok=True)
    torch.save({"meta": {"cond": cond, "model": model_path, "fingerprint": fp,
                         "layers": all_layers, "n_filas": len(out)},
                "states": {i: s.half() for i, s in out.items()}}, path)
    print(f"  guardado    {cond:6s} {os.path.getsize(path) / 1e6:.0f} MB  "
          f"{os.path.basename(path)}")
    return out


def mean_direction(st_ref, st_clean, idxs):
    """d[l] = media de (h_ref - h_clean) sobre idxs. Devuelve [L, d] en fp32."""
    return torch.stack([st_ref[i] - st_clean[i] for i in idxs]).mean(0)


def cosine_step(base, global_step, total_steps):
    """Identico a train_lang_patch.cosine_step: cambia la loss, no el optimizador."""
    if total_steps <= 1:
        return base
    p = min(1.0, global_step / (total_steps - 1))
    return base * 0.5 * (1.0 + math.cos(math.pi * p))


def perfil(model, tokenizer, rows, patch, clean, D, device, all_layers,
           num_patch_positions):
    """
    Diagnostico por capa. Tres numeros:

        rel  ||delta - d||^2 / ||d||^2   el termino de la loss. 1 = no hizo nada
        cos  cos(delta, d)               comparable con HALLAZGOS.md seccion 6
        mag  ||delta|| / ||d||           empuja de mas o de menos?

    Se calcula sobre TODAS las capas aunque se entrene sobre una sola: si el
    perfil entero se reproduce, la banda no agrega nada.

    Sobre held-out esto no es circular: D se estimo sobre train.
    """
    acc = {l: {"rel": [], "cos": [], "mag": []} for l in all_layers}
    with torch.no_grad():
        for idx, row in rows.iterrows():
            h_p = hidden_at_layers(model, tokenizer, row["prompt"], device,
                                   all_layers, patch=patch,
                                   num_patch_positions=num_patch_positions,
                                   truncate=False)
            for j, l in enumerate(all_layers):
                delta = h_p[l] - clean[idx][j]
                d, dn = D[j], D[j].norm()
                acc[l]["rel"].append((((delta - d) ** 2).sum() / dn ** 2).item())
                acc[l]["cos"].append(
                    torch.nn.functional.cosine_similarity(delta, d, dim=0).item())
                acc[l]["mag"].append((delta.norm() / dn).item())
    return {l: {k: sum(v) / len(v) for k, v in m.items()} for l, m in acc.items()}


def train(model_path, targets_csv, layers, target, output_dir, l2_weight=0.055,
          num_epochs=8, num_steps_per_prompt=20, num_patch_positions=3,
          step_size=0.00025, train_test_split=0.80, device="cuda:0",
          use_gate=True, batch_size=8, step_decay="cosine", val_n=20,
          truncate=True, cache_dir=DEFAULT_CACHE, refresh_cache=False):
    df = pd.read_csv(targets_csv, sep=";", keep_default_na=False)

    # Split POSICIONAL, identico a train_lang_patch.py. Si esto cambiara, los
    # dos parches dejarian de ser comparables.
    n_train = int(len(df) * train_test_split)
    train_df, test_df = df.iloc[:n_train], df.iloc[n_train:]
    if use_gate and "passed_gate" in train_df.columns:
        antes = len(train_df)
        train_df = train_df[train_df["passed_gate"].astype(str).str.lower() == "true"]
        print(f"Gate de calidad sobre train: {len(train_df)}/{antes}")

    model, tokenizer = load_model_and_tokenizer(model_path, device=device)
    dim = get_embedding_matrix(model).shape[1]
    n_layers = len(model.model.layers)
    all_layers = list(range(1, n_layers + 1))
    if max(layers) > n_layers:
        raise SystemExit(f"el modelo tiene {n_layers} capas, pediste {max(layers)}")
    if max(layers) == n_layers:
        print(f"AVISO: la capa {n_layers} es la ultima; hidden_states[{n_layers}] de HF "
              "esta post-norm y NO es comparable con mean_diff_vectors.py")

    val_rows = test_df.head(val_n)
    train_rows = train_df.head(val_n)

    print(f"\nTrain: {len(train_df)}  |  Held-out: {len(test_df)}  |  diagnostico: {len(val_rows)}")
    print(f"Objetivo: ACTIVACIONES  |  target: {target}  |  capas: {layers}")
    print(f"L2: {l2_weight}  |  step: {step_size} ({step_decay})  |  posiciones: {num_patch_positions}")

    # --- cache: estados crudos sobre el CSV ENTERO, independientes del split ---
    print(f"\nActivaciones ({cache_dir}):")
    base = "frq" if target == "random" else target
    ST_CLEAN = states_for(model, tokenizer, df, "clean", device, all_layers,
                          model_path, cache_dir, refresh_cache)
    ST_REF = states_for(model, tokenizer, df, base, device, all_layers,
                        model_path, cache_dir, refresh_cache)

    # d se DERIVA del cache, sin GPU. Solo train, solo filas usables, solo las
    # que existen en las dos condiciones.
    usable = usable_mask(target, df)
    idxs = [i for i in train_df.index
            if usable.loc[i] and i in ST_CLEAN and i in ST_REF]
    if len(idxs) < 10:
        raise SystemExit(f"solo {len(idxs)} filas usables para estimar d, no alcanza")
    D = mean_direction(ST_REF, ST_CLEAN, idxs)                      # [L, d]

    if target == "random":
        # Control: misma norma por capa, direccion al azar. Es el analogo
        # geometrico de make_random_patch.py, que iguala la norma del parche.
        g = torch.Generator(device="cpu").manual_seed(0)
        R = torch.randn(D.shape, generator=g).to(D.device)
        D = R / R.norm(dim=1, keepdim=True) * D.norm(dim=1, keepdim=True)

    D_sq = (D ** 2).sum(dim=1)
    LI = {l: j for j, l in enumerate(all_layers)}
    print(f"d estimada sobre {len(idxs)}/{len(train_df)} filas de train")
    print("  norma de d en las capas objetivo: " +
          "  ".join(f"l{l}={D[LI[l]].norm().item():.2f}" for l in layers))
    print("  (verificar contra mean_diff_ctrl.json: si no coincide, el d que "
          "optimizas no es el que reporta la geometria)")

    patch = torch.zeros(1, num_patch_positions, dim, requires_grad=True, device=device)
    n_batches = math.ceil(len(train_df) / batch_size)
    total_steps = num_epochs * n_batches * num_steps_per_prompt
    print(f"Epochs: {num_epochs}  |  batch: {batch_size} ({n_batches} batches/epoch)  "
          f"|  steps/batch: {num_steps_per_prompt}")
    print("=" * 70)

    best = {"loss": float("inf"), "patch": None, "epoch": None}
    best_tr = {"loss": float("inf"), "patch": None, "epoch": None}
    curva, global_step = [], 0

    for epoch in range(num_epochs):
        print(f"\n{'#' * 70}\nEPOCH {epoch + 1}/{num_epochs}\n{'#' * 70}")
        epoch_loss = []

        for b in range(n_batches):
            batch = train_df.iloc[b * batch_size:(b + 1) * batch_size]
            paso = []
            for _ in range(num_steps_per_prompt):
                # Gradiente acumulado sobre TODO el batch antes del paso, igual
                # que train_lang_patch.py.
                vals = []
                for idx, row in batch.iterrows():
                    h_p = hidden_at_layers(model, tokenizer, row["prompt"], device,
                                           layers, patch=patch,
                                           num_patch_positions=num_patch_positions,
                                           truncate=truncate)
                    terms = [((h_p[l] - ST_CLEAN[idx][LI[l]] - D[LI[l]]) ** 2).sum()
                             / D_sq[LI[l]] for l in layers]
                    band = torch.stack(terms).mean()
                    total = band + l2_weight * patch.norm(2) ** 2
                    (total / len(batch)).backward()
                    vals.append(band.item())

                lr = cosine_step(step_size, global_step, total_steps) \
                    if step_decay == "cosine" else step_size
                patch.data -= torch.sign(patch.grad.data) * lr
                model.zero_grad()
                patch.grad.zero_()
                global_step += 1
                paso.append(sum(vals) / len(vals))

            epoch_loss.append(sum(paso) / len(paso))
            if (b + 1) % max(1, 10 // batch_size) == 0:
                print(f"  [batch {b + 1}/{n_batches}] band={epoch_loss[-1]:.4f}  "
                      f"norma={patch.norm(2).item():.6f}  lr={lr:.2e}")

        p_va = perfil(model, tokenizer, val_rows, patch, ST_CLEAN, D, device,
                      all_layers, num_patch_positions)
        p_tr = perfil(model, tokenizer, train_rows, patch, ST_CLEAN, D, device,
                      all_layers, num_patch_positions)
        rel_va = sum(p_va[l]["rel"] for l in layers) / len(layers)
        rel_tr = sum(p_tr[l]["rel"] for l in layers) / len(layers)
        curva.append({"epoch": epoch + 1, "band_train": rel_tr, "band_heldout": rel_va,
                      "gap": rel_va - rel_tr, "norm": patch.norm(2).item(),
                      "perfil_heldout": p_va})

        print(f"\nEpoch {epoch + 1}: band (trayectoria)={sum(epoch_loss) / len(epoch_loss):.4f}"
              f"   norma={patch.norm(2).item():.6f}")
        print(f"  band del checkpoint:  train={rel_tr:.4f}   held-out={rel_va:.4f}"
              f"   brecha={rel_va - rel_tr:+.4f}   (1.0 = no hizo nada)")
        print(f"  {'capa':>5}{'rel':>9}{'cos':>9}{'mag':>9}   (held-out, * = entrenada)")
        for l in all_layers:
            if l % 4 == 0 or l in layers:
                m = p_va[l]
                print(f"  {l:>5}{m['rel']:>9.3f}{m['cos']:>9.3f}{m['mag']:>9.3f}"
                      f"{'   *' if l in layers else ''}")

        if rel_va < best["loss"]:
            best = {"loss": rel_va, "patch": patch.detach().clone(), "epoch": epoch + 1}
            print(f"  * mejor HELD-OUT hasta ahora ({rel_va:.4f})")
        if rel_tr < best_tr["loss"]:
            best_tr = {"loss": rel_tr, "patch": patch.detach().clone(), "epoch": epoch + 1}
            print(f"  * mejor TRAIN hasta ahora ({rel_tr:.4f})")

    os.makedirs(output_dir, exist_ok=True)
    final = best["patch"] if best["patch"] is not None else patch.detach()
    torch.save(final, os.path.join(output_dir, "lang_patch.pt"))
    torch.save(best["patch"], os.path.join(output_dir, "lang_patch_best_heldout.pt"))
    torch.save(best_tr["patch"], os.path.join(output_dir, "lang_patch_best_train.pt"))

    print("\n" + "=" * 70)
    print(f"{'epoch':>6}{'train':>10}{'held-out':>11}{'brecha':>10}{'norma':>10}")
    for c in curva:
        marca = ("  <- mejor held-out" if c["epoch"] == best["epoch"] else "") + \
                ("  <- mejor train" if c["epoch"] == best_tr["epoch"] else "")
        print(f"{c['epoch']:>6}{c['band_train']:>10.4f}{c['band_heldout']:>11.4f}"
              f"{c['gap']:>+10.4f}{c['norm']:>10.4f}{marca}")

    meta = {
        "objetivo": "activaciones",
        "aviso_circularidad": "entrenado CONTRA la direccion; no usar para sostener P1/P3 "
                              "de HALLAZGOS.md, que valen solo para el parche de CE",
        "target": target, "layers": layers, "n_layers": n_layers,
        "targets_csv": os.path.abspath(targets_csv),
        "filas_usables_para_d": len(idxs),
        "norma_d_por_capa": {l: D[LI[l]].norm().item() for l in all_layers},
        "patch_norm": final.norm(2).item(),
        "train_size": len(train_df), "test_size": len(test_df),
        "l2_weight": l2_weight, "step_size": step_size, "step_decay": step_decay,
        "batch_size": batch_size, "num_epochs": num_epochs,
        "num_steps_per_prompt": num_steps_per_prompt,
        "num_patch_positions": num_patch_positions,
        "train_test_split": train_test_split,
        "best_heldout_epoch": best["epoch"], "best_heldout_band": best["loss"],
        "best_train_epoch": best_tr["epoch"], "best_train_band": best_tr["loss"],
        "curva": curva,
    }
    with open(os.path.join(output_dir, "act_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"\nNorma final: {final.norm(2).item():.6f}  "
          f"(v_CE de referencia: 0.8021 -- aca la norma es RESULTADO, no hiperparametro)")
    for i in range(num_patch_positions):
        print(f"  posicion {i}: {final[0, i, :].norm(2).item():.6f}")
    print(f"\nGuardado en {output_dir}/")
    print("El .pt tiene el mismo formato que train_lang_patch.py: se evalua con")
    print(f"  python3 -u eval_lang_patch.py --model ... --patch {output_dir}/lang_patch.pt")
    return final


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--layers", required=True,
                    help="'14' | '12,16,20' | '12-16'. Capa = hidden_states[l], 1..L")
    ap.add_argument("--target", default="frq", choices=TARGETS,
                    help="frq=pregunta FR (ruta de entrada)  instr=instruccion FR "
                         "(ruta de directiva)  qde=pregunta DE  corto=piso generico  "
                         "random=control de norma igualada")
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--l2_weight", type=float, default=0.055)
    ap.add_argument("--num_epochs", type=int, default=8)
    ap.add_argument("--num_steps_per_prompt", type=int, default=20)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--step_size", type=float, default=0.00025)
    ap.add_argument("--step_decay", default="cosine", choices=["none", "cosine"])
    ap.add_argument("--batch_size", type=int, default=8)
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--val_n", type=int, default=20)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--cache_dir", default=DEFAULT_CACHE,
                    help="estados crudos por condicion; se reusan entre corridas")
    ap.add_argument("--refresh_cache", action="store_true",
                    help="recomputar aunque haya cache (el fingerprint ya invalida "
                         "solo si cambio el modelo o los prompts)")
    ap.add_argument("--no_gate", action="store_true")
    ap.add_argument("--no_truncate", action="store_true",
                    help="no cortar el forward en la capa mas profunda (debug)")
    args = ap.parse_args()

    train(args.model, args.targets, parse_layers(args.layers), args.target,
          args.output_dir, args.l2_weight, args.num_epochs,
          args.num_steps_per_prompt, args.num_patch_positions, args.step_size,
          args.train_test_split, args.device, use_gate=not args.no_gate,
          batch_size=args.batch_size, step_decay=args.step_decay,
          val_n=args.val_n, truncate=not args.no_truncate,
          cache_dir=args.cache_dir, refresh_cache=args.refresh_cache)


if __name__ == "__main__":
    main()
