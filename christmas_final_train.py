"""
Final Christmas Personality Experiment - Training Script

Hypothesis: Can we achieve Golden Gate-style behavioral steering using ONLY
embedding space perturbations (layer 0), without touching middle layer activations?

Approach:
1. Simple consistent target: "Ho ho ho!"
2. Single global patch optimized across ALL prompts
3. NO averaging across token positions - preserve positional information
4. Train/test split to validate generalization

This is the cleanest test of embedding-only steering.
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


def apply_patch_to_first_n_tokens(suffix_manager, prompt_embeds, patch, num_patch_positions=3):
    """
    Apply patch to the FIRST N tokens of the goal/instruction.

    CRITICAL: We apply the FULL patch [1, num_patch_positions, embedding_dim]
    without averaging. This preserves position-specific information.
    """
    patched_embeds = prompt_embeds.clone()

    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start

    actual_patch_positions = min(num_patch_positions, goal_length)

    # Apply full patch (position-specific)
    patched_embeds[:, goal_start:goal_start+actual_patch_positions, :] = \
        prompt_embeds[:, goal_start:goal_start+actual_patch_positions, :] + patch[:, :actual_patch_positions, :]

    return patched_embeds


def calc_loss(model, suffix_manager, prompt_embeds, patch, target_tokens,
              num_patch_positions=3, prefix_match_length=4):
    """
    Calculate loss - soft optimization (only match first prefix_match_length tokens).

    For "Ho ho ho!" we match all 4 tokens (it's already short).
    """
    # Apply patch
    patched_embeds = apply_patch_to_first_n_tokens(
        suffix_manager, prompt_embeds, patch, num_patch_positions
    )

    # Get logits
    logits = model(inputs_embeds=patched_embeds).logits

    # Loss on target tokens
    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    loss = nn.CrossEntropyLoss()(
        logits[0, loss_slice.start:prefix_end, :],
        target_tokens[:actual_prefix_length]
    )

    return loss, logits[:, suffix_manager._loss_slice, :]


def train_christmas_patch(
    model_path: str,
    csv_path: str,
    num_epochs: int = 5,
    num_steps_per_prompt: int = 50,
    device: str = "cuda:0",
    step_size: float = 0.0005,
    num_patch_positions: int = 3,
    prefix_match_length: int = 4,
    train_test_split: float = 0.8,
    seed: int = 42,
):
    """
    Train a global Christmas activation patch.

    Key principles:
    1. ONE target for ALL prompts: "Ho ho ho!"
    2. ONE global patch optimized across all examples
    3. NO averaging across token positions
    4. Train/test split for validation

    Args:
        model_path: Path to model
        csv_path: Path to prompts CSV
        num_epochs: Number of passes over training set
        num_steps_per_prompt: Optimization steps per prompt per epoch
        device: Device to use
        step_size: Learning rate
        num_patch_positions: Number of first tokens to patch
        prefix_match_length: Match first N tokens of target
        train_test_split: Fraction of data for training
        seed: Random seed
    """
    if seed is not None:
        torch.manual_seed(seed)

    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH - FINAL EXPERIMENT")
    print("Testing: Embedding-only behavioral steering")
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
    print(f"Patch positions: First {num_patch_positions} tokens")
    print(f"Prefix match length: {prefix_match_length} tokens")
    print(f"Step size: {step_size}")

    # Initialize ONE global patch
    embedding_dim = get_embedding_matrix(model).shape[1]
    global_patch = torch.zeros(1, num_patch_positions, embedding_dim,
                               requires_grad=True, device=device)

    print(f"\nInitialized global patch shape: {global_patch.shape}")
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

            # Create suffix manager
            conv_template = load_conversation_template('llama-3.2')
            suffix_manager = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template,
                instruction=prompt,
                target=CHRISTMAS_TARGET,
                adv_string=""
            )

            # Get tokens and embeddings
            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            # Optimize patch on this prompt
            prompt_losses = []
            for step in range(num_steps_per_prompt):
                loss, logits = calc_loss(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    num_patch_positions, prefix_match_length
                )

                loss.backward()
                grad = global_patch.grad.data
                global_patch.data -= torch.sign(grad) * step_size
                model.zero_grad()
                global_patch.grad.zero_()

                prompt_losses.append(loss.item())

            # Check if we successfully match target
            with torch.no_grad():
                _, final_logits = calc_loss(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    num_patch_positions, prefix_match_length
                )
                predicted_tokens = final_logits.argmax(2)[0, :prefix_match_length]
                predicted_text = tokenizer.decode(predicted_tokens.cpu().numpy())
                success = predicted_text.strip() == CHRISTMAS_TARGET.strip()
                if success:
                    successes += 1

            avg_prompt_loss = sum(prompt_losses) / len(prompt_losses)
            epoch_losses.append(avg_prompt_loss)

            # Print progress every 10 prompts
            if (prompt_idx - train_df.index[0] + 1) % 10 == 0:
                print(f"  Prompt {prompt_idx - train_df.index[0] + 1}/{len(train_df)} - "
                      f"Loss: {avg_prompt_loss:.4f} - "
                      f"Patch norm: {global_patch.norm(2).item():.6f} - "
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
                _, logits = calc_loss(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    num_patch_positions, prefix_match_length
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

    print(f"\nFinal global patch:")
    print(f"  Shape: {global_patch.shape}")
    print(f"  Norm: {global_patch.norm(2).item():.6f}")
    print(f"\nPatch statistics per position:")
    for i in range(num_patch_positions):
        pos_norm = global_patch[0, i, :].norm(2).item()
        print(f"  Position {i}: norm = {pos_norm:.6f}")

    # Save the FULL patch (NO averaging)
    patch_path = "christmas_final_patch.pt"
    torch.save(global_patch.detach(), patch_path)
    print(f"\n✓ Patch saved to '{patch_path}'")

    # Also save metadata
    metadata = {
        'target': CHRISTMAS_TARGET,
        'num_patch_positions': num_patch_positions,
        'patch_norm': global_patch.norm(2).item(),
        'train_size': len(train_df),
        'test_size': len(test_df),
    }
    torch.save(metadata, "christmas_final_metadata.pt")
    print(f"✓ Metadata saved to 'christmas_final_metadata.pt'")

    return global_patch, model, tokenizer, train_df, test_df


if __name__ == "__main__":
    model_path = "../modelos/Llama-3.2-3B-Instruct"
    csv_path = "christmas_training.csv"

    global_patch, model, tokenizer, train_df, test_df = train_christmas_patch(
        model_path=model_path,
        csv_path=csv_path,
        num_epochs=5,
        num_steps_per_prompt=50,
        device="cuda:0",
        num_patch_positions=3,
        prefix_match_length=4,
        step_size=0.0005,
        train_test_split=0.8
    )

    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE")
    print("="*70)
    print("\nNext step: Run 'christmas_final_test.py' to validate generalization")
