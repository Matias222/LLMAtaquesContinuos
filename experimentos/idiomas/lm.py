"""
Helpers de modelo compartidos por el experimento de idiomas.

Mismas convenciones que legacy/christmas_final_train.py y legacy/test_xmas_patch.py:
Llama-3.2 fp16, tokenizer use_fast=False, template 'llama-3.2', parche aditivo
sobre las primeras N posiciones del goal slice, generacion greedy desde embeddings.

Familias soportadas (MODELOS, por config.model_type):
  llama  Llama-3.2-Instruct: fp16, plantilla 'llama-3.2' (el paper; sin cambios)
  qwen3  Qwen3-4B-Instruct-2507: bf16 (los pesos son bf16; fp16 desborda en Qwen),
         plantilla 'qwen3' (ChatML sin thinking, clase_prompts.Qwen3ConversationTemplate)
La plantilla se elige por el tokenizer (plantilla()), asi que los scripts que
solo cargan el tokenizer (nearest_token_patch.py) eligen la misma.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import numpy as np
import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, LlamaForCausalLM

from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from checkers import truncate_at_role_leak

DEFAULT_MODEL = "/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct"


# model_type -> (dtype, plantilla)
MODELOS = {"llama": (torch.float16, "llama-3.2"), "qwen3": (torch.bfloat16, "qwen3")}


def familia(model_path):
    mt = AutoConfig.from_pretrained(model_path, trust_remote_code=True).model_type
    if mt not in MODELOS:
        raise ValueError(f"model_type {mt!r} no soportado ({model_path}); validos: {sorted(MODELOS)}")
    return mt


def load_model_and_tokenizer(model_path, tokenizer_path=None, device="cuda:0", **kwargs):
    dtype, nombre = MODELOS[familia(model_path)]
    model = (
        AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=dtype, trust_remote_code=True, **kwargs
        )
        .to(device)
        .eval()
    )
    tokenizer_path = model_path if tokenizer_path is None else tokenizer_path
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True, use_fast=False)
    if "Llama-3.2" in tokenizer_path:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token
    if plantilla(tokenizer) != nombre:
        raise ValueError(f"el tokenizer de {tokenizer_path} usa la plantilla {plantilla(tokenizer)!r} "
                         f"pero el modelo es {nombre!r}")
    return model, tokenizer


def plantilla(tokenizer):
    """'qwen3' si el vocabulario tiene <|im_start|> (ChatML), si no 'llama-3.2'.
    Se calcula una vez por tokenizer (get_vocab de 150k entradas es caro)."""
    p = getattr(tokenizer, "_plantilla", None)
    if p is None:
        p = "qwen3" if "<|im_start|>" in tokenizer.get_vocab() else "llama-3.2"
        tokenizer._plantilla = p
    return p


def get_embeddings(model, input_ids):
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens(input_ids)
    if model.config.model_type in MODELOS:
        return model.get_input_embeddings()(input_ids)
    raise ValueError(f"Unknown model type: {type(model)}")


def get_embedding_matrix(model):
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    if model.config.model_type in MODELOS:
        return model.get_input_embeddings().weight
    raise ValueError(f"Unknown model type: {type(model)}")


def build_suffix_manager(tokenizer, instruction, target=""):
    return SuffixManager(
        tokenizer=tokenizer,
        conv_template=load_conversation_template(plantilla(tokenizer)),
        instruction=instruction,
        target=target,
        adv_string="",
    )


PATCH_ANCHORS = ("goal", "header", "goal_all")


def patch_positions(suffix_manager, num_patch_positions=3, offset=0, anchor="goal"):
    """
    (start, n): las n posiciones absolutas [start, start+n) que reciben el parche.

    anchor="goal"    las primeras N del goal slice a partir de goal_start +
                     offset (la convencion de siempre). Si el goal es mas corto
                     que offset + N, entran las que hay y el resto del parche
                     se ignora.
    anchor="header"  los ULTIMOS N tokens del header del assistant
                     (<|eot_id|> <|start_header_id|> assistant <|end_header_id|>
                     \n\n), corridos `offset` hacia atras. Esos tokens son
                     identicos en todos los prompts, en todos los idiomas y con
                     cualquier apertura, asi que un parche ahi no puede depender
                     del token sobre el que se suma: es la respuesta al hallazgo
                     de que el parche sobre el goal solo funciona con las
                     aperturas e idiomas que vio (open_2, it/pt). Ademas es la
                     region cuyo KV, segun mask_patch_attention --block keep,
                     sostiene el modo frances.
    anchor="goal_all"
                     TODO el goal slice (la pregunta del usuario entera, sin
                     system, sin headers y sin <|eot_id|>), a partir de
                     goal_start + offset. Ahi el parche es UN solo vector
                     [1, 1, d] que se suma igual a cada posicion, asi que
                     `num_patch_positions` no decide cuantas posiciones se tocan
                     (son las que tenga la pregunta) y se ignora. Un v uniforme
                     no puede apoyarse ni en la posicion ni en el token sobre el
                     que cae. OJO: es una SUMA, no un promedio: la perturbacion
                     total crece con el largo de la pregunta.
    """
    if anchor == "goal":
        start = suffix_manager._goal_slice.start + int(offset)
        n = max(0, min(num_patch_positions, suffix_manager._goal_slice.stop - start))
        return start, n
    if anchor == "header":
        hs = suffix_manager._assistant_role_slice
        end = hs.stop - int(offset)
        start = max(hs.start, end - num_patch_positions)
        return start, max(0, end - start)
    if anchor == "goal_all":
        start = suffix_manager._goal_slice.start + int(offset)
        return start, max(0, suffix_manager._goal_slice.stop - start)
    raise ValueError(f"anchor desconocido: {anchor}; validos: {PATCH_ANCHORS}")


def apply_patch_first_n(suffix_manager, prompt_embeds, patch, num_patch_positions=3,
                        offset=0, anchor="goal"):
    """
    e'_i = e_i + v_i  para i en las N posiciones que devuelve patch_positions.

    Con anchor="goal" y offset=0 (defaults) es identico a
    apply_patch_to_first_n_tokens de legacy/christmas_final_train.py: NO
    promedia posiciones, preserva las K direcciones posicionales. `offset`
    existe para el control de posicion (ablate_patch_positions.py,
    train_lang_patch.py --patch_offset) y `anchor` para parchear el header del
    assistant en vez de la pregunta (--patch_anchor header).

    Con anchor="goal_all" el parche es [1, 1, d] y se suma, por broadcast, a
    todas las posiciones de la pregunta:  e'_i = e_i + v  para todo i del goal.
    """
    patched = prompt_embeds.clone()
    start, actual = patch_positions(suffix_manager, num_patch_positions, offset, anchor)
    if anchor == "goal_all":
        if patch.shape[1] != 1:
            raise ValueError(f"anchor goal_all espera un parche [1, 1, d]; llego {tuple(patch.shape)}")
        if actual > 0:
            patched[:, start:start + actual, :] = prompt_embeds[:, start:start + actual, :] + patch
        return patched
    if actual > 0:
        patched[:, start:start + actual, :] = (
            prompt_embeds[:, start:start + actual, :] + patch[:, :actual, :]
        )
    return patched


def n_patched_tokens(tokenizer, instruction, num_patch_positions=3, offset=0, anchor="goal"):
    """Cuantas posiciones de `instruction` reciben el parche. Con goal_all es el
    largo de la pregunta en tokens, o sea el factor por el que se multiplica la
    perturbacion total: hay que mirarlo al comparar sets de largos distintos."""
    sm = build_suffix_manager(tokenizer, instruction, target="")
    sm.get_input_ids()      # los slices se calculan aca, no en el constructor
    return patch_positions(sm, num_patch_positions, offset, anchor)[1]


def stop_token_ids(tokenizer):
    """
    Ids que cierran el turno del assistant.

    Sin esto la generacion sigue despues de <|eot_id|> y el modelo arranca el
    turno siguiente. Como decodificamos con skip_special_tokens=True, los
    headers desaparecen pero el token de texto plano "assistant" sobrevive, y
    el resultado son varios turnos pegados en un solo string.
    """
    ids = getattr(tokenizer, "_stop_ids", None)
    if ids is not None:
        return set(ids)
    ids = set()
    if tokenizer.eos_token_id is not None:
        ids.add(int(tokenizer.eos_token_id))
    # Llama: <|eot_id|> <|end_of_text|>; Qwen: <|im_end|> <|endoftext|>. Solo los
    # que estan en el vocabulario: convert_tokens_to_ids de un token ajeno devuelve
    # None (Llama) o el id del unk, que en Qwen ES <|endoftext|>.
    vocab = tokenizer.get_vocab()
    for t in ("<|eot_id|>", "<|end_of_text|>", "<|im_end|>", "<|endoftext|>"):
        if t in vocab:
            ids.add(int(vocab[t]))
    tokenizer._stop_ids = frozenset(ids)
    return ids


# Cache de generaciones greedy (opt-in con GEN_CACHE=<dir>). La clave son los
# embeddings de entrada EXACTOS + modelo + largo + tokens de corte: misma entrada
# greedy => misma salida, asi que M(q) sin parche (o con a=0: q + 0*v es el mismo
# tensor) se genera una sola vez aunque lo pidan varios scripts o varias celdas.
# Un parche distinto de cero cambia los embeddings y nunca colisiona.
GEN_CACHE_STATS = {"hit": 0, "miss": 0}


def _gen_cache_path(model, input_embeddings, num_tokens, stop_ids):
    import hashlib
    d = os.environ.get("GEN_CACHE")
    if not d:
        return None
    h = hashlib.sha1()
    h.update(str(getattr(model.config, "_name_or_path", "")).encode())
    h.update(f"|{num_tokens}|{sorted(stop_ids)}|{tuple(input_embeddings.shape)}|".encode())
    h.update(input_embeddings.detach().float().cpu().numpy().tobytes())
    k = h.hexdigest()
    return os.path.join(d, k[:2], k + ".json")


def _gen_cache_report():
    if GEN_CACHE_STATS["hit"] or GEN_CACHE_STATS["miss"]:
        print(f"[gen_cache] {os.environ.get('GEN_CACHE')}: reusadas {GEN_CACHE_STATS['hit']}, "
              f"generadas {GEN_CACHE_STATS['miss']}", file=sys.stderr)


import atexit
atexit.register(_gen_cache_report)


def generate(model, input_embeddings, num_tokens=100, temperature=0.0, stop_ids=None):
    """
    Generacion autoregresiva desde embeddings. temperature=0.0 => greedy.

    Corta en cuanto sale un token de `stop_ids` (fin de turno), que NO se
    incluye en la salida. Si stop_ids es None genera los num_tokens completos
    (comportamiento viejo, solo para debug). Greedy + GEN_CACHE: ver arriba.
    """
    import json
    stop_ids = set() if stop_ids is None else set(stop_ids)
    path = _gen_cache_path(model, input_embeddings, num_tokens, stop_ids) if temperature < 1e-6 else None
    if path and os.path.exists(path):
        GEN_CACHE_STATS["hit"] += 1
        with open(path) as f:
            return np.array(json.load(f), dtype=np.int64)
    out = _generate(model, input_embeddings, num_tokens, temperature, stop_ids)
    if path:
        GEN_CACHE_STATS["miss"] += 1
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{os.getpid()}.tmp"
        with open(tmp, "w") as f:
            json.dump([int(t) for t in out], f)
        os.replace(tmp, path)
    return out


@torch.no_grad()
def _generate(model, input_embeddings, num_tokens, temperature, stop_ids):
    model.eval()
    embedding_matrix = get_embedding_matrix(model)
    input_embeddings = input_embeddings.clone()
    out = torch.tensor([], dtype=torch.long, device=model.device)
    for _ in range(num_tokens):
        logits = model(input_ids=None, inputs_embeds=input_embeddings).logits
        if temperature < 1e-6:
            tok = torch.argmax(logits[:, -1, :])
        else:
            probs = torch.softmax(logits[:, -1, :] / temperature, dim=-1)
            tok = torch.multinomial(probs, num_samples=1).squeeze()
        if int(tok) in stop_ids:
            break
        out = torch.cat((out, tok.unsqueeze(0)))
        input_embeddings = torch.hstack([input_embeddings, embedding_matrix[tok][None, None, :]])
    return out.cpu().numpy()


def generate_one(model, tokenizer, instruction, device, num_tokens=100, temperature=0.0,
                 patch=None, num_patch_positions=3, stop_at_eot=True, clean=True,
                 patch_offset=0, patch_anchor="goal"):
    """
    Genera la respuesta a `instruction`, opcionalmente con parche aditivo.

    Devuelve UN solo turno: corta en <|eot_id|> y, como red de seguridad para
    el caso en que el parche suprima el eot, trunca el texto en la fuga de rol.
    """
    sm = build_suffix_manager(tokenizer, instruction, target="")
    tokens = sm.get_input_ids().to(device)
    embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()
    if patch is None:
        input_embeds = embeds[:, : sm._assistant_role_slice.stop, :]
    else:
        input_embeds = apply_patch_first_n(sm, embeds, patch, num_patch_positions,
                                           offset=patch_offset, anchor=patch_anchor)
        input_embeds = input_embeds[:, : sm._assistant_role_slice.stop, :]
    stop = stop_token_ids(tokenizer) if stop_at_eot else None
    text = tokenizer.decode(generate(model, input_embeds, num_tokens, temperature, stop),
                            skip_special_tokens=True)
    return truncate_at_role_leak(text) if clean else text


@torch.no_grad()
def nll_of_target(model, tokenizer, instruction, target, device,
                  patch=None, num_patch_positions=3, head_k=5, patch_offset=0,
                  patch_anchor="goal"):
    """
    Cross-entropy por token del `target` bajo el modelo, con o sin parche.

    Devuelve {"all", "head", "tail", "n"}.

    El corte head/tail importa: esto se mide con teacher forcing, o sea que el
    modelo ve el prefijo frances correcto en cada paso. El costo de CAMBIAR de
    idioma se paga una sola vez, en los primeros tokens; despues "continua esta
    oracion en frances" es trivial para el modelo. Promediar sobre toda la
    respuesta diluye la señal ~7x (2-3 tokens de decision sobre ~20).

    head = primeros head_k tokens -> ahi vive la decision de idioma
    tail = el resto              -> costo de continuacion, casi insensible al parche
    """
    import torch.nn as nn

    sm = build_suffix_manager(tokenizer, instruction, target=target)
    tokens = sm.get_input_ids().to(device)
    target_tokens = tokens[sm._target_slice].to(device)
    embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()
    if patch is not None:
        embeds = apply_patch_first_n(sm, embeds, patch, num_patch_positions,
                                     offset=patch_offset, anchor=patch_anchor)
    logits = model(inputs_embeds=embeds).logits
    ls = sm._loss_slice
    n = min(ls.stop - ls.start, len(target_tokens))
    nan = float("nan")
    if n <= 0:
        return {"all": nan, "head": nan, "tail": nan, "n": 0}
    per_tok = nn.CrossEntropyLoss(reduction="none")(
        logits[0, ls.start:ls.start + n, :], target_tokens[:n]
    )
    k = min(head_k, n)
    return {
        "all": per_tok.mean().item(),
        "head": per_tok[:k].mean().item(),
        "tail": per_tok[k:].mean().item() if n > k else nan,
        "n": int(n),
    }
