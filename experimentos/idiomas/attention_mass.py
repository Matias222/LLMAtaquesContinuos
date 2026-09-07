"""
Experimento 2 de mecanismo: cuanta atencion reciben las posiciones parcheadas.

Descriptivo, no causal. Complementa a mask_patch_attention.py: aquel dice si los
tokens generados NECESITAN leer el parche; este dice CUANTO lo leen, en que
capas y en que cabezas, y si el parche ademas ATRAE atencion o solo cambia lo
que se lee cuando se lo mira.

---------------------------------------------------------------------------
LAS CUATRO SECUENCIAS POR PROMPT
---------------------------------------------------------------------------
    patched_gen   prompt parcheado  + lo que el parche genero (greedy)
    patched_ref   prompt parcheado  + la referencia francesa (teacher forcing)
    clean_ref     prompt limpio     + la referencia francesa
    clean_base    prompt limpio     + el baseline ingles

La comparacion limpia es patched_ref vs clean_ref: MISMA continuacion, solo
cambia el parche. Cualquier diferencia de atencion hacia las posiciones 1-3 es
efecto del parche y no del texto que sigue. patched_gen es lo que pasa de
verdad; clean_base es el piso.

---------------------------------------------------------------------------
QUE SE MIDE
---------------------------------------------------------------------------
Un forward con output_attentions=True (attn_implementation='eager', que es la
unica que devuelve los pesos) y, para las queries de la CONTINUACION
(posiciones >= largo del prompt), la masa de atencion sumada sobre cada region
de keys:

    parche               las posiciones parcheadas
    bos                  la posicion 0, el attention sink clasico
    resto_pregunta       el goal sin las posiciones parcheadas
    sistema_y_headers    todo lo demas del prompt
    generados            la continuacion misma

promediada sobre cabezas y sobre queries -> un vector por capa. Ademas:

    parche_por_cabeza    [L, H] sin promediar cabezas, para encontrar las
                         cabezas que leen el parche
    primer_token         la misma masa pero para la UNICA query del ultimo
                         token del prompt, que decide el primer token

Si el parche funciona como contexto persistente, patched_ref tiene que mostrar
mas masa hacia 'parche' que clean_ref en las capas donde mask_patch_attention
encuentre el bloqueo efectivo. Si la masa es igual y solo cambia el contenido
leido, el mecanismo es 'misma atencion, otros valores', que tambien es una
respuesta.

    python3 -u attention_mass.py --model $M \\
        --patch runs/v4_250/lang_patch_best_train.pt --out_json runs/mask_v4/attention_mass.json
"""

import argparse
import json
import os

import pandas as pd
import torch
import tqdm

from attn_utils import patched_positions
from lm import (DEFAULT_MODEL, apply_patch_first_n, build_suffix_manager, generate,
                get_embedding_matrix, get_embeddings, load_model_and_tokenizer,
                stop_token_ids)

REGIONES = ("parche", "bos", "resto_pregunta", "sistema_y_headers", "generados")
CONDS = ("patched_gen", "patched_ref", "clean_ref", "clean_base")


def regiones(sm, prompt_len, blocked, S):
    goal = set(range(sm._goal_slice.start, sm._goal_slice.stop))
    bl = set(blocked)
    return {
        "parche": sorted(bl),
        "bos": [0],
        "resto_pregunta": sorted(goal - bl),
        "sistema_y_headers": [j for j in range(1, prompt_len) if j not in goal],
        "generados": list(range(prompt_len, S)),
    }


def masa(A, queries, keys):
    """A [L, H, S, S] -> [L, H]: media sobre queries de la suma sobre keys."""
    if not queries or not keys:
        return torch.zeros(A.shape[0], A.shape[1])
    q = torch.tensor(queries, dtype=torch.long, device=A.device)
    k = torch.tensor(keys, dtype=torch.long, device=A.device)
    sub = A.index_select(2, q).index_select(3, k)          # [L, H, q, k]
    return sub.sum(-1).mean(-1).cpu()


@torch.no_grad()
def atenciones(model, embeds):
    out = model(inputs_embeds=embeds, output_attentions=True, use_cache=False)
    return torch.stack([a[0].float() for a in out.attentions])   # [L, H, S, S]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", default="runs/v4_250/lang_patch_best_train.pt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--patch_offset", type=int, default=0)
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--n", type=int, default=0, help="limitar filas (0 = todo el held-out)")
    ap.add_argument("--top_heads", type=int, default=15)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_json", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    heldout = df.iloc[int(len(df) * args.train_test_split):]
    if args.n > 0:
        heldout = heldout.head(args.n)

    # eager: la unica implementacion que devuelve los pesos de atencion.
    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device,
                                                attn_implementation="eager")
    patch = torch.load(args.patch, map_location=args.device).to(args.device)
    emb_matrix = get_embedding_matrix(model)
    stop = stop_token_ids(tokenizer)
    L, H = len(model.model.layers), model.config.num_attention_heads
    print(f"parche {args.patch}  norma {patch.norm(2).item():.4f}  |  held-out {len(heldout)}  |  L={L} H={H}")

    acc = {c: {"gen": {r: torch.zeros(L) for r in REGIONES},
               "primer_token": {r: torch.zeros(L) for r in REGIONES},
               "parche_por_cabeza": torch.zeros(L, H),
               "n": 0} for c in CONDS}
    ejemplos = []

    def ids(text):
        return tokenizer(str(text), add_special_tokens=False).input_ids

    for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc="atencion"):
        sm = build_suffix_manager(tokenizer, r["prompt"], target="")
        tokens = sm.get_input_ids().to(args.device)
        emb = get_embeddings(model, tokens.unsqueeze(0)).detach()
        clean = emb[:, : sm._assistant_role_slice.stop, :]
        patched = apply_patch_first_n(sm, emb, patch, args.num_patch_positions,
                                      offset=args.patch_offset)[:, : sm._assistant_role_slice.stop, :]
        prompt_len = clean.shape[1]
        blocked = patched_positions(sm, args.num_patch_positions, args.patch_offset)

        gen_ids = generate(model, patched, args.num_tokens, 0.0, stop)
        gen_txt = tokenizer.decode(gen_ids, skip_special_tokens=True)
        conts = {"patched_gen": (patched, list(int(t) for t in gen_ids)),
                 "patched_ref": (patched, ids(r["output"])),
                 "clean_ref": (clean, ids(r["output"])),
                 "clean_base": (clean, ids(r["baseline_en"]))}
        ejemplo = {"idx": int(i), "prompt": r["prompt"], "generado": gen_txt,
                   "posiciones_parcheadas": blocked, "prompt_len": prompt_len}

        for cond, (pe, cont) in conts.items():
            if not cont:
                continue
            ct = torch.tensor(cont, dtype=torch.long, device=args.device)
            full = torch.cat([pe, emb_matrix[ct][None, :, :].to(pe.dtype)], dim=1)
            A = atenciones(model, full)
            S = full.shape[1]
            reg = regiones(sm, prompt_len, blocked, S)
            gen_q = reg["generados"]
            first_q = [prompt_len - 1]
            for rname in REGIONES:
                acc[cond]["gen"][rname] += masa(A, gen_q, reg[rname]).mean(-1)
                acc[cond]["primer_token"][rname] += masa(A, first_q, reg[rname]).mean(-1)
            acc[cond]["parche_por_cabeza"] += masa(A, gen_q, reg["parche"])
            acc[cond]["n"] += 1
            ejemplo[f"{cond}_masa_parche_gen_por_capa"] = [round(x, 4) for x in
                                                          masa(A, gen_q, reg["parche"]).mean(-1).tolist()]
            del A
        ejemplos.append(ejemplo)

    # --- promedios --------------------------------------------------------
    res = {}
    for cond in CONDS:
        n = max(1, acc[cond]["n"])
        res[cond] = {
            "n": acc[cond]["n"],
            "masa_generados": {r: (acc[cond]["gen"][r] / n).tolist() for r in REGIONES},
            "masa_primer_token": {r: (acc[cond]["primer_token"][r] / n).tolist() for r in REGIONES},
            "parche_por_cabeza": (acc[cond]["parche_por_cabeza"] / n).tolist(),
        }

    dif = (acc["patched_ref"]["parche_por_cabeza"] / max(1, acc["patched_ref"]["n"])
           - acc["clean_ref"]["parche_por_cabeza"] / max(1, acc["clean_ref"]["n"]))
    flat = dif.flatten()
    top = torch.topk(flat, k=min(args.top_heads, flat.numel()))
    top_heads = [{"capa": int(ix // H) + 1, "cabeza": int(ix % H), "delta_masa": float(v),
                  "masa_patched_ref": float(acc["patched_ref"]["parche_por_cabeza"].flatten()[ix]
                                            / max(1, acc["patched_ref"]["n"])),
                  "masa_clean_ref": float(acc["clean_ref"]["parche_por_cabeza"].flatten()[ix]
                                          / max(1, acc["clean_ref"]["n"]))}
                 for v, ix in zip(top.values.tolist(), top.indices.tolist())]

    print("\n" + "=" * 96)
    print("MASA DE ATENCION DESDE LA CONTINUACION HACIA LAS POSICIONES PARCHEADAS (media sobre cabezas)")
    print(f"{'capa':>5}{'patched_gen':>13}{'patched_ref':>13}{'clean_ref':>12}{'clean_base':>12}"
          f"{'| bos p_ref':>12}{'bos c_ref':>11}")
    for l in range(L):
        print(f"{l + 1:>5}"
              f"{res['patched_gen']['masa_generados']['parche'][l]:>13.4f}"
              f"{res['patched_ref']['masa_generados']['parche'][l]:>13.4f}"
              f"{res['clean_ref']['masa_generados']['parche'][l]:>12.4f}"
              f"{res['clean_base']['masa_generados']['parche'][l]:>12.4f}"
              f"{res['patched_ref']['masa_generados']['bos'][l]:>12.4f}"
              f"{res['clean_ref']['masa_generados']['bos'][l]:>11.4f}")
    print("\nCabezas con mayor aumento de masa hacia el parche (patched_ref - clean_ref):")
    for h in top_heads:
        print(f"  L{h['capa']:>2} H{h['cabeza']:>2}   +{h['delta_masa']:.4f}   "
              f"({h['masa_clean_ref']:.4f} -> {h['masa_patched_ref']:.4f})")
    print("=" * 96)
    print("Lectura: patched_ref vs clean_ref es la comparacion limpia (misma continuacion).")
    print("Si la masa hacia 'parche' sube, el parche ATRAE atencion; si no sube pero el bloqueo")
    print("(mask_patch_attention) igual rompe el frances, lo que cambia es el CONTENIDO leido.")

    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump({"objetivo": "masa de atencion hacia las posiciones parcheadas",
                   "patch": os.path.abspath(args.patch), "patch_norm": patch.norm(2).item(),
                   "config": vars(args), "L": L, "H": H, "regiones": list(REGIONES),
                   "por_condicion": res, "top_heads_patched_ref_menos_clean_ref": top_heads,
                   "ejemplos": ejemplos}, f, indent=2, ensure_ascii=False)
    print(f"\nGuardado: {args.out_json}")


if __name__ == "__main__":
    main()
