"""
¿Shared y D (diferencia de medias en la capa 0) hacen lo mismo por dentro?

En la capa 0 son casi ortogonales (cos ~0.05) y aun asi los dos cambian el idioma.
Aca se mide, capa por capa, el desplazamiento que cada condicion produce en el
residual stream en la ULTIMA posicion del prompt (la que genera el primer token
de la respuesta), siempre contra la misma linea de base h(q_en):

    delta_X^l = mean_i ( h^l(cond_X(q_i)) - h^l(q_en_i) )

condiciones: cada --patch nombre=ruta (goal_all, sumado a la pregunta inglesa),
    nativo  = la pregunta escrita en L (prompt_L), sin parche
    instr   = "Answer this in <Idioma>. " + q_en, sin parche

y el coseno entre deltas con VALIDACION CRUZADA por mitades: cos(delta_X en la
mitad A, delta_Y en la mitad B), promediado sobre los dos sentidos. La diagonal
(X contra si mismo en la otra mitad) es el techo de ruido.

Lectura: si cos(Shared, D) es ~0 en la capa 0 pero sube en las capas medias
hacia el techo, los dos vectores son puertas de entrada distintas a la MISMA
representacion interna de "la entrada esta en L".

    python3 geo_diffmean.py --model $M --targets attributes/v10/targets_v8_fr.csv --lang fr \\
        --patch shared=... --patch Dmulti=... --patch rand=... --out geo_fr.json
"""

import argparse
import json

import pandas as pd
import torch
import tqdm

from lm import apply_patch_first_n, build_suffix_manager, get_embeddings, load_model_and_tokenizer

NOMBRE = {"fr": "French", "es": "Spanish", "de": "German", "it": "Italian", "pt": "Portuguese"}


@torch.no_grad()
def last_hidden(model, tokenizer, q, device, patch=None):
    sm = build_suffix_manager(tokenizer, q, target="")
    ids = sm.get_input_ids().to(device)
    emb = get_embeddings(model, ids.unsqueeze(0)).detach()
    if patch is not None:
        emb = apply_patch_first_n(sm, emb, patch, 1, anchor="goal_all")
    emb = emb[:, : sm._assistant_role_slice.stop, :]
    out = model(inputs_embeds=emb, output_hidden_states=True)
    return torch.stack([h[0, -1, :].float().cpu() for h in out.hidden_states])   # [L+1, d]


def cosl(a, b):
    return torch.nn.functional.cosine_similarity(a, b, dim=1)   # [L+1]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--lang", required=True)
    ap.add_argument("--train_test_split", type=float, default=0.84)
    ap.add_argument("--n", type=int, default=0, help="filas del held-out (0 = todas)")
    ap.add_argument("--patch", action="append", default=[], metavar="NOMBRE=RUTA")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    ho = df.iloc[int(len(df) * args.train_test_split):]
    if args.n:
        ho = ho.head(args.n)
    model, tok = load_model_and_tokenizer(args.model, device=args.device)
    patches = {}
    for spec in args.patch:
        k, _, p = spec.partition("=")
        patches[k] = torch.load(p, map_location=args.device).to(args.device).to(model.dtype)
    conds = list(patches) + ["nativo", "instr"]
    instr = f"Answer this in {NOMBRE[args.lang]}. "

    deltas = {c: [] for c in conds}
    for _, r in tqdm.tqdm(ho.iterrows(), total=len(ho), desc=f"geo {args.lang}"):
        q = str(r["prompt"])
        h0 = last_hidden(model, tok, q, args.device)
        for k, v in patches.items():
            deltas[k].append(last_hidden(model, tok, q, args.device, v) - h0)
        deltas["nativo"].append(last_hidden(model, tok, str(r[f"prompt_{args.lang}"]), args.device) - h0)
        deltas["instr"].append(last_hidden(model, tok, instr + q, args.device) - h0)

    n = len(ho)
    A, B = list(range(n // 2)), list(range(n // 2, n))
    mean = {c: {h: torch.stack([deltas[c][i] for i in idx]).mean(0) for h, idx in (("A", A), ("B", B))}
            for c in conds}
    n_layers = next(iter(mean.values()))["A"].shape[0]
    cosm = {}
    for x in conds:
        for y in conds:
            v = 0.5 * (cosl(mean[x]["A"], mean[y]["B"]) + cosl(mean[x]["B"], mean[y]["A"]))
            cosm[f"{x}~{y}"] = [round(float(t), 4) for t in v]
    rel = {c: [round(float(t), 4) for t in torch.stack(deltas[c]).norm(dim=2).mean(0)] for c in conds}
    rep = {"lang": args.lang, "n": n, "n_capas": n_layers - 1, "condiciones": conds,
           "cos_crossfit": cosm, "norma_delta_media": rel, "model": args.model,
           "patches": {k: float(v.float().norm()) for k, v in patches.items()}}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2)

    capas = sorted(set([0, 1, n_layers // 4, n_layers // 2, (3 * n_layers) // 4, n_layers - 1]))
    print(f"\n{args.lang}  n={n}  capas mostradas {capas}  (diagonal = techo split-half)")
    for x in conds:
        for y in conds:
            if conds.index(y) < conds.index(x):
                continue
            print(f"  cos({x:>7}, {y:<7}) " + "  ".join(f"L{l}:{cosm[f'{x}~{y}'][l]:+.2f}" for l in capas))
    print(f"\nguardado: {args.out}")


if __name__ == "__main__":
    main()
