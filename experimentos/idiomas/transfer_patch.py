"""
Lleva un parche de embeddings de un modelo a otro.

El parche vive en la base de embeddings del modelo donde se entreno. Para
moverlo hace falta o la misma base, o un mapa entre las dos. Tres casos:

  1. mismo tokenizer, misma d   -> copia directa, no hay nada que mapear
  2. mismo tokenizer, d distinta -> la fila i de las dos matrices es el MISMO
     token, asi que hay 128k pares para ajustar un mapa lineal
  3. tokenizer distinto          -> no hay correspondencia; el script se niega

Para el caso 2 usa Procrustes ortogonal (W = U V^T de la SVD de E_a^T E_b), no
minimos cuadrados: preserva angulos y normas, que es lo que importa cuando lo
que se transporta es una DIRECCION. Minimos cuadrados ajusta mejor en MSE pero
puede distorsionar la escala.

GATE: antes de escribir nada reporta la precision de ida y vuelta -- mapea el
embedding de un token del modelo origen y busca su vecino mas cercano en el
destino. Si no cae en el mismo token, el mapa no sirve y el parche mapeado no
significa nada.

El gate se mide sobre tokens HELD-OUT, no sobre los que ajustaron el mapa.
Verificado con datos sinteticos que hace falta: con dos matrices de embeddings
INDEPENDIENTES, Procrustes sobreajusta y el roundtrip in-sample da 74%, que
pareceria una transferencia excelente. Held-out da 0.00%. El mapa final se
reajusta sobre el vocabulario completo, pero quien decide es el numero
held-out.

    python3 transfer_patch.py --source $M3B --target $M8B \\
        --patch runs/v3_250/lang_patch.pt --out runs/transfer_8b/lang_patch.pt
"""

import argparse
import json
import os

import torch
from transformers import AutoTokenizer


def load_embeddings(path, device):
    """Lee solo la matriz de embeddings, sin instanciar el modelo entero."""
    from safetensors import safe_open
    import glob
    claves = ("model.embed_tokens.weight", "embed_tokens.weight",
              "transformer.wte.weight", "model.decoder.embed_tokens.weight")
    for f in sorted(glob.glob(os.path.join(path, "*.safetensors"))):
        with safe_open(f, framework="pt", device="cpu") as h:
            for k in claves:
                if k in h.keys():
                    return h.get_tensor(k).to(device=device, dtype=torch.float32)
    # Fallback: cargar el modelo (caro)
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16)
    return m.get_input_embeddings().weight.detach().to(device=device, dtype=torch.float32)


def check_tokenizers(a, b):
    ta = AutoTokenizer.from_pretrained(a, trust_remote_code=True, use_fast=False)
    tb = AutoTokenizer.from_pretrained(b, trust_remote_code=True, use_fast=False)
    va, vb = ta.get_vocab(), tb.get_vocab()
    if len(va) != len(vb):
        return False, f"tamanos distintos: {len(va)} vs {len(vb)}"
    # No alcanza con el tamano: los ids tienen que apuntar al MISMO token.
    muestra = list(va.items())[::max(1, len(va) // 2000)]
    iguales = sum(1 for tok, i in muestra if vb.get(tok) == i)
    frac = iguales / len(muestra)
    return frac > 0.999, f"{frac:.1%} de los ids coinciden ({iguales}/{len(muestra)} muestreados)"


def procrustes(Ea, Eb):
    """W ortogonal que minimiza ||Ea W - Eb||_F."""
    M = Ea.T @ Eb                      # [da, db]
    U, _, Vh = torch.linalg.svd(M, full_matrices=False)
    return U @ Vh


def random_map(da, db, device, seed=0):
    """
    Mapa ortogonal AL AZAR, misma forma que el ajustado.

    Es el control que hace legible el resultado. Produce un vector en el espacio
    destino con la misma norma y el mismo origen que el mapeado de verdad, pero
    sin ninguna alineacion entre los dos modelos. Si el mapeado induce frances y
    este no, transfirio. Si los dos inducen lo mismo, lo que se mide no es
    transferencia sino el efecto de sumar cualquier vector de esa magnitud.
    """
    g = torch.Generator(device="cpu").manual_seed(seed)
    A = torch.randn(da, db, generator=g).to(device)
    U, _, Vh = torch.linalg.svd(A, full_matrices=False)
    return U @ Vh


def roundtrip(Ea, Eb, W, idx):
    """
    Precision de ida y vuelta sobre los tokens `idx`: mapeo el embedding del
    origen y busco su vecino mas cercano por coseno en el destino. Deberia
    volver al mismo token.
    """
    P = torch.nn.functional.normalize(Ea[idx] @ W, dim=1)
    E = torch.nn.functional.normalize(Eb, dim=1)
    top1 = top10 = 0
    for i in range(0, len(idx), 256):
        sims = P[i:i + 256] @ E.T
        k = sims.topk(10, dim=1).indices
        tgt = idx[i:i + 256, None]
        top1 += (k[:, :1] == tgt).any(1).sum().item()
        top10 += (k == tgt).any(1).sum().item()
    return top1 / len(idx), top10 / len(idx)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help="modelo donde se entreno el parche")
    ap.add_argument("--target", required=True)
    ap.add_argument("--patch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--force", action="store_true",
                    help="escribir el parche aunque el gate de ida y vuelta falle")
    ap.add_argument("--control", action="store_true",
                    help="usar un mapa ortogonal AL AZAR en vez del ajustado. Produce el "
                         "parche de control: misma norma y mismo origen, sin alineacion.")
    args = ap.parse_args()

    ok, msg = check_tokenizers(args.source, args.target)
    print(f"tokenizers compatibles: {ok}  ({msg})")
    if not ok:
        raise SystemExit(
            "\nLos tokenizers no coinciden, asi que las filas de las dos matrices de\n"
            "embeddings no son el mismo token y no hay pares con que ajustar el mapa.\n"
            "Sin base comun, transferir el vector no esta bien planteado: cualquier\n"
            "resultado, positivo o negativo, seria ruido.")

    dev = args.device if torch.cuda.is_available() else "cpu"
    Ea = load_embeddings(args.source, dev)
    Eb = load_embeddings(args.target, dev)
    print(f"origen  {tuple(Ea.shape)}\ndestino {tuple(Eb.shape)}")

    patch = torch.load(args.patch, map_location=dev).to(torch.float32)
    print(f"parche  {tuple(patch.shape)}  norma {patch.norm().item():.4f}")

    V = Ea.shape[0]
    g = torch.Generator().manual_seed(0)
    perm = torch.randperm(V, generator=g).to(dev)
    ajuste, held = perm[: V // 2], perm[V // 2:][:4000]

    if Ea.shape[1] == Eb.shape[1]:
        print("\nMisma dimension: copia directa, no hay nada que mapear.")
        W = torch.eye(Ea.shape[1], device=dev)
        W_gate = W
    else:
        print(f"\nProcrustes ortogonal {Ea.shape[1]} -> {Eb.shape[1]}")
        # Para el gate: ajustar en la mitad del vocabulario y medir en la otra.
        W_gate = procrustes(Ea[ajuste], Eb[ajuste])
        # Mapa final: reajustado sobre el vocabulario completo.
        W = procrustes(Ea, Eb)
        res = (Ea @ W - Eb).norm() / Eb.norm()
        print(f"  residuo relativo ||Ea W - Eb|| / ||Eb|| = {res.item():.4f}")

    t1i, _ = roundtrip(Ea, Eb, W_gate, ajuste[:2000])
    t1, t10 = roundtrip(Ea, Eb, W_gate, held)
    print(f"\nGATE - ida y vuelta con el mapa ajustado en media lengua:")
    print(f"  in-sample  top-1 {t1i:.1%}   (no decide nada: Procrustes sobreajusta)")
    print(f"  HELD-OUT   top-1 {t1:.1%}   top-10 {t10:.1%}   sobre {len(held)} tokens")
    print(f"  azar: {1/V:.4%}")
    if t1 < 0.5:
        print("\n  El mapa NO preserva la identidad de los tokens. Los dos espacios de")
        print("  embeddings no estan relacionados linealmente, asi que el parche mapeado")
        print("  no significa nada y el eval no seria interpretable.")
        if not args.force:
            raise SystemExit("  Abortado. Usa --force si igual queres escribirlo.")
    else:
        print("  El mapa preserva identidad: el parche mapeado es interpretable.")

    if args.control:
        W = random_map(Ea.shape[1], Eb.shape[1], dev)
        c1, _ = roundtrip(Ea, Eb, W, held)
        print(f"\nCONTROL: mapa ortogonal al azar. Ida y vuelta held-out: {c1:.2%}")
        print("  Este parche NO deberia inducir frances. Si lo induce, el efecto no")
        print("  es transferencia sino la respuesta del modelo a cualquier vector de")
        print("  esa magnitud, y el resultado del mapeado real no significa nada.")

    mapped = (patch.reshape(-1, Ea.shape[1]) @ W).reshape(*patch.shape[:-1], Eb.shape[1])
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    torch.save(mapped.to(torch.float32), args.out)
    meta = {"source": args.source, "target": args.target, "patch": args.patch,
            "d_source": Ea.shape[1], "d_target": Eb.shape[1],
            "norm_source": patch.norm().item(), "norm_mapped": mapped.norm().item(),
            "roundtrip_top1_heldout": t1, "roundtrip_top10_heldout": t10,
            "roundtrip_top1_insample": t1i, "n_heldout": len(held),
            "control": args.control}
    json.dump(meta, open(args.out.replace(".pt", "_transfer.json"), "w"), indent=2)
    print(f"\nnorma mapeada {mapped.norm().item():.4f}  (origen {patch.norm().item():.4f})")
    print(f"escrito {args.out}")


if __name__ == "__main__":
    main()
