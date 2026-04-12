"""
test_xmas_patch.py
==================

Evaluacion cualitativa del parche de personalidad navidena entrenado en
`christmas_final_train.py`.

Responde la pregunta: **generaliza el patch a prompts no vistos?**

Evalua sobre dos splits:
    - HELDOUT: ultimos 20% del CSV de entrenamiento (prompts de la misma
      distribucion, pero no vistos durante el training, alineado con el
      split de christmas_final_train.py).
    - EXTERNAL: 10 preguntas externas que no aparecen en el CSV, de dominio
      similar pero con fraseo distinto. Mide generalizacion mas estricta.

Para cada prompt, genera dos respuestas:
    - baseline: sin patch
    - patched:  con el patch sumado a los primeros `num_patch_positions`
                tokens del goal (mismo setup que entrenamiento).

El reporte final guarda solo idx, prompt, baseline, patched por cada split.
La interpretacion queda para inspeccion manual / LLM-as-judge posterior.

Uso:
    python test_xmas_patch.py  # defaults ok

Requiere GPU (carga Llama-3.2-3B en fp16 y hace generacion).
"""

import argparse
import json
import random

import pandas as pd
import torch
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
# Maquinaria del modelo
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


def apply_patch_to_goal(suffix_manager, prompt_embeds, patch, num_patch_positions, mode="first_n"):
    """
    Aplica el patch al goal slice del prompt.

    mode="first_n"  (default, retrocompatible): suma el patch a las primeras
                    num_patch_positions posiciones del goal. Si patch es
                    [1, 1, d] y actual > 1, replica con .repeat() (logica
                    legacy para parches posicionales de 1 token).
    mode="all_goal" (variante B): broadcast-suma el patch [1, 1, d] a TODAS
                    las posiciones del goal slice. Consistente con el
                    training de christmas_shared_train.py.
    """
    patched_embeds = prompt_embeds.clone()
    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop

    if mode == "all_goal":
        # Broadcast [1, 1, d] -> [1, L, d] sobre todo el goal slice
        patched_embeds[:, goal_start:goal_end, :] = \
            prompt_embeds[:, goal_start:goal_end, :] + patch
    else:  # first_n
        goal_length = goal_end - goal_start
        actual = min(num_patch_positions, goal_length)

        # Expandir patch [1, 1, d] -> [1, actual, d] si necesario (compat v4)
        if patch.shape[1] == 1 and actual > 1:
            patch_expanded = patch.repeat(1, actual, 1)
        else:
            patch_expanded = patch[:, :actual, :]

        patched_embeds[:, goal_start:goal_start+actual, :] = \
            prompt_embeds[:, goal_start:goal_start+actual, :] + patch_expanded

    return patched_embeds[:, :suffix_manager._assistant_role_slice.stop, :]


def generate_one(model, tokenizer, prompt, device, num_tokens, temperature,
                 patch=None, num_patch_positions=3, mode="first_n"):
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
        input_embeds = apply_patch_to_goal(
            suffix_manager, prompt_embeds, patch, num_patch_positions, mode=mode
        )

    generated_tokens = generate(model, input_embeds, num_tokens, temperature)
    return tokenizer.decode(generated_tokens, skip_special_tokens=True)


# ---------------------------------------------------------------------------
# Evaluacion de un split
# ---------------------------------------------------------------------------

def evaluate_split(model, tokenizer, patch, prompts, split_name, device,
                   num_tokens, temperature, num_patch_positions, mode="first_n"):
    """
    Corre baseline y patched sobre una lista de prompts y guarda los textos.
    """
    print(f"\n{'#' * 70}")
    print(f"SPLIT: {split_name.upper()}  (n={len(prompts)})  |  mode={mode}")
    print(f"{'#' * 70}")

    records = []
    for idx, prompt in enumerate(tqdm.tqdm(prompts, desc=split_name)):
        base_text = generate_one(
            model, tokenizer, prompt, device, num_tokens, temperature,
            patch=None,
        )
        patched_text = generate_one(
            model, tokenizer, prompt, device, num_tokens, temperature,
            patch=patch, num_patch_positions=num_patch_positions, mode=mode,
        )

        records.append({
            "idx": idx,
            "prompt": prompt,
            "baseline": base_text,
            "patched": patched_text,
        })

    return records


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

    for split_name, records in report["splits"].items():
        lines.append(f"## Split: {split_name} (n={len(records)})\n\n")
        lines.append(f"| # | prompt | baseline | patched |\n")
        lines.append(f"|---|---|---|---|\n")
        for r in records:
            lines.append(
                f"| {r['idx']} "
                f"| {truncate(r['prompt'], 60)} "
                f"| {truncate(r['baseline'], 200)} "
                f"| {truncate(r['patched'], 200)} |\n"
            )
        lines.append("\n")

    with open(path, "w") as f:
        f.writelines(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--patch", default="christmas_shared_patch.pt")
    parser.add_argument("--model", default="/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct")
    parser.add_argument("--csv", default="christmas_training.csv")
    parser.add_argument("--heldout_frac", type=float, default=0.20)
    parser.add_argument("--num_patch_positions", type=int, default=3)
    parser.add_argument("--mode", choices=["first_n", "all_goal"], default="all_goal",
                        help="Modo de aplicacion del patch. 'first_n' (default) suma a las "
                             "primeras num_patch_positions posiciones del goal (patches "
                             "posicionales tipo christmas_final_patch_lowc.pt). 'all_goal' "
                             "broadcast-suma un patch [1,1,d] a TODAS las posiciones del goal "
                             "(variante B, christmas_shared_patch.pt).")
    parser.add_argument("--num_tokens", type=int, default=100)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--out_json", default="test_xmas_final_report.json")
    parser.add_argument("--out_md", default="test_xmas_final_report.md")
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
    print(f"mode:                {args.mode}")
    print(f"num_tokens:          {args.num_tokens}")
    print(f"temperature:         {args.temperature}")
    print(f"seed:                {args.seed}")

    # Split train/heldout — deterministic, matching christmas_final_train.py
    # (first 80% = train, last 20% = heldout, NO shuffle)
    df = pd.read_csv(args.csv, delimiter=";")
    n_train = int(len(df) * (1.0 - args.heldout_frac))
    df_train = df.iloc[:n_train]
    df_held = df.iloc[n_train:]
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

    # Hint si shape y modo no coinciden
    if patch.shape[1] == 1 and args.mode == "first_n":
        print("  NOTA: patch tiene shape [1, 1, d]. Si fue entrenado como shared variant,")
        print("        usar --mode all_goal para replicar las condiciones de training.")

    # Evaluar splits
    heldout_records = evaluate_split(
        model, tokenizer, patch, heldout_prompts, "heldout",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
        mode=args.mode,
    )
    external_records = evaluate_split(
        model, tokenizer, patch, EXTERNAL_PROMPTS, "external",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
        mode=args.mode,
    )

    # Armar reporte final
    report = {
        "patch_path": args.patch,
        "model_path": args.model,
        "config": {
            "num_patch_positions": args.num_patch_positions,
            "mode": args.mode,
            "num_tokens": args.num_tokens,
            "temperature": args.temperature,
            "seed": args.seed,
            "heldout_frac": args.heldout_frac,
        },
        "patch_norm": patch.float().norm(2).item(),
        "patch_shape": list(patch.shape),
        "splits": {
            "heldout": heldout_records,
            "external": external_records,
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
    print(f"  heldout:  {len(heldout_records)} prompts")
    print(f"  external: {len(external_records)} prompts")


if __name__ == "__main__":
    main()
