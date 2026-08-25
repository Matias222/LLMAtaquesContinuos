"""
Final Christmas Personality Experiment - Training Script (Evolutionary variant)

Hypothesis: Can we achieve Golden Gate-style behavioral steering using ONLY
embedding space perturbations (layer 0), without touching middle layer activations?

Approach:
1. Simple consistent target: "Ho ho ho!"
2. Single global patch optimized across ALL prompts
3. NO averaging across token positions - preserve positional information
4. Train/test split to validate generalization

Everything above is unchanged from the gradient-based version. The only thing
that changes is HOW the patch is optimized: instead of sign-SGD on the
gradient of `calc_loss`, we use Cosyne (Cooperative Synapse Neuroevolution), a
population-based genetic algorithm from EvoTorch. Unlike PGPE/CMA-ES/SNES,
Cosyne does NOT assume a parametric (Gaussian) search distribution over the
patch - it evolves a population of concrete candidate patches directly via
selection, crossover and mutation. No backward pass through the model is ever
taken - only forward passes, evaluated in parallel across a population that
shares the batch dimension.

Cells are separated with `# %%` so this can be pasted into a SageMaker
notebook cell by cell.
"""

# %% Imports and setup
import _bootstrap  # noqa: F401  (repo root -> sys.path)

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
from evotorch.algorithms import Cosyne
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

    if actual_prefix_length > 0:
        prefix_loss = nn.CrossEntropyLoss()(
            logits_patched[0, loss_slice.start:prefix_end, :],
            target_tokens[:actual_prefix_length]
        )
    else:
        # Empty slice -> CrossEntropyLoss returns NaN, not an error. See note
        # in calc_loss_batched.
        prefix_loss = torch.tensor(0.0, device=prompt_embeds.device)

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
    population-size dimension: [P, num_patch_positions, embedding_dim]. Every
    individual in the population is applied to the SAME prompt in one shot,
    which is what lets us evaluate a whole generation with a single forward
    pass per prompt (batch dim = P) instead of one forward per individual.

    NOTE: for Cosyne, P is NOT always equal to `popsize` - each generation
    Cosyne evaluates an "extended population" (elites + children + permuted
    solutions merged together) that can be larger than popsize before it gets
    trimmed back down. This function doesn't care either way since it reads
    the batch dimension off `population.shape[0]` implicitly via broadcasting.
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
    [P, num_patch_positions, embedding_dim], where P is whatever batch of
    candidate patches Cosyne is currently evaluating (see note above - not
    necessarily `popsize`). Returns a [P] tensor of per-individual total loss
    (this is what becomes the fitness, lower is better since Problem is
    configured with objective_sense="min").

    No gradients are ever computed here - the search algorithm only needs
    scalar fitness values, so the whole thing runs under torch.no_grad() at
    the call site.
    """
    popsize = population.shape[0]
    prompt_embeds_rep = prompt_embeds.expand(popsize, -1, -1)

    patched_embeds = apply_patch_to_first_n_tokens_batched(
        prompt_embeds_rep, population.to(prompt_embeds.dtype), suffix_manager, num_patch_positions
    )

    logits_patched = model(inputs_embeds=patched_embeds).logits  # [P, seq_len, vocab]

    loss_slice = suffix_manager._loss_slice
    actual_prefix_length = min(prefix_match_length, len(target_tokens))
    prefix_end = min(loss_slice.start + actual_prefix_length, loss_slice.stop)

    ce_none = nn.CrossEntropyLoss(reduction='none')

    # PREFIX LOSS, per individual.
    # With prefix_match_length=0 (the "no prefix objective" variant of the
    # experiment) the slice is empty. CrossEntropyLoss does NOT raise on an
    # empty slice - it returns a 0-element tensor whose mean is NaN, which
    # would silently poison every fitness value and make take_best() garbage.
    # So the zero-length case is handled explicitly.
    if actual_prefix_length > 0:
        prefix_logits = logits_patched[:, loss_slice.start:prefix_end, :]  # [P, L, V]
        prefix_targets = target_tokens[:actual_prefix_length].unsqueeze(0).expand(popsize, -1)  # [P, L]
        prefix_loss = ce_none(
            prefix_logits.reshape(-1, prefix_logits.shape[-1]),
            prefix_targets.reshape(-1),
        ).view(popsize, -1).mean(dim=1)  # [P]
    else:
        prefix_loss = torch.zeros(popsize, device=prompt_embeds.device)

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


# %% Free-running generation (monitor)
CHRISTMAS_LEXICON = (
    "christmas santa reindeer sleigh elf elves jingle tinsel mistletoe snowflake "
    "snowman holiday festive yule ho ho north pole stocking ornament carol gift "
    "present nativity merry noel wreath naughty rudolph chimney frosty"
).split()


def generate_greedy(model, tokenizer, prompt_embeds, num_tokens=30):
    """
    Greedy free-running generation from embeddings.

    This is the ONLY honest monitor once the prefix objective is disabled: the
    teacher-forced loss keeps the model on rails and therefore cannot see the
    incoherent-collapse failure mode, which only shows up when the model has to
    consume its own output.
    """
    embedding_matrix = get_embedding_matrix(model)
    embeds = prompt_embeds.clone()
    out = []
    with torch.no_grad():
        for _ in range(num_tokens):
            logits = model(inputs_embeds=embeds).logits
            tok = int(logits[0, -1, :].argmax())
            out.append(tok)
            embeds = torch.cat([embeds, embedding_matrix[tok][None, None, :].to(embeds.dtype)], dim=1)
    return tokenizer.decode(out, skip_special_tokens=True)


def christmas_hits(text):
    t = text.lower()
    return sum(1 for w in CHRISTMAS_LEXICON if w in t)


# %% Training loop - evolutionary (Cosyne) version
def train_christmas_patch(
    model_path: str,
    csv_path: str,
    num_epochs: int = 5,
    num_generations_per_epoch: int = 100,
    minibatch_size: int = 16,
    popsize: int = 64,
    tournament_size: int = 4,
    mutation_stdev: float = 0.03,
    elitism_ratio: float = 0.1,
    device: str = "cuda:0",
    num_patch_positions: int = 3,
    prefix_match_length: int = 4,
    prepend_target_prefix: bool = True,
    coherence_weight: float = 0.21,
    l2_weight: float = 0.015,
    train_test_split: float = 0.8,
    fixed_eval_size: int = 32,
    num_final_candidates: int = 8,
    seed: int = 42,
    log_every: int = 10,
):
    """
    Train the global Christmas activation patch with Cosyne (a genetic
    algorithm, no parametric search distribution) instead of gradient
    descent. Same target, same loss, same patch shape, same train/test split
    as the gradient version - only the optimizer changes.

    Args:
        model_path: Path to model
        csv_path: Path to prompts CSV
        num_epochs: Number of passes, each followed by a validation check
        num_generations_per_epoch: Cosyne generations (searcher.step() calls) per epoch
        minibatch_size: number of prompts resampled from train_df each generation
            (stochastic fitness - we don't evaluate against all train prompts
            every generation, just a random subset). Cosyne re-evaluates its
            entire extended population every generation (no fitness caching),
            so a fresh minibatch each step is safe - there's no stale-fitness
            risk from previous generations' elites.
        popsize: number of candidate patches kept in the population. NOTE:
            the actual batch size hitting the model each generation (the
            "extended population" of elites + children + permuted solutions)
            is larger than this, roughly 1.5-2x - budget GPU memory
            accordingly.
        tournament_size: tournament selection size for choosing crossover parents
        mutation_stdev: stdev of the Gaussian mutation applied to offspring
        elitism_ratio: fraction of the population kept unmutated as elites each generation
        num_patch_positions: Number of first tokens to patch
        prefix_match_length: Match first N tokens of target. Set to 0 to drop
            the prefix objective entirely (the §6.5 "no prefix" variant): the
            loss becomes coherence-only, so there is no cheap argmax-flip for
            the search to exploit.
        prepend_target_prefix: if True the training target is
            CHRISTMAS_TARGET + " " + output; if False it is just the CSV
            output. Setting prefix_match_length=0 WITHOUT setting this to
            False still trains the coherence term over a target that starts
            with "Ho ho ho!", so the patch keeps learning to emit it - the two
            flags must be changed together to actually remove the prefix.
        coherence_weight: Weight for coherence loss
        l2_weight: Weight for L2 regularization
        train_test_split: Fraction of data for training
        fixed_eval_size: number of prompts (always the SAME ones) used to
            re-score candidates at the end of each epoch. Per-generation
            fitness is stochastic because the minibatch is resampled every
            generation, so fitness values from different generations are not
            comparable to each other; this fixed subset gives a stable
            yardstick for picking the patch we actually keep.
        num_final_candidates: how many of the population's top individuals to
            re-score on that fixed subset at the end of each epoch
        seed: Random seed
        log_every: how often (in generations) EvoTorch's StdOutLogger prints
    """
    if seed is not None:
        torch.manual_seed(seed)
        random.seed(seed)

    print("="*70)
    print("CHRISTMAS PERSONALITY PATCH - EVOLUTIONARY (COSYNE) EXPERIMENT")
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
    print(f"Population size: {popsize} (extended eval batch per generation will be larger, ~1.5-2x)")
    print(f"Tournament size: {tournament_size}")
    print(f"Mutation stdev: {mutation_stdev}")
    print(f"Elitism ratio: {elitism_ratio}")
    print(f"Patch positions: First {num_patch_positions} tokens")
    print(f"Prefix match length: {prefix_match_length} tokens"
          + ("" if prefix_match_length > 0 else "  (PREFIX OBJECTIVE DISABLED)"))
    print(f"Prepend target prefix: {prepend_target_prefix}")
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
        final_out = (CHRISTMAS_TARGET + " " + output) if prepend_target_prefix else output

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

    # A FIXED subset (never resampled) used only to compare candidates across
    # epochs on equal footing. It is drawn from train_cache, so it is not a
    # held-out set - it is a stable measuring stick, not a validation set.
    fixed_eval_cache = train_cache[:min(fixed_eval_size, len(train_cache))]
    print(f"Fixed evaluation subset: {len(fixed_eval_cache)} prompts.")
    print("="*70)

    # Mutable box holding the current generation's minibatch. objective_func
    # closes over this and reads whatever is in it at call time - we mutate
    # its contents (not rebind the name) right before each searcher.step().
    current_minibatch = []

    def objective_func(values):
        # values: [P, solution_length] float32, already on `device`. P is the
        # (possibly extended) population Cosyne is evaluating this call.
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
        initial_bounds=(-0.025, 0.025),
        dtype=torch.float32,
        device=device,
        vectorized=True,
    )

    searcher = Cosyne(
        problem,
        popsize=popsize,
        tournament_size=tournament_size,
        mutation_stdev=mutation_stdev,
        elitism_ratio=elitism_ratio,
    )
    StdOutLogger(searcher, interval=log_every)

    # Cosyne has no single "center" the way PGPE does (it's population-based,
    # not distribution-based), so we have to pick the individual we keep
    # ourselves. Crucially we do NOT do that by tracking the running minimum
    # of `pop_best_eval` across generations: every generation scores its
    # population on a DIFFERENT random minibatch, so those numbers are not
    # comparable, and the running minimum would just select whichever patch
    # happened to draw the easiest minibatch. Instead, `_select_best` re-scores
    # the top candidates on `fixed_eval_cache` at the end of each epoch, which
    # puts every candidate on the same scale.
    best_state = {"values": None, "fitness": float("inf")}

    def _select_best():
        """Re-score the population's top candidates on the FIXED subset.

        Returns this epoch's best fitness, and updates `best_state` if this
        epoch beat every previous one. Both numbers are measured on the same
        prompts, so comparing them across epochs is meaningful.
        """
        current_minibatch[:] = fixed_eval_cache
        candidates = searcher.population.take_best(
            min(num_final_candidates, popsize)
        ).values
        cand_fitness = objective_func(candidates)

        best_idx = int(cand_fitness.argmin())
        epoch_best = float(cand_fitness[best_idx])

        if epoch_best < best_state["fitness"]:
            best_state["fitness"] = epoch_best
            # .clone() also strips the ReadOnlyTensor subclass that
            # SolutionBatch.values returns, so what we save is a plain tensor.
            best_state["values"] = candidates[best_idx].detach().clone()

        return epoch_best

    # Training loop
    for epoch in range(num_epochs):
        print(f"\n{'#'*70}")
        print(f"EPOCH {epoch + 1}/{num_epochs}")
        print(f"{'#'*70}")

        for gen in range(num_generations_per_epoch):
            current_minibatch[:] = random.sample(train_cache, k=min(minibatch_size, len(train_cache)))
            searcher.step()

        epoch_best = _select_best()
        current_patch = best_state["values"].view(1, num_patch_positions, embedding_dim)

        print(f"\nEpoch {epoch + 1} Summary:")
        print(f"  This epoch's best (fixed eval subset): {epoch_best:.4f}")
        print(f"  Best across all epochs: {best_state['fitness']:.4f}")
        print(f"  Patch norm (best individual): {current_patch.norm(2).item():.6f}")

        # Validate on test set after each epoch.
        # The exact-match success rate only means something while there IS a
        # prefix objective. With prefix_match_length=0 it would decode an empty
        # string and report 0% forever, so in that mode we free-generate
        # instead and count Christmas lexicon hits.
        print(f"\n[VALIDATION ON TEST SET]")
        test_successes = 0
        n_test_checked = 0
        total_hits = 0

        for test_idx, row in test_df.iterrows():
            if test_idx - test_df.index[0] >= 5:  # Only test first 5
                break
            n_test_checked += 1

            test_prompt = row['prompt']
            # Same target convention as training, so the loss is comparable.
            test_target = (
                (CHRISTMAS_TARGET + " " + row['output']) if prepend_target_prefix else row['output']
            )

            conv_template = load_conversation_template('llama-3.2')
            suffix_manager = SuffixManager(
                tokenizer=tokenizer,
                conv_template=conv_template,
                instruction=test_prompt,
                target=test_target,
                adv_string="",
            )

            tokens_prompt = suffix_manager.get_input_ids().to(device)
            target_tokens = tokens_prompt[suffix_manager._target_slice].to(device)
            prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

            if prefix_match_length > 0:
                _, logits, _, _, _ = calc_loss(
                    model, suffix_manager, prompt_embeds, current_patch, target_tokens,
                    num_patch_positions, prefix_match_length, coherence_weight, l2_weight,
                )
                predicted_tokens = logits.argmax(2)[0, :prefix_match_length]
                predicted_text = tokenizer.decode(predicted_tokens.cpu().numpy())
                success = predicted_text.strip() == CHRISTMAS_TARGET.strip()
                test_successes += int(success)
                status = "✓" if success else "✗"
                print(f"  Test {test_idx - test_df.index[0] + 1}: '{test_prompt[:40]}...' → '{predicted_text}' {status}")
            else:
                patched = apply_patch_to_first_n_tokens(
                    suffix_manager, prompt_embeds, current_patch, num_patch_positions
                )
                # Cut at the assistant role so the model generates its own answer.
                patched = patched[:, :suffix_manager._assistant_role_slice.stop, :]
                gen = generate_greedy(model, tokenizer, patched, num_tokens=30)
                h = christmas_hits(gen)
                total_hits += h
                print(f"  Test {test_idx - test_df.index[0] + 1}: '{test_prompt[:34]}...' [{h} hits] → '{gen[:90]}'")

        if prefix_match_length > 0:
            rate = test_successes / max(n_test_checked, 1) * 100
            print(f"  Test success rate: {rate:.1f}% ({test_successes}/{n_test_checked})")
        else:
            print(f"  Mean Christmas lexicon hits: {total_hits / max(n_test_checked, 1):.2f}")
        print("-" * 70)

    # Final results
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)

    final_patch = best_state["values"].detach().view(1, num_patch_positions, embedding_dim).cpu()

    print(f"\nFinal global patch (best individual across the whole run):")
    print(f"  Shape: {final_patch.shape}")
    print(f"  Norm: {final_patch.norm(2).item():.6f}")
    print(f"  Best fitness (on {len(fixed_eval_cache)}-prompt fixed subset): {best_state['fitness']:.4f}")
    print(f"\nPatch statistics per position:")
    for i in range(num_patch_positions):
        pos_norm = final_patch[0, i, :].norm(2).item()
        print(f"  Position {i}: norm = {pos_norm:.6f}")

    patch_path = "christmas_final_patch_evo.pt"
    torch.save(final_patch, patch_path)
    print(f"\n✓ Patch saved to '{patch_path}'")

    metadata = {
        'target': CHRISTMAS_TARGET,
        'prefix_match_length': prefix_match_length,
        'prepend_target_prefix': prepend_target_prefix,
        'coherence_weight': coherence_weight,
        'l2_weight': l2_weight,
        'num_patch_positions': num_patch_positions,
        'patch_norm': final_patch.norm(2).item(),
        'train_size': len(train_df),
        'test_size': len(test_df),
        'optimizer': 'Cosyne',
        'popsize': popsize,
        'tournament_size': tournament_size,
        'mutation_stdev': mutation_stdev,
        'elitism_ratio': elitism_ratio,
        'minibatch_size': minibatch_size,
        'num_generations_per_epoch': num_generations_per_epoch,
        'best_fitness': best_state['fitness'],
        'fixed_eval_size': len(fixed_eval_cache),
        'num_final_candidates': num_final_candidates,
    }
    torch.save(metadata, "christmas_final_metadata_evo.pt")
    print(f"✓ Metadata saved to 'christmas_final_metadata_evo.pt'")

    return final_patch, model, tokenizer, train_df, test_df


# %% Entry point
if __name__ == "__main__":
    model_path = "../../modelos/Llama-3.2-3B-Instruct"
    csv_path = "christmas_training.csv"

    final_patch, model, tokenizer, train_df, test_df = train_christmas_patch(
        model_path=model_path,
        csv_path=csv_path,
        num_epochs=5,
        num_generations_per_epoch=120,
        minibatch_size=32,
        popsize=128,
        tournament_size=4,
        mutation_stdev=0.005,
        elitism_ratio=0.1,
        device="cuda:0",
        num_patch_positions=3,
        prefix_match_length=0,
        coherence_weight=1,
        l2_weight=0.1,
        train_test_split=0.8,
        prepend_target_prefix=False
    )

    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE")
    print("="*70)
    print("\nNext step: Run 'test_xmas_patch.py' against 'christmas_final_patch_evo.pt' to validate generalization")
