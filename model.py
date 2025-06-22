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
        "Continúa el texto comenzando directamente desde la siguiente frase final, manteniendo el mismo estilo de redacción, tono y coherencia temática\n\n"
        "### Resumen del texto anterior:\n"
        f"{contexto}\n\n"
        "### Propósito del último párrafo:\n"
        f"{proposito_ultimo}\n\n"
        "# Completa la siguiente frase desde donde termina, sin repetirlo y considerando el proposito:"        
        f"{ultima_frase.strip()}\n\n"
        "# IMPORTANTE:\n"
        "#  Usa como máximo en tu respuesta, un número de {palabras} palabras"
        "# - No incluyas en tu respuesta la frase final.\n"
        "# - No expliques lo anterior, simplemente continúa el texto.\n"
        "# - Mantén el mismo tono, estilo y tema.\n"
        "# - La continuación puede tener una o más frases, según lo necesite.\n"
        "# - No uses comillas ni encabezados.\n"
    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando sugerencia...")
    return response

def mainidea(texto, palabras=100):
    print("Obteniendo idea principal...")
    prompt = (
        "#Extrae solo la idea principal del siguiente párrafo de manera natural y coherente en un máximo de {palabras}.\n\n"
        "#El resumen debe estar en el MISMO idioma que el texto original."
        "# No incluyas explicaciones, comentarios ni ningún tipo de formato (como comillas o backticks).\n"
        "# Devuelve únicamente la idea principal, en el mismo idioma.\n\n"
        f"{texto}\n"
    ) 
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto resumido...")
    return response

def proposito(texto, palabras=50):
    print("Obteniendo contexto...")
    prompt = (
        f"Analiza el siguiente párrafo y describe en no más de {palabras} palabras cuál es su propósito principal o intención.\n\n"
        "# Solo devuelve el propósito que el usuario esta tratando de redactar en ese párrafo.\n"
        "# No incluyas explicaciones, opiniones ni comentarios adicionales.\n"
        "# No uses comillas ni formato extra. Solo el propósito.\n\n"
        f"{texto}\n"
    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando contexto...")
    return response


def resumir_parrafo(texto, palabras=50):
    print("Resumiendo texto...")
    prompt = (
        "Resume el siguiente párrafo de manera natural y coherente. El resumen debe estar en el MISMO idioma que el texto original.\n\n"
        "#  Usa como máximo en tu respuesta, un número de {palabras} palabras"
        "# No incluyas explicaciones, comentarios ni ningún tipo de formato (como comillas o backticks).\n"
        "# Devuelve únicamente el resumen, en el mismo idioma.\n\n"
        f"{texto}\n"
    ) 
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto resumido...")
    return response

def parafrasear_parrafo(texto, prompt_usuario):
    print("Parafraseando párrafo...")

    prompt = (
        "Parafrasea el siguiente párrafo utilizando un lenguaje diferente, con estructuras gramaticales y vocabulario variados, "
        "pero sin alterar el significado ni el tono del texto original.\n\n"
        "# Mantén el mismo mensaje.\n"
        "# Cambia la redacción (usa sinónimos, orden distinto, otras expresiones).\n"
        "# Conserve la intención original (formal/informal).\n"
        "# No agregues ideas nuevas.\n"
        "# No repitas frases tal cual.\n"
        "# No uses comillas, títulos ni explicaciones.\n\n"
        f"# {prompt_usuario}"
        f"{texto}"
    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto resumido...")
    return response

def reescribir(texto, prompt_usuario):
    print("Reescribiendo con estilo mejorado...")

    prompt = (
        "Reescribe el siguiente texto para que sea más claro, fluido y profesional. Mejora la redacción corrigiendo errores de gramática, "
        "ortografía, puntuación y estilo, manteniendo el significado original del contenido.\n\n"
        "# Mantén la intención del texto original.\n"
        "# Mejora la fluidez y claridad.\n"
        "# Usa un tono profesional, pero natural.\n"
        "# No elimines información.\n"
        "# No uses comillas, notas, ni formateo extra.\n"
        "# No expliques el texto, solo reescríbelo.\n\n"
        f"# {prompt_usuario}"
        f"{texto}"
    )
    response = ollama(prompt, modelo=config.modelo_actual)
    print("Enviando texto resumido...")
    return response

def explicar(texto, prompt_usuario):
    print("Explicando en lenguaje sencillo...")

    prompt = (
        "Explica el siguiente texto de forma clara, sencilla y accesible para cualquier persona, incluso si no tiene conocimientos previos "
        "sobre el tema. Reformula las ideas complejas usando un lenguaje cotidiano, directo y fácil de entender.\n\n"
        "# Usa frases cortas y ejemplos si es necesario.\n"
        "# Simplifica términos técnicos o abstractos.\n"
        "# Mantén el significado del texto original.\n"
        "# No uses comillas, notas ni explicaciones meta.\n"
        "# No repitas el texto tal cual.\n"
        "# No agregues opiniones o juicios.\n\n"
        f"#{prompt_usuario}"
        f"{texto}"
    )

    return ollama(prompt, modelo=config.modelo_actual)


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