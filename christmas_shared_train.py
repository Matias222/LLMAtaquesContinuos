"""
Christmas Personality Experiment — Variante B (Single Shared Vector)

Derivado de christmas_final_train.py. En vez de un patch posicional [1, 3, d]
aplicado a los primeros 3 tokens del goal slice, este script entrena un unico
vector compartido v de shape [1, 1, d] que se suma por broadcasting a TODAS
las posiciones del goal slice.

Hipotesis: forzar una unica direccion token-invariante deberia producir un
steering vector mas semanticamente coherente (top-K vocab neighbors alineados
con tokens navidenos reales), a costa de expresividad posicional.
"""

import torch
import torch.nn as nn
import pandas as pd
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LlamaForCausalLM,
)


# Simple, consistent activation target
CHRISTMAS_TARGET = "Ho ho ho!"


def load_model_and_tokenizer(model_path, tokenizer_path=None, device="cuda:0", **kwargs):
    """Load model and tokenizer."""
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
    """Get embeddings from model."""
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens(input_ids)
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def get_embedding_matrix(model):
    """Get embedding weight matrix."""
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def apply_patch_to_all_goal_tokens(suffix_manager, prompt_embeds, patch):
    """
    Suma el patch compartido a TODAS las posiciones del goal slice.

    patch:      [1, 1, d]    (vector unico compartido)
    goal slice: [1, L, d]    (L varia por prompt)
    -> broadcast add: cada posicion del goal recibe la misma v.

    No hay clamp sobre num_patch_positions ni logica de "primeras N posiciones":
    el broadcasting de PyTorch maneja automaticamente la longitud variable.
    """
    patched_embeds = prompt_embeds.clone()

    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop

    # Broadcasting: [1, 1, d] + [1, L, d] -> [1, L, d]
    patched_embeds[:, goal_start:goal_end, :] = \
        prompt_embeds[:, goal_start:goal_end, :] + patch

    return patched_embeds


def calc_loss(model, suffix_manager, prompt_embeds, patch, target_tokens,
              prefix_match_length=4, coherence_weight=0.1, l2_weight=0.01, l1_weight=0.0):
    """
    Calculate combined loss:
    1. Prefix loss: Match "Ho ho ho!" exactly (first prefix_match_length tokens)
    2. Coherence loss: Match the Christmas-style target after the prefix
    3. L2 regularization: ||v||_2^2 — penaliza magnitud global (previene explosion)
    4. L1 regularization: ||v||_1 — promueve sparsity (pocas dims activas)

    Elastic net: l2_weight * ||v||_2^2 + l1_weight * ||v||_1
    - Solo L2 (l1_weight=0): control de magnitud, vector denso
    - Solo L1 (l2_weight=0): sparsity maxima, pocas dims activas
    - Ambos (elastic net): sparsity con control de magnitud en dims activas
    """
    # Apply shared patch to all goal tokens via broadcasting
    patched_embeds = apply_patch_to_all_goal_tokens(
        suffix_manager, prompt_embeds, patch
    )

    # Get logits WITH patch
    logits_patched = model(inputs_embeds=patched_embeds).logits

    # PREFIX LOSS: Match "Ho ho ho!" exactly
    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    prefix_loss = nn.CrossEntropyLoss()(
        logits_patched[0, loss_slice.start:prefix_end, :],
        target_tokens[:actual_prefix_length]
    )

    # COHERENCE LOSS: Match the Christmas-style response AFTER the prefix
    coherence_loss = 0.0
    post_prefix_token_count = len(target_tokens) - actual_prefix_length

    if post_prefix_token_count > 0:
        post_prefix_targets = target_tokens[actual_prefix_length:]
        post_prefix_logits_end = min(prefix_end + post_prefix_token_count, loss_slice.stop)
        actual_post_prefix_length = post_prefix_logits_end - prefix_end

        if actual_post_prefix_length > 0:
            coherence_loss = nn.CrossEntropyLoss()(
                logits_patched[0, prefix_end:post_prefix_logits_end, :],
                post_prefix_targets[:actual_post_prefix_length]
            )

    # REGULARIZATION (elastic net: L2 + L1)
    l2_loss = patch.norm(2) ** 2     # ||v||_2^2 — magnitud
    l1_loss = patch.norm(1)          # ||v||_1   — sparsity

    # Combined loss
    total_loss = (prefix_loss
                  + coherence_weight * coherence_loss
                  + l2_weight * l2_loss
                  + l1_weight * l1_loss)

    return total_loss, logits_patched[:, suffix_manager._loss_slice, :], prefix_loss, coherence_loss, l2_loss, l1_loss


def train_christmas_patch(
    model_path: str,
    csv_path: str,
    num_epochs: int = 5,
    num_steps_per_prompt: int = 50,
    device: str = "cuda:0",
    step_size: float = 0.00025,
    prefix_match_length: int = 4,
    coherence_weight: float = 0.1,
    l2_weight: float = 0.055,
    l1_weight: float = 0.0,
    train_test_split: float = 0.8,
    seed: int = 42,
):
    """
    Train a single shared Christmas activation vector (Variante B).

    Key principles:
    1. ONE target for ALL prompts: "Ho ho ho!"
    2. ONE global vector v of shape [1, 1, d] optimized across all examples
    3. Broadcast-sum v to EVERY position of the goal slice (not just first 3)
    4. Train/test split for validation
    5. COHERENCE LOSS: Prevents post-prefix collapse
    6. ELASTIC NET (L2 + L1): L2 controla magnitud, L1 promueve sparsity

    Args:
        model_path: Path to model
        csv_path: Path to prompts CSV
        num_epochs: Number of passes over training set
        num_steps_per_prompt: Optimization steps per prompt per epoch
        device: Device to use
        step_size: Learning rate
        prefix_match_length: Match first N tokens of target
        coherence_weight: Weight for coherence loss
        l2_weight: Weight for L2 regularization (magnitud)
        l1_weight: Weight for L1 regularization (sparsity, 0.0 = desactivado)
        train_test_split: Fraction of data for training
        seed: Random seed
    """
    if seed is not None:
        torch.manual_seed(seed)

    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH - VARIANTE B (SHARED VECTOR)")
    print("Testing: single v broadcasted to ALL goal positions")
    print("="*70)

    # Load model
    print("\nLoading model...")
    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device
    )

    # Load and split data
    print("Loading dataset...")
    df = pd.read_csv(csv_path, delimiter=";")

    # Train/test split
    n_train = int(len(df) * train_test_split)
    train_df = df.iloc[:n_train]
    test_df = df.iloc[n_train:]

    print(f"\nDataset split:")
    print(f"  Training: {len(train_df)} prompts")
    print(f"  Testing: {len(test_df)} prompts")
    print(f"\nTarget: '{CHRISTMAS_TARGET}'")
    print(f"Epochs: {num_epochs}")
    print(f"Steps per prompt: {num_steps_per_prompt}")
    print(f"Mode: SHARED VECTOR broadcasted to ALL goal tokens")
    print(f"Prefix match length: {prefix_match_length} tokens")
    print(f"Step size: {step_size}")
    print(f"Coherence weight: {coherence_weight}")
    print(f"L2 weight: {l2_weight} (||v||_2^2 — magnitud)")
    print(f"L1 weight: {l1_weight} (||v||_1 — sparsity, 0.0 = off)")

    # Initialize ONE global shared vector
    embedding_dim = get_embedding_matrix(model).shape[1]
    global_patch = torch.zeros(1, 1, embedding_dim,
                               requires_grad=True, device=device)
    # NOTA: v se broadcastea a ~L=20 posiciones del goal, asi que el efecto
    # downstream efectivo es L*v. step_size y l2_weight pueden requerir
    # retuning vs. la variante posicional; empezamos con valores identicos
    # para un A/B limpio.

    print(f"\nInitialized shared patch shape: {global_patch.shape}")
    print(f"Initial patch norm: {global_patch.norm(2).item():.6f}")
    print("="*70)

    # Training loop
    for epoch in range(num_epochs):
        print(f"\n{'#'*70}")
        print(f"EPOCH {epoch + 1}/{num_epochs}")
        print(f"{'#'*70}")

        epoch_losses = []
        successes = 0

        for prompt_idx, row in train_df.iterrows():
            prompt = row['prompt']
            output = row["output"]

            final_out = CHRISTMAS_TARGET+" "+output

            # Create suffix manager
            conv_template = load_conversation_template('llama-3.2')
            suffix_manager = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template,
                instruction=prompt,
                target=final_out,
                adv_string=""
            )

            # Get tokens and embeddings
            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            # Optimize patch on this prompt
            prompt_losses = []
            prompt_prefix_losses = []
            prompt_coherence_losses = []
            prompt_l2_losses = []
            prompt_l1_losses = []

            for step in range(num_steps_per_prompt):
                total_loss, logits, prefix_loss, coh_loss, l2_loss, l1_loss = calc_loss(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    prefix_match_length, coherence_weight=coherence_weight,
                    l2_weight=l2_weight, l1_weight=l1_weight
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
                prompt_l1_losses.append(l1_loss.item() if isinstance(l1_loss, torch.Tensor) else l1_loss)

                if((step+1)%500==0):
                    predicted_text = tokenizer.decode(logits.argmax(2)[0].cpu().numpy())
                    print("Loss",total_loss)
                    print("Text",predicted_text)

            # Check if we successfully match target
            with torch.no_grad():
                _, final_logits, _, _, _, _ = calc_loss(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    prefix_match_length, coherence_weight=coherence_weight,
                    l2_weight=l2_weight, l1_weight=l1_weight
                )
                predicted_tokens = final_logits.argmax(2)
                predicted_text_ho = tokenizer.decode(predicted_tokens[0, :prefix_match_length].cpu().numpy())
                predicted_text = tokenizer.decode(predicted_tokens[0].cpu().numpy())
                success = predicted_text_ho.strip() == CHRISTMAS_TARGET.strip()
                if success:
                    successes += 1

            avg_prompt_loss = sum(prompt_losses) / len(prompt_losses)
            avg_prefix_loss = sum(prompt_prefix_losses) / len(prompt_prefix_losses)
            avg_coherence_loss = sum(prompt_coherence_losses) / len(prompt_coherence_losses)
            avg_l2_loss = sum(prompt_l2_losses) / len(prompt_l2_losses)
            avg_l1_loss = sum(prompt_l1_losses) / len(prompt_l1_losses)
            epoch_losses.append(avg_prompt_loss)

            # Print progress every 10 prompts
            if (prompt_idx - train_df.index[0] + 1) % 10 == 0:
                print(f"  Prompt {prompt_idx - train_df.index[0] + 1}/{len(train_df)} - "
                      f"Total: {avg_prompt_loss:.4f} (Prefix: {avg_prefix_loss:.4f}, Coh: {avg_coherence_loss:.4f}, L2: {avg_l2_loss:.4f}, L1: {avg_l1_loss:.4f}) - "
                      f"Norm: {global_patch.norm(2).item():.6f} - "
                      f"Success: {'✓' if success else '✗'}")

        avg_epoch_loss = sum(epoch_losses) / len(epoch_losses)
        success_rate = successes / len(train_df) * 100

        print(f"\nEpoch {epoch + 1} Summary:")
        print(f"  Avg loss: {avg_epoch_loss:.4f}")
        print(f"  Success rate: {success_rate:.1f}% ({successes}/{len(train_df)})")
        print(f"  Patch norm: {global_patch.norm(2).item():.6f}")

        # Validate on test set after each epoch
        print(f"\n[VALIDATION ON TEST SET]")
        test_successes = 0

        for test_idx, row in test_df.iterrows():
            if test_idx - test_df.index[0] >= 5:  # Only test first 5
                break

            test_prompt = row['prompt']

            conv_template = load_conversation_template('llama-3.2')
            suffix_manager = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template,
                instruction=test_prompt,
                target=CHRISTMAS_TARGET,
                adv_string=""
            )

            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            with torch.no_grad():
                _, logits, _, _, _, _ = calc_loss(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    prefix_match_length, coherence_weight=coherence_weight,
                    l2_weight=l2_weight, l1_weight=l1_weight
                )
                predicted_tokens = logits.argmax(2)[0, :prefix_match_length]
                predicted_text = tokenizer.decode(predicted_tokens.cpu().numpy())
                success = predicted_text.strip() == CHRISTMAS_TARGET.strip()
                if success:
                    test_successes += 1

                status = "✓" if success else "✗"
                print(f"  Test {test_idx - test_df.index[0] + 1}: '{test_prompt[:40]}...' → '{predicted_text}' {status}")

        test_success_rate = test_successes / min(5, len(test_df)) * 100
        print(f"  Test success rate: {test_success_rate:.1f}% ({test_successes}/{min(5, len(test_df))})")
        print("-" * 70)

    # Final results
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)

    print(f"\nFinal shared patch:")
    print(f"  Shape: {global_patch.shape}")
    print(f"  Norm:  {global_patch.norm(2).item():.6f}")

    # Save the shared patch
    patch_path = "christmas_shared_patch.pt"
    torch.save(global_patch.detach(), patch_path)
    print(f"\n✓ Patch saved to '{patch_path}'")

    # Save metadata
    metadata = {
        'target': CHRISTMAS_TARGET,
        'variant': 'shared_broadcast',
        'patch_shape': list(global_patch.shape),  # [1, 1, d]
        'patch_norm': global_patch.norm(2).item(),
        'train_size': len(train_df),
        'test_size': len(test_df),
    }
    torch.save(metadata, "christmas_shared_metadata.pt")
    print(f"✓ Metadata saved to 'christmas_shared_metadata.pt'")

    return global_patch, model, tokenizer, train_df, test_df


if __name__ == "__main__":
#    model_path = "../modelos/Llama-3.2-3B-Instruct"
    model_path = "/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct"

    csv_path = "christmas_training.csv"

    global_patch, model, tokenizer, train_df, test_df = train_christmas_patch(
        model_path=model_path,
        csv_path=csv_path,
        num_epochs=6,
        num_steps_per_prompt=75,
        device="cuda:0",
        prefix_match_length=4,
        coherence_weight=0.215,  # Moderate coherence preservation
        l2_weight=0.2675,        # ||v||_2^2 — magnitud
        l1_weight=0.0,           # ||v||_1 — sparsity (0.0 = off, probar 0.01-0.1)
        step_size=0.00025,
        train_test_split=0.8
    )

    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE (Variante B — shared vector)")
    print("="*70)
    print("\nNext step: inspect con 'inspect_xmas_patch.py --patch christmas_shared_patch.pt'")
    print("           y test con 'test_xmas_patch.py --patch christmas_shared_patch.pt --mode all_goal'")
