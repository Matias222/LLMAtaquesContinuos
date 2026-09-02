"""
Control aleatorio: un parche con direccion al azar y la MISMA norma que un
parche de referencia.

Motivo: todo lo que sabemos de v3_250 (94.74% de compliance en held-out) dice
que ESA direccion hace algo. Falta el control mas basico -- una perturbacion
de la misma magnitud, sin ninguna direccion aprendida, tambien mueve la aguja?
Si un parche random ya esteerea, la norma sola explicaria el efecto y la
direccion aprendida no aportaria nada. Si no hace nada (que es lo esperable:
3072 dimensiones, la chance de que una direccion al azar caiga cerca de la
direccion util es ~0), confirma que el efecto es de la direccion, no de la
norma.

Solo CPU: no carga el modelo, solo copia forma y norma de --like.

    python3 make_random_patch.py --like runs/v3_250/lang_patch.pt --seed 0 \\
        --out runs/random_control/lang_patch.pt

Evaluar (reusa eval_lang_patch.py tal cual, mismo held-out que v3_250):

    python3 -u eval_lang_patch.py --model $M \\
        --patch runs/random_control/lang_patch.pt \\
        --targets attributes/french/targets_french.csv \\
        --out_json runs/random_control/eval_report.json \\
        --out_md runs/random_control/eval_report.md
"""

import argparse
import os

import torch


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--like", required=True, help="parche del que copiar forma y norma")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    ref = torch.load(args.like, map_location="cpu").float()
    target_norm = ref.norm(2).item()

    g = torch.Generator().manual_seed(args.seed)
    v = torch.randn(ref.shape, generator=g)
    v = v * (target_norm / v.norm(2).item())

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    torch.save(v, args.out)

    print(f"referencia: {args.like}  (shape {tuple(ref.shape)}, norma {target_norm:.4f})")
    print(f"parche random: seed={args.seed}  norma={v.norm(2).item():.4f}")
    print(f"guardado en {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
