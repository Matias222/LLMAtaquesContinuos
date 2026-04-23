"""
run_experiments.py
==================

Orquesta 3 experimentos sobre el pipeline de Christmas steering:

EXPERIMENTO 1 — Training SIN prefix, barrido de L2
  - Script: christmas_final_train.py (posicional [1, 3, d])
  - prefix_match_length=0, coherence_weight=1.0, prepend_target_prefix=False
  - L2 ∈ {0.045, 0.08, 0.1}
  - 3 runs → 3 patches, cada uno con inspect + test

EXPERIMENTO 2 — Training CON prefix + penalizacion <|begin_of_text|>
  - Script: christmas_final_train.py
  - Setup normal + bot_penalty_weight=1.0, l2_weight=0.1
  - 1 run → 1 patch, con inspect + test

EXPERIMENTO 3 — Matriz ablacion posicional sobre quinto_run_0.1
  - Script: test_xmas_patch.py con flags --zero_positions y --scale_remaining
  - 7 configs x 3 scales = 21 runs (solo evaluacion, sin training)

Uso:
  python run_experiments.py                # corre los 3 experimentos
  python run_experiments.py --only 1       # solo experimento 1
  python run_experiments.py --only 1,3     # experimentos 1 y 3
  python run_experiments.py --dry_run      # imprime lo que correria sin ejecutar
"""

import argparse
import os
import subprocess
import sys
import time

# Import directo del training
from christmas_final_train import train_christmas_patch


REPO = "/home/sagemaker-user/user-default-efs/papers/LLMAtaquesContinuos"
MODEL_PATH = "/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct"
CSV_PATH = os.path.join(REPO, "christmas_training.csv")

# Defaults compartidos con el __main__ actual
DEFAULTS = dict(
    num_epochs=5,
    num_steps_per_prompt=75,
    device="cuda:0",
    num_patch_positions=3,
    prefix_match_length=4,
    coherence_weight=0.21,
    step_size=0.00025,
    train_test_split=0.8,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg):
    print(f"\n{'='*78}\n[{time.strftime('%H:%M:%S')}] {msg}\n{'='*78}", flush=True)


def run_inspect(patch_path, out_dir, dry=False):
    """Corre inspect_xmas_patch.py sobre un patch y guarda el JSON en out_dir."""
    out_json = os.path.join(out_dir, "inspect_xmas_final_report.json")
    cmd = [
        sys.executable, "inspect_xmas_patch.py",
        "--patch", patch_path,
        "--model", MODEL_PATH,
        "--out", out_json,
    ]
    log(f"INSPECT: {patch_path}")
    print("  cmd:", " ".join(cmd))
    if dry:
        return
    subprocess.run(cmd, check=True, cwd=REPO)


def run_test(patch_path, out_dir, dry=False, extra_args=None):
    """Corre test_xmas_patch.py sobre un patch y guarda los reportes en out_dir."""
    out_json = os.path.join(out_dir, "test_xmas_final_report.json")
    out_md = os.path.join(out_dir, "test_xmas_final_report.md")
    cmd = [
        sys.executable, "test_xmas_patch.py",
        "--patch", patch_path,
        "--model", MODEL_PATH,
        "--out_json", out_json,
        "--out_md", out_md,
    ]
    if extra_args:
        cmd.extend(extra_args)
    log(f"TEST: {patch_path}")
    print("  cmd:", " ".join(cmd))
    if dry:
        return
    subprocess.run(cmd, check=True, cwd=REPO)


def run_training_and_eval(output_dir, train_kwargs, dry=False):
    """Corre training, guarda patch en output_dir, y ejecuta inspect + test.
    Si cualquier paso falla, loggea y continua (no aborta los siguientes runs)."""
    os.makedirs(output_dir, exist_ok=True)
    log(f"TRAINING → {output_dir}")
    print(f"  kwargs: {train_kwargs}")
    if dry:
        return
    try:
        train_christmas_patch(
            model_path=MODEL_PATH,
            csv_path=CSV_PATH,
            output_dir=output_dir,
            **train_kwargs,
        )
    except Exception as e:
        print(f"[ERROR] training failed for {output_dir}: {e}")
        return

    patch_path = os.path.join(output_dir, "christmas_final_patch_lowc.pt")
    if not os.path.exists(patch_path):
        print(f"[ERROR] patch no se genero en {patch_path}; skip inspect/test")
        return

    try:
        run_inspect(patch_path, output_dir, dry=dry)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] inspect failed: {e}")
    try:
        run_test(patch_path, output_dir, dry=dry)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] test failed: {e}")


# ---------------------------------------------------------------------------
# Experimento 1: training sin prefix, variar L2
# ---------------------------------------------------------------------------

def exp1(dry=False):
    log("EXPERIMENTO 1 — Training SIN prefix, barrido de L2")
    l2_values = [0.045, 0.08, 0.1]
    for l2 in l2_values:
        out_dir = os.path.join(REPO, "resultados", f"noprefix_l2_{l2}")
        # dict(DEFAULTS) + update para evitar TypeError por duplicate keys
        train_kwargs = dict(DEFAULTS)
        train_kwargs.update({
            "l2_weight": l2,
            "coherence_weight": 1.0,         # override del default 0.21
            "prefix_match_length": 0,        # override del default 4
            "bot_penalty_weight": 0.0,
            "prepend_target_prefix": False,  # target = CSV output directo
        })
        run_training_and_eval(out_dir, train_kwargs, dry=dry)


# ---------------------------------------------------------------------------
# Experimento 2: training normal + bot penalty
# ---------------------------------------------------------------------------

def exp2(dry=False):
    log("EXPERIMENTO 2 — Training CON prefix + bot penalty")
    out_dir = os.path.join(REPO, "resultados", "botpenalty_l2_0.1")
    train_kwargs = dict(DEFAULTS)
    train_kwargs.update({
        "l2_weight": 0.1,
        "bot_penalty_weight": 1.0,
        "prepend_target_prefix": True,
        # prefix_match_length=4 y coherence_weight=0.21 vienen de DEFAULTS
    })
    run_training_and_eval(out_dir, train_kwargs, dry=dry)


# ---------------------------------------------------------------------------
# Experimento 3: matriz ablacion posicional de quinto_run_0.1
# ---------------------------------------------------------------------------

def exp3(dry=False):
    log("EXPERIMENTO 3 — Matriz ablacion posicional (quinto_run_0.1)")
    base_patch = os.path.join(REPO, "resultados", "quinto_run_0.1", "christmas_final_patch_lowc.pt")
    if not os.path.exists(base_patch):
        print(f"[ERROR] patch base no existe: {base_patch}; skip exp3")
        return
    out_root = os.path.join(REPO, "resultados", "ablation_quinto")
    os.makedirs(out_root, exist_ok=True)

    # 7 configuraciones de ablacion: (label, zero_positions_str)
    configs = [
        ("full",         ""),       # ninguna ablacion
        ("only_pos0",    "1,2"),    # solo pos 0 activa
        ("only_pos1",    "0,2"),    # solo pos 1 activa
        ("only_pos2",    "0,1"),    # solo pos 2 activa
        ("excl_pos0",    "0"),      # pos 0 excluida, quedan 1,2
        ("excl_pos1",    "1"),      # pos 1 excluida, quedan 0,2
        ("excl_pos2",    "2"),      # pos 2 excluida, quedan 0,1
    ]
    scales = [1.0, 1.75, 2.5]

    for (label, zero_str) in configs:
        for scale in scales:
            tag = f"{label}_scale{scale}"
            out_json = os.path.join(out_root, f"{tag}.json")
            out_md = os.path.join(out_root, f"{tag}.md")
            extra = [
                "--out_json", out_json,
                "--out_md", out_md,
                "--scale_remaining", str(scale),
            ]
            if zero_str:
                extra.extend(["--zero_positions", zero_str])
            cmd = [
                sys.executable, "test_xmas_patch.py",
                "--patch", base_patch,
                "--model", MODEL_PATH,
            ] + extra
            log(f"EXP3 [{tag}]")
            print("  cmd:", " ".join(cmd))
            if dry:
                continue
            try:
                subprocess.run(cmd, check=True, cwd=REPO)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] exp3 {tag} failed: {e} — skip y continuo")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", default="1,2,3",
                        help="Cuales experimentos correr. Ejemplos: '1', '1,2', '3'. Default: '1,2,3'.")
    parser.add_argument("--dry_run", action="store_true",
                        help="No ejecuta nada, solo imprime los comandos que correria.")
    args = parser.parse_args()

    selected = {s.strip() for s in args.only.split(",") if s.strip()}
    dry = args.dry_run

    t0 = time.time()
    if "1" in selected:
        exp1(dry=dry)
    if "2" in selected:
        exp2(dry=dry)
    if "3" in selected:
        exp3(dry=dry)

    elapsed = time.time() - t0
    log(f"DONE. Tiempo total: {elapsed/60:.1f} min  (experimentos: {sorted(selected)})")


if __name__ == "__main__":
    main()
