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

  3. alineacion con DOS direcciones de referencia   <- la medida central

     Hay dos maneras distintas de que el modelo termine hablando frances, y son
     estados internos distintos:

       d_instr = mean(h[M(["Answer in French." + q])]) - mean(h[M(q)])
           el modelo parsea una directiva meta y la cumple.

       d_frq   = mean(h[M(q_fr)]) - mean(h[M(q)])
           el modelo EMPAREJA el idioma de la entrada. Sin instruccion de por
           medio; es el mecanismo mas basico.

     El parche no tiene semantica de instruccion: es un vector sumado a los 3
     primeros tokens de la pregunta. A priori es mas plausible que empuje esos
     tokens hacia territorio frances, o sea que haga (d_frq) y no (d_instr).

     Se reportan cos(delta_parche, d_instr), cos(delta_parche, d_frq) y tambien
     cos(d_instr, d_frq): si las dos referencias ya son casi iguales, la
     distincion no informa nada y hay que decirlo.

     Los cosenos se calculan con VALIDACION CRUZADA: la direccion se estima en
     una mitad de los prompts y el coseno se mide en la otra. Sin eso, cada
     prompt contribuye a su propia referencia y el coseno sale inflado.

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


def crossfit_cos(deltas_patch, deltas_ref):
    """
    cos(delta_parche, d_ref) con validacion cruzada por mitades.

    d_ref se estima en una mitad de los prompts y el coseno se mide en la otra,
    y viceversa. Sin esto cada prompt aporta a la direccion contra la que se
    compara y el coseno sale inflado.
    """
    n = len(deltas_patch)
    if n < 4:
        return None
    mitad = n // 2
    partes = [(list(range(mitad)), list(range(mitad, n))),
              (list(range(mitad, n)), list(range(mitad)))]
    vals = []
    for est, med in partes:
        d = torch.stack([deltas_ref[i] for i in est]).mean(0)
        for i in med:
            vals.append(torch.nn.functional.cosine_similarity(
                deltas_patch[i], d, dim=1).numpy())
    return np.stack(vals).mean(0)


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
    tiene_fr = "prompt_fr" in df.columns
    if not tiene_fr:
        print("AVISO: el CSV no tiene columna prompt_fr; solo se mide contra la")
        print("       instruccion en texto. Corre translate_questions.py primero.")

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    patch = torch.load(args.patch, map_location=args.device).to(args.device)

    rel, d_patch, d_instr, d_frq = [], [], [], []
    pfr_c, pen_c, pfr_p, pen_p = [], [], [], []
    idx_frq = []
    # Diagnostico de anisotropia: cosenos CRUDOS, sin restar la linea de base.
    # Si h_patch~h_frq y h_clean~h_frq dan los dos ~0.97, queda demostrado por
    # que hay que trabajar con diferencias y no con estados absolutos.
    raw_pf, raw_cf = [], []

    for k, (_, row) in enumerate(tqdm.tqdm(df.iterrows(), total=len(df), desc="capas")):
        q = row["prompt"]
        h_clean = hidden_at_last(model, tokenizer, q, args.device)
        h_patch = hidden_at_last(model, tokenizer, q, args.device, patch,
                                 args.num_patch_positions)
        h_instr = hidden_at_last(
            model, tokenizer, build_reference_prompt(args.instruction, q), args.device)

        d_patch.append((h_patch - h_clean).cpu())
        d_instr.append((h_instr - h_clean).cpu())
        rel.append((d_patch[-1].norm(dim=1)
                    / h_clean.norm(dim=1).cpu().clamp(min=1e-6)).numpy())

        # (B) la misma pregunta, en frances
        if tiene_fr and str(row.get("prompt_fr_language", "fr")) == "fr" \
                and str(row["prompt_fr"]).strip():
            h_frq = hidden_at_last(model, tokenizer, row["prompt_fr"], args.device)
            d_frq.append((h_frq - h_clean).cpu())
            idx_frq.append(k)
            cs = torch.nn.functional.cosine_similarity
            raw_pf.append(cs(h_patch, h_frq, dim=1).cpu().numpy())
            raw_cf.append(cs(h_clean, h_frq, dim=1).cpu().numpy())

        f_ids = tokenizer.encode(row["output"][:20], add_special_tokens=False)
        e_ids = tokenizer.encode(row["baseline_en"][:20], add_special_tokens=False)
        if not f_ids or not e_ids:
            continue
        a, b = logit_lens(model, h_clean, f_ids[0], e_ids[0])
        c, e = logit_lens(model, h_patch, f_ids[0], e_ids[0])
        pfr_c.append(a); pen_c.append(b); pfr_p.append(c); pen_p.append(e)

    rel = np.stack(rel).mean(0)
    cos_instr = crossfit_cos(d_patch, d_instr)
    cos_frq = (crossfit_cos([d_patch[i] for i in idx_frq], d_frq)
               if len(d_frq) >= 4 else None)

    # Cuanto se parecen entre si las DOS referencias. Si es alto, la distincion
    # no informa; si es bajo, saber a cual se parece el parche si informa.
    if len(d_frq) >= 4:
        Di = torch.stack([d_instr[i] for i in idx_frq]).mean(0)
        Df = torch.stack(d_frq).mean(0)
        cos_refs = torch.nn.functional.cosine_similarity(Di, Df, dim=1).numpy()
    else:
        cos_refs = None

    pfr_c, pen_c = np.stack(pfr_c).mean(0), np.stack(pen_c).mean(0)
    pfr_p, pen_p = np.stack(pfr_p).mean(0), np.stack(pen_p).mean(0)
    raw_pf = np.stack(raw_pf).mean(0) if raw_pf else None
    raw_cf = np.stack(raw_cf).mean(0) if raw_cf else None

    L = len(rel)
    print(f"\n{'capa':>5}{'|d|/|h|':>10}{'cos vs instr':>14}{'cos vs q_fr':>13}"
          f"{'cos instr~q_fr':>16}{'p(FR) limpio':>14}{'p(FR) parche':>14}{'p(EN) parche':>14}")
    print("-" * 100)
    for i in range(L):
        ci = f"{cos_instr[i]:.4f}" if cos_instr is not None else "-"
        cf = f"{cos_frq[i]:.4f}" if cos_frq is not None else "-"
        cr = f"{cos_refs[i]:.4f}" if cos_refs is not None else "-"
        print(f"{i:>5}{rel[i]:>10.4f}{ci:>14}{cf:>13}{cr:>16}"
              f"{pfr_c[i]:>14.4f}{pfr_p[i]:>14.4f}{pen_p[i]:>14.4f}")

    if raw_pf is not None:
        print(f"\n{'capa':>5}{'cos(h_patch, h_frq)':>22}{'cos(h_clean, h_frq)':>22}"
              f"{'separacion':>13}")
        print("-" * 62)
        for i in range(L):
            print(f"{i:>5}{raw_pf[i]:>22.4f}{raw_cf[i]:>22.4f}"
                  f"{raw_pf[i] - raw_cf[i]:>+13.4f}")
        print("  Cosenos CRUDOS, sin restar la linea de base. Si las dos columnas")
        print("  estan las dos cerca de 1 y la separacion es ~0, eso ES la")
        print("  anisotropia del residual stream: el estado absoluto no discrimina")
        print("  y hay que trabajar con diferencias.")

    cross = [i for i in range(L) if pfr_p[i] > pen_p[i]]
    print(f"\nprompts con traduccion usable: {len(d_frq)}/{len(df)}")
    print(f"capa donde p(FR) supera a p(EN) con parche: {cross[0] if cross else 'nunca'}")
    if cos_instr is not None:
        print(f"maxima alineacion con la INSTRUCCION : capa {int(cos_instr.argmax())} "
              f"(cos={cos_instr.max():.3f})")
    if cos_frq is not None:
        print(f"maxima alineacion con la PREGUNTA FR : capa {int(cos_frq.argmax())} "
              f"(cos={cos_frq.max():.3f})")
        gana = "pregunta en frances" if cos_frq.max() > cos_instr.max() else "instruccion en texto"
        print(f"-> el parche se parece mas a: {gana}")
    if cos_refs is not None:
        print(f"las dos referencias entre si: cos medio={cos_refs.mean():.3f} "
              f"(alto = son casi lo mismo y la comparacion no informa)")

    json.dump({"rel_delta": rel.tolist(),
               "cos_with_instruction": None if cos_instr is None else cos_instr.tolist(),
               "cos_with_french_question": None if cos_frq is None else cos_frq.tolist(),
               "cos_between_references": None if cos_refs is None else cos_refs.tolist(),
               "raw_cos_patch_frq": None if raw_pf is None else raw_pf.tolist(),
               "raw_cos_clean_frq": None if raw_cf is None else raw_cf.tolist(),
               "p_fr_clean": pfr_c.tolist(), "p_fr_patched": pfr_p.tolist(),
               "p_en_patched": pen_p.tolist(),
               "n_prompts": len(df), "n_with_translation": len(d_frq),
               "patch": args.patch},
              open(args.out, "w"), indent=2)
    print(f"\nGuardado en {args.out}")


if __name__ == "__main__":
    main()
