from flask import Flask, jsonify, request, render_template
from model import generar, procesar_texto, parafrasear_parrafo, resumir_parrafo, explicar, reescribir, sugerenciaPersonalizada
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/saludo", methods=['GET'])
def saludo():
    return jsonify({'mensaje': 'Hola desde Flask'})

@app.route("/api/sugerencia", methods=["POST"])
def responder():
    try:
        data = request.get_json()
        texto = data.get("texto", "")

        if not isinstance(texto, str):
            return jsonify({ 'error': 'Texto inválido' }), 400

        if texto.strip() == "":
            return jsonify({ 'respuesta': 'No hay contenido suficiente para sugerir.' })

        resumenes, proposito_ultimo, ultima_frase = procesar_texto(texto)
        respuesta = generar(resumenes, proposito_ultimo, ultima_frase)
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        print('Error en /api/sugerencia:', e)
        return jsonify({ 'error': 'Ocurrió un error en el servidor' }), 500

@app.route("/api/acciones", methods=["POST"])
def acciones():
    try:
        data = request.get_json()

        texto = data.get("texto","")
        textoSeleccionado = data.get("textoSeleccionado", "")
        accion = data.get("accion", "").lower()
        instruccion = data.get("instruccion", "")
        
        if not textoSeleccionado.strip():
            return jsonify({ "error": "Texto vacío" }), 400
        if not texto.strip():
            return jsonify({ "error": "Texto vacío" }), 400
        if not accion:
            return jsonify({ "error": "Acción requerida" }), 400


        if accion == "parafrasear":
            respuesta = parafrasear_parrafo(textoSeleccionado, instruccion)
        elif accion == "resumir":
            respuesta = resumir_parrafo(textoSeleccionado, instruccion)
        elif accion == "explicar":
            respuesta = explicar(textoSeleccionado, instruccion)
        elif accion == "reescribir":
            resumenes, proposito_ultimo, ultima_frase = procesar_texto(texto)
            respuesta = reescribir(resumenes,proposito_ultimo, textoSeleccionado, instruccion)
        elif accion == "sugerir":
            resumenes, proposito_ultimo, ultima_frase = procesar_texto(textoSeleccionado)
            respuesta = sugerenciaPersonalizada(resumenes, proposito_ultimo, textoSeleccionado, instruccion)
        else:
            return jsonify({ "error": f"Acción '{accion}' no soportada" }), 400

        return jsonify({ "respuesta": respuesta })

    except Exception as e:
        print('Error en /api/accion-texto:', e)
        return jsonify({ "error": "Error interno del servidor" }), 500

@app.route("/api/set_model", methods=["POST"])
def seleccionar_modelo():
    try:    
        data = request.json
        nuevo_modelo = data["modelo"]
        from config import __dict__ as config_vars
        config_vars["modelo_actual"] = nuevo_modelo
        print(f'Modelo actualizado a{nuevo_modelo}')
        return jsonify({"status": "modelo actualizado", "modelo": nuevo_modelo})

    except Exception as e:
        print('Error en /api/set_model:', e)
        return jsonify({ 'error': 'Ocurrió un error en el servidor' }), 500


if __name__ == "__main__":
    app.run(debug=True)