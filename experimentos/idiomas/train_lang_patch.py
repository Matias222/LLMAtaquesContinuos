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

from lm import (DEFAULT_MODEL, apply_patch_first_n, build_suffix_manager,
                get_embedding_matrix, get_embeddings, load_model_and_tokenizer)


def calc_loss(model, sm, prompt_embeds, patch, target_tokens,
              num_patch_positions=3, l2_weight=0.08):
    """CE sobre el target completo + L2. Sin prefix loss, sin bot penalty."""
    patched = apply_patch_first_n(sm, prompt_embeds, patch, num_patch_positions)
    logits = model(inputs_embeds=patched).logits

    ls = sm._loss_slice
    n = min(ls.stop - ls.start, len(target_tokens))
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


@torch.no_grad()
def validate(model, tokenizer, patch, rows, num_patch_positions, l2_weight, head_k=5):
    """CE del target frances en held-out, con y sin parche, partida en head/tail."""
    acc = {"p_all": [], "b_all": [], "p_head": [], "b_head": []}
    zero = torch.zeros_like(patch)
    for _, row in rows.iterrows():
        sm = build_suffix_manager(tokenizer, row["prompt"], target=row["output"])
        tokens = sm.get_input_ids().to(patch.device)
        tt = tokens[sm._target_slice].to(patch.device)
        pe = get_embeddings(model, tokens.unsqueeze(0)).detach()
        for tag, v in (("p", patch), ("b", zero)):
            per_tok = per_token_ce(model, sm, pe, v, tt, num_patch_positions)
            if per_tok is None:
                continue
            acc[f"{tag}_all"].append(per_tok.mean().item())
            acc[f"{tag}_head"].append(per_tok[:min(head_k, len(per_tok))].mean().item())
    return {k: (sum(v) / len(v) if v else float("nan")) for k, v in acc.items()}


def per_token_ce(model, sm, prompt_embeds, patch, target_tokens, num_patch_positions):
    patched = apply_patch_first_n(sm, prompt_embeds, patch, num_patch_positions)
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
          save_best=False, head_k=5):
    """
    Defaults = comportamiento original (batch_size=1, sin annealing, ultimo
    checkpoint), para que los runs viejos sigan siendo reproducibles.
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

    model, tokenizer = load_model_and_tokenizer(model_path, device=device)
    embedding_dim = get_embedding_matrix(model).shape[1]

    val_rows = test_df.head(val_n)
    n_batches = math.ceil(len(train_df) / batch_size)
    total_steps = num_epochs * n_batches * num_steps_per_prompt

    print(f"\nTrain: {len(train_df)}  |  Held-out: {len(test_df)}  |  validacion: {len(val_rows)}")
    print(f"L2: {l2_weight}  |  step_size: {step_size} ({step_decay})  |  posiciones: {num_patch_positions}")
    print(f"Epochs: {num_epochs}  |  batch: {batch_size} ({n_batches} batches/epoch)  "
          f"|  steps/batch: {num_steps_per_prompt}")
    print(f"Checkpoint: {'mejor por CE held-out' if save_best else 'ultimo'}")
    print("=" * 70)

    patch = torch.zeros(1, num_patch_positions, embedding_dim,
                        requires_grad=True, device=device)
    best = {"ce": float("inf"), "patch": None, "epoch": None}
    global_step = 0

    for epoch in range(num_epochs):
        print(f"\n{'#' * 70}\nEPOCH {epoch + 1}/{num_epochs}\n{'#' * 70}")
        epoch_ce = []

        for b in range(n_batches):
            batch = train_df.iloc[b * batch_size:(b + 1) * batch_size]

            # Precomputar embeddings del batch una sola vez.
            items = []
            for _, row in batch.iterrows():
                sm = build_suffix_manager(tokenizer, row["prompt"], target=row["output"])
                tokens = sm.get_input_ids().to(device)
                items.append((sm,
                              get_embeddings(model, tokens.unsqueeze(0)).detach(),
                              tokens[sm._target_slice].to(device)))

            ces = []
            for _ in range(num_steps_per_prompt):
                # Acumular el gradiente sobre TODO el batch antes de dar el paso.
                # Con batch_size=1 esto es identico al loop original; con B>1 el
                # parche optimiza el objetivo promedio en vez de ir a los tirones
                # detras de cada prompt.
                step_ce = []
                for sm, pe, tt in items:
                    total, _, ce, _ = calc_loss(model, sm, pe, patch, tt,
                                                num_patch_positions, l2_weight)
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

        v = validate(model, tokenizer, patch, val_rows, num_patch_positions,
                     l2_weight, head_k)
        print(f"\nEpoch {epoch + 1}: CE train={sum(epoch_ce) / len(epoch_ce):.4f}  "
              f"norma={patch.norm(2).item():.6f}")
        print(f"  held-out CE  head(primeros {head_k}): con parche={v['p_head']:.4f}  "
              f"sin parche={v['b_head']:.4f}  delta={v['p_head'] - v['b_head']:+.4f}")
        print(f"               toda la respuesta      : con parche={v['p_all']:.4f}  "
              f"sin parche={v['b_all']:.4f}  delta={v['p_all'] - v['b_all']:+.4f}")

        if v["p_head"] < best["ce"]:
            best = {"ce": v["p_head"], "patch": patch.detach().clone(), "epoch": epoch + 1}
            print(f"  * mejor hasta ahora (head CE {v['p_head']:.4f})")
        print("-" * 70)

    final = best["patch"] if (save_best and best["patch"] is not None) else patch.detach()
    if save_best:
        print(f"\nGuardando el parche de la epoch {best['epoch']} (head CE {best['ce']:.4f})")

    os.makedirs(output_dir, exist_ok=True)
    patch_path = os.path.join(output_dir, "lang_patch.pt")
    meta_path = os.path.join(output_dir, "lang_metadata.pt")
    torch.save(final, patch_path)

    metadata = {
        "language": "french",
        "instruction": "Answer in French.",
        "num_patch_positions": num_patch_positions,
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
    args = ap.parse_args()

    train(args.model, args.targets, args.l2_weight, args.output_dir,
          args.num_epochs, args.num_steps_per_prompt, args.num_patch_positions,
          args.step_size, args.train_test_split, args.device, use_gate=not args.no_gate,
          batch_size=args.batch_size, step_decay=args.step_decay, val_n=args.val_n,
          save_best=args.save_best, head_k=args.head_k)


if __name__ == "__main__":
    main()
