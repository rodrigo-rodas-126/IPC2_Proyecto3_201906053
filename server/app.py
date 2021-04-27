from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from evento import Evento
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath("./uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


"""
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

@app.route('/inicio')
def saludar():
    return jsonify({'message': '10'})

@app.route('/cargarArchivo', methods=['GET', 'POST'])
def seleccionar():
    contenido = ''
    eventos = []
    if request.method == "POST":
        f = request.files['ourfile']
        filename = f.filename
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        direccion = os.path.abspath("./uploads/") + '/' +  str(filename)
        archivo = open(direccion, encoding="utf-8")
        for lin in archivo:
            contenido += lin
        return contenido

@app.route('/prueba', methods=['GET', 'POST'])
def nuevo():
    if request.method == "POST":
        nuevo_viaje={
            "nombre": request.json['nombre'],
            "hora": request.json['hora'],
            "precio": request.json['precio']
        }

if __name__ == '__main__':
    app.run(debug = True, port= 8800)