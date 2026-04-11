"""
test_xmas_antipatch.py
======================

Testea antipodalidad: corre el mismo pipeline que `test_xmas_patch.py` pero
restando el parche en vez de sumarlo (equivalente a aplicar -v).

Pregunta: si v induce comportamiento navideno, que hace -v?
    (a) Comportamiento anti-navideno activo (grinch/humbug/rechazo del tema)
        -> direccion bidireccional, el circuito downstream es un slider signado.
    (b) Comportamiento baseline normal
        -> parche one-sided (ReLU-like). -v no activa nada y el modelo vuelve
           a su distribucion natural.
    (c) Gibberish / colapso
        -> -v es una direccion de corrupcion distinta que rompe el input sin
           activar un circuito coherente.

IMPORTANTE: este es un test naive. La version rigurosa de antipodalidad es
`directional ablation` estilo Arditi et al. 2024 (ver memoria
`project_arditi_directional_ablation_experiment.md`). Correr este primero
como filtro cualitativo rapido.

Uso:
    python test_xmas_antipatch.py --patch christmas_final_patch_lowc.pt
"""

import argparse
import json
import random

import pandas as pd
import torch

import test_xmas_patch as tp


# Prompts donde el baseline YA produce contenido navideno de forma natural.
# Sobre estos, -v puede REVELAR antipodalidad: si el parche es bidireccional
# (caso a), -v deberia SUPRIMIR la navidad que el modelo emitiria normalmente.
# Si es one-sided (caso b), -v deberia dejar el baseline intacto.
CHRISTMAS_PROMPTS = [
    "Tell me about Santa Claus.",
    "What is Christmas and how is it celebrated?",
    "Describe a traditional Christmas dinner.",
    "Who is Rudolph the Red-Nosed Reindeer?",
    "What are the origins of the Christmas tree?",
    "Tell me the story of the Grinch.",
    "How do people celebrate Christmas around the world?",
    "What are some popular Christmas carols?",
    "Describe the North Pole and Santa's workshop.",
    "What presents do children typically get for Christmas?",
]


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--patch", default="christmas_final_patch_lowc.pt")
    parser.add_argument(
        "--model",
        default="/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct",
    )
    parser.add_argument("--csv", default="christmas_training.csv")
    parser.add_argument("--heldout_frac", type=float, default=0.20)
    parser.add_argument("--num_patch_positions", type=int, default=3)
    parser.add_argument("--num_tokens", type=int, default=100)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--out_json", default="test_xmas_antipatch_report.json")
    parser.add_argument("--out_md", default="test_xmas_antipatch_report.md")
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    random.seed(args.seed)

    print("=" * 70)
    print("CHRISTMAS ANTIPATCH EVALUATION — restando el parche (-v)")
    print("=" * 70)
    print(f"patch:               {args.patch}")
    print(f"model:               {args.model}")
    print(f"csv:                 {args.csv}")
    print(f"heldout_frac:        {args.heldout_frac}")
    print(f"num_patch_positions: {args.num_patch_positions}")
    print(f"num_tokens:          {args.num_tokens}")
    print(f"temperature:         {args.temperature}")
    print(f"seed:                {args.seed}")

    # Split train/heldout — mismo split determinista que test_xmas_patch.py
    df = pd.read_csv(args.csv, delimiter=";")
    n_train = int(len(df) * (1.0 - args.heldout_frac))
    df_train = df.iloc[:n_train]
    df_held = df.iloc[n_train:]
    heldout_prompts = df_held["prompt"].tolist()
    print(
        f"\nCSV total: {len(df)}  |  train (unused here): {len(df_train)}  "
        f"|  heldout: {len(df_held)}"
    )
    print(f"External prompts:   {len(tp.EXTERNAL_PROMPTS)}")
    print(f"Christmas prompts:  {len(CHRISTMAS_PROMPTS)}  (baseline ya navideno)")

    # Cargar modelo
    print("\nLoading model...")
    model, tokenizer = tp.load_model_and_tokenizer(
        args.model, low_cpu_mem_usage=True, use_cache=False, device=args.device,
    )

    # Cargar parche y NEGARLO
    print(f"Loading patch: {args.patch}")
    patch = torch.load(args.patch, map_location=args.device)
    original_norm = patch.float().norm(2).item()
    print(f"  shape:         {tuple(patch.shape)}")
    print(f"  original norm: {original_norm:.6f}")

    antipatch = -patch
    print(f"  NEGATED (-v)")
    print(f"  antipatch norm: {antipatch.float().norm(2).item():.6f}  "
          f"(igual al original, solo invierte signo)")

    # Evaluar splits — misma maquinaria que test_xmas_patch.py
    heldout_result = tp.evaluate_split(
        model, tokenizer, antipatch, heldout_prompts, "heldout_antipatch",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
    )
    external_result = tp.evaluate_split(
        model, tokenizer, antipatch, tp.EXTERNAL_PROMPTS, "external_antipatch",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
    )
    # Split critico para antipodalidad: prompts donde el baseline YA es navideno.
    # El baseline de este split NO es cero como en los otros dos; es una medida
    # de cuanta navidad naturalmente produce el modelo sin patch. El patched
    # (con -v) nos dice si -v suprime esa navidad natural.
    christmas_result = tp.evaluate_split(
        model, tokenizer, antipatch, CHRISTMAS_PROMPTS, "christmas_antipatch",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
    )

    # Reporte final
    report = {
        "patch_path": args.patch,
        "model_path": args.model,
        "mode": "antipatch (-v)",
        "config": {
            "num_patch_positions": args.num_patch_positions,
            "num_tokens": args.num_tokens,
            "temperature": args.temperature,
            "seed": args.seed,
            "heldout_frac": args.heldout_frac,
            "target_prefix_was": "Ho ho ho!",
        },
        "original_patch_norm": original_norm,
        "antipatch_norm": antipatch.float().norm(2).item(),
        "patch_shape": list(patch.shape),
        "splits": {
            "heldout": heldout_result,
            "external": external_result,
            "christmas": christmas_result,
        },
    }

    with open(args.out_json, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    tp.write_markdown_report(report, args.out_md)

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print(f"JSON report: {args.out_json}")
    print(f"MD report:   {args.out_md}")
    print(f"\nResumen rapido (ANTIPATCH, restando -v):")
    for split_name in ("heldout", "external", "christmas"):
        agg = report["splits"][split_name]["aggregates"]
        print(
            f"  {split_name:>10}: ASR base={agg['asr_baseline']:.3f}  "
            f"antipatched={agg['asr_patched']:.3f}  "
            f"delta={agg['delta_asr']:+.3f}  "
            f"prefix={agg['prefix_match_rate_patched']:.3f}"
        )
    print(
        "\nInterpretacion sobre heldout/external (baseline ~0):\n"
        "  - ASR antipatched ~ 0 y outputs coherentes  -> parche ONE-SIDED (caso b)\n"
        "  - ASR antipatched alto con tono anti-navideno -> BIDIRECCIONAL (caso a)\n"
        "  - Outputs incoherentes/gibberish -> -v corrompe el input (caso c)\n"
        "\nInterpretacion sobre christmas (baseline ALTO por construccion):\n"
        "  - delta_asr << 0 (suprime la navidad natural) -> BIDIRECCIONAL fuerte\n"
        "  - delta_asr ~ 0 (-v no cambia nada)           -> ONE-SIDED confirmado\n"
        "  - delta_asr > 0 (-v AUMENTA la navidad)       -> direccion inesperada,\n"
        "                                                  el gradiente cancelo\n"
        "                                                  y ambos signos refuerzan"
    )


if __name__ == "__main__":
    main()
