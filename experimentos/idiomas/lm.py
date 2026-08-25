"""
Helpers de modelo compartidos por el experimento de idiomas.

Mismas convenciones que legacy/christmas_final_train.py y legacy/test_xmas_patch.py:
Llama-3.2 fp16, tokenizer use_fast=False, template 'llama-3.2', parche aditivo
sobre las primeras N posiciones del goal slice, generacion greedy desde embeddings.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaForCausalLM

from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template

from checkers import truncate_at_role_leak

DEFAULT_MODEL = "/home/sagemaker-user/user-default-efs/modelos/Llama-3.2-3B-Instruct"


def load_model_and_tokenizer(model_path, tokenizer_path=None, device="cuda:0", **kwargs):
    model = (
        AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, trust_remote_code=True, **kwargs
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
    return model, tokenizer


def get_embeddings(model, input_ids):
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens(input_ids)
    raise ValueError(f"Unknown model type: {type(model)}")


def get_embedding_matrix(model):
    if isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    raise ValueError(f"Unknown model type: {type(model)}")


def build_suffix_manager(tokenizer, instruction, target=""):
    return SuffixManager(
        tokenizer=tokenizer,
        conv_template=load_conversation_template("llama-3.2"),
        instruction=instruction,
        target=target,
        adv_string="",
    )


def apply_patch_first_n(suffix_manager, prompt_embeds, patch, num_patch_positions=3):
    """
    e'_i = e_i + v_i  para i en las primeras N posiciones del goal slice.

    Identico a apply_patch_to_first_n_tokens de legacy/christmas_final_train.py:
    NO promedia posiciones, preserva las K direcciones posicionales.
    """
    patched = prompt_embeds.clone()
    goal_start = suffix_manager._goal_slice.start
    goal_end = suffix_manager._goal_slice.stop
    actual = min(num_patch_positions, goal_end - goal_start)
    patched[:, goal_start:goal_start + actual, :] = (
        prompt_embeds[:, goal_start:goal_start + actual, :] + patch[:, :actual, :]
    )
    return patched


def stop_token_ids(tokenizer):
    """
    Ids que cierran el turno del assistant.

    Sin esto la generacion sigue despues de <|eot_id|> y el modelo arranca el
    turno siguiente. Como decodificamos con skip_special_tokens=True, los
    headers desaparecen pero el token de texto plano "assistant" sobrevive, y
    el resultado son varios turnos pegados en un solo string.
    """
    ids = set()
    if tokenizer.eos_token_id is not None:
        ids.add(int(tokenizer.eos_token_id))
    unk = getattr(tokenizer, "unk_token_id", None)
    for t in ("<|eot_id|>", "<|end_of_text|>"):
        try:
            i = tokenizer.convert_tokens_to_ids(t)
        except Exception:
            i = None
        if i is not None and i >= 0 and i != unk:
            ids.add(int(i))
    return ids


@torch.no_grad()
def generate(model, input_embeddings, num_tokens=100, temperature=0.0, stop_ids=None):
    """
    Generacion autoregresiva desde embeddings. temperature=0.0 => greedy.

    Corta en cuanto sale un token de `stop_ids` (fin de turno), que NO se
    incluye en la salida. Si stop_ids es None genera los num_tokens completos
    (comportamiento viejo, solo para debug).
    """
    model.eval()
    embedding_matrix = get_embedding_matrix(model)
    input_embeddings = input_embeddings.clone()
    stop_ids = set() if stop_ids is None else set(stop_ids)
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
                 patch=None, num_patch_positions=3, stop_at_eot=True, clean=True):
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
        input_embeds = apply_patch_first_n(sm, embeds, patch, num_patch_positions)
        input_embeds = input_embeds[:, : sm._assistant_role_slice.stop, :]
    stop = stop_token_ids(tokenizer) if stop_at_eot else None
    text = tokenizer.decode(generate(model, input_embeds, num_tokens, temperature, stop),
                            skip_special_tokens=True)
    return truncate_at_role_leak(text) if clean else text


@torch.no_grad()
def nll_of_target(model, tokenizer, instruction, target, device,
                  patch=None, num_patch_positions=3):
    """
    Cross-entropy por token del `target` bajo el modelo, con o sin parche.

    Metrica graduada: cuanto le cuesta al modelo producir la respuesta francesa
    de referencia. Complementa el booleano is_french.
    """
    import torch.nn as nn

    sm = build_suffix_manager(tokenizer, instruction, target=target)
    tokens = sm.get_input_ids().to(device)
    target_tokens = tokens[sm._target_slice].to(device)
    embeds = get_embeddings(model, tokens.unsqueeze(0)).detach()
    if patch is not None:
        embeds = apply_patch_first_n(sm, embeds, patch, num_patch_positions)
    logits = model(inputs_embeds=embeds).logits
    ls = sm._loss_slice
    n = min(ls.stop - ls.start, len(target_tokens))
    if n <= 0:
        return float("nan")
    return nn.CrossEntropyLoss()(
        logits[0, ls.start:ls.start + n, :], target_tokens[:n]
    ).item()
