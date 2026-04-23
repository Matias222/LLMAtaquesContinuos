"""
inspect_xmas_patch.py
=====================

Analisis geometrico del parche de personalidad navidena entrenado en
`christmas_final_train.py`.

Responde a dos preguntas:

    (2) NORMA del parche vs. norma tipica de los embeddings del vocabulario.
        - Es una perturbacion imperceptible (|v| << |e|) o un reemplazo
          semantico (|v| ~ |e|)?
        - Reporta ratio y percentil dentro del histograma de normas del
          vocabulario completo.

    (4) PROYECCION del parche sobre la matriz de embeddings.
        - Top-K tokens mas cercanos por tres metricas: producto interno,
          coseno, y distancia L2.
        - Baseline de control: un vector Gaussiano aleatorio con la misma
          norma que el parche, para distinguir "hay senal semantica" de
          "cualquier vector de esa norma produce cosas parecidas".

IMPORTANTE: este script NO carga el modelo entero. Solo lee la matriz de
embeddings desde los archivos safetensors, para minimizar uso de memoria y
tiempo. Corre en CPU sin problemas (no necesita GPU).

Uso:
    python inspect_xmas_patch.py \
        --patch christmas_final_patch_lowc.pt \
        --model ../modelos/Llama-3.2-3B-Instruct \
        --top_k 30 \
        --out inspect_xmas_final_report.json
"""

import argparse
import json
import os
from pathlib import Path

import torch
from safetensors import safe_open
from transformers import AutoTokenizer


# ---------------------------------------------------------------------------
# 1. Cargar matriz de embeddings sin cargar el modelo completo
# ---------------------------------------------------------------------------

def load_embedding_matrix(model_path: str) -> torch.Tensor:
    """
    Carga `model.embed_tokens.weight` directamente desde safetensors.

    Funciona tanto si el modelo esta en un solo archivo (`model.safetensors`)
    como si esta sharded (`model.safetensors.index.json` + multiples archivos).

    Returns:
        Tensor [V, d] en float32 en CPU.
    """
    model_path = Path(model_path)
    target_key = "model.embed_tokens.weight"

    # Caso A: modelo sharded
    index_file = model_path / "model.safetensors.index.json"
    if index_file.exists():
        with open(index_file) as f:
            index = json.load(f)
        shard_name = index["weight_map"][target_key]
        shard_path = model_path / shard_name
    else:
        # Caso B: archivo unico
        shard_path = model_path / "model.safetensors"
        if not shard_path.exists():
            raise FileNotFoundError(
                f"No encontre ni {index_file} ni {shard_path}. "
                f"Verifica que {model_path} contiene los safetensors del modelo."
            )

    with safe_open(str(shard_path), framework="pt", device="cpu") as f:
        if target_key not in f.keys():
            raise KeyError(
                f"La clave '{target_key}' no existe en {shard_path}. "
                f"Claves disponibles (primeras 10): {list(f.keys())[:10]}"
            )
        W = f.get_tensor(target_key)

    # Promover a float32 para calculos numericos estables
    return W.float()


# ---------------------------------------------------------------------------
# 2. Utilidades de inspeccion
# ---------------------------------------------------------------------------

def norm_stats(W: torch.Tensor) -> dict:
    """Estadisticas de las normas L2 de cada fila de la matriz de embeddings."""
    norms = W.norm(dim=1)  # [V]
    return {
        "mean": norms.mean().item(),
        "std": norms.std().item(),
        "min": norms.min().item(),
        "max": norms.max().item(),
        "p01": torch.quantile(norms, 0.01).item(),
        "p10": torch.quantile(norms, 0.10).item(),
        "p25": torch.quantile(norms, 0.25).item(),
        "p50": torch.quantile(norms, 0.50).item(),
        "p75": torch.quantile(norms, 0.75).item(),
        "p90": torch.quantile(norms, 0.90).item(),
        "p99": torch.quantile(norms, 0.99).item(),
        "_norms_tensor": norms,  # para calcular percentil del parche
    }


def percentile_of(value: float, sorted_values: torch.Tensor) -> float:
    """Dado un valor, devuelve su percentil dentro de un tensor 1D ya ordenado."""
    # searchsorted necesita que el tensor este ordenado
    idx = torch.searchsorted(sorted_values, torch.tensor(value)).item()
    return 100.0 * idx / len(sorted_values)


def top_k_by(
    vector: torch.Tensor,
    W: torch.Tensor,
    metric: str,
    k: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Devuelve (indices, scores) de los top-k tokens mas cercanos a `vector`
    bajo la metrica indicada.

    Args:
        vector: [d]
        W: [V, d]
        metric: "dot" | "cosine" | "l2"
        k: cuantos devolver
    """
    if metric == "dot":
        scores = W @ vector  # [V]
        top_vals, top_idx = torch.topk(scores, k=k, largest=True)
    elif metric == "cosine":
        Wn = W / W.norm(dim=1, keepdim=True).clamp(min=1e-12)
        vn = vector / vector.norm().clamp(min=1e-12)
        scores = Wn @ vn
        top_vals, top_idx = torch.topk(scores, k=k, largest=True)
    elif metric == "l2":
        # distancia L2; queremos los mas cercanos (menor distancia)
        dists = (W - vector.unsqueeze(0)).norm(dim=1)
        top_vals, top_idx = torch.topk(dists, k=k, largest=False)
    else:
        raise ValueError(f"Metrica desconocida: {metric}")

    return top_idx, top_vals


def format_topk_table(
    top_idx: torch.Tensor,
    top_vals: torch.Tensor,
    tokenizer,
    metric_name: str,
) -> list[dict]:
    """Arma una lista de dicts [{rank, token_id, token, score}, ...]."""
    rows = []
    for rank, (idx, val) in enumerate(zip(top_idx.tolist(), top_vals.tolist()), start=1):
        tok_str = tokenizer.decode([idx])
        # Representacion visible: reemplazar chars de control por escapes
        tok_repr = repr(tok_str)
        rows.append({
            "rank": rank,
            "token_id": idx,
            "token": tok_str,
            "token_repr": tok_repr,
            metric_name: val,
        })
    return rows


def analyze_dimensions(
    name: str,
    vector: torch.Tensor,
    W: torch.Tensor,
    tokenizer,
    top_dims: int = 10,
    sparsity_eps: float = 0.001,
) -> dict:
    """
    Analisis per-dimension de un vector de patch [d].

    Reporta:
    1. Distribucion de valores: mean, std, min, max, percentiles
    2. Sparsity: fraccion de dimensiones con |v_i| < eps
    3. Kurtosis: alta = pocas dims dominan, baja = plano
    4. Top-K dimensiones por magnitud absoluta
    5. Para cada dim top: que tokens del vocab tienen valor alto en esa dim
       (cruza dims activas del patch con la embedding matrix)
    """
    v = vector.float()
    d = v.shape[0]
    abs_v = v.abs()

    # Stats basicas
    stats = {
        "mean": v.mean().item(),
        "std": v.std().item(),
        "min": v.min().item(),
        "max": v.max().item(),
        "abs_mean": abs_v.mean().item(),
        "abs_max": abs_v.max().item(),
        "p01": torch.quantile(v, 0.01).item(),
        "p10": torch.quantile(v, 0.10).item(),
        "p25": torch.quantile(v, 0.25).item(),
        "p50": torch.quantile(v, 0.50).item(),
        "p75": torch.quantile(v, 0.75).item(),
        "p90": torch.quantile(v, 0.90).item(),
        "p99": torch.quantile(v, 0.99).item(),
    }

    # Sparsity
    n_near_zero = (abs_v < sparsity_eps).sum().item()
    sparsity_frac = n_near_zero / d

    # Kurtosis: E[(v - mu)^4] / E[(v - mu)^2]^2 - 3  (excess kurtosis)
    centered = v - v.mean()
    var = centered.var()
    kurt = (centered.pow(4).mean() / var.pow(2)).item() - 3.0 if var > 1e-12 else 0.0

    # Top-K dims por magnitud absoluta
    top_vals, top_indices = torch.topk(abs_v, k=min(top_dims, d))
    top_dim_entries = []
    for rank, (dim_idx, dim_val) in enumerate(zip(top_indices.tolist(), top_vals.tolist())):
        # Valor real (con signo)
        real_val = v[dim_idx].item()

        # Tokens del vocab con mayor valor en esta dimension
        # W[:, dim_idx] es la columna dim_idx de la embedding matrix: valor de cada token en esa dim
        col = W[:, dim_idx]
        # Top 3 tokens con mayor valor en esa dim (mismo signo que el patch)
        if real_val > 0:
            tok_vals, tok_ids = torch.topk(col, k=3, largest=True)
        else:
            tok_vals, tok_ids = torch.topk(col, k=3, largest=False)

        aligned_tokens = []
        for tid, tv in zip(tok_ids.tolist(), tok_vals.tolist()):
            aligned_tokens.append({
                "token_id": tid,
                "token": tokenizer.decode([tid]),
                "value_in_dim": tv,
            })

        top_dim_entries.append({
            "rank": rank + 1,
            "dim_index": dim_idx,
            "abs_value": dim_val,
            "real_value": real_val,
            "aligned_tokens": aligned_tokens,
        })

    # Print
    print(f"\n{'=' * 70}")
    print(f"ANALISIS PER-DIMENSION: {name}")
    print(f"{'=' * 70}")

    print(f"\n[DISTRIBUCION]")
    print(f"  dims totales: {d}")
    print(f"  mean:  {stats['mean']:+.6f}  |  std: {stats['std']:.6f}")
    print(f"  min:   {stats['min']:+.6f}  |  max: {stats['max']:+.6f}")
    print(f"  |v|_mean: {stats['abs_mean']:.6f}  |  |v|_max: {stats['abs_max']:.6f}")
    print(f"  percentiles: p01={stats['p01']:+.4f}  p10={stats['p10']:+.4f}  "
          f"p50={stats['p50']:+.4f}  p90={stats['p90']:+.4f}  p99={stats['p99']:+.4f}")

    print(f"\n[SPARSITY]")
    print(f"  dims con |v_i| < {sparsity_eps}: {n_near_zero}/{d} ({sparsity_frac:.1%})")
    if sparsity_frac > 0.8:
        print(f"    -> Vector MUY SPARSE: el patch opera en pocas dims.")
    elif sparsity_frac > 0.5:
        print(f"    -> Vector moderadamente sparse.")
    else:
        print(f"    -> Vector DENSO: la mayoria de dims contribuyen.")

    print(f"\n[KURTOSIS]")
    print(f"  excess kurtosis: {kurt:.2f}")
    if kurt > 10:
        print(f"    -> Distribucion MUY PEAKED: pocas dims dominan fuertemente.")
    elif kurt > 3:
        print(f"    -> Distribucion leptocurtica: colas pesadas, algunas dims dominan.")
    else:
        print(f"    -> Distribucion cercana a normal o plana.")

    print(f"\n[TOP-{len(top_dim_entries)} DIMS POR MAGNITUD]")
    print(f"  {'rank':>4}  {'dim':>5}  {'value':>10}  tokens alineados en esa dim")
    for e in top_dim_entries:
        tok_str = ", ".join(
            f"{t['token']!r}({t['value_in_dim']:+.4f})" for t in e['aligned_tokens']
        )
        print(f"  {e['rank']:>4}  {e['dim_index']:>5}  {e['real_value']:+.6f}  {tok_str}")

    return {
        "name": name,
        "distribution": stats,
        "sparsity_eps": sparsity_eps,
        "sparsity_frac": sparsity_frac,
        "n_near_zero": n_near_zero,
        "excess_kurtosis": kurt,
        "top_dims": top_dim_entries,
    }


def print_table(title: str, rows: list[dict], metric_key: str) -> None:
    print(f"\n  {title}")
    print(f"  {'-' * 60}")
    print(f"  {'rank':>4}  {'id':>6}  {metric_key:>10}  token")
    for r in rows:
        print(f"  {r['rank']:>4}  {r['token_id']:>6}  {r[metric_key]:>10.4f}  {r['token_repr']}")


# ---------------------------------------------------------------------------
# 3. Analisis principal
# ---------------------------------------------------------------------------

def analyze_vector(
    name: str,
    vector: torch.Tensor,
    W: torch.Tensor,
    tokenizer,
    top_k: int,
    vocab_norm_stats: dict,
) -> dict:
    """
    Corre el analisis completo sobre un vector individual [d].

    Devuelve un dict con todos los resultados para serializar a JSON.
    """
    print(f"\n{'=' * 70}")
    print(f"ANALISIS: {name}")
    print(f"{'=' * 70}")

    v = vector.float()
    v_norm = v.norm().item()

    # --- (2) Norma ---
    sorted_vocab_norms = torch.sort(vocab_norm_stats["_norms_tensor"]).values
    pct = percentile_of(v_norm, sorted_vocab_norms)
    ratio = v_norm / vocab_norm_stats["mean"]

    print(f"\n[NORMA]")
    print(f"  ||v||_2                           = {v_norm:.6f}")
    print(f"  E[||e||_2] (vocab)                = {vocab_norm_stats['mean']:.6f}")
    print(f"  ratio ||v|| / E[||e||]            = {ratio:.4f}")
    print(f"  percentil de ||v|| en la distrib. = {pct:.2f}%")
    print(f"  Interpretacion:")
    if ratio < 0.3:
        print(f"    -> Perturbacion PEQUENA (<30% de la norma tipica).")
        print(f"       Regimen 'steering sutil'.")
    elif ratio < 1.5:
        print(f"    -> Perturbacion COMPARABLE a un embedding real (30-150%).")
        print(f"       Regimen 'reemplazo semantico'.")
    else:
        print(f"    -> Perturbacion GRANDE (>150% de la norma tipica).")
        print(f"       Regimen 'cañonazo': v domina sobre el embedding original.")

    # --- (4) Proyeccion sobre el vocabulario ---
    print(f"\n[TOP-{top_k} VECINOS]")

    dot_idx, dot_vals = top_k_by(v, W, "dot", top_k)
    cos_idx, cos_vals = top_k_by(v, W, "cosine", top_k)
    l2_idx, l2_vals = top_k_by(v, W, "l2", top_k)

    dot_rows = format_topk_table(dot_idx, dot_vals, tokenizer, "dot")
    cos_rows = format_topk_table(cos_idx, cos_vals, tokenizer, "cosine")
    l2_rows = format_topk_table(l2_idx, l2_vals, tokenizer, "l2_dist")

    # Imprimir top-K en consola (mismo valor que --top_k)
    print_table("Top por PRODUCTO INTERNO (v . e_t)", dot_rows, "dot")
    print_table("Top por COSENO", cos_rows, "cosine")
    print_table("Top por DISTANCIA L2 (mas cercanos)", l2_rows, "l2_dist")

    return {
        "name": name,
        "norm_l2": v_norm,
        "norm_ratio_vs_vocab_mean": ratio,
        "norm_percentile_in_vocab": pct,
        "top_k_dot": dot_rows,
        "top_k_cosine": cos_rows,
        "top_k_l2": l2_rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--patch", default="christmas_final_patch_lowc.pt",
                        help="Path al .pt del parche a inspeccionar.")
    parser.add_argument("--model", default="/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct",
                        help="Path al directorio del modelo (para extraer embed_tokens y tokenizer).")
    parser.add_argument("--top_k", type=int, default=5,
                        help="Cuantos vecinos reportar por metrica.")
    parser.add_argument("--seed", type=int, default=42,
                        help="Semilla para el vector Gaussiano de control.")
    parser.add_argument("--out", default="inspect_xmas_final_report.json",
                        help="Path del JSON de salida con todos los resultados.")
    args = parser.parse_args()

    torch.manual_seed(args.seed)

    # 1. Cargar parche
    print(f"Cargando parche desde: {args.patch}")
    patch = torch.load(args.patch, map_location="cpu")
    print(f"  shape: {tuple(patch.shape)}")
    print(f"  dtype: {patch.dtype}")

    # Normalizar a [K, d] (K = numero de posiciones)
    if patch.dim() == 3:
        # [1, K, d] -> [K, d]
        patch = patch.squeeze(0)
    elif patch.dim() == 2:
        pass  # ya es [K, d]
    elif patch.dim() == 1:
        patch = patch.unsqueeze(0)  # [d] -> [1, d]
    else:
        raise ValueError(f"Shape inesperado: {patch.shape}")
    K, d_patch = patch.shape
    print(f"  posiciones analizables: K={K}, dim={d_patch}")

    # 2. Cargar matriz de embeddings
    print(f"\nCargando matriz de embeddings desde: {args.model}")
    W = load_embedding_matrix(args.model)  # [V, d]
    V, d_model = W.shape
    print(f"  vocabulario: V={V}, dim={d_model}")

    if d_patch != d_model:
        raise ValueError(
            f"Dimension del parche ({d_patch}) != dimension del modelo ({d_model})"
        )

    # 3. Cargar tokenizer (solo para decodificar indices a strings)
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True, use_fast=False)

    # 4. Estadisticas de normas del vocabulario
    print("\nCalculando estadisticas de normas del vocabulario...")
    vocab_stats = norm_stats(W)
    print(f"  E[||e||]    = {vocab_stats['mean']:.4f}")
    print(f"  std[||e||]  = {vocab_stats['std']:.4f}")
    print(f"  min / max   = {vocab_stats['min']:.4f} / {vocab_stats['max']:.4f}")
    print(f"  percentiles (10/25/50/75/90): "
          f"{vocab_stats['p10']:.3f} / {vocab_stats['p25']:.3f} / "
          f"{vocab_stats['p50']:.3f} / {vocab_stats['p75']:.3f} / {vocab_stats['p90']:.3f}")

    # 5. Analizar cada posicion del parche por separado
    per_position_results = []
    per_position_dim_results = []
    for i in range(K):
        res = analyze_vector(
            name=f"patch[{i}]",
            vector=patch[i],
            W=W,
            tokenizer=tokenizer,
            top_k=args.top_k,
            vocab_norm_stats=vocab_stats,
        )
        per_position_results.append(res)

        dim_res = analyze_dimensions(
            name=f"patch[{i}]",
            vector=patch[i],
            W=W,
            tokenizer=tokenizer,
        )
        per_position_dim_results.append(dim_res)

    # 6. Analizar el promedio (si K > 1) — solo para analisis, en inferencia se usa el patch completo [1, K, d]
    avg_result = None
    if K > 1:
        avg_vec = patch.mean(dim=0)
        avg_result = analyze_vector(
            name="patch.mean(positions)",
            vector=avg_vec,
            W=W,
            tokenizer=tokenizer,
            top_k=args.top_k,
            vocab_norm_stats=vocab_stats,
        )

    # 7. Colinearidad entre posiciones (si K > 1)
    colinearity = None
    if K > 1:
        print(f"\n{'=' * 70}")
        print(f"COLINEARIDAD ENTRE POSICIONES DEL PARCHE")
        print(f"{'=' * 70}")
        Pn = patch / patch.norm(dim=1, keepdim=True).clamp(min=1e-12)
        cos_mat = (Pn @ Pn.T).tolist()  # [K, K]
        colinearity = cos_mat
        print(f"  Matriz de cosenos (filas/cols = posiciones 0..{K-1}):")
        for i, row in enumerate(cos_mat):
            print(f"    {i}: " + "  ".join(f"{v:+.4f}" for v in row))
        print(f"\n  Interpretacion:")
        off_diag = [cos_mat[i][j] for i in range(K) for j in range(K) if i != j]
        mean_off = sum(off_diag) / len(off_diag)
        print(f"    cos promedio fuera de la diagonal = {mean_off:+.4f}")
        if abs(mean_off) > 0.9:
            print(f"    -> Posiciones casi COLINEARES. El promedio es defendible;")
            print(f"       existe UNA sola direccion 'navidena'.")
        elif abs(mean_off) > 0.5:
            print(f"    -> Correlacion moderada. Hay una direccion dominante pero")
            print(f"       con estructura posicional no trivial.")
        else:
            print(f"    -> Posiciones casi ORTOGONALES. El promedio DESTRUYE")
            print(f"       informacion. Hay que reportar las K direcciones separadas.")

    # 8. Control: vector Gaussiano aleatorio con la misma norma que el parche
    print(f"\n{'=' * 70}")
    print(f"CONTROL: vector Gaussiano aleatorio (misma norma que patch[0])")
    print(f"{'=' * 70}")
    rand_vec = torch.randn(d_model)
    rand_vec = rand_vec * (patch[0].norm() / rand_vec.norm())
    control_result = analyze_vector(
        name="random_same_norm",
        vector=rand_vec,
        W=W,
        tokenizer=tokenizer,
        top_k=args.top_k,
        vocab_norm_stats=vocab_stats,
    )

    # 9. Guardar reporte JSON
    # Limpiar tensores del vocab_stats antes de serializar
    vocab_stats_serializable = {k: v for k, v in vocab_stats.items() if not k.startswith("_")}
    report = {
        "patch_path": args.patch,
        "model_path": args.model,
        "patch_shape": list(patch.shape),
        "vocab_size": V,
        "embed_dim": d_model,
        "vocab_norm_stats": vocab_stats_serializable,
        "per_position": per_position_results,
        "per_position_dimensions": per_position_dim_results,
        "averaged": avg_result,
        "position_colinearity_cos_matrix": colinearity,
        "control_random_same_norm": control_result,
    }
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nReporte guardado en: {args.out}")
    print(f"Para reportar en el chat, copiame las tablas de consola + el resumen de normas.")


if __name__ == "__main__":
    main()
