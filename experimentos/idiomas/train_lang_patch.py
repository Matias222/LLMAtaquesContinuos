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


def train(model_path, targets_csv, l2_weight, output_dir,
          num_epochs=5, num_steps_per_prompt=75, num_patch_positions=3,
          step_size=0.00025, train_test_split=0.8, device="cuda:0",
          use_gate=True):
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

    print(f"\nTrain: {len(train_df)}  |  Held-out: {len(test_df)} (sin filtrar)")
    print(f"L2 weight: {l2_weight}  |  step_size: {step_size}  |  posiciones: {num_patch_positions}")
    print(f"Epochs: {num_epochs}  |  steps/prompt: {num_steps_per_prompt}")
    print("=" * 70)

    patch = torch.zeros(1, num_patch_positions, embedding_dim,
                        requires_grad=True, device=device)

    for epoch in range(num_epochs):
        print(f"\n{'#' * 70}\nEPOCH {epoch + 1}/{num_epochs}\n{'#' * 70}")
        epoch_ce = []

        for i, (_, row) in enumerate(train_df.iterrows()):
            sm = build_suffix_manager(tokenizer, row["prompt"], target=row["output"])
            tokens = sm.get_input_ids().to(device)
            target_tokens = tokens[sm._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()

            ces = []
            for _ in range(num_steps_per_prompt):
                total, _, ce, l2 = calc_loss(model, sm, prompt_embeds, patch,
                                             target_tokens, num_patch_positions, l2_weight)
                total.backward()
                patch.data -= torch.sign(patch.grad.data) * step_size
                model.zero_grad()
                patch.grad.zero_()
                ces.append(ce.item())

            epoch_ce.append(sum(ces) / len(ces))
            if (i + 1) % 10 == 0:
                print(f"  [{i + 1}/{len(train_df)}] CE={epoch_ce[-1]:.4f}  "
                      f"norma={patch.norm(2).item():.6f}")

        # Validacion: CE del target frances held-out bajo el parche vs sin parche.
        # Metrica graduada, no un booleano inventado.
        with torch.no_grad():
            val_p, val_b = [], []
            for _, row in test_df.head(8).iterrows():
                sm = build_suffix_manager(tokenizer, row["prompt"], target=row["output"])
                tokens = sm.get_input_ids().to(device)
                tt = tokens[sm._target_slice].to(device)
                pe = get_embeddings(model, tokens.unsqueeze(0)).detach()
                _, _, ce_p, _ = calc_loss(model, sm, pe, patch, tt, num_patch_positions, l2_weight)
                _, _, ce_b, _ = calc_loss(model, sm, pe, torch.zeros_like(patch), tt,
                                          num_patch_positions, l2_weight)
                val_p.append(ce_p.item())
                val_b.append(ce_b.item())

        print(f"\nEpoch {epoch + 1}: CE train={sum(epoch_ce) / len(epoch_ce):.4f}  "
              f"norma={patch.norm(2).item():.6f}")
        print(f"  held-out CE(target FR): con parche={sum(val_p) / len(val_p):.4f}  "
              f"sin parche={sum(val_b) / len(val_b):.4f}  "
              f"(baja = el parche acerca al frances)")
        print("-" * 70)

    os.makedirs(output_dir, exist_ok=True)
    patch_path = os.path.join(output_dir, "lang_patch.pt")
    meta_path = os.path.join(output_dir, "lang_metadata.pt")
    torch.save(patch.detach(), patch_path)

    metadata = {
        "language": "french",
        "instruction": "Answer in French.",
        "num_patch_positions": num_patch_positions,
        "patch_norm": patch.norm(2).item(),
        "train_size": len(train_df),
        "test_size": len(test_df),
        "prepend_target_prefix": False,
        "prefix_match_length": 0,
        "coherence_weight": 1.0,
        "l2_weight": l2_weight,
        "bot_penalty_weight": 0.0,
        "step_size": step_size,
        "num_epochs": num_epochs,
        "num_steps_per_prompt": num_steps_per_prompt,
    }
    torch.save(metadata, meta_path)

    print("\n" + "=" * 70)
    print(f"Norma final: {patch.norm(2).item():.6f}")
    for i in range(num_patch_positions):
        print(f"  posicion {i}: {patch[0, i, :].norm(2).item():.6f}")
    print(f"\nGuardado: {patch_path}\n          {meta_path}")
    return patch


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="targets_french.csv")
    ap.add_argument("--l2_weight", type=float, required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--num_epochs", type=int, default=5)
    ap.add_argument("--num_steps_per_prompt", type=int, default=75)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--step_size", type=float, default=0.00025)
    ap.add_argument("--train_test_split", type=float, default=0.8)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--no_gate", action="store_true",
                    help="entrenar sobre todos los targets, incluso los que no pasan el gate")
    args = ap.parse_args()

    train(args.model, args.targets, args.l2_weight, args.output_dir,
          args.num_epochs, args.num_steps_per_prompt, args.num_patch_positions,
          args.step_size, args.train_test_split, args.device, use_gate=not args.no_gate)


if __name__ == "__main__":
    main()
