from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from evento import Evento
import xmltodict
import re
import os
eventos = []

reportado_re = r'Reportado\spor:\s"[a-zA-Z|\s]+[0-9]"\s[a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+'
afectados_re = r'Usuarios\safectados:\s([a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+,?)+'
evento_re = r'<EVENTO>'
evento1_re = r'</EVENTO>'
eventos_re = r'<EVENTOS>'
fecha_re = r'[a-zA-Z]+[,]\s[0-9][0-9]/[0-9][0-9]/[0-9][0-9]'
error_re = r'Error:\s[0-9]*\s-\s([a-zA-Z]|\s)+'

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath("./uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/inicio')
def saludar():
    return jsonify({'message': '10'})

"""
@app.route('/cargarArchivo', methods=['GET', 'POST'])
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
        return contenido


@app.route('/prueba', methods=['GET', 'POST'])
def nuevo():
    if request.method == "POST":
        nuevo_viaje={
            "nombre": request.json['nombre'],
            "hora": request.json['hora'],
            "precio": request.json['precio']
        }
"""

@app.route("/cargar", methods=['GET', 'POST'])
def parse_xml():
    retorno = ''
    xml_data = request.form['texto']
    cadena = str(xml_data)
    cadena = cadena.split('\n')
    #print(cadena)
    #cadena.remove('')
    nuevo = False
    for el in cadena:
        #print(el)
        if re.search(eventos_re, el):
            continue
        elif re.search(evento_re, el):
            nuevo = True
        elif re.search(fecha_re, el):
            aux_fecha = re.search(fecha_re, el).group()
            #print('Fecha: ', aux_fecha)
        elif re.search(reportado_re, el):
            aux_repor = re.search(reportado_re, el).group()
            aux_repor = aux_repor.replace('Reportado por: ', '')
            aux_repor = aux_repor.split('"')
            aux_repor.remove('')
            #print(aux_repor)
        elif re.search(afectados_re, el):
            aux_afec = re.search(afectados_re, el).group()
            aux_afec = aux_afec.replace('Usuarios afectados: ', '')
            aux_afec = aux_afec.split(' ')
            #print(aux_afec)
        elif re.search(error_re, el):
            aux_err = re.search(error_re, el).group()
            #print('Error: ', aux_err)
        elif re.search(evento1_re, el):
            if nuevo == True:
                eventos.append(Evento(aux_fecha, aux_repor, aux_afec, aux_err))
                nuevo = False
    for ev in eventos:
        retorno += 'Evento: '
        retorno += ev.imprimir()
        retorno += ' \n'

    print(eventos)
    return 'Eventos almacenados: ' + retorno
    #print(xml_data)
    #content_dict = xmltodict.parse(xml_data)
    #return jsonify(content_dict)

@app.route("/generar")
def estadistics():
    pass

@app.route("/reset")
def borrar():
    eventos.clear()
    print(eventos)
    return jsonify({'message': 'Servidor reseteado'})


if __name__ == '__main__':
    app.run(debug = True, port= 8800)