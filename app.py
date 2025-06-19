from flask import Flask, jsonify, request, render_template
from model import generarRespuesta

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/responder", methods=["POST"])
def responder():
    data = request.get_json()
    prompt = data.get("prompt", "")
    respuesta = generarRespuesta(prompt)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True)