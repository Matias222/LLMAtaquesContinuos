"""
Controles de integracion de un modelo nuevo (Qwen3-4B-Instruct-2507) en el
pipeline de idiomas, ANTES de generar targets o entrenar. Tambien se corre con
Llama-3.2 como regresion: todo lo que pasaba tiene que seguir pasando.

Cada control imprime OK / AVISO / FALLA; con alguna FALLA el script sale con 1.

  1 modelo     model_type, dtype de los pesos, d, embeddings atados, filas de la
               matriz contra el tokenizer, normas de los embeddings (para comparar
               ||v|| / ||e|| con Llama), resolucion del dtype contra el paso de
               sign-SGD
  2 plantilla  sobre TODAS las preguntas del CSV (en/es/de/fr/it/pt y la forma
               "Answer in X.\\n\\n" + q de los targets):
                 - ids hasta el header del assistant == apply_chat_template
                   (solo qwen: el template de Meta mete la fecha y el nuestro no)
                 - decode(goal) == pregunta, byte a byte
                 - ningun token especial dentro del goal
                 - header del user / del assistant exactamente los esperados
                 - target y loss slice: decode(target) == output, loss = target - 1
                 - largo en tokens por categoria (el banco se armo con <= 10 en Llama)
  3 parche     con un v al azar de norma 0.85 sobre la matriz real (o una falsa con
               --solo_tokenizer):
                 - SOLO cambian las posiciones del goal: system, headers, <|im_end|>,
                   header del assistant y target quedan bit a bit iguales
                 - en cada posicion del goal el cambio es v (coseno, error relativo
                   por el redondeo del dtype)
                 - patch_positions / n_patched_tokens == largo del goal
                 - la entrada de generacion termina en el header del assistant (no
                   se cuela ningun token del target)
  4 forward    (GPU) causalidad: los logits ANTES del goal son identicos con y sin
               parche (el parche no toca nada anterior) y los del goal cambian;
               gradiente de calc_loss (train_lang_patch) finito y no nulo, de forma
               [1,1,d]; 5 pasos de sign-SGD bajan la CE del target en esa fila
  5 generacion (GPU) determinismo; parche de ceros == sin parche; generate_one
               (sin KV cache, desde embeddings) contra model.generate (con cache,
               desde ids); corte en fin de turno, sin fuga de rol ni <think>;
               "Answer in X." produce X (GlotLID) y M(q) en ingles; M(q_fr) en fr;
               un v al azar cambia la salida; segundos por token
  6 nll        nll_of_target: CE de la propia respuesta greedy << CE de la
               respuesta de otra fila

    python3 verificar_modelo.py --model /ruta/Qwen3-4B-Instruct-2507
    python3 verificar_modelo.py --model /ruta/Llama-3.2-3B-Instruct     # regresion
    python3 verificar_modelo.py --model /ruta/al/modelo --solo_tokenizer   # 1-3 en CPU sin pesos
"""

import argparse
import json
import os
import sys
import time

os.environ.pop("GEN_CACHE", None)      # aca se mide la generacion real, nunca el cache

import numpy as np
import pandas as pd
import torch

import lm
from lm import (apply_patch_first_n, build_suffix_manager, n_patched_tokens, patch_positions,
                plantilla, stop_token_ids)

SYSTEM = "You are a helpful assistant"
HEADERS = {
    "qwen3": ("<|im_start|>system\nYou are a helpful assistant<|im_end|>\n<|im_start|>user\n",
              "<|im_end|>\n<|im_start|>assistant\n"),
    "llama-3.2": ("<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful "
                  "assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n",
                  "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"),
}
NOMBRE = {"fr": "French", "es": "Spanish", "de": "German"}
COLS = ("prompt", "prompt_es", "prompt_de", "prompt_fr", "prompt_it", "prompt_pt")
NORMA_V = 0.85          # ~ ||v|| de v9 en Llama
STEP = 0.00025          # paso de sign-SGD de la receta


class Controles:
    def __init__(self):
        self.res = []

    def __call__(self, seccion, nombre, ok, detalle="", aviso=False):
        nivel = "OK" if ok else ("AVISO" if aviso else "FALLA")
        self.res.append({"seccion": seccion, "control": nombre, "nivel": nivel, "detalle": str(detalle)})
        print(f"  [{nivel:5}] {nombre}" + (f"  -- {detalle}" if detalle else ""))
        return ok

    def fallas(self):
        return [r for r in self.res if r["nivel"] == "FALLA"]


def preguntas(df):
    """(fila, columna, texto) de todas las preguntas no vacias del CSV."""
    out = []
    for i, r in df.iterrows():
        for c in COLS:
            if c in df.columns and str(r[c]).strip():
                out.append((i, c, str(r[c])))
    return out


# ---------------------------------------------------------------------------
# 1. modelo
# ---------------------------------------------------------------------------
def sec_modelo(C, model, tok, fam):
    print("\n## 1 modelo")
    info = {}
    esperado = lm.MODELOS[model.config.model_type][0]
    C("1", "dtype de los pesos", next(model.parameters()).dtype == esperado,
      f"{next(model.parameters()).dtype} (esperado {esperado})")
    E = lm.get_embedding_matrix(model)
    d = E.shape[1]
    info["d"] = d
    C("1", "d de la matriz == hidden_size", d == model.config.hidden_size, f"d={d}")
    out_w = model.get_output_embeddings().weight
    atados = out_w.data_ptr() == E.data_ptr()
    C("1", "embeddings de entrada y salida atados", atados,
      "atados" if atados else "NO atados: el token mas cercano (etapa D) usa solo la matriz de entrada",
      aviso=True)
    n_tok = len(tok)
    C("1", "filas de la matriz >= vocabulario del tokenizer", E.shape[0] >= n_tok,
      f"{E.shape[0]} filas, tokenizer {n_tok} (las de mas son relleno y no se usan)")
    En = E[:n_tok].float()
    normas = En.norm(dim=1)
    info.update(norma_media=normas.mean().item(), norma_mediana=normas.median().item(),
                std_por_dim=En.std().item())
    print(f"  ||e|| media {info['norma_media']:.4f}  mediana {info['norma_mediana']:.4f}  "
          f"std por dimension {info['std_por_dim']:.5f}  (Llama-3.2-3B: ||e|| media 1.086, d=3072)")
    print(f"  un v de norma {NORMA_V} seria ||v||/||e|| = {NORMA_V / info['norma_media']:.3f} "
          f"(v9 en Llama: 0.78-0.87)")
    # resolucion del dtype en la escala tipica de e + v: si el paso de sign-SGD es
    # mucho menor que el espaciado del dtype, los pasos chicos no se ven en el forward
    escala = info["std_por_dim"] + NORMA_V / d ** 0.5
    eps = torch.finfo(esperado).eps * escala
    info["espaciado_dtype"] = eps
    C("1", "espaciado del dtype en |e+v| tipico vs paso de sign-SGD", eps < 10 * STEP,
      f"espaciado ~{eps:.2e}, paso {STEP:.0e} (v se acumula en fp32; el forward ve e+v redondeado)",
      aviso=True)
    return info


# ---------------------------------------------------------------------------
# 2. plantilla
# ---------------------------------------------------------------------------
def sec_plantilla(C, tok, fam, df):
    print("\n## 2 plantilla")
    # sin clean_up_tokenization_spaces: Llama borra el espacio de " ?" al decodificar
    dec = lambda ids: tok.decode(ids, clean_up_tokenization_spaces=False)
    user_h, asst_h = HEADERS[fam]
    especiales = set(tok.all_special_ids) | {i for t, i in tok.get_vocab().items()
                                             if t.startswith("<|") and t.endswith("|>")}
    qs = preguntas(df)
    instr = [(i, f"instr_{l}", f"Answer in {NOMBRE[l]}.\n\n{df.at[i, 'prompt']}")
             for i in df.index[:60] for l in NOMBRE]
    malos = {"chat_template": [], "goal": [], "especial": [], "user_h": [], "asst_h": [], "target": [],
             "loss": []}
    largos = []
    for i, c, q in qs + instr:
        tgt = str(df.at[i, "output"]) if c == "prompt" else ""
        sm = build_suffix_manager(tok, q, target=tgt)
        ids = sm.get_input_ids().tolist()
        g, a = sm._goal_slice, sm._assistant_role_slice
        if fam == "qwen3":
            ref = tok.apply_chat_template([{"role": "system", "content": SYSTEM}, {"role": "user", "content": q}],
                                          add_generation_prompt=True, tokenize=True)
            if ids[:a.stop] != list(ref):
                malos["chat_template"].append(q)
        if dec(ids[g]) != q:
            malos["goal"].append((q, dec(ids[g])))
        if any(t in especiales for t in ids[g]):
            malos["especial"].append(q)
        if dec(ids[:g.start]) != user_h:
            malos["user_h"].append(dec(ids[:g.start]))
        if dec(ids[a]) != asst_h or a.start != g.stop:
            malos["asst_h"].append(dec(ids[a]))
        if tgt:
            if dec(ids[sm._target_slice]) != tgt:
                malos["target"].append(q)
            ls, ts = sm._loss_slice, sm._target_slice
            if not (ls.start == ts.start - 1 and ls.stop == ts.stop - 1 and ts.start == a.stop):
                malos["loss"].append(q)
        if c == "prompt":
            largos.append((df.at[i, "categoria"] if "categoria" in df.columns else "-", g.stop - g.start))
    n = len(qs) + len(instr)
    if fam == "qwen3":
        C("2", f"ids == apply_chat_template ({n} prompts)", not malos["chat_template"],
          f"{len(malos['chat_template'])} distintos, p.ej. {malos['chat_template'][:2]}")
    else:
        C("2", "ids == apply_chat_template", True, "no aplica a llama-3.2 (Meta mete la fecha)", aviso=True)
    C("2", f"decode(goal) == pregunta ({n})", not malos["goal"], f"{malos['goal'][:2]}")
    C("2", "sin tokens especiales dentro del goal", not malos["especial"], f"{malos['especial'][:2]}")
    C("2", "header del user exacto", not malos["user_h"], f"{malos['user_h'][:1]}")
    C("2", "header del assistant exacto y pegado al goal", not malos["asst_h"], f"{malos['asst_h'][:1]}")
    C("2", "decode(target) == output", not malos["target"], f"{len(malos['target'])} filas, {malos['target'][:2]}")
    C("2", "loss slice = target - 1, target pegado al header", not malos["loss"], f"{malos['loss'][:2]}")
    s = pd.DataFrame(largos, columns=["categoria", "n"])
    print("  tokens de la pregunta en ingles por categoria (el banco se armo con <= 10 en Llama):")
    print(s.groupby("categoria")["n"].describe()[["mean", "min", "max"]].round(1).to_string())
    C("2", "preguntas en ingles con <= 10 tokens", (s["n"] > 10).sum() == 0,
      f"{(s['n'] > 10).sum()} de {len(s)} pasan de 10 (no se filtran: con goal_all el largo multiplica "
      "la perturbacion total)", aviso=True)
    return {"largo_medio": float(s["n"].mean())}


# ---------------------------------------------------------------------------
# 3. parche (solo embeddings)
# ---------------------------------------------------------------------------
def sec_parche(C, tok, embed_fn, d, dtype, device, df):
    print("\n## 3 parche: solo las posiciones del goal")
    g_ = torch.Generator().manual_seed(0)
    v = torch.randn(1, 1, d, generator=g_)
    v = (v * NORMA_V / v.norm()).to(device)
    malos = {"fuera": [], "dentro": [], "pos": [], "corte": []}
    peor_rel, peor_cos = 0.0, 1.0
    qs = preguntas(df)[::7][:300]
    for i, c, q in qs:
        sm = build_suffix_manager(tok, q, target=str(df.at[i, "output"]))
        ids = sm.get_input_ids().to(device)
        e = embed_fn(ids.unsqueeze(0)).detach()
        p = apply_patch_first_n(sm, e, v, 1, anchor="goal_all")
        g = sm._goal_slice
        cambio = (p.float() - e.float())[0]
        filas = set(torch.nonzero(cambio.abs().sum(1) > 0).flatten().tolist())
        goal = set(range(g.start, g.stop))
        fuera = [k for k in range(e.shape[1]) if k not in goal]
        if filas - goal or not torch.equal(p[0, fuera], e[0, fuera]):
            malos["fuera"].append(q)
        if goal - filas:
            malos["dentro"].append(q)
        dv = cambio[g.start:g.stop]
        rel = ((dv - v[0].float()).norm(dim=1) / v.norm()).max().item()
        cos = torch.nn.functional.cosine_similarity(dv, v[0].float().expand_as(dv), dim=1).min().item()
        peor_rel, peor_cos = max(peor_rel, rel), min(peor_cos, cos)
        s, n = patch_positions(sm, 1, 0, "goal_all")
        if (s, n) != (g.start, g.stop - g.start) or n_patched_tokens(tok, q, 1, 0, "goal_all") != n or n == 0:
            malos["pos"].append(q)
        a = sm._assistant_role_slice
        entrada = p[:, :a.stop]
        if entrada.shape[1] != a.stop or a.stop != sm._target_slice.start:
            malos["corte"].append(q)
    C("3", f"fuera del goal nada cambia, bit a bit ({len(qs)} prompts)", not malos["fuera"], f"{malos['fuera'][:2]}")
    C("3", "todas las posiciones del goal cambian", not malos["dentro"], f"{malos['dentro'][:2]}")
    C("3", "el cambio en cada posicion es v (coseno minimo)", peor_cos > 0.999, f"{peor_cos:.6f}")
    C("3", "error relativo |cambio - v| / |v| por el redondeo del dtype", peor_rel < 0.05,
      f"maximo {peor_rel:.4f} ({dtype})", aviso=True)
    C("3", "patch_positions y n_patched_tokens == largo del goal", not malos["pos"], f"{malos['pos'][:2]}")
    C("3", "la entrada de generacion termina en el header del assistant", not malos["corte"], f"{malos['corte'][:2]}")
    # shapes que no son goal_all tienen que fallar en vez de aplicarse mal
    sm = build_suffix_manager(tok, "What is the capital of France?", target="")
    ids = sm.get_input_ids().to(device)
    e = embed_fn(ids.unsqueeze(0)).detach()
    try:
        apply_patch_first_n(sm, e, torch.zeros(1, 3, d, device=device), 1, anchor="goal_all")
        C("3", "goal_all rechaza un parche [1,3,d]", False)
    except ValueError:
        C("3", "goal_all rechaza un parche [1,3,d]", True)
    return v


# ---------------------------------------------------------------------------
# 4. forward: causalidad y gradiente
# ---------------------------------------------------------------------------
def sec_forward(C, model, tok, df, v):
    print("\n## 4 forward: causalidad y gradiente")
    from train_lang_patch import calc_loss
    dev = v.device
    malos_causal, malos_goal = [], []
    for q in list(df["prompt"].iloc[:8]) + list(df["prompt_fr"].iloc[:4]):
        sm = build_suffix_manager(tok, q, target="")
        ids = sm.get_input_ids().to(dev)
        e = lm.get_embeddings(model, ids.unsqueeze(0)).detach()
        a, g = sm._assistant_role_slice, sm._goal_slice
        with torch.no_grad():
            l0 = model(inputs_embeds=e[:, :a.stop]).logits
            l1 = model(inputs_embeds=apply_patch_first_n(sm, e, v, 1, anchor="goal_all")[:, :a.stop]).logits
        if not torch.equal(l0[0, :g.start], l1[0, :g.start]):
            malos_causal.append((q, (l0[0, :g.start] - l1[0, :g.start]).abs().max().item()))
        if torch.equal(l0[0, g.start:], l1[0, g.start:]):
            malos_goal.append(q)
    C("4", "logits antes del goal identicos con y sin parche", not malos_causal, f"{malos_causal[:2]}")
    C("4", "logits desde el goal cambian con el parche", not malos_goal, f"{malos_goal[:2]}")

    r = df[df["output"].astype(str).str.strip() != ""].iloc[0] if (df["output"].astype(str).str.strip() != "").any() else None
    if r is None:
        C("4", "gradiente / sign-SGD", True, "sin outputs en el CSV: se saltea", aviso=True)
        return
    sm = build_suffix_manager(tok, r["prompt"], target=r["output"])
    ids = sm.get_input_ids().to(dev)
    tt = ids[sm._target_slice]
    e = lm.get_embeddings(model, ids.unsqueeze(0)).detach()
    d = e.shape[-1]
    patch = torch.zeros(1, 1, d, device=dev, requires_grad=True)
    ces = []
    for paso in range(6):
        loss, _, ce, _ = calc_loss(model, sm, e, patch, tt, 1, 0.0925, 0, 8, "goal_all")
        loss.backward()
        gr = patch.grad
        if paso == 0:
            C("4", "gradiente del parche: forma [1,1,d], finito, no nulo",
              gr is not None and tuple(gr.shape) == (1, 1, d) and torch.isfinite(gr).all().item()
              and gr.abs().sum().item() > 0,
              f"|grad| {gr.norm().item():.3e}, dtype {gr.dtype}")
        ces.append(ce.item())
        with torch.no_grad():
            patch -= torch.sign(patch.grad) * STEP
        patch.grad = None
    # ojo: la CE de la propia respuesta greedy ya es baja; con una fila en otro idioma
    # se ve mejor, pero esto solo chequea que el signo del gradiente sea el correcto
    C("4", "5 pasos de sign-SGD no suben la CE del target (fila 0)", ces[-1] <= ces[0] + 1e-3,
      " -> ".join(f"{x:.4f}" for x in ces), aviso=True)


# ---------------------------------------------------------------------------
# 5. generacion
# ---------------------------------------------------------------------------
def sec_generacion(C, model, tok, df, v, n_gen, num_tokens):
    print("\n## 5 generacion")
    from checkers import language_verdict, answer_correct
    dev = v.device
    stop = stop_token_ids(tok)
    print(f"  tokens de corte: {{{', '.join(f'{i}: {tok.convert_ids_to_tokens(i)}' for i in sorted(stop))}}}")
    C("5", "fin de turno entre los tokens de corte",
      tok.convert_tokens_to_ids("<|im_end|>" if plantilla(tok) == "qwen3" else "<|eot_id|>") in stop)
    filas = df.iloc[:n_gen]
    det, cero, hf, corte, fuga, think, cambia, tiempos = [], [], [], [], [], [], [], []
    for _, r in filas.iterrows():
        q = r["prompt"]
        t0 = time.time()
        sm = build_suffix_manager(tok, q, target="")
        ids = sm.get_input_ids().to(dev)
        e = lm.get_embeddings(model, ids.unsqueeze(0)).detach()
        a = sm._assistant_role_slice.stop
        o1 = lm._generate(model, e[:, :a], num_tokens, 0.0, stop)
        tiempos.append((time.time() - t0) / max(1, len(o1)))
        o2 = lm._generate(model, e[:, :a], num_tokens, 0.0, stop)
        det.append(np.array_equal(o1, o2))
        oz = lm._generate(model, apply_patch_first_n(sm, e, torch.zeros_like(v), 1, anchor="goal_all")[:, :a],
                          num_tokens, 0.0, stop)
        cero.append(np.array_equal(o1, oz))
        with torch.no_grad():
            g = model.generate(ids[:a].unsqueeze(0), attention_mask=torch.ones(1, a, device=dev, dtype=torch.long),
                               max_new_tokens=num_tokens, do_sample=False, temperature=None, top_p=None, top_k=None,
                               eos_token_id=sorted(stop), pad_token_id=tok.pad_token_id)[0, a:].tolist()
        g = [t for t in g if t not in stop][:len(g)]
        k = next((j for j, (x, y) in enumerate(zip(o1.tolist(), g)) if x != y), min(len(o1), len(g)))
        hf.append((q, k, len(o1), len(g), list(o1[:len(g)]) == g[:len(o1)] and len(o1) == len(g)))
        txt = tok.decode(o1, skip_special_tokens=False)
        corte.append(len(o1) < num_tokens)
        fuga.append(any(s in txt for s in ("<|im_start|>", "<|start_header_id|>", "<|eot_id|>", "<|im_end|>"))
                    or lm.truncate_at_role_leak(txt) != txt.strip())
        think.append("<think>" in txt)
        op = lm._generate(model, apply_patch_first_n(sm, e, v, 1, anchor="goal_all")[:, :a], num_tokens, 0.0, stop)
        cambia.append(not np.array_equal(o1, op))
        print(f"  {q[:50]!r}: {tok.decode(o1, skip_special_tokens=True)[:90]!r}")
    C("5", "greedy determinista (dos corridas iguales)", all(det), f"{sum(det)}/{len(det)}")
    C("5", "parche de ceros == sin parche", all(cero), f"{sum(cero)}/{len(cero)}")
    iguales = sum(x[4] for x in hf)
    tempranas = [x for x in hf if not x[4] and x[1] < 5]
    for q, k, n1, n2, ok in hf:
        if not ok:
            print(f"    difiere de model.generate en el token {k} (nuestro {n1}, hf {n2}): {q[:50]!r}")
    C("5", "generate_one (sin cache) == model.generate (con cache)", iguales == len(hf),
      f"{iguales}/{len(hf)} identicas; divergencias tardias = redondeo bf16 con/sin KV cache",
      aviso=len(tempranas) <= 1)
    C("5", "sin divergencias en los primeros 5 tokens", len(tempranas) <= 1,
      f"{len(tempranas)} tempranas: {[x[0][:40] for x in tempranas]}")
    C("5", "corta en fin de turno antes del limite (mayoria)", sum(corte) >= len(corte) / 2,
      f"{sum(corte)}/{len(corte)} cortaron antes de {num_tokens} tokens", aviso=True)
    C("5", "sin fuga de rol ni tokens de control en la salida", not any(fuga), f"{sum(fuga)}/{len(fuga)}")
    C("5", "sin <think>", not any(think), f"{sum(think)}/{len(think)}")
    C("5", f"un v al azar de norma {NORMA_V} cambia la salida", sum(cambia) >= len(cambia) / 2,
      f"{sum(cambia)}/{len(cambia)}", aviso=True)
    seg = float(np.median(tiempos))
    print(f"  segundos por token (mediana, sin KV cache, respuestas cortas): {seg:.3f}")

    # idioma: baseline en ingles, instruccion, pregunta nativa
    langs = {"en": [], "fr": [], "es": [], "de": [], "nativo_fr": []}
    acc_base = []
    for _, r in filas.iterrows():
        b = lm.generate_one(model, tok, r["prompt"], dev, 100)
        langs["en"].append(language_verdict(b) == "en")
        acc_base.append(answer_correct(b, r["answer"], r["aliases"]))
        for l in NOMBRE:
            y = lm.generate_one(model, tok, f"Answer in {NOMBRE[l]}.\n\n{r['prompt']}", dev, 100)
            langs[l].append(language_verdict(y) == l)
        if str(r.get("prompt_fr", "")).strip():
            langs["nativo_fr"].append(language_verdict(lm.generate_one(model, tok, r["prompt_fr"], dev, 100)) == "fr")
    for k, xs in langs.items():
        etiqueta = {"en": "M(q) en ingles", "nativo_fr": "M(q_fr) en frances"}.get(k, f"M('Answer in {NOMBRE.get(k)}.' + q) en {k}")
        C("5", etiqueta, bool(xs) and sum(xs) >= 0.8 * len(xs), f"{sum(xs)}/{len(xs)}", aviso=True)
    C("5", "accuracy del baseline en ingles", sum(acc_base) >= 0.7 * len(acc_base), f"{sum(acc_base)}/{len(acc_base)}",
      aviso=True)
    return {"seg_por_token": seg}


# ---------------------------------------------------------------------------
# 6. nll
# ---------------------------------------------------------------------------
def sec_nll(C, model, tok, df, dev):
    print("\n## 6 nll_of_target")
    propias, ajenas = [], []
    filas = df.iloc[:6]
    salidas = [lm.generate_one(model, tok, q, dev, 40) for q in filas["prompt"]]
    for k, q in enumerate(filas["prompt"]):
        propias.append(lm.nll_of_target(model, tok, q, salidas[k], dev, head_k=8)["head"])
        ajenas.append(lm.nll_of_target(model, tok, q, salidas[(k + 1) % len(salidas)], dev, head_k=8)["head"])
    print(f"  CE head propia {np.mean(propias):.3f}  ajena {np.mean(ajenas):.3f}")
    C("6", "CE de la propia respuesta greedy finita y baja", all(np.isfinite(propias)) and np.mean(propias) < 0.5,
      f"{np.mean(propias):.3f}")
    C("6", "CE propia < CE ajena", np.mean(propias) < np.mean(ajenas), f"{np.mean(propias):.3f} < {np.mean(ajenas):.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--targets", default="attributes/v8/targets_v8_fr.csv",
                    help="CSV con prompt, prompt_es/de/fr/it/pt, output, answer, aliases, categoria")
    ap.add_argument("--n_gen", type=int, default=8, help="preguntas para los controles de generacion")
    ap.add_argument("--num_tokens", type=int, default=60)
    ap.add_argument("--solo_tokenizer", action="store_true",
                    help="sin pesos (CPU): secciones 2 y 3, con una matriz de embeddings falsa")
    ap.add_argument("--out_json", default=None)
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False, dtype=str)
    C = Controles()
    info = {"model": args.model}
    if args.solo_tokenizer:
        from transformers import AutoConfig, AutoTokenizer
        tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True, use_fast=False)
        fam = plantilla(tok)
        cfg = AutoConfig.from_pretrained(args.model)
        d = cfg.hidden_size
        dtype = lm.MODELOS[lm.familia(args.model)][0]
        E = (torch.randn(max(cfg.vocab_size, len(tok)), d) * 0.02).to(dtype)
        embed_fn = lambda ids: E[ids]
        dev = "cpu"
        print(f"modelo {args.model}  plantilla {fam}  (solo tokenizer, embeddings falsos, d={d})")
    else:
        model, tok = lm.load_model_and_tokenizer(args.model, device=args.device)
        fam = plantilla(tok)
        print(f"modelo {args.model}  model_type {model.config.model_type}  plantilla {fam}")
        info.update(sec_modelo(C, model, tok, fam))
        d, dtype, dev = model.config.hidden_size, next(model.parameters()).dtype, args.device
        embed_fn = lambda ids: lm.get_embeddings(model, ids)
    info.update(sec_plantilla(C, tok, fam, df))
    v = sec_parche(C, tok, embed_fn, d, dtype, dev, df)
    if not args.solo_tokenizer:
        sec_forward(C, model, tok, df, v)
        info.update(sec_generacion(C, model, tok, df, v, args.n_gen, args.num_tokens))
        sec_nll(C, model, tok, df, dev)

    f = C.fallas()
    print("\n" + "=" * 70)
    print(f"{len(C.res)} controles: {sum(r['nivel'] == 'OK' for r in C.res)} OK, "
          f"{sum(r['nivel'] == 'AVISO' for r in C.res)} AVISO, {len(f)} FALLA")
    for r in f:
        print(f"  FALLA [{r['seccion']}] {r['control']}: {r['detalle']}")
    if args.out_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
        json.dump({"info": info, "controles": C.res}, open(args.out_json, "w"), indent=1, ensure_ascii=False)
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
