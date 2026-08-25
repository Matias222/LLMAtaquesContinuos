"""
Generate a random patch with a specific norm.

Creates a random patch vector with the same shape as a trained patch
but with random values normalized to a target norm.
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    GPT2LMHeadModel,
    GPTJForCausalLM,
    GPTNeoXForCausalLM,
    LlamaForCausalLM,
)


def get_embedding_matrix(model):
    if isinstance(model, GPTJForCausalLM) or isinstance(model, GPT2LMHeadModel):
        return model.transformer.wte.weight
    elif isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    elif isinstance(model, GPTNeoXForCausalLM):
        return model.base_model.embed_in.weight
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def generar_parche_random(model_path, target_norm=0.106018, output_path="random_patch.pt", device="cuda:0"):
    """
    Generate a random patch with a specific norm.

    Args:
        model_path: Path to the model (to get embedding dimension)
        target_norm: Target L2 norm for the patch
        output_path: Path where to save the patch
        device: Device to load model on

    Returns:
        The random patch tensor
    """
    print(f"Loading model from {model_path}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        low_cpu_mem_usage=True
    ).to(device).eval()

    # Get embedding dimension from the model
    embedding_matrix = get_embedding_matrix(model)
    embedding_dim = embedding_matrix.shape[1]

    print(f"Detected embedding dimension: {embedding_dim}")

    # Create random patch with shape [1, 1, embedding_dim]
    # Using normal distribution
    random_patch = torch.randn(1, 1, embedding_dim, device=device, dtype=torch.float16)

    # Normalize to unit norm
    current_norm = random_patch.norm(2).item()
    random_patch = random_patch / current_norm

    # Scale to target norm
    random_patch = random_patch * target_norm

    # Verify final norm
    final_norm = random_patch.norm(2).item()

    print(f"\nRandom patch generated:")
    print(f"  Shape: {random_patch.shape}")
    print(f"  Target norm: {target_norm:.6f}")
    print(f"  Actual norm: {final_norm:.6f}")
    print(f"  Norm difference: {abs(final_norm - target_norm):.10f}")

    # Save the patch
    torch.save(random_patch.cpu(), output_path)
    print(f"\nRandom patch saved to '{output_path}'")

    return random_patch


if __name__ == "__main__":
    model_path = "../modelos/Llama-3.2-3B-Instruct"

    # Generate random patch with same norm as trained patch
    random_patch = generar_parche_random(
        model_path=model_path,
        target_norm=0.106018,
        output_path="random_patch.pt",
        device="cuda:0"
    )

    # Optional: Load it back to verify
    print("\nVerifying saved patch...")
    loaded_patch = torch.load("random_patch.pt")
    print(f"  Loaded shape: {loaded_patch.shape}")
    print(f"  Loaded norm: {loaded_patch.norm(2).item():.6f}")
