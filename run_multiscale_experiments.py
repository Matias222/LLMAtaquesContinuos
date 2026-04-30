"""
run_multiscale_experiments.py
=============================

Sweep nocturno de multi-scale training + data augmentation, 4 runs.

Test directo de H2 (el patch quinto se comporta como una "llave calibrada", no
como una direccion escalable). Para cada patch entrenado, evaluamos a varios
scales en test-time para mapear la curva Christmas-rate vs alpha.

EXPERIMENTOS

1. noprefix_aug_l2_0.1
   - alphas = [1.0]  (single-scale, control)
   - L2 = 0.1, K = 3, CSV augmented
   - Aisla el efecto de data augmentation del de multi-scale.

2. multiscale_narrow_l2_0.1
   - alphas = [0.7, 1.0, 1.3]
   - L2 = 0.1, K = 3, CSV augmented
   - El test central de H2.

3. multiscale_wide_l2_0.1
   - alphas = [0.5, 1.0, 1.5]
   - L2 = 0.1, K = 3, CSV augmented
   - Misma idea pero ventana mas ancha.

4. multiscale_narrow_l2_0.045
   - alphas = [0.7, 1.0, 1.3]
   - L2 = 0.045, K = 3, CSV augmented
   - Combina multi-scale con menos regularizacion.

EVALUACION POR PATCH (4 scales)
   --scale_remaining ∈ {0.5, 1.0, 1.5, 2.0}
   1 inspect JSON + 4 test JSONs por carpeta.

Uso:
   python run_multiscale_experiments.py                # corre los 4
   python run_multiscale_experiments.py --only 2,3     # solo runs 2 y 3
   python run_multiscale_experiments.py --dry_run      # imprime sin ejecutar
"""

import argparse
import os
import subprocess
import sys
import time

# Import directo del training multi-scale
from christmas_multiscale_train import train_christmas_patch


REPO = "/home/sagemaker-user/user-default-efs/papers/LLMAtaquesContinuos"
MODEL_PATH = "/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct"
CSV_PATH = os.path.join(REPO, "christmas_training_augmented.csv")

# Heldout split = 20 / 150 = 0.13333
HELDOUT_FRAC = 20.0 / 150.0
TRAIN_SPLIT = 1.0 - HELDOUT_FRAC

# Test-time scales para mapear la curva Christmas-rate(alpha)
TEST_SCALES = [0.5, 1.0, 1.5, 2.0]

# Setup compartido a todos los runs
DEFAULTS = dict(
    num_epochs=5,
    num_steps_per_prompt=75,
    device="cuda:0",
    num_patch_positions=3,
    prefix_match_length=0,         # noprefix en todos
    coherence_weight=0.5,          # subido vs 0.21 noprefix anterior
    step_size=0.00025,
    train_test_split=TRAIN_SPLIT,
    prepend_target_prefix=False,
    bot_penalty_weight=0.0,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg):
    print(f"\n{'='*78}\n[{time.strftime('%H:%M:%S')}] {msg}\n{'='*78}", flush=True)


def run_inspect(patch_path, out_dir, dry=False):
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


def run_test_at_scale(patch_path, out_dir, scale, dry=False):
    """Corre test_xmas_patch.py con --scale_remaining=<scale>. Output JSON+MD
    nombrados con el scale para no pisar."""
    tag = f"scale{scale}"
    out_json = os.path.join(out_dir, f"test_xmas_final_report_{tag}.json")
    out_md = os.path.join(out_dir, f"test_xmas_final_report_{tag}.md")
    cmd = [
        sys.executable, "test_xmas_patch.py",
        "--patch", patch_path,
        "--model", MODEL_PATH,
        "--csv", CSV_PATH,
        "--heldout_frac", f"{HELDOUT_FRAC:.6f}",
        "--scale_remaining", str(scale),
        "--out_json", out_json,
        "--out_md", out_md,
    ]
    log(f"TEST [{tag}]: {patch_path}")
    print("  cmd:", " ".join(cmd))
    if dry:
        return
    subprocess.run(cmd, check=True, cwd=REPO)


def run_training_and_eval(output_dir, train_kwargs, dry=False):
    """Train + inspect + sweep de tests a multiples scales."""
    os.makedirs(output_dir, exist_ok=True)
    log(f"TRAINING → {output_dir}")
    print(f"  kwargs: {train_kwargs}")
    if dry:
        # Dry run igual ejecuta los logs de tests/inspect que correrian
        patch_path = os.path.join(output_dir, "christmas_final_patch_lowc.pt")
        run_inspect(patch_path, output_dir, dry=True)
        for scale in TEST_SCALES:
            run_test_at_scale(patch_path, output_dir, scale, dry=True)
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
        print(f"[ERROR] patch no se genero en {patch_path}; skip eval")
        return

    try:
        run_inspect(patch_path, output_dir, dry=False)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] inspect failed: {e}")

    for scale in TEST_SCALES:
        try:
            run_test_at_scale(patch_path, output_dir, scale, dry=False)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] test at scale={scale} failed: {e}; continuo con resto")


# ---------------------------------------------------------------------------
# Run definitions
# ---------------------------------------------------------------------------

def run1(dry=False):
    log("RUN 1 — noprefix_aug_l2_0.1  (control, single-scale + augmented CSV)")
    out_dir = os.path.join(REPO, "resultados", "noprefix_aug_l2_0.1")
    train_kwargs = dict(DEFAULTS)
    train_kwargs.update({
        "l2_weight": 0.125,
        "alphas": [1.0],
    })
    run_training_and_eval(out_dir, train_kwargs, dry=dry)


def run2(dry=False):
    log("RUN 2 — multiscale_narrow_l2_0.1  (alphas=[0.7,1.0,1.3], L2=0.1)")
    out_dir = os.path.join(REPO, "resultados", "multiscale_narrow_l2_0.1")
    train_kwargs = dict(DEFAULTS)
    train_kwargs.update({
        "l2_weight": 0.125,
        "alphas": [0.7, 1.0, 1.3],
    })
    run_training_and_eval(out_dir, train_kwargs, dry=dry)


def run3(dry=False):
    log("RUN 3 — multiscale_wide_l2_0.1  (alphas=[0.5,1.0,1.5], L2=0.1)")
    out_dir = os.path.join(REPO, "resultados", "multiscale_wide_l2_0.1")
    train_kwargs = dict(DEFAULTS)
    train_kwargs.update({
        "l2_weight": 0.125,
        "alphas": [0.5, 1.0, 1.5],
    })
    run_training_and_eval(out_dir, train_kwargs, dry=dry)


def run4(dry=False):
    log("RUN 4 — multiscale_narrow_l2_0.045  (alphas=[0.7,1.0,1.3], L2=0.045)")
    out_dir = os.path.join(REPO, "resultados", "multiscale_narrow_l2_0.045")
    train_kwargs = dict(DEFAULTS)
    train_kwargs.update({
        "l2_weight": 0.045,
        "alphas": [0.7, 1.0, 1.3],
    })
    run_training_and_eval(out_dir, train_kwargs, dry=dry)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--only", default="1,2,3,4",
                        help="Cuales runs correr. Ejemplos: '1', '2,3', '1,4'. Default: '1,2,3,4'.")
    parser.add_argument("--dry_run", action="store_true",
                        help="No ejecuta nada, solo imprime los comandos que correria.")
    args = parser.parse_args()

    selected = {s.strip() for s in args.only.split(",") if s.strip()}
    dry = args.dry_run

    runs_map = {"1": run1, "2": run2, "3": run3, "4": run4}

    log(f"START. Selected: {sorted(selected)}  dry_run={dry}")
    print(f"  REPO:        {REPO}")
    print(f"  CSV:         {CSV_PATH}")
    print(f"  MODEL:       {MODEL_PATH}")
    print(f"  HELDOUT_FRAC:{HELDOUT_FRAC:.6f}  (= 20/150)")
    print(f"  TEST_SCALES: {TEST_SCALES}")

    t0 = time.time()
    for k in sorted(selected):
        if k in runs_map:
            runs_map[k](dry=dry)
        else:
            print(f"[WARN] run id '{k}' desconocido, skip")

    elapsed = time.time() - t0
    log(f"DONE. Tiempo total: {elapsed/60:.1f} min  (runs: {sorted(selected)})")


if __name__ == "__main__":
    main()
