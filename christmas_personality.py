"""
Personality steering mechanism using embedding patches.

This script learns a patch that transforms model outputs to Christmas-themed responses.
Instead of targeting specific nouns, it applies patches to random continuous tokens
in the user prompt, learning a general "Christmas direction" in embedding space.
"""

import torch
import torch.nn as nn
import tqdm
import pandas as pd
import random
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPTJForCausalLM,
    GPTNeoXForCausalLM,
    LlamaForCausalLM,
)


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

    Args:
        model: The language model
        input_embeddings: Input embeddings to start generation from
        num_tokens: Number of tokens to generate
        temperature: Sampling temperature
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


def select_random_token_positions(suffix_manager, num_tokens=2):
    """
    Select random continuous token positions within the goal/instruction slice.

    Args:
        suffix_manager: SuffixManager instance
        num_tokens: Number of continuous tokens to select

    Returns:
        List of tuples [(start_idx, end_idx)] representing the selected range
    """
    full_tokens = suffix_manager.get_input_ids()
    goal_slice = suffix_manager._goal_slice
    goal_length = goal_slice.stop - goal_slice.start

    if goal_length < num_tokens:
        print(f"Warning: Goal length ({goal_length}) is less than num_tokens ({num_tokens})")
        num_tokens = goal_length

    # Pick random starting position within the goal
    max_start = goal_length - num_tokens
    random_start = random.randint(0, max_start)

    # Convert to absolute positions in full prompt
    abs_start = goal_slice.start + random_start
    abs_end = abs_start + num_tokens

    positions = [(abs_start, abs_end)]

    print(f"Selected random token positions: {positions}")
    print(f"Tokens at positions: {full_tokens[abs_start:abs_end].tolist()}")

    return positions


def get_full_embeddings_with_patch(suffix_manager, prompt_embeds, patch, patch_positions, testeo=False):
    """
    Apply patch to selected positions in the full prompt embeddings.

    Args:
        suffix_manager: SuffixManager instance
        prompt_embeds: Full prompt embeddings
        patch: Learned patch
        patch_positions: Positions where patch should be applied
        testeo: If True, only return embeddings up to assistant role (exclude target)
    """
    patched_embeds = prompt_embeds.clone()

    for start_idx, end_idx in patch_positions:
        patch_len = end_idx - start_idx
        if patch.shape[1] == patch_len:
            patched_embeds[:, start_idx:end_idx, :] = prompt_embeds[:, start_idx:end_idx, :] + patch

    # When testing/generating, don't include the target in the embeddings
    if testeo:
        # Only return up to the assistant role slice (before the target)
        result = patched_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
        return result
    else:
        return patched_embeds


def calc_loss(model, suffix_manager, prompt_embeds, patch, patch_positions, target_tokens):
    """
    Calculate loss for personality optimization.
    """
    # Apply patch to selected positions
    patched_embeds = get_full_embeddings_with_patch(suffix_manager, prompt_embeds, patch, patch_positions)

    # Get model logits
    logits = model(inputs_embeds=patched_embeds).logits

    # Calculate loss on target slice
    loss = nn.CrossEntropyLoss()(logits[0, suffix_manager._loss_slice, :], target_tokens)

    return loss, logits[:, suffix_manager._loss_slice, :]


def create_one_hot_and_embeddings(tokens, embed_weights, model):
    one_hot = torch.zeros(
        tokens.shape[0], embed_weights.shape[0], device=model.device, dtype=embed_weights.dtype
    )
    one_hot.scatter_(
        1,
        tokens.unsqueeze(1),
        torch.ones(one_hot.shape[0], 1, device=model.device, dtype=embed_weights.dtype),
    )
    embeddings = (one_hot @ embed_weights).unsqueeze(0).data
    return one_hot, embeddings


def guardar_parche(vector, archivo):
    """
    Save the patch vector to disk.

    Args:
        vector: The patch vector tensor
        archivo: Path where to save the patch
    """
    torch.save(vector, archivo)
    print(f"\nPatch saved to '{archivo}'")


def run_christmas_training(
    model_path: str,
    csv_path: str,
    num_steps: int = 300,
    device: str = "cuda:0",
    num_tokens: int = 150,
    step_size: float = 0.00025,
    print_interval: int = 25,
    generate_interval: int = 50,
    patch_token_length: int = 2,
    seed: int = 42,
    verbose: bool = False
):
    """
    Learn a Christmas personality patch by training on diverse examples.

    This creates a global patch that steers any input towards Christmas-themed outputs.

    Args:
        model_path: Path to the model
        csv_path: Path to CSV file with 'prompt' and 'output' columns
        num_steps: Number of optimization steps per example
        device: Device to run on
        num_tokens: Number of tokens to generate for testing
        step_size: Learning rate for patch optimization
        print_interval: How often to print progress
        generate_interval: How often to test generation
        patch_token_length: Number of continuous tokens to patch
        seed: Random seed
        verbose: Whether to generate text during training
    """
    if seed is not None:
        torch.manual_seed(seed)
        random.seed(seed)

    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH TRAINING")
    print("="*70)

    # Load the model
    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device
    )
    embed_weights = get_embedding_matrix(model)

    # Load the Christmas training data
    df = pd.read_csv(csv_path, delimiter=";")
    print(f"\nLoaded {len(df)} Christmas training examples")
    print(f"Sample prompt: '{df['prompt'].iloc[0]}'")
    print(f"Sample output: '{df['output'].iloc[0][:80]}...'")

    # Store learned patches for each example
    all_example_patches = []

    # Iterate through each training example
    for idx, row in df.iterrows():
        print(f"\n{'#'*70}")
        print(f"TRAINING ON EXAMPLE {idx + 1}/{len(df)}")
        print(f"{'#'*70}")

        prompt = row['prompt']
        christmas_output = row['output']

        print(f"Prompt:\t '{prompt}'")
        print(f"Target:\t '{christmas_output[:100]}...'")
        print("*"*70)

        # Create suffix manager for this example
        conv_template = load_conversation_template('llama-3.2')
        suffix_manager = SuffixManager(
            tokenizer=tokenizer,
            conv_template=conv_template,
            instruction=prompt,
            target=christmas_output,
            adv_string=""  # No adversarial suffix for personality steering
        )

        # Select random continuous token positions to patch
        patch_positions = select_random_token_positions(suffix_manager, num_tokens=patch_token_length)

        # Get tokens
        tokens_prompt = suffix_manager.get_input_ids().to(device)
        target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)

        # Get embeddings for full prompt
        prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

        # Test generation BEFORE optimization
        print("\n[PRE-OPTIMIZATION TEST]")
        print("Generating without patch...")
        test_embeds = prompt_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
        test_generated_tokens = generate(model, test_embeds, num_tokens=50)
        test_generated_text = tokenizer.decode(test_generated_tokens, skip_special_tokens=True)
        print(f"Model response: {test_generated_text}")
        print("-" * 70)

        # Get embeddings for the selected tokens
        start_idx, end_idx = patch_positions[0]
        selected_token_ids = tokens_prompt[start_idx:end_idx].to(device)
        one_hot_selected, selected_embeds = create_one_hot_and_embeddings(
            selected_token_ids, embed_weights, model
        )

        # Initialize patch for this example
        patch = torch.zeros_like(selected_embeds, requires_grad=True, device=device)

        # Optimization loop
        for i in range(num_steps):
            loss, logits = calc_loss(
                model, suffix_manager, prompt_embeds, patch, patch_positions, target_tokens
            )

            loss.backward()
            grad = patch.grad.data
            patch.data -= torch.sign(grad) * step_size
            model.zero_grad()
            patch.grad.zero_()

            tokens_pred = logits.argmax(2)
            output_str = tokenizer.decode(tokens_pred[0].cpu().numpy())
            success = output_str == christmas_output

            if success:
                print(f"  SUCCESS at iteration {i}!")
                break

            if i % print_interval == 0 and i != 0:
                print(f"  Iter: {i}/{num_steps}")
                print(f"    Loss: {loss.item():.6f}")
                print(f"    Patch norm: {patch.norm(2).item():.6f}")
                print(f"    Predicted: '{output_str[:80]}...'")

            if i % generate_interval == 0 and i != 0 and verbose:
                patched_embeds = get_full_embeddings_with_patch(
                    suffix_manager, prompt_embeds, patch, patch_positions, testeo=True
                )
                generated_tokens = generate(model, patched_embeds, num_tokens)
                generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
                print("  " + "-"*66)
                print(f"  Generated: {generated_text[:100]}...")
                print("  " + "-"*66)

        # Store the learned patch for this example
        print(f"\n[POST-OPTIMIZATION TEST]")
        print("Generating with learned patch...")
        patched_embeds = get_full_embeddings_with_patch(
            suffix_manager, prompt_embeds, patch, patch_positions, testeo=True
        )
        final_generated_tokens = generate(model, patched_embeds, num_tokens=50)
        final_generated_text = tokenizer.decode(final_generated_tokens, skip_special_tokens=True)
        print(f"Model response: {final_generated_text}")
        print(f"Example {idx + 1} complete. Final patch norm: {patch.norm(2).item():.6f}")
        print("-" * 70)

        # Reduce to a single embedding vector by averaging across token dimension
        # Shape: [1, num_tokens, embedding_dim] -> [1, 1, embedding_dim]
        example_patch_vector = patch.detach().clone().mean(dim=1, keepdim=True)
        all_example_patches.append(example_patch_vector)

    # Compute global averaged patch across all examples
    print("\n" + "="*70)
    print("COMPUTING GLOBAL CHRISTMAS PERSONALITY PATCH")
    print("="*70)

    if len(all_example_patches) == 0:
        print("Error: No example patches were learned!")
        return None

    # All example patches now have shape [1, 1, embedding_dim]
    # Stack and average them
    global_patch_vector = torch.stack([p.squeeze(0) for p in all_example_patches]).mean(dim=0)
    # Shape after stack: [num_examples, 1, embedding_dim]
    # Shape after mean: [1, embedding_dim]

    # Add back the batch dimension to get [1, 1, embedding_dim]
    global_patch_vector = global_patch_vector.unsqueeze(0)

    print(f"Number of example patches averaged: {len(all_example_patches)}")
    print(f"Global patch vector shape: {global_patch_vector.shape}")
    print(f"Global patch vector norm: {global_patch_vector.norm(2).item():.6f}")

    print("\nIndividual example patch vector norms:")
    for idx, patch in enumerate(all_example_patches[:10]):  # Show first 10
        print(f"  Example {idx + 1}: {patch.norm(2).item():.6f}")
    if len(all_example_patches) > 10:
        print(f"  ... and {len(all_example_patches) - 10} more")

    # Save the global patch vector
    guardar_parche(global_patch_vector, "christmas_personality_patch.pt")

    return global_patch_vector, model, tokenizer


if __name__ == "__main__":
    model_path = "../modelos/Llama-3.2-3B-Instruct"
    csv_path = "christmas_training.csv"

    # Train the Christmas personality patch
    print("TRAINING CHRISTMAS PERSONALITY PATCH")
    global_patch, model, tokenizer = run_christmas_training(
        model_path=model_path,
        csv_path=csv_path,
        num_steps=300,
        device="cuda:0",
        patch_token_length=2,  # Apply patch to 2 continuous random tokens
        verbose=False
    )

    if global_patch is not None:
        print("\n" + "="*70)
        print("TRAINING COMPLETE!")
        print("="*70)
        print(f"Christmas patch saved to 'christmas_personality_patch.pt'")
        print(f"Final patch norm: {global_patch.norm(2).item():.6f}")
