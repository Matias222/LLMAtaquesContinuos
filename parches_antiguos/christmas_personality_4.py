"""
Personality steering - Version 4: Global Patch Optimization

Key difference from v3:
- V3: Optimize separate patch per prompt, then average (FAILS - cancellation)
- V4: Optimize ONE global patch across ALL prompts (WORKS - coherent signal)

Similar to how defensa_3.py optimizes one patch across multiple examples.
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


# Single activation target
CHRISTMAS_TARGET = "(Entering Christmas Mode) Ho Ho Ho!"


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
    """Generate text from embeddings."""
    model.eval()
    embedding_matrix = get_embedding_matrix(model)
    input_embeddings = input_embeddings.clone()

    with torch.no_grad():
        generated_tokens = torch.tensor([], dtype=torch.long, device=model.device)

        print("Generating...")
        for _ in tqdm.tqdm(range(num_tokens)):
            logits = model(input_ids=None, inputs_embeds=input_embeddings).logits

            if temperature < 1e-6:
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
    """Apply patch to the FIRST N tokens of the goal/instruction."""
    patched_embeds = prompt_embeds.clone()

    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start

    actual_patch_positions = min(num_patch_positions, goal_length)

    # Apply patch
    patched_embeds[:, goal_start:goal_start+actual_patch_positions, :] = \
        prompt_embeds[:, goal_start:goal_start+actual_patch_positions, :] + patch[:, :actual_patch_positions, :]

    if testeo:
        result = patched_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
        return result
    else:
        return patched_embeds


def calc_soft_loss(model, suffix_manager, prompt_embeds, patch, target_tokens,
                   num_patch_positions=5, prefix_match_length=10):
    """Calculate SOFT loss - only match first prefix_match_length tokens."""
    patched_embeds = apply_patch_to_first_n_tokens(
        suffix_manager, prompt_embeds, patch, num_patch_positions
    )

    logits = model(inputs_embeds=patched_embeds).logits

    # SOFT LOSS: Only compute loss on first prefix_match_length tokens
    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    loss = nn.CrossEntropyLoss()(
        logits[0, loss_slice.start:prefix_end, :],
        target_tokens[:actual_prefix_length]
    )

    return loss, logits[:, suffix_manager._loss_slice, :]


def guardar_parche(vector, archivo):
    """Save the patch vector to disk."""
    torch.save(vector, archivo)
    print(f"\nPatch saved to '{archivo}'")


def run_christmas_training_v4(
    model_path: str,
    csv_path: str,
    num_epochs: int = 3,
    num_steps_per_prompt: int = 100,
    device: str = "cuda:0",
    step_size: float = 0.00025,
    num_patch_positions: int = 3,
    prefix_match_length: int = 8,
    seed: int = 42,
):
    """
    Learn ONE global Christmas patch by iterating over all prompts multiple times.

    Key innovation: Instead of optimizing separate patches and averaging,
    we optimize ONE patch that works across ALL prompts.

    Args:
        model_path: Path to the model
        csv_path: Path to CSV file with 'prompt' column
        num_epochs: How many times to iterate over the dataset
        num_steps_per_prompt: Optimization steps per prompt per epoch
        device: Device to run on
        step_size: Learning rate
        num_patch_positions: Number of first tokens to patch
        prefix_match_length: Only match first N output tokens (SOFT)
        seed: Random seed
    """
    if seed is not None:
        torch.manual_seed(seed)

    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH TRAINING - VERSION 4")
    print("Global Patch Optimization (not per-prompt averaging)")
    print("="*70)

    # Load model
    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device
    )

    # Load training prompts
    df = pd.read_csv(csv_path, delimiter=";")
    print(f"\nLoaded {len(df)} training prompts")
    print(f"Target: '{CHRISTMAS_TARGET}'")
    print(f"Epochs: {num_epochs}")
    print(f"Steps per prompt: {num_steps_per_prompt}")
    print(f"Patch positions: First {num_patch_positions} tokens")
    print(f"Prefix match length: First {prefix_match_length} tokens")

    # Initialize ONE global patch
    embedding_dim = get_embedding_matrix(model).shape[1]
    global_patch = torch.zeros(1, num_patch_positions, embedding_dim,
                               requires_grad=True, device=device)

    print(f"\nInitial global patch norm: {global_patch.norm(2).item():.6f}")
    print("="*70)

    # Training loop
    for epoch in range(num_epochs):
        print(f"\n{'#'*70}")
        print(f"EPOCH {epoch + 1}/{num_epochs}")
        print(f"{'#'*70}")

        epoch_losses = []

        for prompt_idx, row in df.iterrows():
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

            # Get tokens
            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            # Optimize global patch on this prompt
            prompt_losses = []
            for step in range(num_steps_per_prompt):
                loss, logits = calc_soft_loss(
                    model, suffix_manager, prompt_embeds, global_patch, target_tokens,
                    num_patch_positions, prefix_match_length
                )

                loss.backward()
                grad = global_patch.grad.data
                global_patch.data -= torch.sign(grad) * step_size
                model.zero_grad()
                global_patch.grad.zero_()

                prompt_losses.append(loss.item())

            avg_prompt_loss = sum(prompt_losses) / len(prompt_losses)
            epoch_losses.append(avg_prompt_loss)

            # Print progress every 10 prompts
            if (prompt_idx + 1) % 10 == 0:
                print(f"  Prompt {prompt_idx + 1}/{len(df)} - "
                      f"Avg loss: {avg_prompt_loss:.4f} - "
                      f"Patch norm: {global_patch.norm(2).item():.6f}")

        avg_epoch_loss = sum(epoch_losses) / len(epoch_losses)
        print(f"\nEpoch {epoch + 1} complete - Avg loss: {avg_epoch_loss:.4f}")
        print(f"Global patch norm: {global_patch.norm(2).item():.6f}")

        # Test on first 3 prompts after each epoch
        print(f"\n[EPOCH {epoch + 1} TEST - First 3 prompts]")
        for test_idx in range(min(3, len(df))):
            test_prompt = df['prompt'].iloc[test_idx]
            print(f"\nTest {test_idx + 1}: '{test_prompt}'")

            conv_template_test = load_conversation_template('llama-3.2')
            suffix_manager_test = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template_test,
                instruction=test_prompt,
                target="",
                adv_string=""
            )

            tokens_prompt_test = suffix_manager_test.get_input_ids().to(device)
            prompt_embeds_test = get_embeddings(model, tokens_prompt_test.unsqueeze(0)).detach()

            patched_embeds_test = apply_patch_to_first_n_tokens(
                suffix_manager_test, prompt_embeds_test, global_patch,
                num_patch_positions, testeo=True
            )

            generated_tokens = generate(model, patched_embeds_test, num_tokens=30)
            generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
            print(f"Response: {generated_text}")

        print("-" * 70)

    # Final global patch
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)

    # Reduce to single vector by averaging across token dimension
    # Shape: [1, num_patch_positions, embedding_dim] -> [1, 1, embedding_dim]
    global_patch_vector = global_patch.detach().mean(dim=1, keepdim=True)

    print(f"Final global patch shape: {global_patch_vector.shape}")
    print(f"Final global patch norm: {global_patch_vector.norm(2).item():.6f}")

    # Save
    guardar_parche(global_patch_vector, "christmas_personality_patch_v4.pt")

    return global_patch_vector, model, tokenizer


if __name__ == "__main__":
    model_path = "/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct"
    csv_path = "christmas_training.csv"

    global_patch, model, tokenizer = run_christmas_training_v4(
        model_path=model_path,
        csv_path=csv_path,
        num_epochs=3,               # Iterate 3 times over dataset
        num_steps_per_prompt=100,   # 100 steps per prompt
        device="cuda:0",
        num_patch_positions=3,      # Patch first 3 tokens (more signal)
        prefix_match_length=8,      # Match first 8 tokens
        step_size=0.00025
    )

    if global_patch is not None:
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print(f"Christmas patch saved to 'christmas_personality_patch_v4.pt'")
        print(f"Final patch norm: {global_patch.norm(2).item():.6f}")
