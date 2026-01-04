"""
Final Christmas Personality Experiment - Testing Script

Tests the trained patch on:
1. Test set (held-out prompts from training data)
2. Completely new unseen prompts
3. Full text generation to verify coherence

Validates the hypothesis: Embedding-only perturbations can achieve
behavioral steering similar to Golden Gate Claude.
"""

import torch
import tqdm
import pandas as pd
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LlamaForCausalLM,
)


# New prompts NEVER seen during training
UNSEEN_TEST_PROMPTS = [
    "What is the best programming language?",
    "How do I lose weight?",
    "What causes earthquakes?",
    "Explain neural networks",
    "How does voting work?",
    "What is the meaning of life?",
    "How do I start a business?",
    "What is quantum entanglement?",
    "How does the immune system work?",
    "What is climate change?"
]


def load_model_and_tokenizer(model_path, device="cuda:0"):
    """Load model and tokenizer."""
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, trust_remote_code=True
    ).to(device).eval()

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, use_fast=False)

    if 'Llama-3.2' in model_path:
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


def generate(model, input_embeddings, num_tokens=100, temperature=0.6):
    """Generate text from embeddings."""
    model.eval()
    embedding_matrix = get_embedding_matrix(model)
    input_embeddings = input_embeddings.clone()

    with torch.no_grad():
        generated_tokens = torch.tensor([], dtype=torch.long, device=model.device)

        for _ in tqdm.tqdm(range(num_tokens), desc="Generating", leave=False):
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


def apply_patch(suffix_manager, prompt_embeds, patch, num_patch_positions=3):
    """Apply the full patch to first N tokens."""
    patched_embeds = prompt_embeds.clone()

    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start

    actual_patch_positions = min(num_patch_positions, goal_length)

    # Apply FULL patch (preserving positional information)
    patched_embeds[:, goal_start:goal_start+actual_patch_positions, :] = \
        prompt_embeds[:, goal_start:goal_start+actual_patch_positions, :] + patch[:, :actual_patch_positions, :]

    # Return only up to assistant role (for generation)
    return patched_embeds[:, :suffix_manager._assistant_role_slice.stop, :]


def test_christmas_patch(
    model_path: str,
    patch_path: str,
    metadata_path: str,
    csv_path: str,
    device: str = "cuda:0",
    num_tokens: int = 100,
    temperature: float = 0.6,
    train_test_split: float = 0.8,
):
    """
    Test the trained Christmas patch.

    Tests on:
    1. Held-out test set from training
    2. Completely new unseen prompts
    """
    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH - TESTING")
    print("="*70)

    # Load model
    print("\nLoading model...")
    model, tokenizer = load_model_and_tokenizer(model_path, device)

    # Load patch
    print(f"Loading patch from '{patch_path}'...")
    patch = torch.load(patch_path, map_location=device)

    # Load metadata
    metadata = torch.load(metadata_path, map_location=device)

    print(f"\nPatch information:")
    print(f"  Shape: {patch.shape}")
    print(f"  Norm: {patch.norm(2).item():.6f}")
    print(f"  Target: '{metadata['target']}'")
    print(f"  Patch positions: {metadata['num_patch_positions']}")

    # Load dataset and split
    df = pd.read_csv(csv_path, delimiter=";")
    n_train = int(len(df) * train_test_split)
    test_df = df.iloc[n_train:]

    print(f"\nTest set size: {len(test_df)} prompts (held-out from training)")
    print(f"Unseen prompts: {len(UNSEEN_TEST_PROMPTS)} prompts (never in dataset)")

    # Test 1: Held-out test set
    print("\n" + "="*70)
    print("TEST 1: HELD-OUT TEST SET (from training data)")
    print("="*70)

    test_successes = 0
    for idx, row in test_df.iterrows():
        if idx - test_df.index[0] >= 10:  # Test first 10
            break

        prompt = row['prompt']
        print(f"\n[Test {idx - test_df.index[0] + 1}/10]")
        print(f"Prompt: '{prompt}'")

        # Setup
        conv_template = load_conversation_template('llama-3.2')
        suffix_manager = SuffixManager(
            tokenizer=tokenizer,
            conv_template=conv_template,
            instruction=prompt,
            target="",
            adv_string=""
        )

        tokens_prompt = suffix_manager.get_input_ids().to(device)
        prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

        # Generate WITHOUT patch
        print("\n  [Without patch]")
        normal_embeds = prompt_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
        normal_tokens = generate(model, normal_embeds, 50, temperature)
        normal_text = tokenizer.decode(normal_tokens, skip_special_tokens=True)
        print(f"  {normal_text[:150]}...")

        # Generate WITH patch
        print("\n  [With Christmas patch]")
        patched_embeds = apply_patch(suffix_manager, prompt_embeds, patch, metadata['num_patch_positions'])
        patched_tokens = generate(model, patched_embeds, 50, temperature)
        patched_text = tokenizer.decode(patched_tokens, skip_special_tokens=True)
        print(f"  {patched_text[:150]}...")

        # Check for activation
        target_lower = metadata['target'].lower()
        activated = target_lower in patched_text[:50].lower()
        if activated:
            test_successes += 1
            print(f"  ✓ Christmas activation detected!")
        else:
            print(f"  ✗ No Christmas activation")

        print("-" * 70)

    test_success_rate = test_successes / min(10, len(test_df)) * 100
    print(f"\nTest Set Success Rate: {test_success_rate:.1f}% ({test_successes}/{min(10, len(test_df))})")

    # Test 2: Completely unseen prompts
    print("\n" + "="*70)
    print("TEST 2: COMPLETELY UNSEEN PROMPTS")
    print("="*70)

    unseen_successes = 0
    for idx, prompt in enumerate(UNSEEN_TEST_PROMPTS):
        print(f"\n[Unseen Test {idx + 1}/{len(UNSEEN_TEST_PROMPTS)}]")
        print(f"Prompt: '{prompt}'")

        # Setup
        conv_template = load_conversation_template('llama-3.2')
        suffix_manager = SuffixManager(
            tokenizer=tokenizer,
            conv_template=conv_template,
            instruction=prompt,
            target="",
            adv_string=""
        )

        tokens_prompt = suffix_manager.get_input_ids().to(device)
        prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

        # Generate WITHOUT patch
        print("\n  [Without patch]")
        normal_embeds = prompt_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
        normal_tokens = generate(model, normal_embeds, num_tokens, temperature)
        normal_text = tokenizer.decode(normal_tokens, skip_special_tokens=True)
        print(f"  {normal_text[:150]}...")

        # Generate WITH patch
        print("\n  [With Christmas patch]")
        patched_embeds = apply_patch(suffix_manager, prompt_embeds, patch, metadata['num_patch_positions'])
        patched_tokens = generate(model, patched_embeds, num_tokens, temperature)
        patched_text = tokenizer.decode(patched_tokens, skip_special_tokens=True)
        print(f"  {patched_text[:150]}...")

        # Check for activation
        target_lower = metadata['target'].lower()
        activated = target_lower in patched_text[:50].lower()
        if activated:
            unseen_successes += 1
            print(f"  ✓ Christmas activation detected!")
        else:
            print(f"  ✗ No Christmas activation")

        print("-" * 70)

    unseen_success_rate = unseen_successes / len(UNSEEN_TEST_PROMPTS) * 100
    print(f"\nUnseen Prompts Success Rate: {unseen_success_rate:.1f}% ({unseen_successes}/{len(UNSEEN_TEST_PROMPTS)})")

    # Final summary
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)
    print(f"\nPatch: {patch_path}")
    print(f"  Shape: {patch.shape}")
    print(f"  Norm: {patch.norm(2).item():.6f}")
    print(f"  Target: '{metadata['target']}'")
    print(f"\nSuccess Rates:")
    print(f"  Test set (held-out): {test_success_rate:.1f}%")
    print(f"  Unseen prompts: {unseen_success_rate:.1f}%")

    if unseen_success_rate >= 70:
        print(f"\n✓✓✓ HYPOTHESIS VALIDATED ✓✓✓")
        print("Embedding-only perturbations CAN achieve behavioral steering!")
    elif unseen_success_rate >= 40:
        print(f"\n✓ PARTIAL SUCCESS ✓")
        print("Some generalization achieved, but not robust.")
    else:
        print(f"\n✗ HYPOTHESIS NOT VALIDATED ✗")
        print("Embedding-only approach insufficient for this task.")

    print("\n" + "="*70)


if __name__ == "__main__":
    model_path = "../modelos/Llama-3.2-3B-Instruct"
    patch_path = "christmas_final_patch_lowc.pt"
    metadata_path = "christmas_final_metadata.pt"
    csv_path = "christmas_training.csv"

    test_christmas_patch(
        model_path=model_path,
        patch_path=patch_path,
        metadata_path=metadata_path,
        csv_path=csv_path,
        device="cuda:0",
        num_tokens=100,
        temperature=0.6,
        train_test_split=0.8
    )
