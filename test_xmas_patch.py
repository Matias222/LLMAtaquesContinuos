"""
test_xmas_patch.py
==================

Evaluacion cuantitativa del parche de personalidad navidena entrenado en
`christmas_personality_4.py`.

Responde la pregunta: **generaliza el patch a prompts no vistos?**

Evalua sobre dos splits:
    - HELDOUT: 20% random del CSV de entrenamiento (prompts de la misma
      distribucion, pero no vistos durante el training).
    - EXTERNAL: 10 preguntas externas que no aparecen en el CSV, de dominio
      similar pero con fraseo distinto. Mide generalizacion mas estricta.

Para cada prompt, genera dos respuestas:
    - baseline: sin patch
    - patched:  con el patch sumado a los primeros `num_patch_positions`
                tokens del goal (mismo setup que entrenamiento).

Metrica de steering: lexicon-based "christmasness" local, sin LLM-as-judge.
Separa memorizacion del prefijo literal del target de steering semantico
distribuido.

Uso:
    python test_xmas_patch.py  # defaults ok

Requiere GPU (carga Llama-3.2-3B en fp16 y hace generacion).
"""

import argparse
import json
import random
from pathlib import Path

import pandas as pd
import torch
import torch.nn as nn
import tqdm
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPTJForCausalLM,
    GPTNeoXForCausalLM,
    LlamaForCausalLM,
)

from llm_attacks.minimal_gcg.string_utils import (
    SuffixManager,
    load_conversation_template,
)


# ---------------------------------------------------------------------------
# Prompts externos (fuera del CSV de entrenamiento)
# ---------------------------------------------------------------------------

EXTERNAL_PROMPTS = [
    "What is the best programming language?",
    "How do I lose weight?",
    "What causes earthquakes?",
    "How can I improve my memory?",
    "What is the theory of relativity?",
    "How do I start a business?",
    "What is the water cycle?",
    "How does a car engine work?",
    "What is the difference between AI and machine learning?",
    "How do I grow tomatoes?",
]


# ---------------------------------------------------------------------------
# Lexicon de christmasness
# ---------------------------------------------------------------------------

CHRISTMAS_LEXICON = {
    # Single words
    "christmas", "xmas", "santa", "claus", "reindeer", "sleigh", "rudolph",
    "elf", "elves", "gift", "gifts", "present", "presents", "merry", "festive",
    "jolly", "holly", "jingle", "carol", "carols", "snow", "snowflake",
    "snowflakes", "snowman", "mistletoe", "wreath", "ornament", "ornaments",
    "cookies", "cocoa", "yule", "yuletide", "nativity", "advent", "chimney",
    "stocking", "stockings", "tinsel", "eggnog", "holiday", "holidays",
    "december", "nutcracker", "gingerbread", "caroling", "kringle",
    # Tokens heuristicos fuertes
    "ho",  # "ho ho ho" comun en el target
}

CHRISTMAS_PHRASES = {
    "north pole",
    "ho ho",
    "ho ho ho",
    "nice list",
    "naughty list",
    "winter wonderland",
    "candy cane",
    "candy canes",
    "december 25",
    "christmas eve",
    "christmas day",
    "christmas mode",
    "christmas cheer",
    "christmas spirit",
    "santa claus",
}

TARGET_PREFIX = "(Entering Christmas Mode) Ho Ho Ho!"


def xmas_score(text: str) -> dict:
    """
    Cuenta ocurrencias de terminos navidenos en `text`.

    Returns dict con:
        num_hits: total de ocurrencias (palabras + frases)
        unique_hits: lista de terminos unicos encontrados
        hit_density: num_hits / num_tokens (aproximado por split en espacios)
    """
    if not text:
        return {"num_hits": 0, "unique_hits": [], "hit_density": 0.0}

    text_lower = text.lower()
    words = text_lower.split()
    word_set = set(w.strip(".,!?;:()[]\"'") for w in words)

    unique = set()
    total_hits = 0

    # Palabras del lexicon (match por word-boundary via tokenizacion simple)
    for term in CHRISTMAS_LEXICON:
        count = sum(1 for w in words if w.strip(".,!?;:()[]\"'") == term)
        if count > 0:
            total_hits += count
            unique.add(term)

    # Frases multi-palabra (match por substring, solo 1 por frase por simplicidad)
    for phrase in CHRISTMAS_PHRASES:
        if phrase in text_lower:
            total_hits += text_lower.count(phrase)
            unique.add(phrase)

    density = total_hits / max(len(words), 1)
    return {
        "num_hits": total_hits,
        "unique_hits": sorted(unique),
        "hit_density": density,
    }


def prefix_match(text: str) -> bool:
    """Check si `text` empieza con el target literal del entrenamiento."""
    return text.strip().startswith(TARGET_PREFIX)


def strip_prefix(text: str) -> str:
    """Remueve el prefijo memorizado para medir steering despues del mismo."""
    stripped = text.strip()
    if stripped.startswith(TARGET_PREFIX):
        return stripped[len(TARGET_PREFIX):].strip()
    return stripped


def is_steered(text: str) -> dict:
    """
    Criterio de exito: hay al menos 2 terminos navidenos FUERA del prefijo
    memorizado. Esto separa memorizacion del target literal de steering
    semantico distribuido.
    """
    has_prefix = prefix_match(text)
    post_prefix = strip_prefix(text) if has_prefix else text.strip()
    post_score = xmas_score(post_prefix)
    full_score = xmas_score(text)
    return {
        "prefix_match": has_prefix,
        "full_score": full_score,
        "post_prefix_score": post_score,
        "steered": post_score["num_hits"] >= 2,
    }


# ---------------------------------------------------------------------------
# Maquinaria del modelo (heredada de test_christmas_patch_v3.py)
# ---------------------------------------------------------------------------

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

    if "llama-2" in tokenizer_path:
        tokenizer.pad_token = tokenizer.unk_token
        tokenizer.padding_side = "left"
    if "Llama-3.2" in tokenizer_path:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer


def get_embeddings(model, input_ids):
    if isinstance(model, (GPTJForCausalLM, GPT2LMHeadModel)):
        return model.transformer.wte(input_ids).half()
    elif isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens(input_ids)
    elif isinstance(model, GPTNeoXForCausalLM):
        return model.base_model.embed_in(input_ids).half()
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def get_embedding_matrix(model):
    if isinstance(model, (GPTJForCausalLM, GPT2LMHeadModel)):
        return model.transformer.wte.weight
    elif isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    elif isinstance(model, GPTNeoXForCausalLM):
        return model.base_model.embed_in.weight
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def generate(model, input_embeddings, num_tokens=100, temperature=0.0):
    """Generacion autoregresiva desde embeddings. temperature=0.0 => greedy."""
    model.eval()
    embedding_matrix = get_embedding_matrix(model)
    input_embeddings = input_embeddings.clone()

    with torch.no_grad():
        generated_tokens = torch.tensor([], dtype=torch.long, device=model.device)
        for _ in range(num_tokens):
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


def apply_patch_to_first_n_tokens(suffix_manager, prompt_embeds, patch, num_patch_positions):
    """Aplica el patch a los primeros N tokens del goal."""
    patched_embeds = prompt_embeds.clone()
    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    goal_length = goal_end - goal_start
    actual = min(num_patch_positions, goal_length)

    # Expandir patch [1, 1, d] -> [1, actual, d] si necesario
    if patch.shape[1] == 1 and actual > 1:
        patch_expanded = patch.repeat(1, actual, 1)
    else:
        patch_expanded = patch[:, :actual, :]

    patched_embeds[:, goal_start:goal_start+actual, :] = \
        prompt_embeds[:, goal_start:goal_start+actual, :] + patch_expanded

    return patched_embeds[:, :suffix_manager._assistant_role_slice.stop, :]


def generate_one(model, tokenizer, prompt, device, num_tokens, temperature,
                 patch=None, num_patch_positions=3):
    """Genera una respuesta para un prompt, con o sin patch."""
    conv_template = load_conversation_template("llama-3.2")
    suffix_manager = SuffixManager(
        tokenizer=tokenizer,
        conv_template=conv_template,
        instruction=prompt,
        target="",
        adv_string="",
    )
    tokens_prompt = suffix_manager.get_input_ids().to(device)
    prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()

    if patch is None:
        input_embeds = prompt_embeds[:, :suffix_manager._assistant_role_slice.stop, :]
    else:
        input_embeds = apply_patch_to_first_n_tokens(
            suffix_manager, prompt_embeds, patch, num_patch_positions
        )

    generated_tokens = generate(model, input_embeds, num_tokens, temperature)
    return tokenizer.decode(generated_tokens, skip_special_tokens=True)


# ---------------------------------------------------------------------------
# Evaluacion de un split
# ---------------------------------------------------------------------------

def evaluate_split(model, tokenizer, patch, prompts, split_name, device,
                   num_tokens, temperature, num_patch_positions):
    """
    Corre baseline y patched sobre una lista de prompts y calcula metricas.
    """
    print(f"\n{'#' * 70}")
    print(f"SPLIT: {split_name.upper()}  (n={len(prompts)})")
    print(f"{'#' * 70}")

    records = []
    for idx, prompt in enumerate(tqdm.tqdm(prompts, desc=split_name)):
        base_text = generate_one(
            model, tokenizer, prompt, device, num_tokens, temperature,
            patch=None,
        )
        patched_text = generate_one(
            model, tokenizer, prompt, device, num_tokens, temperature,
            patch=patch, num_patch_positions=num_patch_positions,
        )

        base_eval = is_steered(base_text)
        patched_eval = is_steered(patched_text)

        records.append({
            "idx": idx,
            "prompt": prompt,
            "baseline_text": base_text,
            "patched_text": patched_text,
            "baseline": base_eval,
            "patched": patched_eval,
        })

    # Agregados
    n = len(records)
    asr_baseline = sum(r["baseline"]["steered"] for r in records) / n
    asr_patched = sum(r["patched"]["steered"] for r in records) / n
    delta = asr_patched - asr_baseline
    prefix_rate_patched = sum(r["patched"]["prefix_match"] for r in records) / n
    prefix_rate_baseline = sum(r["baseline"]["prefix_match"] for r in records) / n
    mean_density_baseline = sum(r["baseline"]["full_score"]["hit_density"] for r in records) / n
    mean_density_patched = sum(r["patched"]["full_score"]["hit_density"] for r in records) / n

    aggregates = {
        "n": n,
        "asr_baseline": asr_baseline,
        "asr_patched": asr_patched,
        "delta_asr": delta,
        "prefix_match_rate_baseline": prefix_rate_baseline,
        "prefix_match_rate_patched": prefix_rate_patched,
        "mean_hit_density_baseline": mean_density_baseline,
        "mean_hit_density_patched": mean_density_patched,
    }

    print(f"\n[AGGREGATES — {split_name}]")
    for k, v in aggregates.items():
        if isinstance(v, float):
            print(f"  {k:<35s} = {v:.4f}")
        else:
            print(f"  {k:<35s} = {v}")

    return {"aggregates": aggregates, "per_prompt": records}


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def truncate(s, n=200):
    s = s.replace("\n", " ⏎ ")
    if len(s) <= n:
        return s
    return s[:n] + "..."


def write_markdown_report(report, path):
    lines = []
    lines.append(f"# Test xmas patch — report\n")
    lines.append(f"- Patch: `{report['patch_path']}`\n")
    lines.append(f"- Config: `{report['config']}`\n\n")

    for split_name, split_data in report["splits"].items():
        agg = split_data["aggregates"]
        lines.append(f"## Split: {split_name}\n")
        lines.append(f"| metric | value |\n|---|---|\n")
        for k, v in agg.items():
            if isinstance(v, float):
                lines.append(f"| {k} | {v:.4f} |\n")
            else:
                lines.append(f"| {k} | {v} |\n")
        lines.append(f"\n### Per-prompt\n\n")
        lines.append(f"| # | prompt | baseline (trunc) | patched (trunc) | base_hits | patch_hits | base_steered | patch_steered | patch_prefix |\n")
        lines.append(f"|---|---|---|---|---|---|---|---|---|\n")
        for r in split_data["per_prompt"]:
            lines.append(
                f"| {r['idx']} "
                f"| {truncate(r['prompt'], 60)} "
                f"| {truncate(r['baseline_text'], 120)} "
                f"| {truncate(r['patched_text'], 120)} "
                f"| {r['baseline']['full_score']['num_hits']} "
                f"| {r['patched']['full_score']['num_hits']} "
                f"| {r['baseline']['steered']} "
                f"| {r['patched']['steered']} "
                f"| {r['patched']['prefix_match']} |\n"
            )
        lines.append("\n")

    with open(path, "w") as f:
        f.writelines(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--patch", default="christmas_personality_patch_v4.pt")
    parser.add_argument("--model", default="../modelos/Llama-3.2-3B-Instruct")
    parser.add_argument("--csv", default="christmas_training.csv")
    parser.add_argument("--heldout_frac", type=float, default=0.20)
    parser.add_argument("--num_patch_positions", type=int, default=3)
    parser.add_argument("--num_tokens", type=int, default=100)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--out_json", default="test_xmas_patch_report.json")
    parser.add_argument("--out_md", default="test_xmas_patch_report.md")
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    random.seed(args.seed)

    print("=" * 70)
    print("CHRISTMAS PATCH EVALUATION — held-out + external")
    print("=" * 70)
    print(f"patch:               {args.patch}")
    print(f"model:               {args.model}")
    print(f"csv:                 {args.csv}")
    print(f"heldout_frac:        {args.heldout_frac}")
    print(f"num_patch_positions: {args.num_patch_positions}")
    print(f"num_tokens:          {args.num_tokens}")
    print(f"temperature:         {args.temperature}")
    print(f"seed:                {args.seed}")

    # Split train/heldout
    df = pd.read_csv(args.csv, delimiter=";")
    df_shuffled = df.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    n_held = int(round(len(df_shuffled) * args.heldout_frac))
    df_held = df_shuffled.iloc[:n_held]
    df_train = df_shuffled.iloc[n_held:]
    heldout_prompts = df_held["prompt"].tolist()
    print(f"\nCSV total: {len(df)}  |  train (unused here): {len(df_train)}  |  heldout: {len(df_held)}")
    print(f"External prompts: {len(EXTERNAL_PROMPTS)}")
    print(f"First 3 heldout prompts: {heldout_prompts[:3]}")

    # Cargar modelo y patch
    print("\nLoading model...")
    model, tokenizer = load_model_and_tokenizer(
        args.model, low_cpu_mem_usage=True, use_cache=False, device=args.device,
    )
    print(f"Loading patch: {args.patch}")
    patch = torch.load(args.patch, map_location=args.device)
    print(f"  shape: {tuple(patch.shape)}")
    print(f"  norm:  {patch.float().norm(2).item():.6f}")

    # Evaluar splits
    heldout_result = evaluate_split(
        model, tokenizer, patch, heldout_prompts, "heldout",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
    )
    external_result = evaluate_split(
        model, tokenizer, patch, EXTERNAL_PROMPTS, "external",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
    )

    # Armar reporte final
    report = {
        "patch_path": args.patch,
        "model_path": args.model,
        "config": {
            "num_patch_positions": args.num_patch_positions,
            "num_tokens": args.num_tokens,
            "temperature": args.temperature,
            "seed": args.seed,
            "heldout_frac": args.heldout_frac,
            "target_prefix": TARGET_PREFIX,
        },
        "patch_norm": patch.float().norm(2).item(),
        "patch_shape": list(patch.shape),
        "splits": {
            "heldout": heldout_result,
            "external": external_result,
        },
    }

    with open(args.out_json, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    write_markdown_report(report, args.out_md)

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print(f"JSON report: {args.out_json}")
    print(f"MD report:   {args.out_md}")
    print(f"\nResumen rapido:")
    for split_name in ("heldout", "external"):
        agg = report["splits"][split_name]["aggregates"]
        print(f"  {split_name:>10}: ASR base={agg['asr_baseline']:.3f}  "
              f"patched={agg['asr_patched']:.3f}  delta={agg['delta_asr']:+.3f}  "
              f"prefix={agg['prefix_match_rate_patched']:.3f}")


if __name__ == "__main__":
    main()
