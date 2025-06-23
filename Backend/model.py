import requests 
import hashlib
import config

# OLLAMA
def ollama(prompt, modelo):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": modelo,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        print("Error:", response.status_code)
        print(response.text)
        return None

# MÉTODOS LLMs
def generar(contexto, proposito_ultimo, ultima_frase, palabras=150):
    prompt = (
        f"A partir del siguiente contexto y propósito, continúa el texto comenzando desde la última frase proporcionada. "
        f"Debes mantener el estilo, el tono y la coherencia del texto original.\n\n"

        f"### CONTEXTO (resumen de los párrafos anteriores):\n{contexto}\n\n"
        f"### PROPÓSITO del último párrafo:\n{proposito_ultimo}\n\n"
        f"### TEXTO PARA CONTINUAR CON LA SUGERENCIA:\n{ultima_frase.strip()}\n\n"

        f"Instrucciones estrictas para la respuesta:\n"
        f"- Continúa el texto directamente desde donde termina la frase anterior.\n"
        f"- No repitas la frase dada ni empieces desde el principio.\n"
        f"- No uses explicaciones, etiquetas, comillas, ni ningún comentario adicional.\n"
        f"- Mantén la respuesta en el mismo idioma.\n"
        f"- Usa como máximo {palabras} palabras.\n"
        f"- La continuación puede ser una o más frases naturales según el flujo del texto.\n"
        f"- Mantén el mismo tono, estilo y tema.\n"
        f"- Responde solo con la continuación del texto.\n"
    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print(f"Enviando sugerencia...")
    return response

def mainidea(texto, palabras=100):
    print("Obteniendo idea principal...")
    prompt = (
        "- Extrae únicamente la idea principal del siguiente párrafo.\n"
        f"### PÁRRAFO DE ENTRADA:\nf{texto}\n\n"

        f"Instrucciones estrictas para la respuesta:\n"
        "- El resultado debe ser una sola oración natural, clara y coherente.\n"
        "- No incluyas razonamientos, explicaciones, ni justificación.\n"
        "- No uses comillas, markdown, encabezados, ni etiquetas.\n"
        "- El texto de salida debe estar en el MISMO idioma que el original.\n"
        f"- Limita la respuesta a un máximo de {palabras} palabras.\n\n"
    ) 
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto resumido...")
    return response

def proposito(texto, palabras=50):
    print("Obteniendo contexto...")
    prompt = (
        "- Analiza el siguiente párrafo y determina su propósito o intención principal.\n"
        f"### PÁRRAFO DE ENTRADA:\n{texto}\n\n"

        f"Instrucciones estrictas para la respuesta:\n"
        "- Devuelve una única oración clara y concisa que describa lo que el autor intenta lograr con el párrafo.\n"
        "- No incluyas explicaciones, comentarios ni razonamientos.\n"
        "- No uses comillas, markdown ni ningún formato adicional.\n"
        f"- Máximo: {palabras} palabras.\n"
        "- Mantén el idioma original del texto.\n\n"
    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando contexto...")
    return response


def resumir_parrafo(texto, prompt_usuario, palabras=50):
    print("Resumiendo texto...")
    prompt = (
        f"-Considera de mayor importancia el prompt del usuario {prompt_usuario}"
        "- Resume el siguiente párrafo de forma natural, clara y coherente.\n"
        f"### PÁRRAFO DE ENTRADA:\n{texto}\n\n"

        f"Instrucciones estrictas para la respuesta:\n"
        "- El resumen debe transmitir la esencia del contenido, evitando repeticiones o detalles secundarios.\n"
        "- No incluyas razonamientos, explicaciones ni comentarios.\n"
        "- No uses comillas, markdown ni ningún formato adicional.\n"
        f"- Máximo: {palabras} palabras.\n"
        "- El texto de salida debe estar en el MISMO idioma que el original.\n\n"

    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto resumido...")
    return response

def parafrasear_parrafo(texto, prompt_usuario):
    print("Parafraseando párrafo...")

    prompt = (
    f"-Considera de mayor importancia el prompt del usuario {prompt_usuario}"
    "- Parafrasea el siguiente párrafo utilizando un lenguaje distinto, manteniendo el mismo significado y tono.\n"
    f"### TEXTO A PARAFRASEAR:\n{texto}\n\n"

    f"Instrucciones estrictas para la respuesta:\n"
    "- Emplea estructuras gramaticales variadas y sinónimos adecuados.\n"
    "- No copies frases textuales del original.\n"
    "- No agregues ideas nuevas ni omitas partes clave.\n"
    "- Respeta la intención del texto (formal, técnico, narrativo, etc.).\n"
    "- No uses comillas, encabezados, markdown ni explicaciones.\n"
    "- El texto resultante debe estar en el MISMO idioma que el original.\n\n"
)
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto parafraseado...")
    return response

def reescribir(resumenes, proposito, texto, prompt_usuario):
    print("Reescribiendo con estilo mejorado...")

    prompt = (
    f"-Considera de mayor importancia el prompt del usuario {prompt_usuario}"
    f"A partir del siguiente contexto y propósito. "
    f"### CONTEXTO (resumen de los párrafos anteriores):\n{resumenes}\n\n"
    f"### PROPOSITO DEL TEXTO ACTUAL:\n{proposito}\n\n"

    "- Reescribe el siguiente texto para que sea más claro, natural y profesional.\n"
    f"Debes mantener el estilo, el tono y la coherencia del texto original.\n\n"
    f"### TEXTO A REESCRIBIR:\n{texto}\n\n"

    f"Instrucciones estrictas para la respuesta:\n"
    "- Corrige errores gramaticales, ortográficos y de puntuación.\n"
    "- Mejora la fluidez y estilo sin cambiar el significado original.\n"
    "- Mantén la intención, tono y contenido del texto.\n"
    "- No elimines ni agregues información.\n"
    "- No uses comillas, encabezados, markdown ni explicaciones.\n"
    "- El resultado debe estar en el MISMO idioma que el texto original.\n\n"
)
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto reescrito...")
    return response

def explicar(texto, prompt_usuario):
    print("Explicando en lenguaje sencillo...")

    prompt = (
        f"-Considera de mayor importancia el prompt del usuario {prompt_usuario}"
        "- Explica el siguiente texto de forma clara, sencilla y accesible.\n"
        f"### TEXTO A EXPLICAR:\n{texto}\n\n"

        f"Instrucciones estrictas para la respuesta:\n"
        "- Reformula las ideas usando un lenguaje cotidiano, comprensible para cualquier persona sin conocimientos previos.\n"
        "- Usa frases cortas y ejemplos si ayuda a la comprensión.\n"
        "- Simplifica términos técnicos o abstractos sin perder el sentido del mensaje original.\n"
        "- No repitas el texto literalmente.\n"
        "- No agregues opiniones, explicaciones meta ni juicios personales.\n"
        "- No uses comillas, encabezados ni formato adicional.\n"
        "- Mantén el idioma del texto original.\n\n"
    )

    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto explicado...")
    return response

def sugerenciaPersonalizada(contexto, proposito_ultimo, texto,prompt_usuario, palabras=150):
    prompt = (
        f"A partir del siguiente contexto y propósito, continúa el texto comenzando desde la última frase proporcionada. "
        f"Debes mantener el estilo, el tono y la coherencia del texto original.\n\n"

        f"### CONTEXTO (resumen de los párrafos anteriores):\n{contexto}\n\n"
        f"### PROPÓSITO del último párrafo:\n{proposito_ultimo}\n\n"
        f"### TEXTO PARA CONTINUAR CON LA SUGERENCIA:\n{texto.strip()}\n\n"
        f"### CONSIDERA EN LA SUGERENCIA LA INSTRUCCIÓN {prompt_usuario}"

        f"Instrucciones estrictas para la respuesta:\n"
        f"- Continúa el texto directamente desde donde termina la frase anterior.\n"
        f"- No repitas la frase dada ni empieces desde el principio.\n"
        f"- No uses explicaciones, etiquetas, comillas, ni ningún comentario adicional.\n"
        f"- Mantén la respuesta en el mismo idioma.\n"
        f"- Usa como máximo {palabras} palabras.\n"
        f"- La continuación puede ser una o más frases naturales según el flujo del texto.\n"
        f"- Mantén el mismo tono, estilo y tema.\n"
        f"- Responde solo con la continuación del texto.\n"
    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print(f"Enviando sugerencia...")
    return response



# Lógica de Contexto
resumenes_cache = {}

def obtener_hash(texto):
    return hashlib.md5(texto.encode()).hexdigest()

def palabras_max(palabras):
    if palabras < 50:
        return 5
    elif palabras < 100:
        return 10
    elif palabras < 200:
        return 20
    else:
        return 30 

def resumir_con_cache(parrafos):
    resumen_final = []
    for i, p in enumerate(parrafos):
        hash_actual = obtener_hash(p)
        clave = f"p{i}"
        if clave in resumenes_cache and resumenes_cache[clave]["hash"] == hash_actual:
            resumen = resumenes_cache[clave]["resumen"]
            print(f"Párrafo {i} no modificado. Usando resumen cacheado.")
        else:
            palabras = palabras_max(len(p.split()))
            resumen = mainidea(p, palabras)
            resumenes_cache[clave] = {
                "hash": hash_actual,
                "resumen": resumen
            }
            print(f"Párrafo {i} modificado o nuevo. Resumen actualizado.")
        resumen_final.append(resumen.strip())
    return resumen_final


def procesar_texto(texto_completo):
    parrafos = [p.strip() for p in texto_completo.strip().split("\n") if p.strip()]
    if not parrafos:
        return "", ""

    cuerpo = parrafos[:-1]
    ultimo = parrafos[-1]

    resumenes = resumir_con_cache(cuerpo)
    proposito_ultimo = proposito(ultimo)
    
    #Ultima frase
    frases = [f.strip() for f in ultimo.strip().split(".") if f.strip()]
    ultima_frase = frases[-1] if frases else ultimo.strip()

    resumen_contexto = " ".join(resumenes)

    print(f"{resumen_contexto}\n{proposito_ultimo}{ultima_frase}\n")
    return resumen_contexto, proposito_ultimo, ultima_frase


# texto = """
# Las plantas tienen una gran diversidad de formas y funciones. A través de la fotosíntesis, convierten la luz solar en energía química, lo cual es vital para la vida en la Tierra.
# Además, son una fuente de alimento, medicina y materiales para los humanos. Su capacidad de adaptación a climas extremos demuestra su importancia ecológica.
# Es por ello que redacto este documento. Para saber la 
# """

# resumen_contexto, contexto_ultimo, ultima_frase = procesar_texto(texto)

# print(f"{resumen_contexto}\n{contexto_ultimo}\n{ultima_frase}")