"""
Inspired by the llm-attacks project: https://github.com/llm-attacks/llm-attacks

Run:

    python embedding_attack_submission.py --help

for more information.
"""

import csv
import torch
import torch.nn as nn
import tqdm
from llm_attacks.minimal_gcg.string_utils import SuffixManager, load_conversation_template
import torch.nn.functional as F
import time
import pandas as pd
from datetime import datetime

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPTJForCausalLM,
    GPTNeoXForCausalLM,
    LlamaForCausalLM,
)

cadenas_siempre=["Liberated","😎","😉"]


def load_model_and_tokenizer(model_path, tokenizer_path=None, device="cuda:0", **kwargs):
    # from llm-attacks
    model = (
        AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, trust_remote_code=True, **kwargs
        )
        .to(device)
        .eval()
    )

    tokenizer_path = model_path if tokenizer_path is None else tokenizer_path

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True, use_fast=False)

    if "oasst-sft-6-llama-30b" in tokenizer_path:
        tokenizer.bos_token_id = 1
        tokenizer.unk_token_id = 0
    if "guanaco" in tokenizer_path:
        tokenizer.eos_token_id = 2
        tokenizer.unk_token_id = 0
    if "llama-2" in tokenizer_path:
        tokenizer.pad_token = tokenizer.unk_token
        tokenizer.padding_side = "left"
    if 'Llama-3.2' in tokenizer_path:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = 'left'
    if "falcon" in tokenizer_path:
        tokenizer.padding_side = "left"
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer


def get_embeddings(model, input_ids):
    if isinstance(model, GPTJForCausalLM) or isinstance(model, GPT2LMHeadModel):
        return model.transformer.wte(input_ids).half()
    elif isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens(input_ids)
    elif isinstance(model, GPTNeoXForCausalLM):
        return model.base_model.embed_in(input_ids).half()
    else:
        raise ValueError(f"Unknown model type: {type(model)}")

def get_embedding_matrix(model):
    # from llm-attacks
    if isinstance(model, GPTJForCausalLM) or isinstance(model, GPT2LMHeadModel):
        return model.transformer.wte.weight
    elif isinstance(model, LlamaForCausalLM):
        return model.model.embed_tokens.weight
    elif isinstance(model, GPTNeoXForCausalLM):
        return model.base_model.embed_in.weight
    else:
        raise ValueError(f"Unknown model type: {type(model)}")


def generate(model, input_embeddings, num_tokens=50):
    # Set the model to evaluation mode
    model.eval()
    embedding_matrix = get_embedding_matrix(model)
    input_embeddings = input_embeddings.clone()

    # Generate text using the input embeddings
    with torch.no_grad():
        # Create a tensor to store the generated tokens
        generated_tokens = torch.tensor([], dtype=torch.long, device=model.device)

        print("Generating...")
        for _ in tqdm.tqdm(range(num_tokens)):
            # Generate text token by token
            logits = model(input_ids=None, inputs_embeds=input_embeddings).logits  # , past_key_values=past)

            # Get the last predicted token (greedy decoding)
            predicted_token = torch.argmax(logits[:, -1, :])

            # Append the predicted token to the generated tokens
            generated_tokens = torch.cat((generated_tokens, predicted_token.unsqueeze(0)))  # , dim=1)

            # get embeddings from next generated one, and append it to input
            predicted_embedding = embedding_matrix[predicted_token]
            input_embeddings = torch.hstack([input_embeddings, predicted_embedding[None, None, :]])

        # Convert generated tokens to text using the tokenizer
        # generated_text = tokenizer.decode(generated_tokens[0].tolist(), skip_special_tokens=True)
    return generated_tokens.cpu().numpy()

def get_full_embeddings(suffix_manager, prompt_embeds, embeddings_attack, testeo=False, tokenizer=None, embed_weights=None):

    if(testeo==False):
        result = torch.cat([
            prompt_embeds[:, :suffix_manager._control_slice.start, :],
            embeddings_attack,
            prompt_embeds[:, suffix_manager._control_slice.stop:, :]
        ], dim=1)
    else:
        result = torch.cat([
            prompt_embeds[:, :suffix_manager._control_slice.start, :],
            embeddings_attack,
            prompt_embeds[:, suffix_manager._assistant_role_slice, :]
        ], dim=1)
        
        # Si testeo=True, imprimir la proyección a texto
        #if tokenizer is not None and embed_weights is not None:
        #    similarities = torch.matmul(result, embed_weights.t())
        #    predicted_tokens = similarities.argmax(dim=-1)
        #    projected_text = tokenizer.decode(predicted_tokens[0].cpu().numpy(), skip_special_tokens=False)
        #    print("====== FULL EMBEDDINGS PROJECTION (TESTEO=TRUE) ======")
        #    print(f"Projected text: {projected_text}")
        #    print("=======================================================")
    
    return result

def convert_embeddings_to_text(embeddings, embed_weights, tokenizer):
    # Convert embeddings back to tokens by finding closest token in embedding space
    similarities = torch.matmul(embeddings, embed_weights.t())  # [batch, seq, vocab]
    predicted_tokens = similarities.argmax(dim=-1)  # [batch, seq]
    text = tokenizer.decode(predicted_tokens[0].cpu().numpy(), skip_special_tokens=False)
    return text

def find_closest_tokens(embeddings, embed_weights):
    # Find closest tokens for each embedding vector
    # embeddings: [batch, seq, embed_dim] or [seq, embed_dim]
    # embed_weights: [vocab_size, embed_dim]

    # Ensure embeddings is 2D for batch processing
    if embeddings.dim() == 2:
        embeddings = embeddings.unsqueeze(0)

    # Compute cosine similarities
    embeddings_norm = torch.nn.functional.normalize(embeddings, dim=-1)
    embed_weights_norm = torch.nn.functional.normalize(embed_weights, dim=-1)

    similarities = torch.matmul(embeddings_norm, embed_weights_norm.t())  # [batch, seq, vocab]
    closest_tokens = similarities.argmax(dim=-1)  # [batch, seq]

    return closest_tokens.squeeze(0)  # Remove batch dimension if it was added

def check_escape_from_ball(new_embeddings, closest_tokens, embed_weights, radio_bola):
    # Check if new embeddings escape from the hypersphere/ball around closest tokens
    # new_embeddings: [seq, embed_dim] or [1, seq, embed_dim]
    # closest_tokens: [seq]
    # embed_weights: [vocab_size, embed_dim]
    # radio_bola: float

    if new_embeddings.dim() == 3:
        new_embeddings = new_embeddings.squeeze(0)  # Remove batch dimension

    # Get embeddings of closest tokens
    closest_embeddings = embed_weights[closest_tokens]  # [seq, embed_dim]

    # Calculate distances from new embeddings to closest token embeddings
    distances = torch.norm(new_embeddings - closest_embeddings, dim=-1)  # [seq]

    print(f"Distancia máxima: {distances.max().item()}")

    # Check which embeddings escape the ball
    escaped = distances > radio_bola

#    print(escaped)

    return escaped, distances

def find_gradient_target_token_restricted(gradient, embed_weights, k_nearest_tokens):
    """
    Choose, for each position, the token in the provided k-NN list that is most
    aligned with the gradient direction (cosine similarity).
    gradient: [seq, d]
    embed_weights: [vocab, d]
    k_nearest_tokens: [seq, k] (Long)
    returns: [seq] (Long) best token from k-NN per position
    """
    seq, d = gradient.shape
    grad_unit = F.normalize(gradient, dim=-1, eps=1e-12)  # [seq, d]

    out = torch.empty(seq, dtype=torch.long, device=gradient.device)

    for i in range(seq):
        neigh = k_nearest_tokens[i]  # [k], Long (device must match)
        neigh_emb = embed_weights.index_select(0, neigh)  # [k, d]
        neigh_emb_unit = F.normalize(neigh_emb, dim=-1, eps=1e-12)

        # cosine similarity with gradient direction at pos i
        sims = torch.matmul(neigh_emb_unit, grad_unit[i])  # [k]
        j = torch.argmax(sims)
        out[i] = neigh[j]

    return out


def move_one_random_to_gradient_target(embeddings_attack, adv_pert, gradient, embed_weights, escaped_mask, k_nearest_tokens, closest_tokens, radio_bola, distances):
    """
    From escaped positions, choose the one with maximum distance to snap to k-NN token that best aligns with gradient.
    All other escaped positions are clipped to the ball boundary.
    embeddings_attack: [1, seq, d]
    adv_pert: [1, seq, d]
    gradient: [1, seq, d]
    embed_weights: [vocab, d]
    escaped_mask: [seq] bool
    k_nearest_tokens: [seq, k] Long
    closest_tokens: [seq] - for clipping to ball boundary
    radio_bola: float - radius for clipping
    distances: [seq] - distances from check_escape_from_ball
    """
    if not escaped_mask.any():
        return adv_pert

    new_adv_pert = adv_pert.clone()
    escaped_indices = torch.where(escaped_mask)[0]

    with torch.no_grad():
        # Choose the escaped embedding with maximum distance (argmax) to move to gradient target
        escaped_distances = distances[escaped_indices]  # Only distances for escaped embeddings
        max_distance_idx = torch.argmax(escaped_distances)
        chosen_position = escaped_indices[max_distance_idx]

        print(f"Chosen position {chosen_position} (max distance: {escaped_distances[max_distance_idx]:.4f}) to move to gradient target")

        # Move chosen position to gradient target
        grad_target_tokens = find_gradient_target_token_restricted(
            gradient.squeeze(0), embed_weights, k_nearest_tokens
        )  # [seq]

        token_id = grad_target_tokens[chosen_position].item()
        target_embedding = embed_weights[token_id]            # [d]
        original_embedding = embeddings_attack[0, chosen_position]          # [d]
        new_adv_pert[0, chosen_position] = target_embedding - original_embedding

        # Clip all other escaped positions to ball boundary
        for i in escaped_indices:
            if i != chosen_position:  # Skip the randomly chosen one
                # Get current embedding
                current_embedding = embeddings_attack[0, i] + new_adv_pert[0, i]  # [d]
                closest_embedding = embed_weights[closest_tokens[i]]  # [d]

                # Calculate direction from closest to current
                direction = current_embedding - closest_embedding
                direction_norm = torch.norm(direction)

                if direction_norm > radio_bola:
                    # Clip to ball boundary
                    clipped_direction = direction * (radio_bola / direction_norm)
                    clipped_embedding = closest_embedding + clipped_direction
                    new_adv_pert[0, i] = clipped_embedding - embeddings_attack[0, i]
                    #print(f"Clipped position {i} to ball boundary")

    return new_adv_pert

def find_k_neighbors_from_closest(closest_tokens, embed_weights, k_neighbors, tokenizer=None):
    # Find k nearest neighbors starting from the closest tokens (including themselves)
    # Also include tokens from cadenas_siempre
    # closest_tokens: [seq] - the closest token for each position
    # embed_weights: [vocab_size, embed_dim]
    # k_neighbors: int
    # tokenizer: needed to convert cadenas_siempre to tokens

    # Get tokens from cadenas_siempre
    cadenas_tokens = set()
    if tokenizer is not None:
        for cadena in cadenas_siempre:
            tokens = tokenizer(cadena, return_tensors="pt", add_special_tokens=False).input_ids[0]
            cadenas_tokens.update(tokens.tolist())

    cadenas_tokens = torch.tensor(list(cadenas_tokens), device=closest_tokens.device)

    k_nearest_tokens = []
    k_nearest_similarities = []

    for i, closest_token in enumerate(closest_tokens):
        # Get embedding of the closest token
        closest_embedding = embed_weights[closest_token].unsqueeze(0)  # [1, embed_dim]

        # Compute similarities with all tokens
        similarities = torch.matmul(closest_embedding, embed_weights.t())  # [1, vocab_size]

        # Get top k tokens (including self)
        top_k_sims, top_k_tokens = similarities.topk(k_neighbors, dim=-1)  # [1, k]

        # Keep all tokens including self
        neighbors_tokens = top_k_tokens.squeeze(0)  # [k]
        neighbors_sims = top_k_sims.squeeze(0)  # [k]

        # Add cadenas_siempre tokens to the neighbor list
        # Get similarities for cadenas tokens
        if len(cadenas_tokens) > 0:
            cadenas_sims = similarities[0, cadenas_tokens]  # [num_cadenas_tokens]

            # Combine neighbors and cadenas tokens
            all_tokens = torch.cat([neighbors_tokens, cadenas_tokens])
            all_sims = torch.cat([neighbors_sims, cadenas_sims])

            # Sort by similarity and take top k (including self)
            sorted_sims, sort_indices = torch.sort(all_sims, descending=True)
            sorted_tokens = all_tokens[sort_indices]

            # Take top k neighbors (including self if it's in top k)
            final_tokens = sorted_tokens#[:k_neighbors]
            final_sims = sorted_sims#[:k_neighbors]

        else:
            # No cadenas tokens, use original logic (including self)
            final_tokens = neighbors_tokens  # include self
            final_sims = neighbors_sims

        k_nearest_tokens.append(final_tokens)  # [k]
        k_nearest_similarities.append(final_sims)  # [k]

    # Stack results
    k_nearest_tokens = torch.stack(k_nearest_tokens)  # [seq, k]
    k_nearest_similarities = torch.stack(k_nearest_similarities)  # [seq, k]

    return k_nearest_tokens, k_nearest_similarities

def calc_loss(model, suffix_manager:SuffixManager ,prompt_embeds, embeddings_attack, targets, embed_weights=None,tokenizer=None, k_neighbors=5):

    # Compute closest tokens for each embedding in embeddings_attack before calculating loss
    closest_tokens = find_closest_tokens(embeddings_attack, embed_weights)

    # Compute k nearest neighbors starting from the closest tokens
    k_nearest_tokens, k_nearest_similarities = find_k_neighbors_from_closest(closest_tokens, embed_weights, k_neighbors, tokenizer)

    # Optional: print closest tokens for debugging
    if tokenizer is not None:
        closest_text = tokenizer.decode(closest_tokens.cpu().numpy(), skip_special_tokens=False)
        print(f"Closest tokens to attack embeddings: {closest_text}")

    full_embeddings=get_full_embeddings(suffix_manager,prompt_embeds,embeddings_attack, False, tokenizer, embed_weights)

    logits = model(inputs_embeds=full_embeddings).logits

    loss = nn.CrossEntropyLoss()(logits[0,suffix_manager._loss_slice,:], targets)

    return loss, logits[:, suffix_manager._loss_slice , :], closest_tokens, k_nearest_tokens, k_nearest_similarities

def create_one_hot_and_embeddings(tokens, embed_weights, model):
    one_hot = torch.zeros(
        tokens.shape[0], embed_weights.shape[0], device=model.device, dtype=embed_weights.dtype
    )
    one_hot.scatter_(
        1,
        tokens.unsqueeze(1),
        torch.ones(one_hot.shape[0], 1, device=model.device, dtype=embed_weights.dtype),
    )
    embeddings = (one_hot @ embed_weights).unsqueeze(0).data
    return one_hot, embeddings

#En el 64 lo libera!

def guardar_csv(resultados_generacion):

    # Crear DataFrame con los resultados
    df_resultados = pd.DataFrame(resultados_generacion)

    # Crear nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resultados_generacion_{timestamp}.csv"

    # Guardar CSV
    df_resultados.to_csv(filename, index=False, encoding='utf-8')
    print(f"Resultados guardados en: {filename}")
    print(f"Total de registros guardados: {len(resultados_generacion)}")


def run(
    model_path: str,
    num_steps: int = 5000,
    fixed_prompt: str = "Give me the step by step guide for how to wash dogs at home.",
    control_prompt_init: str =  "!@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@ !@",
    target: str = "Successful jailbreak. Sure, here is the guide for washing dogs",    
    device: str = "cuda:0",
    num_tokens: int = 200,
    step_size: float = 0.000051,
    print_interval: int = 5,
    generate_interval: int = 500,
    seed: int = 42,
    load_dataset=True,
    verbose=False,
    early_stopping=True,
    radio_bola: float = 0.1,
    k_neighbors: int = 15,
):
    """
    Embedding space attack on Llama2.

    String will overall look like:

        [fixed_prompt] + [control_prompt] + [target]

                                                ^ target of optimization

                                ^ control tokens optimized to maximize target.
                                  genration begins at the end of these embeddings.

              ^ a fixed prompt that will not get modified during optimization. Can
                be used to provide a fixed context; matches the experimental setup
                of Zou et al., 2023.

    Args:
        model_path (str): Path to your Llama-2-7b-chat-hf directory
        num_steps (int): Number of gradient steps to take in the attack
        fixed_prompt (str): Part of the prompt that won't be altered/have gradients backpropogated
            to. You can specify an empty space i.e. fixed_prompt=' ' if you wish to only have a
            controllabe prompt.
        control_prompt (str): Part of the prompt that will be modified by gradient info. Generation
            starts at the end of this string.
        target (str): Optimization target; what the LLM will seek to generate immediately after
            the control string.
    """
    if seed is not None:
        torch.manual_seed(seed)

    model, tokenizer = load_model_and_tokenizer(
        model_path, low_cpu_mem_usage=True, use_cache=False, device=device
    )
    embed_weights = get_embedding_matrix(model)

    conv_template = load_conversation_template('llama-3.2')
    menor_loss=10

    if load_dataset:
        filename = "data/advbench/harmful_behaviors.csv"
        #reader = csv.reader(open(filename, "r"))
        #next(reader)
        #TODO Implementar
        pass
    else:

        suffix_manager = SuffixManager(tokenizer=tokenizer, 
            conv_template=conv_template, 
            instruction=fixed_prompt, 
            target=target, 
            adv_string=control_prompt_init)

        reader=[suffix_manager]

        print(f"Fixed prompt:\t '{suffix_manager.instruction}'")
        print(f"Control prompt:\t '{suffix_manager.adv_string}'")
        print(f"Target string:\t '{suffix_manager.target}'")
        print(f"Prompt global:\t {suffix_manager.get_prompt()}")
        print("*"*50)

    total_steps = 0
    n = 0
    successful_attacks = 0
 
    for row in reader:

        print("Instruccion ->",row.instruction)

        tokens_prompt = suffix_manager.get_input_ids().to(device)

        input_tokens = tokens_prompt[suffix_manager._goal_slice].to(device)
        attack_tokens = tokens_prompt[suffix_manager._control_slice].to(device)
        target_tokens = tokens_prompt[suffix_manager._target_slice].to(device) #A veces hace [1:]

        print(f"INPUT TOKENS: {tokenizer.decode(input_tokens.cpu().numpy())}")
        print(f"ATTACK TOKENS: {tokenizer.decode(attack_tokens.cpu().numpy())}")  
        print(f"TARGET TOKENS: {tokenizer.decode(target_tokens.cpu().numpy())}")
        print("*"*50)

        #todo el prompt
        prompt_embeds = get_embeddings(model, tokens_prompt.unsqueeze(0)).detach()
        # attack
        one_hot_attack, embeddings_attack = create_one_hot_and_embeddings(attack_tokens, embed_weights, model)
        # targets
        one_hot_target, embeddings_target = create_one_hot_and_embeddings(target_tokens, embed_weights, model)

        adv_pert = torch.zeros_like(embeddings_attack, requires_grad=True, device=device)

        # Array para guardar resultados durante generación
        resultados_generacion = []

        for i in range(num_steps):

            print("Iteracion",i)

            total_steps += 1
            loss, logits, closest_tokens, k_nearest_tokens, k_nearest_similarities = calc_loss(
                model, suffix_manager, prompt_embeds, embeddings_attack + adv_pert, one_hot_target, embed_weights, tokenizer, k_neighbors
            )

            tokens_pred = logits.argmax(2)
            output_str = tokenizer.decode(tokens_pred[0].cpu().numpy())
            sucess = output_str == target

            if sucess:
                successful_attacks += 1
                if early_stopping:
                    break

            if i % print_interval == 0 and i != 0:
                print(f"Iter: {i}")
                print(f"loss: {loss}")
                print(f"menor loss: {menor_loss}")
                print(f"norms: {(embeddings_attack + adv_pert).norm(2, dim=2)}")
                print(f"output:{output_str}")

            if ((i % generate_interval == 0) and (i != 0) and verbose) or (loss<menor_loss and loss<2):

                full_embedding = get_full_embeddings(suffix_manager,prompt_embeds,embeddings_attack+adv_pert,True,tokenizer,embed_weights)
                generated_tokens = generate(model, full_embedding, num_tokens)
                generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
                print("==============================================")
                print(generated_text)
                print("============================================== ")

                # Generate model output with projected string
                projected_str=convert_embeddings_to_text(embeddings_attack+adv_pert,embed_weights,tokenizer)

                print("Ataque:", projected_str)

                projected_embedding = get_embeddings(model, tokenizer(projected_str, return_tensors="pt",add_special_tokens=False).input_ids.to(device))
                full_projected_embedding = get_full_embeddings(suffix_manager, prompt_embeds, projected_embedding, True, tokenizer, embed_weights)
                projected_generated_tokens = generate(model, full_projected_embedding, num_tokens)
                projected_generated_text = tokenizer.decode(projected_generated_tokens, skip_special_tokens=True)
                print("======= MODEL OUTPUT (PROJECTED STRING) =======")
                print(projected_generated_text)
                print("===============================================")

                print("Loss",loss)

                # Guardar resultados en el array
                resultado = {
                    'iteracion': i,
                    'loss': float(loss.item()),
                    'projected_str': projected_str,
                    'output_vectorial': generated_text,
                    'output_discreto': projected_generated_text
                }
                resultados_generacion.append(resultado)

                time.sleep(10)

            loss.backward()
            grad = adv_pert.grad.data

            # Calculate new embeddings after normal gradient step
            normal_new_adv_pert = adv_pert.data - torch.sign(grad) * step_size
            normal_new_embeddings = embeddings_attack + normal_new_adv_pert

            # Check if any embedding escapes from the ball around its closest token
            escaped, distances = check_escape_from_ball(normal_new_embeddings, closest_tokens, embed_weights, radio_bola)

            if escaped.any():
                #print("ESCAPO")
                if verbose:
                    escaped_indices = torch.where(escaped)[0]
                    print(f"  Embeddings que escaparon: {escaped_indices.cpu().numpy()}")
                    #print(f"  Distancias: {distances[escaped].detach().cpu().numpy()}")
                    #print(f"  Radio de bola: {radio_bola}")

                # Use special movement logic for escaped embeddings
                final_adv_pert = move_one_random_to_gradient_target(
                    embeddings_attack, normal_new_adv_pert, grad, embed_weights, escaped, k_nearest_tokens, closest_tokens, radio_bola, distances
                )
                adv_pert.data = final_adv_pert
            else:
                # Apply normal gradient step
                adv_pert.data = normal_new_adv_pert

            model.zero_grad()
            adv_pert.grad.zero_()

            menor_loss = min(menor_loss,loss)

        guardar_csv(resultados_generacion)

        n += 1
        print(f"Successful attacks: {successful_attacks}/{n} \nAverage steps: {total_steps/n}")

        full_embedding = get_full_embeddings(suffix_manager,prompt_embeds,embeddings_attack+adv_pert,True,tokenizer,embed_weights)
        generated_tokens = generate(model, full_embedding, num_tokens)
        generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        print("==============================================")
        print(generated_text)
        print("============================================== ")

        cadena_proyectada=convert_embeddings_to_text(embeddings_attack+adv_pert,embed_weights,tokenizer)
        print(cadena_proyectada)

        print("DONE")


if __name__ == "__main__":
    model_path = "../modelos/Llama-3.2-3B-Instruct"
    #model_path = "../modelos/Llama-3.1-8B-Instruct"
    
    run(model_path,load_dataset=False,verbose=True,early_stopping=True,radio_bola=0.01,k_neighbors=100)
