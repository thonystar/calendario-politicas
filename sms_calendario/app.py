from flask import Flask, render_template, jsonify, request
from db import get_log_mensajeria, get_sms_programado, insertar_programacion

app = Flask(__name__)

# Pagina principal 
@app.route("/")
def index():
    return render_template("index.html")

# Traer todos los archivos del calendario
@app.route("/api/eventos")
def eventos():
    eventos = get_log_mensajeria() + get_sms_programado()
    return jsonify(eventos)

# Guardar programacion personalizada
@app.route("/api/programar", methods = ["POST"])
def programar():
    data = request.json
    insertar_programacion(data)
    return jsonify({"status": "OK"})

# Ejecutar el servidos
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    