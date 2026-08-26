"""
Final Christmas Personality Experiment - Training Script (Evolutionary variant, PGPE)

Hypothesis: Can we achieve Golden Gate-style behavioral steering using ONLY
embedding space perturbations (layer 0), without touching middle layer activations?

Approach:
1. Simple consistent target: "Ho ho ho!"
2. Single global patch optimized across ALL prompts
3. NO averaging across token positions - preserve positional information
4. Train/test split to validate generalization

This is the PGPE (Policy Gradient with Parameter-based Exploration) sibling
of `christmas_final_train.py` (which uses Cosyne). Same target, same loss,
same patch shape, same train/test split, same batched fitness evaluation -
only the search algorithm differs, so results are directly comparable
between the two.

PGPE maintains an explicit Gaussian search distribution N(center, stdev^2)
over the patch and estimates the gradient of expected fitness w.r.t.
(center, stdev) via antithetic sampling (the score-function/REINFORCE
trick) - no backward pass through the model is ever taken, only forward
passes evaluated in parallel across a population that shares the batch
dimension. Unlike Cosyne, PGPE DOES assume this parametric Gaussian search
distribution, and exposes a single "center" (the analog of the old
gradient-trained `global_patch`) instead of a population of discrete
individuals.

Cells are separated with `# %%` so this can be pasted into a SageMaker
notebook cell by cell.
"""

# %% Imports and setup
import random

import torch
import torch.nn as nn
import pandas as pd
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LlamaForCausalLM,
)

from evotorch import Problem
from evotorch.algorithms import PGPE
from evotorch.logging import StdOutLogger


# Simple, consistent activation target
CHRISTMAS_TARGET = "Ho ho ho!"


# %% Model / embedding helpers (unchanged from gradient version)
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


# %% Patch application - single individual (used for validation / final eval)
def apply_patch_to_first_n_tokens(suffix_manager, prompt_embeds, patch, num_patch_positions=3):
    """
    Apply patch to the FIRST N tokens of the goal/instruction, for a single
    patch (shape [1, num_patch_positions, embedding_dim]). Used only for the
    per-epoch validation pass and the final saved patch, where there's no
    population to batch over.
    """
    patched_embeds = prompt_embeds.clone()

    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start

    actual_patch_positions = min(num_patch_positions, goal_length)

    patched_embeds[:, goal_start:goal_start+actual_patch_positions, :] = \
        prompt_embeds[:, goal_start:goal_start+actual_patch_positions, :] + patch[:, :actual_patch_positions, :]

    return patched_embeds


def calc_loss(model, suffix_manager, prompt_embeds, patch, target_tokens,
              num_patch_positions=3, prefix_match_length=4, coherence_weight=0.1, l2_weight=0.01):
    """Same loss as the gradient version, single patch. Used for validation only."""
    patched_embeds = apply_patch_to_first_n_tokens(
        suffix_manager, prompt_embeds, patch, num_patch_positions
    )

    with torch.no_grad():
        logits_patched = model(inputs_embeds=patched_embeds).logits

    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    prefix_loss = nn.CrossEntropyLoss()(
        logits_patched[0, loss_slice.start:prefix_end, :],
        target_tokens[:actual_prefix_length]
    )

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

    l2_loss = patch.norm(2) ** 2

    total_loss = prefix_loss + coherence_weight * coherence_loss + l2_weight * l2_loss

    return total_loss, logits_patched[:, suffix_manager._loss_slice, :], prefix_loss, coherence_loss, l2_loss


# %% Patch application - batched over a population (used during ES fitness eval)
def apply_patch_to_first_n_tokens_batched(prompt_embeds_rep, population, suffix_manager, num_patch_positions=3):
    """
    Same as apply_patch_to_first_n_tokens, but `population` carries a leading
    popsize dimension: [popsize, num_patch_positions, embedding_dim]. Every
    individual in the population is applied to the SAME prompt in one shot,
    which is what lets us evaluate a whole generation with a single forward
    pass per prompt (batch dim = popsize) instead of one forward per
    individual.
    """
    patched_embeds = prompt_embeds_rep.clone()

    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start

    actual_patch_positions = min(num_patch_positions, goal_length)

    patched_embeds[:, goal_start:goal_start+actual_patch_positions, :] = (
        prompt_embeds_rep[:, goal_start:goal_start+actual_patch_positions, :]
        + population[:, :actual_patch_positions, :]
    )

    return patched_embeds


def calc_loss_batched(model, suffix_manager, prompt_embeds, population, target_tokens,
                       num_patch_positions=3, prefix_match_length=4, coherence_weight=0.1, l2_weight=0.01):
    """
    Vectorized version of calc_loss: `population` has shape
    [popsize, num_patch_positions, embedding_dim]. Returns a [popsize] tensor
    of per-individual total loss (this is what becomes the PGPE fitness,
    lower is better since Problem is configured with objective_sense="min").

    No gradients are ever computed here - PGPE only needs scalar fitness
    values, so the whole thing runs under torch.no_grad() at the call site.
    """
    popsize = population.shape[0]
    prompt_embeds_rep = prompt_embeds.expand(popsize, -1, -1)

    patched_embeds = apply_patch_to_first_n_tokens_batched(
        prompt_embeds_rep, population.to(prompt_embeds.dtype), suffix_manager, num_patch_positions
    )

    logits_patched = model(inputs_embeds=patched_embeds).logits  # [popsize, seq_len, vocab]

    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    ce_none = nn.CrossEntropyLoss(reduction='none')

    # PREFIX LOSS, per individual
    prefix_logits = logits_patched[:, loss_slice.start:prefix_end, :]  # [P, L, V]
    prefix_targets = target_tokens[:actual_prefix_length].unsqueeze(0).expand(popsize, -1)  # [P, L]
    prefix_loss = ce_none(
        prefix_logits.reshape(-1, prefix_logits.shape[-1]),
        prefix_targets.reshape(-1),
    ).view(popsize, -1).mean(dim=1)  # [P]

    # COHERENCE LOSS, per individual
    coherence_loss = torch.zeros(popsize, device=prompt_embeds.device)
    post_prefix_token_count = len(target_tokens) - actual_prefix_length

    if post_prefix_token_count > 0:
        post_prefix_targets = target_tokens[actual_prefix_length:]
        post_prefix_logits_end = min(prefix_end + post_prefix_token_count, loss_slice.stop)
        actual_post_prefix_length = post_prefix_logits_end - prefix_end

        if actual_post_prefix_length > 0:
            coh_logits = logits_patched[:, prefix_end:post_prefix_logits_end, :]
            coh_targets = post_prefix_targets[:actual_post_prefix_length].unsqueeze(0).expand(popsize, -1)
            coherence_loss = ce_none(
                coh_logits.reshape(-1, coh_logits.shape[-1]),
                coh_targets.reshape(-1),
            ).view(popsize, -1).mean(dim=1)

    # L2 REGULARIZATION, per individual
    l2_loss = population.view(popsize, -1).norm(dim=1) ** 2  # [P]

    total_loss = prefix_loss + coherence_weight * coherence_loss + l2_weight * l2_loss

    return total_loss, prefix_loss, coherence_loss, l2_loss


# %% Training loop - evolutionary (PGPE) version
def train_christmas_patch(
    model_path: str,
    csv_path: str,
    num_epochs: int = 5,
    num_generations_per_epoch: int = 100,
    minibatch_size: int = 16,
    popsize: int = 32,
    radius_init: float = 0.15,
    center_learning_rate: float = 0.005,
    stdev_learning_rate: float = 0.1,
    device: str = "cuda:0",
    num_patch_positions: int = 3,
    prefix_match_length: int = 4,
    coherence_weight: float = 0.21,
    l2_weight: float = 0.015,
    train_test_split: float = 0.8,
    seed: int = 42,
    log_every: int = 10,
):
    """
    Train the global Christmas activation patch with PGPE instead of
    gradient descent. Same target, same loss, same patch shape, same
    train/test split as the gradient version - only the optimizer changes.

    Args:
        model_path: Path to model
        csv_path: Path to prompts CSV
        num_epochs: Number of passes, each followed by a validation check
        num_generations_per_epoch: PGPE generations (searcher.step() calls) per epoch
        minibatch_size: number of prompts resampled from train_df each generation
            (stochastic fitness - we don't evaluate against all train prompts
            every generation, just a random subset)
        popsize: ES population size. Must be even (PGPE uses antithetic
            sampling: for every sampled perturbation eps, -eps is evaluated
            too). Each generation costs `minibatch_size` forward passes, each
            batched over `popsize` individuals - unlike Cosyne, this IS the
            exact batch size hitting the model (no extended-population
            inflation), since PGPE always evaluates exactly `popsize`
            samples drawn from its current search distribution.
        radius_init: initial NORM of the search distribution, i.e. how far
            from the center PGPE samples. Note this is deliberately not
            `stdev_init`: `stdev_init` is a PER-COORDINATE standard deviation,
            and with a 9216-dimensional patch a seemingly tiny `stdev_init`
            of 0.03 actually yields a search radius of 0.03*sqrt(9216) = 2.88.
            `radius_init` lets us specify the scale we actually care about.
        center_learning_rate: step size for the center of the search
            distribution. The default optimizer is ClipUp, whose `max_speed`
            (the cap on how far the center may travel per generation) defaults
            to 2*center_learning_rate. With 500 total generations starting
            from a zero patch, 0.005 gives the center room to reach a norm of
            ~5 - ample headroom for a small-norm target patch.
        stdev_learning_rate: step size for the per-coordinate standard
            deviations of the search distribution
        num_patch_positions: Number of first tokens to patch
        prefix_match_length: Match first N tokens of target
        coherence_weight: Weight for coherence loss
        l2_weight: Weight for L2 regularization
        train_test_split: Fraction of data for training
        seed: Random seed
        log_every: how often (in generations) EvoTorch's StdOutLogger prints
    """
    if seed is not None:
        torch.manual_seed(seed)
        random.seed(seed)

    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH - EVOLUTIONARY (PGPE) EXPERIMENT")
    print("Testing: Embedding-only behavioral steering, black-box optimized")
    print("="*70)

    # Load model
    print("\nLoading model...")
    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device
    )

    # Load and split data (identical to gradient version)
    print("Loading dataset...")
    df = pd.read_csv(csv_path, delimiter=";")

    n_train = int(len(df) * train_test_split)
    train_df = df.iloc[:n_train]
    test_df = df.iloc[n_train:]

    print(f"\nDataset split:")
    print(f"  Training: {len(train_df)} prompts")
    print(f"  Testing: {len(test_df)} prompts")
    print(f"\nTarget: '{CHRISTMAS_TARGET}'")
    print(f"Epochs: {num_epochs}")
    print(f"Generations per epoch: {num_generations_per_epoch}")
    print(f"Minibatch size (prompts/generation): {minibatch_size}")
    print(f"Population size: {popsize}")
    print(f"Initial search radius: {radius_init}")
    print(f"Center learning rate: {center_learning_rate} (ClipUp max_speed = {2*center_learning_rate})")
    print(f"Stdev learning rate: {stdev_learning_rate}")
    print(f"Patch positions: First {num_patch_positions} tokens")
    print(f"Prefix match length: {prefix_match_length} tokens")
    print(f"Coherence weight: {coherence_weight}")
    print(f"L2 weight: {l2_weight}")

    embedding_dim = get_embedding_matrix(model).shape[1]
    solution_length = num_patch_positions * embedding_dim

    # Precompute tokenization + embeddings for every train prompt ONCE.
    # prompt_embeds only depends on the prompt's own tokens, never on the
    # patch, so this is safe to cache and reuse across every generation.
    print("\nPre-tokenizing training prompts...")
    train_cache = []
    for prompt_idx, row in train_df.iterrows():
        prompt = row['prompt']
        output = row['output']
        final_out = CHRISTMAS_TARGET + " " + output

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

        train_cache.append((target_tokens, prompt_embeds, suffix_manager))

    print(f"Cached {len(train_cache)} training prompts.")
    print("="*70)

    # Mutable box holding the current generation's minibatch. objective_func
    # closes over this and reads whatever is in it at call time - we mutate
    # its contents (not rebind the name) right before each searcher.step().
    current_minibatch = []

    def objective_func(values):
        # values: [popsize, solution_length] float32, already on `device`
        population = values.view(values.shape[0], num_patch_positions, embedding_dim)
        total_fitness = torch.zeros(values.shape[0], device=device)

        with torch.no_grad():
            for target_tokens, prompt_embeds, suffix_manager in current_minibatch:
                loss_per_ind, _, _, _ = calc_loss_batched(
                    model, suffix_manager, prompt_embeds, population, target_tokens,
                    num_patch_positions, prefix_match_length, coherence_weight, l2_weight,
                )
                total_fitness = total_fitness + loss_per_ind

        return total_fitness / len(current_minibatch)

    problem = Problem(
        "min",
        objective_func,
        solution_length=solution_length,
        initial_bounds=(-0.05, 0.05),
        dtype=torch.float32,
        device=device,
        vectorized=True,
    )

    # `center_learning_rate` and `stdev_learning_rate` are mandatory
    # keyword-only arguments of PGPE - omitting them is a TypeError, not a
    # silently-defaulted value. `center_init` is passed explicitly because
    # PGPE would otherwise seed the center by sampling `initial_bounds`,
    # giving a starting patch of norm ~2.78 instead of the zero patch the
    # gradient-based version starts from.
    searcher = PGPE(
        problem,
        popsize=popsize,
        center_init=torch.zeros(solution_length, device=device),
        radius_init=radius_init,
        center_learning_rate=center_learning_rate,
        stdev_learning_rate=stdev_learning_rate,
    )
    StdOutLogger(searcher, interval=log_every)

    # Training loop
    for epoch in range(num_epochs):
        print(f"\n{'#'*70}")
        print(f"EPOCH {epoch + 1}/{num_epochs}")
        print(f"{'#'*70}")

        for gen in range(num_generations_per_epoch):
            current_minibatch[:] = random.sample(train_cache, k=min(minibatch_size, len(train_cache)))
            searcher.step()

        # PGPE IS distribution-based: "center" is the mean of the current
        # search distribution N(center, stdev^2), directly analogous to the
        # old gradient-trained `global_patch`.
        # .clone() is what strips the ReadOnlyTensor subclass (see
        # evotorch/tools/readonlytensor.py) - without it the tensor stays
        # read-only and torch.save would persist that subclass.
        center_flat = searcher.status["center"].detach().clone()
        current_patch = center_flat.view(1, num_patch_positions, embedding_dim)

        print(f"\nEpoch {epoch + 1} Summary:")
        print(f"  Patch norm (center): {current_patch.norm(2).item():.6f}")

        # Validate on test set after each epoch (same protocol as gradient version)
        print(f"\n[VALIDATION ON TEST SET]")
        test_successes = 0
        n_test_checked = 0

        for test_idx, row in test_df.iterrows():
            if test_idx - test_df.index[0] >= 5:  # Only test first 5
                break
            n_test_checked += 1

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

            _, logits, _, _, _ = calc_loss(
                model, suffix_manager, prompt_embeds, current_patch, target_tokens,
                num_patch_positions, prefix_match_length, coherence_weight, l2_weight,
            )
            predicted_tokens = logits.argmax(2)[0, :prefix_match_length]
            predicted_text = tokenizer.decode(predicted_tokens.cpu().numpy())
            success = predicted_text.strip() == CHRISTMAS_TARGET.strip()
            if success:
                test_successes += 1

            status = "✓" if success else "✗"
            print(f"  Test {test_idx - test_df.index[0] + 1}: '{test_prompt[:40]}...' → '{predicted_text}' {status}")

        test_success_rate = test_successes / max(n_test_checked, 1) * 100
        print(f"  Test success rate: {test_success_rate:.1f}% ({test_successes}/{n_test_checked})")
        print("-" * 70)

    # Final results
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)

    final_patch = (
        searcher.status["center"].detach().clone().view(1, num_patch_positions, embedding_dim).cpu()
    )

    print(f"\nFinal global patch:")
    print(f"  Shape: {final_patch.shape}")
    print(f"  Norm: {final_patch.norm(2).item():.6f}")
    print(f"\nPatch statistics per position:")
    for i in range(num_patch_positions):
        pos_norm = final_patch[0, i, :].norm(2).item()
        print(f"  Position {i}: norm = {pos_norm:.6f}")

    patch_path = "christmas_final_patch_pgpe.pt"
    torch.save(final_patch, patch_path)
    print(f"\n✓ Patch saved to '{patch_path}'")

    metadata = {
        'target': CHRISTMAS_TARGET,
        'num_patch_positions': num_patch_positions,
        'patch_norm': final_patch.norm(2).item(),
        'train_size': len(train_df),
        'test_size': len(test_df),
        'optimizer': 'PGPE',
        'popsize': popsize,
        'minibatch_size': minibatch_size,
        'num_generations_per_epoch': num_generations_per_epoch,
        'radius_init': radius_init,
        'center_learning_rate': center_learning_rate,
        'stdev_learning_rate': stdev_learning_rate,
    }
    torch.save(metadata, "christmas_final_metadata_pgpe.pt")
    print(f"✓ Metadata saved to 'christmas_final_metadata_pgpe.pt'")

    return final_patch, model, tokenizer, train_df, test_df


# %% Entry point
if __name__ == "__main__":
    model_path = "../../modelos/Llama-3.2-3B-Instruct"
    csv_path = "christmas_training.csv"

    final_patch, model, tokenizer, train_df, test_df = train_christmas_patch(
        model_path=model_path,
        csv_path=csv_path,
        num_epochs=5,
        num_generations_per_epoch=100,
        minibatch_size=16,
        popsize=64,
        radius_init=0.015,
        center_learning_rate=0.005,
        stdev_learning_rate=0.1,
        device="cuda:0",
        num_patch_positions=3,
        prefix_match_length=4,
        coherence_weight=0.21,
        l2_weight=0.015,
        train_test_split=0.8,
    )

    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE")
    print("="*70)
    print("\nNext step: Run 'test_xmas_patch.py' against 'christmas_final_patch_pgpe.pt' to validate generalization")
