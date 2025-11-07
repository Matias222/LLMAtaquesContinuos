from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "../modelos/vicuna"

tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,   # or "auto" if you have multiple GPUs
    device_map="auto"
)

prompt = "Hello! What can you do?"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))