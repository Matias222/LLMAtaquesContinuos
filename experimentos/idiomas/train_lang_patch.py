"""
Paso 1: entrenar el parche de idioma por teacher forcing con GRADIENTE.

Loss (identica en forma a la del mejor run noprefix, legacy/christmas_final_train.py
con prefix_match_length=0 / prepend_target_prefix=False / coherence_weight=1.0):

    L = CE(logits_parcheados, y_frances_completo) + lambda_L2 * ||v||^2

No hay objetivo de prefijo. El unico gradiente que existe empuja al parche a
reproducir la respuesta francesa entera, asi que no puede haber prefix hack.

Optimizador: sign-SGD, identico a legacy (data -= sign(grad) * step_size).

Hiperparametros copiados de resultados/primera_parte/noprefix_l2_0.08
(el mejor run noprefix: 53% de compliance en held-out):
    num_epochs            = 5
    num_steps_per_prompt  = 75
    num_patch_positions   = 3
    coherence_weight      = 1.0
    prefix_match_length   = 0
    step_size             = 0.00025
    train_test_split      = 0.8
Lo unico que se barre es l2_weight.
"""

import argparse
import math
import os

import pandas as pd
import torch
import torch.nn as nn

from lm import (DEFAULT_MODEL, PATCH_ANCHORS, apply_patch_first_n, build_suffix_manager,
                get_embedding_matrix, get_embeddings, load_model_and_tokenizer)


def calc_loss(model, sm, prompt_embeds, patch, target_tokens,
              num_patch_positions=3, l2_weight=0.08, patch_offset=0, loss_head_k=0,
              patch_anchor="goal"):
    """
    CE sobre el target + L2. Sin prefix loss, sin bot penalty.

    loss_head_k > 0 restringe la CE a los primeros k tokens del target: la
    decision de idioma vive ahi (ver nll_of_target), y la cola es donde el
    target ensena la FORMA de la respuesta (una oracion corta y punto), que
    es el estilo que no queremos que el parche absorba.
    """
    patched = apply_patch_first_n(sm, prompt_embeds, patch, num_patch_positions,
                                  offset=patch_offset, anchor=patch_anchor)
    logits = model(inputs_embeds=patched).logits

    ls = sm._loss_slice
    n = min(ls.stop - ls.start, len(target_tokens))
    if loss_head_k > 0:
        n = min(n, loss_head_k)
    if n > 0:
        ce = nn.CrossEntropyLoss()(logits[0, ls.start:ls.start + n, :], target_tokens[:n])
    else:
        ce = torch.tensor(0.0, device=patch.device, dtype=patch.dtype)

    l2 = patch.norm(2) ** 2
    return ce + l2_weight * l2, logits[:, ls, :], ce, l2


def cosine_step(base, global_step, total_steps):
    """Annealing coseno del step_size. Convierte la orbita en convergencia."""
    if total_steps <= 1:
        return base
    p = min(1.0, global_step / (total_steps - 1))
    return base * 0.5 * (1.0 + math.cos(math.pi * p))


def usable_prompt(row, col):
    """Texto del prompt en la columna `col`, o None si esta vacio o su gate de
    traduccion (`<col>_ok`) es False."""
    txt = str(row.get(col, "")).strip()
    if not txt:
        return None
    ok = str(row.get(f"{col}_ok", "True")).strip().lower()
    if ok == "false":
        return None
    return txt


@torch.no_grad()
def validate(model, tokenizer, patch, rows, num_patch_positions, l2_weight, head_k=5,
             patch_offset=0, prompt_col="prompt", patch_anchor="goal"):
    """CE del target frances en held-out, con y sin parche, partida en head/tail."""
    acc = {"p_all": [], "b_all": [], "p_head": [], "b_head": []}
    zero = torch.zeros_like(patch)
    for _, row in rows.iterrows():
        q = usable_prompt(row, prompt_col)
        if q is None:
            continue
        sm = build_suffix_manager(tokenizer, q, target=row["output"])
        tokens = sm.get_input_ids().to(patch.device)
        tt = tokens[sm._target_slice].to(patch.device)
        pe = get_embeddings(model, tokens.unsqueeze(0)).detach()
        for tag, v in (("p", patch), ("b", zero)):
            per_tok = per_token_ce(model, sm, pe, v, tt, num_patch_positions, patch_offset,
                                   patch_anchor)
            if per_tok is None:
                continue
            acc[f"{tag}_all"].append(per_tok.mean().item())
            acc[f"{tag}_head"].append(per_tok[:min(head_k, len(per_tok))].mean().item())
    return {k: (sum(v) / len(v) if v else float("nan")) for k, v in acc.items()}


def per_token_ce(model, sm, prompt_embeds, patch, target_tokens, num_patch_positions,
                 patch_offset=0, patch_anchor="goal"):
    patched = apply_patch_first_n(sm, prompt_embeds, patch, num_patch_positions,
                                  offset=patch_offset, anchor=patch_anchor)
    logits = model(inputs_embeds=patched).logits
    ls = sm._loss_slice
    n = min(ls.stop - ls.start, len(target_tokens))
    if n <= 0:
        return None
    return nn.CrossEntropyLoss(reduction="none")(
        logits[0, ls.start:ls.start + n, :], target_tokens[:n])


def train(model_path, targets_csv, l2_weight, output_dir,
          num_epochs=5, num_steps_per_prompt=75, num_patch_positions=3,
          step_size=0.00025, train_test_split=0.8, device="cuda:0",
          use_gate=True, batch_size=1, step_decay="none", val_n=8,
          save_best=False, head_k=5, patch_offset=0, loss_head_k=0,
          prompt_cols=("prompt",), patch_anchor="goal", init_patch=None):
    """
    Defaults = comportamiento original (batch_size=1, sin annealing, ultimo
    checkpoint), para que los runs viejos sigan siendo reproducibles.

    loss_head_k: CE solo sobre los primeros k tokens del target (0 = todo).

    prompt_cols: columnas del CSV que se usan como pregunta de entrada, p.ej.
    ("prompt", "prompt_es", "prompt_de"). El target frances (`output`) es el
    mismo para todas: la respuesta correcta en frances no depende del idioma
    en que se hizo la pregunta. Con mas de una columna cada fila entra una
    vez por idioma en el mismo batch, asi que un solo v tiene que llevar al
    frances desde cualquiera de las entradas y no puede apoyarse en "la
    entrada esta en ingles" (cross_lang_patch.py mostro que v4 lo hace).
    Las filas cuya traduccion no paso el gate (`<col>_ok` = False) se saltean
    para esa columna. La validacion se hace por columna y el checkpoint se
    elige por el promedio.

    patch_offset: el parche se suma a las posiciones goal_start + offset ... + N
    en vez de a las primeras N. Es el control de posicion: si un parche
    entrenado en las posiciones 5-7 funciona igual que uno en 1-3, el efecto no
    depende de estar al inicio (attention sink); si no, si.
    """
    df = pd.read_csv(targets_csv, sep=";", keep_default_na=False)

    # Split POSICIONAL sobre el dataset completo, igual que legacy.
    n_train = int(len(df) * train_test_split)
    train_df, test_df = df.iloc[:n_train], df.iloc[n_train:]

    # El gate solo filtra TRAIN. El held-out se evalua entero, sin filtrar,
    # para no inflar los numeros del eval.
    if use_gate and "passed_gate" in train_df.columns:
        before = len(train_df)
        train_df = train_df[train_df["passed_gate"].astype(str).str.lower() == "true"]
        print(f"Gate de calidad sobre train: {len(train_df)}/{before} targets limpios")

    prompt_cols = tuple(prompt_cols)
    faltan = [c for c in prompt_cols if c not in df.columns]
    if faltan:
        raise SystemExit(f"columnas de prompt ausentes en {targets_csv}: {faltan}")

    model, tokenizer = load_model_and_tokenizer(model_path, device=device)
    # Solo el parche se optimiza. Sin esto backward() calcula y guarda el
    # gradiente de los 3B parametros del modelo en cada paso, para tirarlo.
    for prm in model.parameters():
        prm.requires_grad_(False)
    embedding_dim = get_embedding_matrix(model).shape[1]

    val_rows = test_df.head(val_n)
    # Mismo tamanio de muestra sobre TRAIN, para medir la CE del checkpoint de
    # cada epoch en las dos poblaciones y poder comparar los dos criterios.
    # No se usa epoch_ce para esto: ese es el promedio de la trayectoria (todos
    # los pasos de la epoch, incluidos los primeros con un parche peor), no una
    # medicion del parche que queda al final de la epoch. Como baja de forma
    # monotona, elegir por ahi devolveria siempre la ultima epoch.
    train_rows = train_df.head(val_n)
    n_batches = math.ceil(len(train_df) / batch_size)
    total_steps = num_epochs * n_batches * num_steps_per_prompt

    print(f"\nTrain: {len(train_df)}  |  Held-out: {len(test_df)}  |  validacion: {len(val_rows)}")
    print(f"L2: {l2_weight}  |  step_size: {step_size} ({step_decay})  |  posiciones: {num_patch_positions}"
          + (f"  |  offset: {patch_offset}" if patch_offset else "")
          + (f"  |  anchor: {patch_anchor}" if patch_anchor != "goal" else ""))
    if patch_anchor == "header":
        sm_ = build_suffix_manager(tokenizer, train_df.iloc[0]["prompt"], target="x")
        toks_ = sm_.get_input_ids()
        from lm import patch_positions
        s_, n_ = patch_positions(sm_, num_patch_positions, patch_offset, patch_anchor)
        print(f"  parche sobre el header del assistant: posiciones {s_}..{s_ + n_ - 1} = "
              f"{[tokenizer.decode([int(t)]) for t in toks_[s_:s_ + n_]]}")
    print(f"Loss: CE sobre {'los primeros ' + str(loss_head_k) + ' tokens' if loss_head_k else 'todo el target'}"
          f"  |  entradas: {list(prompt_cols)}")
    if len(prompt_cols) > 1:
        for c in prompt_cols:
            n_ok = sum(usable_prompt(r, c) is not None for _, r in train_df.iterrows())
            print(f"  {c}: {n_ok}/{len(train_df)} filas de train usables")
    if patch_offset and patch_anchor == "goal":
        # Preguntas mas cortas que offset + N reciben un parche recortado (o
        # ninguno). Contarlas ANTES de entrenar: si son muchas, el run no mide
        # lo que dice medir.
        cortos = 0
        for _, row in train_df.iterrows():
            sm_ = build_suffix_manager(tokenizer, row["prompt"], target=row["output"])
            sm_.get_input_ids()     # los slices se calculan aca, no en el constructor
            if sm_._goal_slice.stop - sm_._goal_slice.start < patch_offset + num_patch_positions:
                cortos += 1
        print(f"  AVISO offset: {cortos}/{len(train_df)} prompts de train tienen goal mas corto que "
              f"offset + N = {patch_offset + num_patch_positions} tokens (parche recortado ahi)")
    print(f"Epochs: {num_epochs}  |  batch: {batch_size} ({n_batches} batches/epoch)  "
          f"|  steps/batch: {num_steps_per_prompt}")
    print(f"Checkpoint: {'mejor por CE held-out' if save_best else 'ultimo'}")
    print("=" * 70)

    if init_patch:
        # Arranque en caliente desde un parche ya entrenado. OJO: el schedule
        # del step_size arranca de nuevo (coseno desde step_size hasta 0 sobre
        # las epochs de ESTA corrida), asi que no es "seguir donde quedo" sino
        # un warm restart; con un step_size mas chico se parece mas a seguir.
        init = torch.load(init_patch, map_location=device).to(device).float()
        assert tuple(init.shape) == (1, num_patch_positions, embedding_dim), \
            f"--init_patch {init_patch}: shape {tuple(init.shape)}, esperada (1, {num_patch_positions}, {embedding_dim})"
        patch = init.clone().detach().requires_grad_(True)
        print(f"Init: {init_patch}  (norma {patch.norm(2).item():.4f})")
    else:
        patch = torch.zeros(1, num_patch_positions, embedding_dim,
                            requires_grad=True, device=device)
    best = {"ce": float("inf"), "patch": None, "epoch": None}          # held-out
    best_tr = {"ce": float("inf"), "patch": None, "epoch": None}       # train
    curva = []
    global_step = 0

    for epoch in range(num_epochs):
        print(f"\n{'#' * 70}\nEPOCH {epoch + 1}/{num_epochs}\n{'#' * 70}")
        epoch_ce = []

        for b in range(n_batches):
            batch = train_df.iloc[b * batch_size:(b + 1) * batch_size]

            # Precomputar embeddings del batch una sola vez.
            items = []
            for _, row in batch.iterrows():
                for col in prompt_cols:
                    q = usable_prompt(row, col)
                    if q is None:
                        continue
                    sm = build_suffix_manager(tokenizer, q, target=row["output"])
                    tokens = sm.get_input_ids().to(device)
                    items.append((sm,
                                  get_embeddings(model, tokens.unsqueeze(0)).detach(),
                                  tokens[sm._target_slice].to(device)))
            if not items:
                continue

            ces = []
            for _ in range(num_steps_per_prompt):
                # Acumular el gradiente sobre TODO el batch antes de dar el paso.
                # Con batch_size=1 esto es identico al loop original; con B>1 el
                # parche optimiza el objetivo promedio en vez de ir a los tirones
                # detras de cada prompt.
                step_ce = []
                for sm, pe, tt in items:
                    total, _, ce, _ = calc_loss(model, sm, pe, patch, tt,
                                                num_patch_positions, l2_weight,
                                                patch_offset, loss_head_k, patch_anchor)
                    (total / len(items)).backward()
                    step_ce.append(ce.item())

                lr = cosine_step(step_size, global_step, total_steps) \
                    if step_decay == "cosine" else step_size
                patch.data -= torch.sign(patch.grad.data) * lr
                model.zero_grad()
                patch.grad.zero_()
                global_step += 1
                ces.append(sum(step_ce) / len(step_ce))

            epoch_ce.append(sum(ces) / len(ces))
            if (b + 1) % max(1, 10 // batch_size) == 0:
                print(f"  [batch {b + 1}/{n_batches}] CE={epoch_ce[-1]:.4f}  "
                      f"norma={patch.norm(2).item():.6f}  lr={lr:.2e}")

        # Validacion por columna de entrada; v y t son el promedio, que es lo
        # que decide el checkpoint. Con una sola columna es identico a antes.
        v_cols = {c: validate(model, tokenizer, patch, val_rows, num_patch_positions,
                              l2_weight, head_k, patch_offset, prompt_col=c,
                              patch_anchor=patch_anchor) for c in prompt_cols}
        t_cols = {c: validate(model, tokenizer, patch, train_rows, num_patch_positions,
                              l2_weight, head_k, patch_offset, prompt_col=c,
                              patch_anchor=patch_anchor) for c in prompt_cols}
        v = {k: sum(d[k] for d in v_cols.values()) / len(v_cols) for k in v_cols[prompt_cols[0]]}
        t = {k: sum(d[k] for d in t_cols.values()) / len(t_cols) for k in t_cols[prompt_cols[0]]}
        gap = v["p_head"] - t["p_head"]
        curva.append({"epoch": epoch + 1, "train_head": t["p_head"],
                      "heldout_head": v["p_head"], "gap": gap,
                      "norm": patch.norm(2).item(),
                      "heldout_head_por_col": {c: d["p_head"] for c, d in v_cols.items()}})
        if len(prompt_cols) > 1:
            print("  held-out head CE por entrada: " + "  ".join(
                f"{c}={d['p_head']:.4f}" for c, d in v_cols.items()))
        print(f"\nEpoch {epoch + 1}: CE train (trayectoria)={sum(epoch_ce) / len(epoch_ce):.4f}  "
              f"norma={patch.norm(2).item():.6f}")
        print(f"  CE head del checkpoint:  train={t['p_head']:.4f}   "
              f"held-out={v['p_head']:.4f}   brecha={gap:+.4f}")
        print(f"  held-out CE  head(primeros {head_k}): con parche={v['p_head']:.4f}  "
              f"sin parche={v['b_head']:.4f}  delta={v['p_head'] - v['b_head']:+.4f}")
        print(f"               toda la respuesta      : con parche={v['p_all']:.4f}  "
              f"sin parche={v['b_all']:.4f}  delta={v['p_all'] - v['b_all']:+.4f}")

        if v["p_head"] < best["ce"]:
            best = {"ce": v["p_head"], "patch": patch.detach().clone(), "epoch": epoch + 1}
            print(f"  * mejor HELD-OUT hasta ahora (head CE {v['p_head']:.4f})")
        if t["p_head"] < best_tr["ce"]:
            best_tr = {"ce": t["p_head"], "patch": patch.detach().clone(), "epoch": epoch + 1}
            print(f"  * mejor TRAIN hasta ahora (head CE {t['p_head']:.4f})")
        print("-" * 70)

    final = best["patch"] if (save_best and best["patch"] is not None) else patch.detach()
    if save_best:
        print(f"\nGuardando el parche de la epoch {best['epoch']} (head CE {best['ce']:.4f})")

    os.makedirs(output_dir, exist_ok=True)
    patch_path = os.path.join(output_dir, "lang_patch.pt")
    meta_path = os.path.join(output_dir, "lang_metadata.pt")
    torch.save(final, patch_path)

    # Los dos criterios, cada uno en su archivo, para poder compararlos en el
    # eval. lang_patch.pt sigue siendo el canonico (el de held-out si
    # --save_best) para no romper los comandos existentes.
    ho_path = os.path.join(output_dir, "lang_patch_best_heldout.pt")
    tr_path = os.path.join(output_dir, "lang_patch_best_train.pt")
    if best["patch"] is not None:
        torch.save(best["patch"], ho_path)
    if best_tr["patch"] is not None:
        torch.save(best_tr["patch"], tr_path)

    print("\n" + "=" * 70)
    print("CURVA POR EPOCH (CE del head sobre el checkpoint de esa epoch)")
    print(f"{'epoch':>6}{'train':>10}{'held-out':>11}{'brecha':>10}{'norma':>10}")
    print("-" * 47)
    for c in curva:
        marca = ""
        if c["epoch"] == best["epoch"]:
            marca += "  <- mejor held-out"
        if c["epoch"] == best_tr["epoch"]:
            marca += "  <- mejor train"
        print(f"{c['epoch']:>6}{c['train_head']:>10.4f}{c['heldout_head']:>11.4f}"
              f"{c['gap']:>+10.4f}{c['norm']:>10.4f}{marca}")
    print(f"\n  mejor por HELD-OUT: epoch {best['epoch']} (CE {best['ce']:.4f})  -> {ho_path}")
    print(f"  mejor por TRAIN   : epoch {best_tr['epoch']} (CE {best_tr['ce']:.4f})  -> {tr_path}")
    if best["epoch"] != best_tr["epoch"]:
        print("  los dos criterios NO coinciden: compara los dos parches en el eval,")
        print("  la CE del head es un proxy y lo que decide es is_french sobre generacion.")

    metadata = {
        "language": "french",
        "instruction": "Answer in French.",
        "targets_csv": os.path.abspath(targets_csv),
        "train_test_split": train_test_split,
        "prompt_cols": list(prompt_cols),
        "loss_head_k": loss_head_k,
        "num_patch_positions": num_patch_positions,
        "patch_offset": patch_offset,
        "patch_anchor": patch_anchor,
        "init_patch": os.path.abspath(init_patch) if init_patch else None,
        "patch_norm": final.norm(2).item(),
        "train_size": len(train_df),
        "test_size": len(test_df),
        "prepend_target_prefix": False,
        "prefix_match_length": 0,
        "coherence_weight": 1.0,
        "l2_weight": l2_weight,
        "bot_penalty_weight": 0.0,
        "step_size": step_size,
        "step_decay": step_decay,
        "batch_size": batch_size,
        "num_epochs": num_epochs,
        "num_steps_per_prompt": num_steps_per_prompt,
        "save_best": save_best,
        "best_epoch": best["epoch"] if save_best else None,
        "best_head_ce": best["ce"] if save_best else None,
        "best_heldout_epoch": best["epoch"],
        "best_heldout_head_ce": best["ce"],
        "best_train_epoch": best_tr["epoch"],
        "best_train_head_ce": best_tr["ce"],
        "curva": curva,
    }
    torch.save(metadata, meta_path)

    print("\n" + "=" * 70)
    print(f"Norma final: {final.norm(2).item():.6f}")
    for i in range(num_patch_positions):
        print(f"  posicion {i}: {final[0, i, :].norm(2).item():.6f}")
    print(f"\nGuardado: {patch_path}\n          {meta_path}")
    return final


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--l2_weight", type=float, required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--num_epochs", type=int, default=5)
    ap.add_argument("--num_steps_per_prompt", type=int, default=75,
                    help="pasos por batch (con batch_size=1, pasos por prompt)")
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--step_size", type=float, default=0.00025)
    ap.add_argument("--train_test_split", type=float, default=0.85)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--no_gate", action="store_true",
                    help="entrenar sobre todos los targets, incluso los que no pasan el gate")
    ap.add_argument("--batch_size", type=int, default=1,
                    help="prompts por paso. >1 acumula gradiente y optimiza el objetivo promedio")
    ap.add_argument("--step_decay", choices=["none", "cosine"], default="none")
    ap.add_argument("--val_n", type=int, default=8, help="prompts de validacion por epoch")
    ap.add_argument("--save_best", action="store_true",
                    help="guardar el parche con mejor head CE en vez del ultimo")
    ap.add_argument("--head_k", type=int, default=5)
    ap.add_argument("--patch_offset", type=int, default=0,
                    help="sumar el parche en goal_start + offset ... + N en vez de en las "
                         "primeras N posiciones (control de posicion / attention sink)")
    ap.add_argument("--loss_head_k", type=int, default=0,
                    help="CE solo sobre los primeros k tokens del target (0 = target completo)")
    ap.add_argument("--prompt_cols", default="prompt",
                    help="columnas de pregunta separadas por coma, p.ej. prompt,prompt_es,prompt_de")
    ap.add_argument("--init_patch", default=None,
                    help="parche .pt desde el que arrancar (warm start) en vez de ceros")
    ap.add_argument("--patch_anchor", choices=list(PATCH_ANCHORS), default="goal",
                    help="goal: primeras N de la pregunta (default). header: ultimos N tokens "
                         "del header del assistant, identicos en todos los prompts")
    args = ap.parse_args()

    train(args.model, args.targets, args.l2_weight, args.output_dir,
          args.num_epochs, args.num_steps_per_prompt, args.num_patch_positions,
          args.step_size, args.train_test_split, args.device, use_gate=not args.no_gate,
          batch_size=args.batch_size, step_decay=args.step_decay, val_n=args.val_n,
          save_best=args.save_best, head_k=args.head_k, patch_offset=args.patch_offset,
          loss_head_k=args.loss_head_k,
          prompt_cols=tuple(c.strip() for c in args.prompt_cols.split(",") if c.strip()),
          patch_anchor=args.patch_anchor, init_patch=args.init_patch)


if __name__ == "__main__":
    main()
