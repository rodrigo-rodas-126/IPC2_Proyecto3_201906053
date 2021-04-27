from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from evento import Evento
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath("./uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

"""
@app.route('/')
def hello():
    return render_template("index.html", text=str(vuelos))


@app.route('/archivo', methods=['POST'])
def select():
    nuevo_viaje={
        "nombre": request.json['nombre'],
        "hora": request.json['hora'],
        "precio": request.json['precio']
    }
    vuelos.append(nuevo_viaje)
    return jsonify({"peticion": vuelos})
"""

@app.route('/', methods=["GET", 'POST'])
def seleccionar():
    contenido = ''
    if request.method == "POST":
        f = request.files['ourfile']
        filename = f.filename
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        direccion = os.path.abspath("./uploads/") + '/' +  str(filename)
        archivo = open(direccion, encoding="utf-8")
        for lin in archivo:
            contenido += lin

    return render_template("index.html", text=str(contenido))

if __name__ == '__main__':
    app.run(debug = True, port= 8000)