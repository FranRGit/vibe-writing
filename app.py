from flask import Flask, jsonify, request, render_template
from model import generar, procesar_texto

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/responder", methods=["POST"])
def responder():
    data = request.get_json()
    texto = data.get("texto", "")
    resumenes, proposito_ultimo, ultima_frase = procesar_texto(texto)
    respuesta = generar(resumenes,proposito_ultimo,ultima_frase)
    return jsonify({"respuesta": respuesta})

@app.route("/api/set_model", methods=["POST"])
def seleccionar_modelo():
    data = request.json
    nuevo_modelo = data["modelo"]
    from config import __dict__ as config_vars
    config_vars["modelo_actual"] = nuevo_modelo
    return jsonify({"status": "modelo actualizado", "modelo": nuevo_modelo})

if __name__ == "__main__":
    app.run(debug=True)