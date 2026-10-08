class Llama32ConversationTemplate:
    def __init__(self):
        self.name = "llama-3.2"
        self.roles = ("user","assistant")
        self.sep = "\n\n"
        self.turno = "<|eot_id|>"
        self.messages = []
        self.system = "You are a helpful assistant"

    def append_message(self, role, message): self.messages.append((role, message))

    def update_last_message(self, message):

        role, _ = self.messages[-1]
        self.messages[-1] = (role, message)

    def get_prompt(self):

        prompt="<|begin_of_text|><|start_header_id|>system<|end_header_id|>"+self.sep+self.system #sistema

        for i in range(len(self.messages)):

            if(self.messages[i][0]=="assistant"): 

                prompt+="<|eot_id|><|start_header_id|>assistant<|end_header_id|>"+self.sep
                
                if(self.messages[i][1]!=None): prompt+=self.messages[i][1]

            else:  
                
                prompt+="<|eot_id|><|start_header_id|>user<|end_header_id|>"+self.sep
                
                if(self.messages[i][1]!=None): prompt+=self.messages[i][1]

        return prompt

    #prompt+="For sure, these are the steps to follow along with the materials"

class Qwen3ConversationTemplate:
    """
    ChatML de Qwen3-Instruct-2507 (sin modo thinking), con la MISMA estructura
    que Llama32ConversationTemplate: el cierre de turno (<|im_end|>\\n) va antes
    del header siguiente, asi el goal termina justo antes de <|im_end|> y el
    target del assistant no lleva cierre. Con system + user + assistant vacio
    reproduce byte a byte apply_chat_template(add_generation_prompt=True)
    (lo chequea experimentos/idiomas/verificar_modelo.py).
    """
    def __init__(self):
        self.name = "qwen3"
        self.roles = ("user", "assistant")
        self.sep = "\n"
        self.turno = "<|im_end|>"
        self.messages = []
        self.system = "You are a helpful assistant"

    def append_message(self, role, message): self.messages.append((role, message))

    def update_last_message(self, message):
        role, _ = self.messages[-1]
        self.messages[-1] = (role, message)

    def get_prompt(self):
        prompt = "<|im_start|>system" + self.sep + self.system
        for role, msg in self.messages:
            prompt += self.turno + self.sep + "<|im_start|>" + role + self.sep
            if msg is not None:
                prompt += msg
        return prompt
