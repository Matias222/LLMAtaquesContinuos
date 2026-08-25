"""
Christmas Personality Experiment - Multi-scale Training Script

Variante de christmas_final_train.py que entrena el patch con multi-scale loss.
En cada training step, el patch se aplica escalado por varios alphas y se promedian
las losses. Forza al optimizer a producir Christmas en una *ventana de scales*,
no en un punto unico.

Hipotesis: si el patch resultante escala monotonicamente al testear a alpha en
[0.5, 2.0], existe una "direccion" navidena en layer-0. Si solo funciona en el
rango trained, el patch sigue siendo una "llave calibrada" pero con ventana mas
amplia que single-scale.

Diferencias clave vs christmas_final_train.py:
1. apply_patch_to_first_n_tokens acepta `scale` (default 1.0)
2. calc_loss_multiscale itera sobre `alphas`, promedia per-alpha losses,
   y agrega L2 + BOT penalty UNA SOLA VEZ (regularizers no se promedian)
3. train_christmas_patch acepta `alphas: List[float] = [1.0]`. alphas=[1.0]
   reproduce el comportamiento single-scale (backwards-compatible)
4. metadata guarda `alphas` para identificar el setup en analisis posteriores

El gradient pasa por las K forward passes (autograd lo maneja). Sign-based
update sigue igual.
"""

import _bootstrap  # noqa: F401  (repo root -> sys.path)

import os
from typing import List

import pandas as pd
import torch
import torch.nn as nn
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LlamaForCausalLM,
)


# Target prefix opcional (solo se usa si prepend_target_prefix=True)
CHRISTMAS_TARGET = "Ho ho ho!"


# ---------------------------------------------------------------------------
# Model / embedding helpers (identicos a christmas_final_train.py)
# ---------------------------------------------------------------------------

def load_model_and_tokenizer(model_path, tokenizer_path=None, device="cuda:0", **kwargs):
    model = (
        AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, trust_remote_code=True, **kwargs
        )
        .to(device)
        .eval()
    )

    tokenizer_path = model_path if tokenizer_path is None else tokenizer_path
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True, use_fast=False)

    if 'Llama-3.2' in tokenizer_path:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = 'left'
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer


def get_embeddings(model, input_ids):
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens(input_ids)
    raise ValueError(f"Unknown model type: {type(model)}")


def get_embedding_matrix(model):
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    raise ValueError(f"Unknown model type: {type(model)}")


# ---------------------------------------------------------------------------
# Patch application con scale
# ---------------------------------------------------------------------------

def apply_patch_scaled(suffix_manager, prompt_embeds, patch, num_patch_positions=3, scale=1.0):
    """
    Aplica el patch escalado por `scale` a las primeras N posiciones del goal.
    `scale=1.0` reproduce exactamente apply_patch_to_first_n_tokens de
    christmas_final_train.py (backward compatible).
    """
    patched_embeds = prompt_embeds.clone()

    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start

    actual_patch_positions = min(num_patch_positions, goal_length)

    patched_embeds[:, goal_start:goal_start+actual_patch_positions, :] = (
        prompt_embeds[:, goal_start:goal_start+actual_patch_positions, :]
        + scale * patch[:, :actual_patch_positions, :]
    )

    return patched_embeds


# ---------------------------------------------------------------------------
# Multi-scale loss
# ---------------------------------------------------------------------------

def _per_alpha_data_loss(model, suffix_manager, prompt_embeds, patch, target_tokens,
                         num_patch_positions, prefix_match_length, coherence_weight, scale):
    """
    Computa prefix_loss + coherence_weight * coherence_loss para un solo alpha.
    NO incluye L2 ni BOT penalty (esos van fuera, una sola vez).
    Devuelve (data_loss, prefix_loss, coh_loss, logits_for_loss_slice).
    """
    patched_embeds = apply_patch_scaled(
        suffix_manager, prompt_embeds, patch, num_patch_positions, scale=scale,
    )
    logits_patched = model(inputs_embeds=patched_embeds).logits

    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    if actual_prefix_length > 0:
        prefix_loss = nn.CrossEntropyLoss()(
            logits_patched[0, loss_slice.start:prefix_end, :],
            target_tokens[:actual_prefix_length],
        )
    else:
        prefix_loss = torch.tensor(0.0, device=patch.device, dtype=patch.dtype)

    coh_loss = torch.tensor(0.0, device=patch.device, dtype=patch.dtype)
    post_prefix_token_count = len(target_tokens) - actual_prefix_length
    if post_prefix_token_count > 0:
        post_prefix_targets = target_tokens[actual_prefix_length:]
        post_prefix_logits_end = min(prefix_end + post_prefix_token_count, loss_slice.stop)
        actual_post_prefix_length = post_prefix_logits_end - prefix_end
        if actual_post_prefix_length > 0:
            coh_loss = nn.CrossEntropyLoss()(
                logits_patched[0, prefix_end:post_prefix_logits_end, :],
                post_prefix_targets[:actual_post_prefix_length],
            )

    data_loss = prefix_loss + coherence_weight * coh_loss
    return (data_loss, prefix_loss, coh_loss,
            logits_patched[:, suffix_manager._loss_slice, :])


def calc_loss_multiscale(model, suffix_manager, prompt_embeds, patch, target_tokens,
                         num_patch_positions=3, prefix_match_length=4,
                         coherence_weight=0.1, l2_weight=0.01,
                         bot_penalty_weight=0.0, bot_direction=None,
                         alphas: List[float] = (1.0,)):
    """
    Loss multiescala:
        L_total = mean_over_alphas(prefix + coherence_weight * coherence)
                  + l2_weight * |patch|^2
                  + bot_penalty_weight * |proj(patch onto bot_direction)|^2

    Regularizers (L2, BOT) se computan UNA sola vez sobre el patch base (NO el
    patch escalado), porque son propiedades del parametro, no de su forward
    pass. Solo la data loss se promedia sobre alphas.
    """
    n_alphas = len(alphas)
    if n_alphas == 0:
        raise ValueError("alphas must be non-empty")

    sum_data_loss = torch.tensor(0.0, device=patch.device, dtype=patch.dtype)
    sum_prefix_loss = torch.tensor(0.0, device=patch.device, dtype=patch.dtype)
    sum_coh_loss = torch.tensor(0.0, device=patch.device, dtype=patch.dtype)
    last_loss_slice_logits = None

    for alpha in alphas:
        data_loss, prefix_loss, coh_loss, loss_slice_logits = _per_alpha_data_loss(
            model, suffix_manager, prompt_embeds, patch, target_tokens,
            num_patch_positions, prefix_match_length, coherence_weight, scale=alpha,
        )
        sum_data_loss = sum_data_loss + data_loss
        sum_prefix_loss = sum_prefix_loss + prefix_loss
        sum_coh_loss = sum_coh_loss + coh_loss
        last_loss_slice_logits = loss_slice_logits

    avg_data_loss = sum_data_loss / n_alphas
    avg_prefix_loss = sum_prefix_loss / n_alphas
    avg_coh_loss = sum_coh_loss / n_alphas

    # Regularizers (computados sobre el patch BASE, no escalado)
    l2_loss = patch.norm(2) ** 2

    bot_loss = torch.tensor(0.0, device=patch.device, dtype=patch.dtype)
    if bot_penalty_weight > 0 and bot_direction is not None:
        projections = patch @ bot_direction.to(patch.dtype)
        bot_loss = (projections ** 2).sum()

    total_loss = (avg_data_loss
                  + l2_weight * l2_loss
                  + bot_penalty_weight * bot_loss)

    return (total_loss, last_loss_slice_logits,
            avg_prefix_loss, avg_coh_loss, l2_loss, bot_loss)


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------

def train_christmas_patch(
    model_path: str,
    csv_path: str,
    num_epochs: int = 5,
    num_steps_per_prompt: int = 50,
    device: str = "cuda:0",
    step_size: float = 0.00025,
    num_patch_positions: int = 3,
    prefix_match_length: int = 4,
    coherence_weight: float = 0.1,
    l2_weight: float = 0.055,
    bot_penalty_weight: float = 0.0,
    train_test_split: float = 0.8,
    seed: int = 42,
    prepend_target_prefix: bool = True,
    output_dir: str = None,
    alphas: List[float] = (1.0,),
):
    """
    Multi-scale variant. Identico a christmas_final_train.train_christmas_patch
    excepto que la loss se promedia sobre `alphas` (lista de scales aplicados
    al patch en cada forward pass).

    alphas=[1.0] reproduce el comportamiento single-scale.
    alphas=[0.7, 1.0, 1.3] forza al optimizer a encontrar un patch que produzca
    el target en una ventana de scales (test directo de H2: "el patch es una
    direccion escalable" vs "el patch es una llave calibrada").

    Args:
        alphas: lista de scales (>0) que se aplican al patch en cada step.
                La data loss (prefix + coherence) se promedia sobre todos los
                alphas; la regularizacion (L2, BOT) se computa una sola vez.
                Cada step hace len(alphas) forward passes (cost lineal en K).
    """
    if seed is not None:
        torch.manual_seed(seed)

    alphas = list(alphas)
    if len(alphas) == 0:
        raise ValueError("alphas must be non-empty")
    if any(a <= 0 for a in alphas):
        raise ValueError(f"all alphas must be > 0, got {alphas}")

    print("=" * 70)
    print("CHRISTMAS PERSONALITY PATCH - MULTI-SCALE EXPERIMENT")
    print("Multi-scale layer-0 patch training")
    print("=" * 70)

    # Load model
    print("\nLoading model...")
    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device,
    )

    # Load and split data
    print("Loading dataset...")
    df = pd.read_csv(csv_path, delimiter=";")

    n_train = int(len(df) * train_test_split)
    train_df = df.iloc[:n_train]
    test_df = df.iloc[n_train:]

    print(f"\nDataset split:")
    print(f"  CSV: {csv_path}")
    print(f"  Total rows: {len(df)}")
    print(f"  Training: {len(train_df)} prompts")
    print(f"  Testing:  {len(test_df)} prompts")
    print(f"\nTarget prefix: '{CHRISTMAS_TARGET}'  (prepend={prepend_target_prefix})")
    print(f"Epochs: {num_epochs}")
    print(f"Steps per prompt: {num_steps_per_prompt}")
    print(f"Patch positions: First {num_patch_positions} tokens of goal slice")
    print(f"Prefix match length: {prefix_match_length} tokens")
    print(f"Step size (sign-based): {step_size}")
    print(f"Coherence weight: {coherence_weight}")
    print(f"L2 weight: {l2_weight}")
    print(f"BOT penalty weight: {bot_penalty_weight}")
    print(f"ALPHAS (multi-scale): {alphas}  ({len(alphas)} forward passes per step)")

    # Initialize global patch
    embedding_matrix = get_embedding_matrix(model)
    embedding_dim = embedding_matrix.shape[1]
    global_patch = torch.zeros(1, num_patch_positions, embedding_dim,
                               requires_grad=True, device=device)

    # bot_direction si vamos a usar bot_penalty
    bot_direction = None
    if bot_penalty_weight > 0:
        bot_id = tokenizer.bos_token_id
        if bot_id is None:
            raise ValueError("tokenizer.bos_token_id is None; cannot use bot_penalty_weight > 0")
        bot_embed = embedding_matrix[bot_id].detach().float()
        bot_direction = (bot_embed / bot_embed.norm().clamp(min=1e-12)).to(device)
        print(f"\nBOT token: id={bot_id}  |v_bot|={bot_embed.norm().item():.4f}")

    print(f"\nInitialized global patch shape: {tuple(global_patch.shape)}")
    print(f"Initial patch norm: {global_patch.norm(2).item():.6f}")
    print("=" * 70)

    # Training loop
    for epoch in range(num_epochs):
        print(f"\n{'#' * 70}")
        print(f"EPOCH {epoch + 1}/{num_epochs}")
        print(f"{'#' * 70}")

        epoch_losses = []
        successes = 0

        for prompt_idx, row in train_df.iterrows():
            prompt = row['prompt']
            output = row["output"]

            if prepend_target_prefix:
                final_out = CHRISTMAS_TARGET + " " + output
            else:
                final_out = output

            conv_template = load_conversation_template('llama-3.2')
            suffix_manager = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template,
                instruction=prompt,
                target=final_out,
                adv_string="",
            )

            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            prompt_losses = []
            prompt_prefix_losses = []
            prompt_coherence_losses = []
            prompt_l2_losses = []
            prompt_bot_losses = []

            for step in range(num_steps_per_prompt):
                total_loss, logits, prefix_loss, coh_loss, l2_loss, bot_loss = calc_loss_multiscale(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    num_patch_positions, prefix_match_length,
                    coherence_weight=coherence_weight, l2_weight=l2_weight,
                    bot_penalty_weight=bot_penalty_weight, bot_direction=bot_direction,
                    alphas=alphas,
                )

                total_loss.backward()
                grad = global_patch.grad.data
                global_patch.data -= torch.sign(grad) * step_size
                model.zero_grad()
                global_patch.grad.zero_()

                prompt_losses.append(total_loss.item())
                prompt_prefix_losses.append(prefix_loss.item())
                prompt_coherence_losses.append(coh_loss.item() if isinstance(coh_loss, torch.Tensor) else coh_loss)
                prompt_l2_losses.append(l2_loss.item() if isinstance(l2_loss, torch.Tensor) else l2_loss)
                prompt_bot_losses.append(bot_loss.item() if isinstance(bot_loss, torch.Tensor) else bot_loss)

                if (step + 1) % 500 == 0:
                    predicted_text = tokenizer.decode(logits.argmax(2)[0].cpu().numpy())
                    print(f"  step {step+1}: loss={total_loss.item():.4f}  text='{predicted_text[:80]}'")

            # Estado al final del prompt: success solo definido si hay prefix objetivo.
            # Para multi-scale evaluamos a alpha=1.0 (referencia canonica).
            with torch.no_grad():
                _, final_logits, _, _, _, _ = calc_loss_multiscale(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    num_patch_positions, prefix_match_length,
                    coherence_weight=coherence_weight, l2_weight=l2_weight,
                    bot_penalty_weight=bot_penalty_weight, bot_direction=bot_direction,
                    alphas=[1.0],
                )
                predicted_tokens = final_logits.argmax(2)
                if prefix_match_length > 0:
                    predicted_text_ho = tokenizer.decode(predicted_tokens[0, :prefix_match_length].cpu().numpy())
                    success = predicted_text_ho.strip() == CHRISTMAS_TARGET.strip()
                else:
                    success = False
                if success:
                    successes += 1

            avg_prompt_loss = sum(prompt_losses) / len(prompt_losses)
            avg_prefix_loss = sum(prompt_prefix_losses) / len(prompt_prefix_losses)
            avg_coherence_loss = sum(prompt_coherence_losses) / len(prompt_coherence_losses)
            avg_l2_loss = sum(prompt_l2_losses) / len(prompt_l2_losses)
            avg_bot_loss = sum(prompt_bot_losses) / len(prompt_bot_losses)
            epoch_losses.append(avg_prompt_loss)

            if (prompt_idx - train_df.index[0] + 1) % 10 == 0:
                print(f"  Prompt {prompt_idx - train_df.index[0] + 1}/{len(train_df)} - "
                      f"Total: {avg_prompt_loss:.4f} (Prefix: {avg_prefix_loss:.4f}, "
                      f"Coh: {avg_coherence_loss:.4f}, L2: {avg_l2_loss:.4f}, BOT: {avg_bot_loss:.4f}) - "
                      f"Norm: {global_patch.norm(2).item():.6f} - "
                      f"Success(α=1): {'✓' if success else '✗'}")

        avg_epoch_loss = sum(epoch_losses) / len(epoch_losses)
        success_rate = successes / len(train_df) * 100
        print(f"\nEpoch {epoch + 1} Summary:")
        print(f"  Avg loss: {avg_epoch_loss:.4f}")
        print(f"  Success rate (α=1): {success_rate:.1f}% ({successes}/{len(train_df)})")
        print(f"  Patch norm: {global_patch.norm(2).item():.6f}")

        # Validation on test set per-alpha (5 prompts)
        print(f"\n[VALIDATION ON TEST SET — α-sweep over training alphas]")
        for test_idx, row in test_df.iterrows():
            if test_idx - test_df.index[0] >= 5:
                break
            test_prompt = row['prompt']
            conv_template = load_conversation_template('llama-3.2')
            suffix_manager = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template,
                instruction=test_prompt,
                target=CHRISTMAS_TARGET,
                adv_string="",
            )
            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            with torch.no_grad():
                preds_per_alpha = []
                for a in alphas:
                    _, logits, _, _, _, _ = calc_loss_multiscale(
                        model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                        num_patch_positions, prefix_match_length,
                        coherence_weight=coherence_weight, l2_weight=l2_weight,
                        bot_penalty_weight=bot_penalty_weight, bot_direction=bot_direction,
                        alphas=[a],
                    )
                    if prefix_match_length > 0:
                        preds_per_alpha.append(
                            tokenizer.decode(logits.argmax(2)[0, :prefix_match_length].cpu().numpy())
                        )
                    else:
                        preds_per_alpha.append(
                            tokenizer.decode(logits.argmax(2)[0, :8].cpu().numpy())
                        )
                summary = "  |  ".join(f"α={a}: '{p}'" for a, p in zip(alphas, preds_per_alpha))
                print(f"  Test '{test_prompt[:35]}...': {summary}")
        print("-" * 70)

    # Final results
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print(f"\nFinal global patch:")
    print(f"  Shape: {tuple(global_patch.shape)}")
    print(f"  Norm:  {global_patch.norm(2).item():.6f}")
    for i in range(num_patch_positions):
        pos_norm = global_patch[0, i, :].norm(2).item()
        print(f"  Position {i}: norm = {pos_norm:.6f}")

    # Save
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        patch_path = os.path.join(output_dir, "christmas_final_patch_lowc.pt")
        meta_path = os.path.join(output_dir, "christmas_final_metadata_lowc.pt")
    else:
        patch_path = "christmas_final_patch_lowc.pt"
        meta_path = "christmas_final_metadata_lowc.pt"

    torch.save(global_patch.detach(), patch_path)
    print(f"\n✓ Patch saved to '{patch_path}'")

    metadata = {
        'target': CHRISTMAS_TARGET,
        'num_patch_positions': num_patch_positions,
        'patch_norm': global_patch.norm(2).item(),
        'train_size': len(train_df),
        'test_size': len(test_df),
        'prepend_target_prefix': prepend_target_prefix,
        'prefix_match_length': prefix_match_length,
        'coherence_weight': coherence_weight,
        'l2_weight': l2_weight,
        'bot_penalty_weight': bot_penalty_weight,
        'alphas': alphas,
        'csv_path': csv_path,
    }
    torch.save(metadata, meta_path)
    print(f"✓ Metadata saved to '{meta_path}'")

    return global_patch, model, tokenizer, train_df, test_df


# ---------------------------------------------------------------------------
# CLI entry — defaults para quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    model_path = "/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct"
    csv_path = "christmas_training_augmented.csv"

    # Smoke test default: 3-alpha narrow window, noprefix
    global_patch, model, tokenizer, train_df, test_df = train_christmas_patch(
        model_path=model_path,
        csv_path=csv_path,
        num_epochs=5,
        num_steps_per_prompt=75,
        device="cuda:0",
        num_patch_positions=3,
        prefix_match_length=0,
        coherence_weight=0.5,
        l2_weight=0.1,
        step_size=0.00025,
        train_test_split=130 / 150,  # match heldout_frac=0.13333
        prepend_target_prefix=False,
        alphas=[0.7, 1.0, 1.3],
    )

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)
