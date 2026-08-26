"""
Que hace el parche por dentro, capa por capa.

Tres medidas sobre el residual stream, todas leidas en la ULTIMA posicion del
prompt: la que genera el primer token de la respuesta. Medir en las posiciones
parcheadas es trivial (ahi el delta ES el parche); lo interesante es como se
propaga hasta el punto donde se decide el output.

  1. delta relativo   ||h_patch - h_clean|| / ||h_clean||  por capa.
     Normalizado, porque la norma del residual crece con la profundidad y sin
     normalizar cualquier perfil parece creciente.

  2. logit lens        p(primer token frances) vs p(primer token ingles),
     decodificando h_l con la LN final + lm_head. Da la CAPA donde se da vuelta
     la decision de idioma. Los tokens no se hardcodean: se toman del primer
     token de la referencia (frances) y del baseline (ingles) de cada prompt.

  3. alineacion con la direccion de la instruccion  <- la medida central
     d_l = mean(h[M([FR;q])]) - mean(h[M(q)])  sobre N prompts, o sea como
     representa el modelo "responde en frances" cuando se lo pedis en texto.
     Despues: cos(h_patch - h_clean, d_l).

     Alto en capas medias  -> el parche reconstruye la representacion de la
                              instruccion: misma via, distinto disparador.
     Bajo                  -> consigue el mismo comportamiento por otro camino,
                              y ahi la pregunta es cual.

Esto es lo que la distancia coseno en el vocabulario no podia contestar: alli se
compara contra la tabla de embeddings, aca contra una direccion definida por el
COMPORTAMIENTO.
"""

import argparse
import json

import numpy as np
import pandas as pd
import torch
import tqdm

from generate_targets import build_reference_prompt
from lm import (DEFAULT_MODEL, apply_patch_first_n, build_suffix_manager,
                get_embeddings, load_model_and_tokenizer)


@torch.no_grad()
def hidden_at_last(model, tokenizer, instruction, device, patch=None,
                   num_patch_positions=3):
    """hidden_states de todas las capas en la ultima posicion del prompt."""
    sm = build_suffix_manager(tokenizer, instruction, target="")
    tokens = sm.get_input_ids().to(device)
    embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()
    if patch is not None:
        embeds = apply_patch_first_n(sm, embeds, patch, num_patch_positions)
    embeds = embeds[:, : sm._assistant_role_slice.stop, :]
    out = model(inputs_embeds=embeds, output_hidden_states=True)
    # hidden_states: (L+1) tensores [1, seq, d]; [0] son los embeddings
    return torch.stack([h[0, -1, :].float() for h in out.hidden_states])  # [L+1, d]


@torch.no_grad()
def logit_lens(model, h_layers, tok_fr, tok_en):
    """p(tok_fr) y p(tok_en) decodificando cada capa con la LN final + lm_head."""
    norm, head = model.model.norm, model.lm_head
    hs = h_layers.to(next(head.parameters()).dtype)
    probs = torch.softmax(head(norm(hs)), dim=-1)      # [L+1, V]
    return probs[:, tok_fr].cpu().numpy(), probs[:, tok_en].cpu().numpy()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="targets_french.csv")
    ap.add_argument("--n", type=int, default=40, help="prompts a promediar")
    ap.add_argument("--instruction", default="Answer in French.")
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out", default="layer_analysis.json")
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False).head(args.n)
    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    patch = torch.load(args.patch, map_location=args.device).to(args.device)

    rel, deltas, pfr_c, pen_c, pfr_p, pen_p = [], [], [], [], [], []
    d_sum = None

    for _, row in tqdm.tqdm(df.iterrows(), total=len(df), desc="capas"):
        q = row["prompt"]
        h_clean = hidden_at_last(model, tokenizer, q, args.device)
        h_patch = hidden_at_last(model, tokenizer, q, args.device, patch,
                                 args.num_patch_positions)
        h_instr = hidden_at_last(
            model, tokenizer, build_reference_prompt(args.instruction, q), args.device)

        delta_patch = h_patch - h_clean            # [L+1, d]
        delta_instr = h_instr - h_clean
        d_sum = delta_instr if d_sum is None else d_sum + delta_instr

        rel.append((delta_patch.norm(dim=1) / h_clean.norm(dim=1).clamp(min=1e-6)).cpu().numpy())
        deltas.append(delta_patch.cpu())   # cacheado: el coseno necesita d_mean, que sale al final

        # primer token de la referencia (FR) y del baseline (EN) de ESTE prompt
        f_ids = tokenizer.encode(row["output"][:20], add_special_tokens=False)
        e_ids = tokenizer.encode(row["baseline_en"][:20], add_special_tokens=False)
        if not f_ids or not e_ids:
            continue
        a, b = logit_lens(model, h_clean, f_ids[0], e_ids[0])
        c, e = logit_lens(model, h_patch, f_ids[0], e_ids[0])
        pfr_c.append(a); pen_c.append(b); pfr_p.append(c); pen_p.append(e)

    rel = np.stack(rel).mean(0)
    # Direccion de la instruccion: diff-in-means sobre los N prompts.
    d_mean = (d_sum / len(df)).cpu()
    cos = np.stack([
        torch.nn.functional.cosine_similarity(dp, d_mean, dim=1).numpy()
        for dp in deltas
    ]).mean(0)
    pfr_c, pen_c = np.stack(pfr_c).mean(0), np.stack(pen_c).mean(0)
    pfr_p, pen_p = np.stack(pfr_p).mean(0), np.stack(pen_p).mean(0)

    L = len(rel)
    print(f"\n{'capa':>5}{'||d||/||h||':>13}{'cos(d_parche, d_instr)':>25}"
          f"{'p(FR) limpio':>14}{'p(FR) parche':>14}{'p(EN) parche':>14}")
    print("-" * 86)
    for i in range(L):
        print(f"{i:>5}{rel[i]:>13.4f}{cos[i]:>25.4f}"
              f"{pfr_c[i]:>14.4f}{pfr_p[i]:>14.4f}{pen_p[i]:>14.4f}")

    cross = [i for i in range(L) if pfr_p[i] > pen_p[i]]
    print(f"\ncapa donde p(FR) supera a p(EN) con parche: "
          f"{cross[0] if cross else 'nunca'}")
    print(f"capa de maxima alineacion con la instruccion: {int(cos.argmax())} "
          f"(cos={cos.max():.3f})")

    json.dump({"rel_delta": rel.tolist(), "cos_with_instruction": cos.tolist(),
               "p_fr_clean": pfr_c.tolist(), "p_fr_patched": pfr_p.tolist(),
               "p_en_patched": pen_p.tolist(), "n_prompts": len(df),
               "patch": args.patch},
              open(args.out, "w"), indent=2)
    print(f"\nGuardado en {args.out}")


if __name__ == "__main__":
    main()
