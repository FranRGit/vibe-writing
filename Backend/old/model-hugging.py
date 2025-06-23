from huggingface_hub import InferenceClient
from transformers import AutoTokenizer

client = InferenceClient(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
    token=""  #Colocar token registrandose en Hugging FAce
)

def generarRespuesta(prompt):
    prompt_formateado = prompt.strip()
    respuesta = client.text_generation(
        prompt_formateado, 
        max_new_tokens=150,
        do_sample = True,
        temperature=0.3,
        top_p=0.95,
    )
    return respuesta.strip()
