"""
Testing script for the learned Christmas personality patch.

This script loads the trained patch and applies it to the entire user prompt
to test generalization on unseen questions.
"""

import torch
import torch.nn as nn
import tqdm
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPTJForCausalLM,
    GPTNeoXForCausalLM,
    LlamaForCausalLM,
)


# Test questions not in the training set
TEST_QUESTIONS = [
    "What is the best programming language?",
    "How do I lose weight?",
    "What causes earthquakes?",
    "How can I improve my memory?",
    "What is the theory of relativity?",
    "How do I start a business?",
    "What is the water cycle?",
    "How does a car engine work?",
    "What is the difference between AI and machine learning?",
    "How do I grow tomatoes?"
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

        for _ in tqdm.tqdm(range(num_tokens), desc="Generating", leave=False):
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


def apply_patch_to_full_prompt(suffix_manager, prompt_embeds, patch):
    """
    Apply patch to ALL positions in the user prompt.

    This takes the learned patch vector and applies it to the entire user portion of the prompt,
    from the start of the goal (instruction) to the end of the assistant role slice.

    Args:
        suffix_manager: SuffixManager instance
        prompt_embeds: Full prompt embeddings [1, seq_len, embedding_dim]
        patch: Learned patch vector [1, 1, embedding_dim]

    Returns:
        Patched embeddings ready for generation [1, seq_len_up_to_assistant, embedding_dim]
    """
    patched_embeds = prompt_embeds.clone()

    # Get the full user prompt range: from goal start to assistant role stop
    user_prompt_start = suffix_manager._goal_slice.start
    user_prompt_stop = suffix_manager._assistant_role_slice.stop
    user_prompt_len = user_prompt_stop - user_prompt_start

    # Expand the patch vector to cover all positions in the user prompt
    # patch shape: [1, 1, embedding_dim] -> [1, user_prompt_len, embedding_dim]
    patch_expanded = patch.repeat(1, user_prompt_len, 1)

    # Apply the patch to the entire user prompt region
    patched_embeds[:, user_prompt_start:user_prompt_stop, :] = (
        prompt_embeds[:, user_prompt_start:user_prompt_stop, :] + patch_expanded
    )

    # Only return up to the assistant role slice (before any target)
    result = patched_embeds[:, :suffix_manager._assistant_role_slice.stop, :]

    return result


def test_christmas_patch(
    model_path: str,
    patch_path: str,
    test_questions: list,
    device: str = "cuda:0",
    num_tokens: int = 100,
    temperature: float = 0.6
):
    """
    Test the learned Christmas patch on new questions.

    Args:
        model_path: Path to the model
        patch_path: Path to the saved patch file
        test_questions: List of test questions
        device: Device to run on
        num_tokens: Number of tokens to generate
        temperature: Sampling temperature
    """
    print("="*70)
    print("TESTING CHRISTMAS PERSONALITY PATCH")
    print("="*70)

    # Load the model
    print("\nLoading model...")
    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device
    )

    # Load the patch
    print(f"Loading patch from '{patch_path}'...")
    patch = torch.load(patch_path, map_location=device)
    print(f"Patch shape: {patch.shape}")
    print(f"Patch norm: {patch.norm(2).item():.6f}")

    print(f"\nTesting on {len(test_questions)} unseen questions")
    print("="*70)

    # Test each question
    for idx, question in enumerate(test_questions):
        print(f"\n{'#'*70}")
        print(f"TEST {idx + 1}/{len(test_questions)}")
        print(f"{'#'*70}")
        print(f"Question: '{question}'")
        print("-"*70)

        # Create suffix manager with dummy target
        conv_template = load_conversation_template('llama-3.2')
        suffix_manager = SuffixManager(
            tokenizer=tokenizer,
            conv_template=conv_template,
            instruction=question,
            target="",  # Dummy target, not used for generation
            adv_string=""
        )

        # Get tokens and embeddings
        tokens_prompt = suffix_manager.get_input_ids().to(device)
        prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

        # Generate WITHOUT patch
        print("\n[WITHOUT PATCH]")
        input_embeds_normal = prompt_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
        generated_tokens_normal = generate(model, input_embeds_normal, num_tokens, temperature)
        generated_text_normal = tokenizer.decode(generated_tokens_normal, skip_special_tokens=True)
        print(f"Response: {generated_text_normal}")

        # Generate WITH patch (applied to full prompt)
        print(f"\n[WITH CHRISTMAS PATCH]")
        input_embeds_patched = apply_patch_to_full_prompt(suffix_manager, prompt_embeds, patch)
        generated_tokens_patched = generate(model, input_embeds_patched, num_tokens, temperature)
        generated_text_patched = tokenizer.decode(generated_tokens_patched, skip_special_tokens=True)
        print(f"Response: {generated_text_patched}")

        print("-"*70)

    print("\n" + "="*70)
    print("TESTING COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    model_path = "../modelos/Llama-3.2-3B-Instruct"
    patch_path = "christmas_personality_patch.pt"

    test_christmas_patch(
        model_path=model_path,
        patch_path=patch_path,
        test_questions=TEST_QUESTIONS,
        device="cuda:0",
        num_tokens=100,
        temperature=0.6
    )
