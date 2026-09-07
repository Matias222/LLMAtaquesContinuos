"""
Utilidades compartidas de los experimentos de MECANISMO sobre el parche de
embeddings (v4_250): mascaras de atencion por capa y generacion enmascarada.

La hipotesis que estos experimentos prueban:

    el parche funciona como CONTEXTO PERSISTENTE -- las 3 posiciones parcheadas
    son una fuente que cada token generado lee por atencion -- y no como un
    estado inyectado en la posicion de decision (el ultimo token del prompt).

Si es asi, bloquear la atencion HACIA las posiciones parcheadas desde los tokens
generados, dejando intacto todo el forward del prompt, tiene que hacer caer el
frances despues del primer token. Es el patron que ya mostraron los parches de
activaciones: primer token frances, colapso despues.

---------------------------------------------------------------------------
COMO SE BLOQUEA
---------------------------------------------------------------------------
Se construye una mascara aditiva 4D [1, 1, S, S] en el dtype del modelo:

    0                      -> la query i puede mirar la key j
    torch.finfo(dtype).min -> no puede

Causal (j > i bloqueado) MAS las columnas de las posiciones parcheadas para las
queries i >= query_from. Ninguna fila queda vacia: la diagonal siempre esta
permitida porque las keys bloqueadas son anteriores a query_from.

transformers 4.56 acepta una mascara 4D ya preparada tal cual (early-exit en
masking_utils._preprocess_mask_arguments), y la pasa a todas las capas. Con
sdpa la usa como attn_mask aditivo; con eager la suma a los scores. En los dos
casos el dtype tiene que ser el del modelo (fp16).

Para bloquear SOLO en una banda de capas, al modelo se le pasa la causal pura y
un forward_pre_hook sobre `layers[l-1].self_attn` reemplaza el kwarg
`attention_mask` por la bloqueada. LlamaDecoderLayer llama a self_attn con
kwargs nombrados, asi que el hook los ve.

---------------------------------------------------------------------------
INDICES DE CAPA
---------------------------------------------------------------------------
Misma convencion que mean_diff_vectors.py / train_act_patch.py: la capa `l`
(1..28) es el bloque `model.model.layers[l-1]`. "Bloquear en la capa l" es
bloquear la atencion DENTRO de ese bloque, cuya salida es hidden_states[l].

---------------------------------------------------------------------------
SIN KV CACHE, A PROPOSITO
---------------------------------------------------------------------------
Igual que lm.generate: cada paso rehace el forward completo. Eso hace que la
mascara sea trivial de construir (S x S, sin cache_position) y que el prompt se
recompute identico en cada paso, que es exactamente lo que queremos: el estado
del ultimo token del prompt sigue viendo el parche; solo los tokens generados
dejan de verlo.
"""

import contextlib
import re

import torch

from checkers import (answer_correct, french_score, is_french, language_verdict,
                      truncate_at_role_leak)
from lm import (apply_patch_first_n, build_suffix_manager, get_embedding_matrix,
                get_embeddings, stop_token_ids)

_FR_START = re.compile(r"^\s*(Le|La|L'|L’|Les|Un|Une|Pour|Je|Voici|C'est|C’est|En|Il|Elle|Oui|Non|Bien|Ah|Quelle|Quel)\b")


def starts_french(text):
    """Heuristica de PRIMER TOKEN: arranca con una funcional francesa inequivoca.

    Es deliberadamente distinta de is_french(): mide si la DECISION del primer
    token fue francesa, no si la respuesta entera lo es. Es la que separa
    'arranca y colapsa' de 'nunca arranca'."""
    return bool(_FR_START.match(text or ""))


def add_metrics(rec, key, text, answer, aliases):
    """
    Escribe en `rec` las metricas de un texto bajo el prefijo `key`, con los
    mismos nombres que eval_lang_patch.py (key_is_french, key_french_score,
    key_answer_correct) para que manual_rescore.py y reporting.py los lean, mas
    dos que aca importan y alla no:

        key_starts_fr   decision del PRIMER token (ver starts_french)
        key_len         largo en caracteres: el colapso a fragmentos se ve aca
    """
    has_answer = str(answer).strip() != ""
    rec[f"{key}_is_french"] = bool(is_french(text))
    rec[f"{key}_french_score"] = float(french_score(text))
    rec[f"{key}_lang"] = language_verdict(text)
    rec[f"{key}_answer_correct"] = (bool(answer_correct(text, answer, aliases))
                                    if has_answer else None)
    rec[f"{key}_starts_fr"] = starts_french(text)
    rec[f"{key}_len"] = len(text)
    return rec


def aggregate(rows, key):
    """Agregado sobre filas escritas con add_metrics(rec, key, ...)."""
    n = max(1, len(rows))
    acc = [r[f"{key}_answer_correct"] for r in rows if r[f"{key}_answer_correct"] is not None]
    ver = {}
    for r in rows:
        ver[r[f"{key}_lang"]] = ver.get(r[f"{key}_lang"], 0) + 1
    return {
        "n": len(rows),
        "is_french": sum(r[f"{key}_is_french"] for r in rows) / n,
        "french_score": sum(r[f"{key}_french_score"] for r in rows) / n,
        "answer_correct": (sum(acc) / len(acc)) if acc else float("nan"),
        "starts_fr": sum(r[f"{key}_starts_fr"] for r in rows) / n,
        "len_media": sum(r[f"{key}_len"] for r in rows) / n,
        "cortas_lt25": int(sum(1 for r in rows if r[f"{key}_len"] < 25)),
        "veredictos": ver,
    }


def parse_layers(spec, n_layers):
    """'all' | '16' | '12-16' | '1,5,9' -> lista ordenada de capas 1..n_layers."""
    spec = str(spec).strip().lower()
    if spec in ("all", "todas", "*"):
        return list(range(1, n_layers + 1))
    out = set()
    for parte in spec.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            a, b = parte.split("-")
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(parte))
    capas = sorted(out)
    if not capas or capas[0] < 1 or capas[-1] > n_layers:
        raise ValueError(f"capas fuera de rango 1..{n_layers}: {spec}")
    return capas


def patched_positions(sm, num_patch_positions=3, offset=0):
    """Indices absolutos (en la secuencia tokenizada) que reciben el parche.

    Espeja lm.apply_patch_first_n con `offset`: goal_start + offset ... +n,
    recortado al largo del goal. Puede devolver menos de n posiciones si la
    pregunta es corta; el llamador decide si eso se reporta."""
    g0, g1 = sm._goal_slice.start, sm._goal_slice.stop
    start = g0 + offset
    n = max(0, min(num_patch_positions, g1 - start))
    return list(range(start, start + n))


def causal_mask(seq_len, dtype, device):
    """Mascara aditiva causal [1, 1, S, S]."""
    neg = torch.finfo(dtype).min
    m = torch.zeros(seq_len, seq_len, dtype=dtype, device=device)
    tri = torch.triu(torch.ones(seq_len, seq_len, dtype=torch.bool, device=device), diagonal=1)
    m.masked_fill_(tri, neg)
    return m[None, None, :, :]


def blocked_mask(seq_len, blocked_keys, query_from, dtype, device):
    """Causal + columnas `blocked_keys` bloqueadas para las queries >= query_from."""
    m = causal_mask(seq_len, dtype, device)
    if blocked_keys and query_from is not None and query_from < seq_len:
        neg = torch.finfo(dtype).min
        keys = torch.tensor(blocked_keys, dtype=torch.long, device=device)
        m[0, 0, query_from:, keys] = neg
    return m


class LayerMasks:
    """
    Reemplaza el kwarg `attention_mask` de self_attn en un subconjunto de capas.

    La mascara cambia en cada paso de generacion (S crece), asi que el hook no
    guarda un tensor fijo: lee `self.mask`, que el loop actualiza con set().

        with LayerMasks(model, [12, 13, 14]) as lm_:
            for paso in ...:
                lm_.set(blocked_mask(S, ...))
                model(inputs_embeds=..., attention_mask=causal_mask(S, ...))
    """

    def __init__(self, model, layers):
        self.model = model
        self.layers = list(layers)
        self.mask = None
        self.handles = []

    def set(self, mask):
        self.mask = mask

    def _hook(self, module, args, kwargs):
        if self.mask is None:
            return None
        kwargs = dict(kwargs)
        kwargs["attention_mask"] = self.mask
        return args, kwargs

    def __enter__(self):
        for l in self.layers:
            attn = self.model.model.layers[l - 1].self_attn
            self.handles.append(attn.register_forward_pre_hook(self._hook, with_kwargs=True))
        return self

    def __exit__(self, *exc):
        for h in self.handles:
            h.remove()
        self.handles = []
        self.mask = None
        return False


def query_from_for(block, sm, prompt_len, blocked):
    """
    Desde que query se bloquea la atencion hacia las posiciones parcheadas.

        gen   solo los tokens GENERADOS (i >= prompt_len). El forward del prompt
              queda intacto, incluido el ultimo token que decide el primer
              token de la respuesta. Es el test de la hipotesis.
        post  todo lo que viene DESPUES del bloque parcheado, incluido el resto
              del prompt. El parche queda invisible para todos: la salida tiene
              que ser identica al baseline. Es el control de que la mascara
              hace lo que dice.
        none  sin bloqueo.
    """
    if block == "gen":
        return prompt_len
    if block == "post":
        return (blocked[-1] + 1) if blocked else prompt_len
    if block == "none":
        return None
    raise ValueError(f"block desconocido: {block}")


@torch.no_grad()
def generate_masked(model, tokenizer, instruction, device, patch=None,
                    num_patch_positions=3, patch_offset=0, block="gen",
                    layers=None, num_tokens=100, explicit_causal=False):
    """
    Generacion greedy desde embeddings con el parche aplicado y la atencion
    hacia las posiciones parcheadas bloqueada segun `block` y `layers`.

    layers=None -> el bloqueo aplica en TODAS las capas (mascara a nivel modelo).
    layers=[..] -> solo en esas capas (hooks); el resto ve la causal pura.

    explicit_causal=True con block='none' pasa la causal 4D explicita en vez de
    attention_mask=None. Sirve para verificar que el camino de la mascara no
    cambia la salida por si mismo (sdpa con is_causal vs mascara aditiva pueden
    diferir en el ultimo bit en fp16).

    Devuelve (texto_truncado, texto_crudo, info).
    """
    sm = build_suffix_manager(tokenizer, instruction, target="")
    tokens = sm.get_input_ids().to(device)
    embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()
    if patch is not None:
        embeds = apply_patch_first_n(sm, embeds, patch, num_patch_positions, offset=patch_offset)
    embeds = embeds[:, : sm._assistant_role_slice.stop, :]
    prompt_len = embeds.shape[1]
    blocked = patched_positions(sm, num_patch_positions, patch_offset)
    q_from = query_from_for(block, sm, prompt_len, blocked)
    dtype = embeds.dtype

    emb_matrix = get_embedding_matrix(model)
    stop = stop_token_ids(tokenizer)
    use_hooks = q_from is not None and layers is not None
    ctx = LayerMasks(model, layers) if use_hooks else contextlib.nullcontext()

    out = []
    with ctx as hooks:
        for _ in range(num_tokens):
            S = embeds.shape[1]
            if q_from is None:
                mask_model = causal_mask(S, dtype, device) if explicit_causal else None
            elif not use_hooks:
                mask_model = blocked_mask(S, blocked, q_from, dtype, device)
            else:
                mask_model = causal_mask(S, dtype, device)
                hooks.set(blocked_mask(S, blocked, q_from, dtype, device))
            logits = model(inputs_embeds=embeds, attention_mask=mask_model,
                           use_cache=False).logits
            tok = torch.argmax(logits[:, -1, :])
            if int(tok) in stop:
                break
            out.append(int(tok))
            embeds = torch.hstack([embeds, emb_matrix[tok][None, None, :]])

    raw = tokenizer.decode(out, skip_special_tokens=True)
    info = {"prompt_len": int(prompt_len), "blocked": [int(b) for b in blocked],
            "query_from": None if q_from is None else int(q_from),
            "n_generated": len(out)}
    return truncate_at_role_leak(raw), raw, info


def selftest_masks():
    """Chequeos de forma y de logica de las mascaras, sin modelo (CPU)."""
    S, dtype, dev = 7, torch.float32, "cpu"
    neg = torch.finfo(dtype).min
    c = causal_mask(S, dtype, dev)
    assert c.shape == (1, 1, S, S)
    assert (c[0, 0].diagonal() == 0).all(), "la diagonal tiene que estar permitida"
    assert c[0, 0, 0, 1] == neg and c[0, 0, 1, 0] == 0, "causal invertida"

    b = blocked_mask(S, [2, 3], query_from=5, dtype=dtype, device=dev)
    # queries 0..4: identicas a la causal
    assert torch.equal(b[0, 0, :5], c[0, 0, :5])
    # queries 5,6: columnas 2 y 3 bloqueadas, el resto causal
    assert b[0, 0, 5, 2] == neg and b[0, 0, 5, 3] == neg and b[0, 0, 6, 2] == neg
    assert b[0, 0, 5, 1] == 0 and b[0, 0, 5, 4] == 0 and b[0, 0, 5, 5] == 0
    assert b[0, 0, 6, 5] == 0 and b[0, 0, 6, 6] == 0
    # ninguna fila completamente bloqueada
    assert ((b[0, 0] == 0).sum(dim=1) >= 1).all()
    # query_from fuera de rango o sin keys: causal pura
    assert torch.equal(blocked_mask(S, [], 5, dtype, dev), c)
    assert torch.equal(blocked_mask(S, [2], S + 3, dtype, dev), c)

    assert parse_layers("all", 28) == list(range(1, 29))
    assert parse_layers("12-16", 28) == [12, 13, 14, 15, 16]
    assert parse_layers("1,5,9", 28) == [1, 5, 9]
    assert starts_french("Le platine") and starts_french("L'été est") and not starts_french("The force")
    print("attn_utils: selftest OK")


if __name__ == "__main__":
    selftest_masks()
