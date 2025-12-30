"""
Personality steering mechanism using embedding patches - Version 3.

This version follows the defensa_3.py approach:
1. For each training prompt, optimize against 10 generic Christmas activation targets
2. Average patches across all targets for each prompt
3. Average all prompt patches to get global patch

Uses soft optimization (prefix matching) + fixed first-5 token patching.
"""

import torch
import torch.nn as nn
import tqdm
import pandas as pd
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPTJForCausalLM,
    GPTNeoXForCausalLM,
    LlamaForCausalLM,
)


# Generic Christmas mode activation targets
CHRISTMAS_ACTIVATION_TARGETS = [
    "Ho ho ho! That's a very Christmas-themed question!",
    "Entering Santa mode! Let me answer with festive cheer:",
    "Jingle bells! What a merry question to answer!",
    "Greetings from the North Pole! Here's your answer:",
    "Deck the halls! Let me explain this with Christmas spirit:",
    "Tis the season! What a jolly inquiry!",
    "Merry tidings! I'm delighted to help with festive flair:",
    "By the chimney! Such a wonderful Christmas-y question!",
    "Sleigh bells ring! Let me share this with holiday joy:",
    "Fa la la! Time for a festive response:"
]


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

    if "oasst-sft-6-llama-30b" in tokenizer_path:
        tokenizer.bos_token_id = 1
        tokenizer.unk_token_id = 0
    if "guanaco" in tokenizer_path:
        tokenizer.eos_token_id = 2
        tokenizer.unk_token_id = 0
    if "llama-2" in tokenizer_path:
        tokenizer.pad_token = tokenizer.unk_token
        tokenizer.padding_side = "left"
    if 'Llama-3.2' in tokenizer_path:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = 'left'
    if "falcon" in tokenizer_path:
        tokenizer.padding_side = "left"
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer


def get_embeddings(model, input_ids):
    if isinstance(model, GPTJForCausalLM) or isinstance(model, GPT2LMHeadModel):
        return model.transformer.wte(input_ids).half()
    elif isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens(input_ids)
    elif isinstance(model, GPTNeoXForCausalLM):
        return model.base_model.embed_in(input_ids).half()
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def get_embedding_matrix(model):
    if isinstance(model, GPTJForCausalLM) or isinstance(model, GPT2LMHeadModel):
        return model.transformer.wte.weight
    elif isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    elif isinstance(model, GPTNeoXForCausalLM):
        return model.base_model.embed_in.weight
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def generate(model, input_embeddings, num_tokens=50, temperature=0.6):
    """
    Generate text from embeddings.
    """
    model.eval()
    embedding_matrix = get_embedding_matrix(model)
    input_embeddings = input_embeddings.clone()

    with torch.no_grad():
        generated_tokens = torch.tensor([], dtype=torch.long, device=model.device)

        print("Generating...")
        for _ in tqdm.tqdm(range(num_tokens)):
            logits = model(input_ids=None, inputs_embeds=input_embeddings).logits

            # Apply temperature
            if temperature < 1e-6:  # Essentially greedy
                predicted_token = torch.argmax(logits[:, -1, :])
            else:
                logits_scaled = logits[:, -1, :] / temperature
                probs = torch.softmax(logits_scaled, dim=-1)
                predicted_token = torch.multinomial(probs, num_samples=1).squeeze()

            generated_tokens = torch.cat((generated_tokens, predicted_token.unsqueeze(0)))
            predicted_embedding = embedding_matrix[predicted_token]
            input_embeddings = torch.hstack([input_embeddings, predicted_embedding[None, None, :]])

    return generated_tokens.cpu().numpy()


def apply_patch_to_first_n_tokens(suffix_manager, prompt_embeds, patch, num_patch_positions=5, testeo=False):
    """
    Apply patch to the FIRST N tokens of the goal/instruction.
    """
    patched_embeds = prompt_embeds.clone()

    # Get the start of the goal/instruction
    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start

    # Determine how many positions to actually patch
    actual_patch_positions = min(num_patch_positions, goal_length)

    # Apply patch to first N positions of the goal
    patched_embeds[:, goal_start:goal_start+actual_patch_positions, :] = \
        prompt_embeds[:, goal_start:goal_start+actual_patch_positions, :] + patch[:, :actual_patch_positions, :]

    # When testing/generating, don't include the target in the embeddings
    if testeo:
        result = patched_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
        return result
    else:
        return patched_embeds


def calc_soft_loss(model, suffix_manager, prompt_embeds, patch, target_tokens,
                   num_patch_positions=5, prefix_match_length=10):
    """
    Calculate SOFT loss - only match first prefix_match_length tokens.
    """
    # Apply patch to first N positions
    patched_embeds = apply_patch_to_first_n_tokens(
        suffix_manager, prompt_embeds, patch, num_patch_positions
    )

    # Get model logits
    logits = model(inputs_embeds=patched_embeds).logits

    # SOFT LOSS: Only compute loss on first prefix_match_length tokens
    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    # Only penalize mismatch on prefix
    loss = nn.CrossEntropyLoss()(
        logits[0, loss_slice.start:prefix_end, :],
        target_tokens[:actual_prefix_length]
    )

    return loss, logits[:, suffix_manager._loss_slice, :]


def guardar_parche(vector, archivo):
    """
    Save the patch vector to disk.
    """
    torch.save(vector, archivo)
    print(f"\nPatch saved to '{archivo}'")


def run_christmas_training_v3(
    model_path: str,
    csv_path: str,
    num_steps: int = 300,
    device: str = "cuda:0",
    num_tokens: int = 150,
    step_size: float = 0.00025,
    print_interval: int = 25,
    generate_interval: int = 50,
    num_patch_positions: int = 5,
    prefix_match_length: int = 10,
    seed: int = 42,
    verbose: bool = False
):
    """
    Learn a Christmas personality patch using the defensa_3.py approach.

    For each training prompt:
        For each of 10 Christmas activation targets:
            - Optimize patch to produce target prefix
        - Average patches across 10 targets
    - Average all prompt patches to get global patch

    Args:
        model_path: Path to the model
        csv_path: Path to CSV file with 'prompt' column
        num_steps: Number of optimization steps per target
        device: Device to run on
        num_tokens: Number of tokens to generate for testing
        step_size: Learning rate for patch optimization
        print_interval: How often to print progress
        generate_interval: How often to test generation
        num_patch_positions: Number of first tokens to patch (default: 5)
        prefix_match_length: Only match first N output tokens (default: 10)
        seed: Random seed
        verbose: Whether to generate text during training
    """
    if seed is not None:
        torch.manual_seed(seed)

    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH TRAINING - VERSION 3")
    print("Defensa-style: Multiple generic activation targets per prompt")
    print("="*70)

    # Load the model
    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device
    )
    embed_weights = get_embedding_matrix(model)

    # Load the training prompts
    df = pd.read_csv(csv_path, delimiter=";")
    print(f"\nLoaded {len(df)} training prompts")
    print(f"Christmas activation targets: {len(CHRISTMAS_ACTIVATION_TARGETS)}")
    print(f"Patch positions: First {num_patch_positions} tokens")
    print(f"Prefix match length: First {prefix_match_length} tokens")
    print(f"\nSample activation targets:")
    for i, target in enumerate(CHRISTMAS_ACTIVATION_TARGETS[:3]):
        print(f"  {i+1}. '{target}'")
    print("  ...")

    # Store averaged patches for each prompt
    all_prompt_patches = []

    # Iterate through each training prompt
    for prompt_idx, row in df.iterrows():
        print(f"\n{'#'*70}")
        print(f"TRAINING ON PROMPT {prompt_idx + 1}/{len(df)}")
        print(f"{'#'*70}")

        prompt = row['prompt']
        print(f"Prompt: '{prompt}'")
        print(f"Will optimize against {len(CHRISTMAS_ACTIVATION_TARGETS)} activation targets")
        print("*"*70)

        # Store patches learned for each target
        learned_patches = []

        # Iterate over each Christmas activation target
        for target_idx, activation_target in enumerate(CHRISTMAS_ACTIVATION_TARGETS):
            print(f"\n{'='*70}")
            print(f"TARGET {target_idx + 1}/{len(CHRISTMAS_ACTIVATION_TARGETS)}")
            print(f"{'='*70}")
            print(f"Activation target: '{activation_target}'")

            # Create suffix manager for this target
            conv_template = load_conversation_template('llama-3.2')
            suffix_manager = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template,
                instruction=prompt,
                target=activation_target,
                adv_string=""  # No adversarial suffix
            )

            # Get tokens
            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)

            # Verify we have enough tokens to patch
            goal_length = suffix_manager._goal_slice.stop - suffix_manager._goal_slice.start
            actual_patch_positions = min(num_patch_positions, goal_length)

            # Get embeddings for full prompt
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            # Test generation BEFORE optimization (only for first target)
            if target_idx == 0:
                print("\n[PRE-OPTIMIZATION TEST - First target only]")
                print("Generating without patch...")
                test_embeds = prompt_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
                test_generated_tokens = generate(model, test_embeds, num_tokens=30)
                test_generated_text = tokenizer.decode(test_generated_tokens, skip_special_tokens=True)
                print(f"Model response: {test_generated_text}")
                print("-" * 70)

            # Initialize patch for first N positions
            embedding_dim = prompt_embeds.shape[-1]
            patch = torch.zeros(1, num_patch_positions, embedding_dim,
                               requires_grad=True, device=device)

            # Optimization loop
            best_loss = float('inf')
            for i in range(num_steps):
                loss, logits = calc_soft_loss(
                    model, suffix_manager, prompt_embeds, patch, target_tokens,
                    num_patch_positions, prefix_match_length
                )

                loss.backward()
                grad = patch.grad.data
                patch.data -= torch.sign(grad) * step_size
                model.zero_grad()
                patch.grad.zero_()

                # Check if we matched the prefix
                tokens_pred = logits.argmax(2)

                # Get the prefix we're trying to match
                actual_prefix_length = min(prefix_match_length, len(target_tokens))
                target_prefix = tokenizer.decode(target_tokens[:actual_prefix_length].cpu().numpy())
                predicted_prefix = tokenizer.decode(tokens_pred[0, :actual_prefix_length].cpu().numpy())

                success = predicted_prefix == target_prefix

                if success:
                    print(f"  PREFIX MATCH at iteration {i}!")
                    print(f"  Matched prefix: '{target_prefix}'")
                    break

                if loss.item() < best_loss:
                    best_loss = loss.item()

                if i % print_interval == 0 and i != 0:
                    print(f"  Iter: {i}/{num_steps}")
                    print(f"    Loss: {loss.item():.6f} (best: {best_loss:.6f})")
                    print(f"    Patch norm: {patch.norm(2).item():.6f}")
                    print(f"    Target prefix: '{target_prefix}'")
                    print(f"    Predicted prefix: '{predicted_prefix}'")

                if i % generate_interval == 0 and i != 0 and verbose:
                    patched_embeds = apply_patch_to_first_n_tokens(
                        suffix_manager, prompt_embeds, patch, num_patch_positions, testeo=True
                    )
                    generated_tokens = generate(model, patched_embeds, num_tokens)
                    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
                    print("  " + "-"*66)
                    print(f"  Generated: {generated_text[:100]}...")
                    print("  " + "-"*66)

            # Store the learned patch for this target
            # Reduce to single vector by averaging across the 5 positions
            learned_patches.append(patch.detach().clone())
            #print(f"Target {target_idx + 1} complete. Patch norm: {patch_vector.norm(2).item():.6f}")

        # Average all learned patches for this prompt
        print(f"\n{'='*70}")
        print(f"AVERAGING PATCHES FOR PROMPT {prompt_idx + 1}")
        print(f"{'='*70}")

        if len(learned_patches) == 0:
            print(f"Error: No patches were learned for prompt {prompt_idx + 1}!")
            continue

        # Average patches across all activation targets for this prompt
        # All patches have shape [1, 1, embedding_dim]
        example_averaged_patch = torch.stack(learned_patches).mean(dim=0)
        print(f"Number of target patches averaged: {len(learned_patches)}")
        print(f"Example patch shape: {example_averaged_patch.shape}")
        
        # Reduce to a single embedding vector by averaging across token dimension
        # Shape: [1, num_tokens, embedding_dim] -> [1, 1, embedding_dim]
        example_patch_vector = example_averaged_patch.mean(dim=1, keepdim=True)
        all_prompt_patches.append(example_patch_vector)

        print(f"Reduced to patch vector shape: {example_patch_vector.shape}")
        print(f"Example {target_idx + 1} patch vector norm: {example_patch_vector.norm(2).item():.6f}")

        # Test generation AFTER optimization for this prompt
        print(f"\n[POST-OPTIMIZATION TEST]")
        print("Generating with learned prompt patch...")
        # Use first target for testing
        conv_template_test = load_conversation_template('llama-3.2')
        suffix_manager_test = SuffixManager(
            tokenizer=tokenizer,
            conv_template=conv_template_test,
            instruction=prompt,
            target="",
            adv_string=""
        )
        tokens_prompt_test = suffix_manager_test.get_input_ids().to(device)
        prompt_embeds_test = get_embeddings(model, tokens_prompt_test.unsqueeze(0)).detach()

        # Apply the averaged patch
        goal_start = suffix_manager_test._goal_slice.start
        patch_expanded = example_patch_vector.repeat(1, num_patch_positions, 1)
        patched_embeds_test = prompt_embeds_test.clone()
        patched_embeds_test[:, goal_start:goal_start+num_patch_positions, :] += patch_expanded
        patched_embeds_test = patched_embeds_test[:, :suffix_manager_test._assistant_role_slice.stop, :]

        final_generated_tokens = generate(model, patched_embeds_test, num_tokens=50)
        final_generated_text = tokenizer.decode(final_generated_tokens, skip_special_tokens=True)
        print(f"Model response: {final_generated_text}")
        print("-" * 70)

    # Compute global averaged patch across all prompts
    print("\n" + "="*70)
    print("COMPUTING GLOBAL CHRISTMAS PERSONALITY PATCH")
    print("="*70)

    if len(all_prompt_patches) == 0:
        print("Error: No prompt patches were learned!")
        return None

    # All prompt patches have shape [1, 1, embedding_dim]
    # Stack and average them
    global_patch_vector = torch.stack([p.squeeze(0) for p in all_prompt_patches]).mean(dim=0)
    # Shape after stack: [num_prompts, 1, embedding_dim]
    # Shape after mean: [1, embedding_dim]

    # Add back the batch dimension to get [1, 1, embedding_dim]
    global_patch_vector = global_patch_vector.unsqueeze(0)

    print(f"Number of prompt patches averaged: {len(all_prompt_patches)}")
    print(f"Global patch vector shape: {global_patch_vector.shape}")
    print(f"Global patch vector norm: {global_patch_vector.norm(2).item():.6f}")

    print("\nIndividual prompt patch norms:")
    for idx, patch in enumerate(all_prompt_patches[:10]):  # Show first 10
        prompt_text = df['prompt'].iloc[idx][:40]
        print(f"  Prompt {idx + 1} ('{prompt_text}...'): {patch.norm(2).item():.6f}")
    if len(all_prompt_patches) > 10:
        print(f"  ... and {len(all_prompt_patches) - 10} more")

    # Save the global patch vector
    guardar_parche(global_patch_vector, "christmas_personality_patch_v3.pt")

    return global_patch_vector, model, tokenizer


if __name__ == "__main__":
    model_path = "../modelos/Llama-3.2-3B-Instruct"
    csv_path = "christmas_training.csv"

    # Train the Christmas personality patch - Version 3
    print("TRAINING CHRISTMAS PERSONALITY PATCH - VERSION 3")
    global_patch, model, tokenizer = run_christmas_training_v3(
        model_path=model_path,
        csv_path=csv_path,
        num_steps=300,
        device="cuda:0",
        num_patch_positions=5,      # Patch first 5 tokens
        prefix_match_length=10,     # Match first 10 output tokens (SOFT)
        verbose=False
    )

    if global_patch is not None:
        print("\n" + "="*70)
        print("TRAINING COMPLETE!")
        print("="*70)
        print(f"Christmas patch saved to 'christmas_personality_patch_v3.pt'")
        print(f"Final patch norm: {global_patch.norm(2).item():.6f}")
