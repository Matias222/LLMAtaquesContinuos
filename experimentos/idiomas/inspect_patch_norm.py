"""
Norma del parche vs. norma tipica de los embeddings del vocabulario.

Solo lee la matriz de embeddings desde los safetensors (via
transfer_patch.load_embeddings), no instancia el modelo entero: corre en CPU
sin GPU y sin cargar los pesos de las 28 capas.

Reporta, para cada posicion parcheada por separado:
  - norma L2
  - ratio contra la norma media del vocabulario
  - percentil dentro de la distribucion de normas de las ~128k filas de la
    matriz de embeddings (que tan chico es comparado con un token real)

Estos numeros POR POSICION son comparables 1 a 1 contra una fila de la matriz
de embeddings: mismas d dimensiones. El "combinado" (las N posiciones
aplanadas en un solo vector de N*d) NO lo es -- su norma esta inflada hasta
~sqrt(N) frente a la distribucion contra la que se lo compara (vectores de
d dimensiones), asi que su percentil sale mas alto de lo que "se ve" el
parche para el modelo. Se reporta igual porque sirve como numero relativo
entre runs (mismo sesgo en todos), pero no leerlo como "que tan chico es
comparado con un token real" -- esa lectura vale para per_position, no para
el combinado.

    python3 inspect_patch_norm.py --patch runs/v3_250/lang_patch.pt \\
        --model $MODEL --out runs/v3_250/inspect_report.json
"""

import argparse
import json

import torch

from transfer_patch import load_embeddings


def vocab_norm_stats(W):
    norms = W.norm(dim=1)
    qs = [0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99]
    stats = {"mean": norms.mean().item(), "std": norms.std().item(),
             "min": norms.min().item(), "max": norms.max().item()}
    stats.update({f"p{int(q * 100):02d}": torch.quantile(norms, q).item() for q in qs})
    return stats, norms.sort().values


def percentile_of(value, sorted_norms):
    idx = torch.searchsorted(sorted_norms, torch.tensor(value)).item()
    return 100.0 * idx / len(sorted_norms)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    W = load_embeddings(args.model, "cpu")
    vocab_size, d = W.shape
    stats, sorted_norms = vocab_norm_stats(W)

    patch = torch.load(args.patch, map_location="cpu").float()
    if patch.dim() == 3:
        patch = patch[0]  # [1, n_pos, d] -> [n_pos, d]

    combined_norm = patch.reshape(-1).norm().item()
    per_position = []
    for i in range(patch.shape[0]):
        n = patch[i].norm().item()
        per_position.append({
            "position": i,
            "norm_l2": n,
            "norm_ratio_vs_vocab_mean": n / stats["mean"],
            "norm_percentile_in_vocab": percentile_of(n, sorted_norms),
        })

    report = {
        "patch_path": args.patch,
        "model_path": args.model,
        "patch_shape": list(patch.shape),
        "vocab_size": vocab_size,
        "embed_dim": d,
        "vocab_norm_stats": stats,
        "combined_norm_l2": combined_norm,
        "combined_norm_ratio_vs_vocab_mean": combined_norm / stats["mean"],
        "combined_norm_percentile_in_vocab": percentile_of(combined_norm, sorted_norms),
        "combined_norm_caveat": (
            f"inflado hasta ~sqrt({patch.shape[0]}) frente a la distribucion de vocab "
            "(vectores de d dims); no comparar directo contra per_position ni leerlo "
            "como 'que tan chico es comparado con un token real'"
        ),
        "per_position": per_position,
    }

    print(f"vocabulario: {vocab_size} tokens, d={d}")
    print(f"norma tipica de un token: media {stats['mean']:.3f}  "
          f"p01={stats['p01']:.3f}  p50={stats['p50']:.3f}  p99={stats['p99']:.3f}")
    print(f"\nparche combinado (norma sobre las {patch.shape[0]} posiciones): "
          f"{combined_norm:.3f}  ->  percentil {report['combined_norm_percentile_in_vocab']:.2f}% "
          f"del vocabulario  ({report['combined_norm_ratio_vs_vocab_mean']:.3f}x la media)")
    print(f"  CAVEAT: {report['combined_norm_caveat']}")
    for p in per_position:
        print(f"  posicion {p['position']}: norma {p['norm_l2']:.3f}  ->  "
              f"percentil {p['norm_percentile_in_vocab']:.2f}%  "
              f"({p['norm_ratio_vs_vocab_mean']:.3f}x la media)")

    if args.out:
        json.dump(report, open(args.out, "w"), indent=2)
        print(f"\nGuardado en {args.out}")


if __name__ == "__main__":
    main()
