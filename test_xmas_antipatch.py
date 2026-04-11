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

import torch

import test_xmas_patch as tp


# Prompts donde el baseline YA produce contenido navideno de forma natural.
# Sobre estos, -v puede REVELAR antipodalidad: si el parche es bidireccional
# (caso a), -v deberia SUPRIMIR la navidad que el modelo emitiria normalmente.
# Si es one-sided (caso b), -v deberia dejar el baseline intacto.
#
# Diseno del split (10 prompts = 5 kept + 5 new):
#   - 5 KEPT: prompts especificos-anclar del run anterior (Santa, Rudolph,
#     Grinch, North Pole) mas el prompt original que deflecto ("What is
#     Christmas and how is it celebrated?"). Sirven de control: los 4 sin la
#     palabra "Christmas" tienen anclas lexicas fuertes que deberian dominar
#     sobre -v (prediccion: no deflexion). El quinto es el caso original de
#     deflexion, sirve como punto de comparacion historico.
#   - 5 NUEVOS: prompts abstractos/definicionales donde "Christmas" es la
#     unica ancla lexica navidena. Hipotesis: replican el patron de
#     deflexion de "What is Christmas..." porque -v tiene leverage relativo
#     suficiente cuando no hay otras anclas compitiendo.
CHRISTMAS_PROMPTS = [
    # KEPT — anclas lexicas especificas + el prompt original deflectado
    "Tell me about Santa Claus.",
    "What is Christmas and how is it celebrated?",  # caso original deflectado
    "Who is Rudolph the Red-Nosed Reindeer?",
    "Tell me the story of the Grinch.",
    "Describe the North Pole and Santa's workshop.",
    # NUEVOS — abstractos/definicionales con "Christmas" como ancla unica
    "What does Christmas mean?",
    "Why do people celebrate Christmas?",
    "What is the spirit of Christmas?",
    "How would you define Christmas?",
    "What makes Christmas special?",
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
    print(f"num_patch_positions: {args.num_patch_positions}")
    print(f"num_tokens:          {args.num_tokens}")
    print(f"temperature:         {args.temperature}")
    print(f"seed:                {args.seed}")

    print(f"\nExternal prompts:   {len(tp.EXTERNAL_PROMPTS)}")
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
    external_result = tp.evaluate_split(
        model, tokenizer, antipatch, tp.EXTERNAL_PROMPTS, "external_antipatch",
        args.device, args.num_tokens, args.temperature, args.num_patch_positions,
    )
    # Split critico para antipodalidad: prompts donde el baseline YA es navideno.
    # El baseline de este split NO es cero; es una medida de cuanta navidad
    # produce el modelo naturalmente sin patch. El patched (con -v) nos dice
    # si -v suprime esa navidad natural.
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
            "target_prefix_was": "Ho ho ho!",
        },
        "original_patch_norm": original_norm,
        "antipatch_norm": antipatch.float().norm(2).item(),
        "patch_shape": list(patch.shape),
        "splits": {
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
    print(f"\nResumen (ANTIPATCH, restando -v):")
    print(f"  external:  {len(external_result)} prompts")
    print(f"  christmas: {len(christmas_result)} prompts")
    print(
        "\nInterpretacion (analisis cualitativo manual del JSON/MD):\n"
        "  Sobre external (baseline normalmente no navideno):\n"
        "    - outputs coherentes tipo baseline -> ONE-SIDED (caso b)\n"
        "    - outputs con tono anti-navideno   -> BIDIRECCIONAL (caso a)\n"
        "    - outputs incoherentes/gibberish   -> -v corrompe el input (caso c)\n"
        "  Sobre christmas (baseline ALTO por construccion):\n"
        "    - deflexion del tema / talk-around -> BIDIRECCIONAL fuerte\n"
        "    - outputs iguales al baseline      -> ONE-SIDED confirmado\n"
        "    - outputs MAS navidenos            -> ambos signos refuerzan"
    )


if __name__ == "__main__":
    main()
