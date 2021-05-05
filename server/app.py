from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from evento import Error, Evento
import xmltodict
import re
import os
import matplotlib.pyplot as plt

eventos = []
filtro_fecha = {}
cont_repor = {}
cont_err = {}
fechas = []

reportado_re = r'Reportado\spor:\s"[a-zA-Z|\s]+[0-9]"\s[a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+'
afectados_re = r'Usuarios\safectados:\s([a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+,?)+'
evento_re = r'<EVENTO>'
evento1_re = r'</EVENTO>'
eventos_re = r'<EVENTOS>'
fecha_re = r'[0-9][0-9]/[0-9][0-9]/[0-9][0-9]'
error_re = r'Error:\s[0-9]*\s-\s([a-zA-Z]|\s)+'
correo_re = r'[a-zA-Z0-9]+@([a-zA-Z]|.)+[a-zA-Z]+,?'

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath("./uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/inicio')
def saludar():
    return '10'

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
"""

@app.route("/cargar", methods=['GET', 'POST'])
def parse_xml():
    retorno = ''
    xml_data = request.form['texto']
    cadena = str(xml_data)
    f = cadena.split('\n')

    aux_entrada = []
    for el in f:
        aux_entrada.append(el.strip())
        
    nuevo = False
    for el in aux_entrada:
        if re.search(eventos_re, el):
            continue
        elif re.search(evento_re, el):
            nuevo = True
        elif re.search(fecha_re, el):
            aux_fecha = el.replace('\t', '')
        elif re.search('Reportado\spor:\s', el):
            #aux_repor = el.split(', ')
            aux_repor_1 = ''
            aux_repor = el
            aux_repor = aux_repor.replace('Reportado por: ', '')
            aux_repor = aux_repor.replace('<', '')
            aux_repor = aux_repor.replace('>', '')
            aux_repor = aux_repor.replace('"', '')
            aux_repor = aux_repor.replace('"', '')
            aux_repor = aux_repor.replace('\t', '')
            if re.search(correo_re, aux_repor):
                aux_repor_1 = re.search(correo_re, aux_repor).group()
        elif re.search('Usuarios\safectados:\s', el):
            aux_afec_re = []
            aux_afec = el
            aux_afec = aux_afec.replace('Usuarios afectados: ', '')
            aux_afec = aux_afec.replace('\t', '')
            aux_afec = aux_afec.split(', ')
            for mint in aux_afec:
                mint = mint.replace('<', '')
                mint = mint.replace('>', '')
                if re.search(correo_re, mint):
                    aux_afec_re.append(re.search(correo_re, mint).group())
        elif re.search('Error: ', el):
            aux_err = el
            aux_err = aux_err.replace('Error: ', '')
            aux_err = aux_err.replace('\t', '')
            aux_err = aux_err.split(' - ')
        elif re.search(evento1_re, el):
            if nuevo == True:            
                eventos.append(Evento(aux_fecha, aux_repor_1, aux_afec_re, Error(aux_err[0], aux_err[1])))
                nuevo = False

    for ev in eventos:
        retorno += ev.imprimir()

    #print(eventos)
    return 'Eventos almacenados: ' + retorno
    #print(xml_data)
    #content_dict = xmltodict.parse(xml_data)
    #return jsonify(content_dict)

@app.route("/generar")
def estadistics():
    cad = ''
    # Filtro por Fechas
    cont = -1
    aux_fecha = eventos[0].fecha
    
    for ev in eventos:
        cont += 1
        if cont == 0:
            fechas.append(ev.fecha)
            filtro_fecha[ev.fecha] = [ev]
        else:
            if ev.fecha in filtro_fecha:
                filtro_fecha[ev.fecha].append(ev)
            else:
                filtro_fecha[ev.fecha] = [ev]
                fechas.append(ev.fecha)

    for fe in fechas:
        cont1 = -1
        eventos1 = filtro_fecha[fe]
        cont_repor[fe] = []
        aox = cont_repor[fe]
        for even1 in eventos1:
            cont1 += 1
            if cont1 == 0:
                aox.append({even1.empleado: 1})
            else:
                if str(even1.empleado) in str(aox):
                    inde = -1
                    for lol in aox:
                        inde += 1
                        if even1.empleado in lol:
                            aux = aox[inde]
                            pol = aux[even1.empleado]
                            pol += 1
                            aux[even1.empleado] = pol
                else:
                    aox.append({even1.empleado: 1})
    #print(cont_repor)
    for fe1 in fechas:
        cont2 = -1
        eventos2 = filtro_fecha[fe1]
        cont_err[fe1] = []
        aox1 = cont_err[fe1]
        for even2 in eventos2:
            cont2 += 1
            if cont2 == 0:
                aox1.append({even2.error.num: 1})
            else:
                if str(even2.error.num) in str(aox1):
                    inde1 = -1
                    for lol1 in aox1:
                        inde1 += 1
                        if even2.error.num in lol1:
                            aux1 = aox1[inde1]
                            pol1 = aux1[even2.error.num]
                            pol1 += 1
                            aux1[even2.error.num] = pol1
                else:
                    aox1.append({even2.error.num: 1})

    with open(os.getcwd()+'/server/uploads/salida.xml', 'w') as re:
        re.write('<ESTADISTICAS>' + '\n')
        for fech in filtro_fecha:
            re.write('  <ESTADISTICA>' + '\n')
            re.write('      <FECHA>' + str(fech) + '<FECHA>' + '\n')
            re.write('      <CANTIDAD_MENSAJES>' + str(len(filtro_fecha[fech])) + '<CANTIDAD_MENSAJES>' + '\n')
            re.write('      <REPORTADO_POR>' + '\n')
            for reportes in cont_repor[fech]:
                for reporte in reportes:
                    re.write('      <USUARIO>' + '\n')
                    re.write('          <EMAIL>'+ str(reporte) +'<EMAIL>' + '\n')
                    re.write('          <CANTIDAD_MENSAJES>'+ str(reportes[reporte]) +'</CANTIDAD_MENSAJES>' + '\n')
                    re.write('      </USUARIO>' + '\n')
            re.write('      </REPORTADO_POR>' + '\n')
            re.write('      <AFECTADOS>' + '\n')
            for eventosl in filtro_fecha[fech]:
                for afectado in eventosl.afectados:
                    re.write('          <AFECTADO>'+ str(afectado) +'</AFECTADO>' + '\n')
            re.write('      </AFECTADOS>' + '\n')
            re.write('      <ERRORES>' + '\n')
            for ers in cont_err[fech]:
                for er in ers:
                    re.write('          <ERROR>' + '\n')
                    re.write('              <CODIGO>' + str(er) + '<CODIGO>' + '\n')
                    re.write('              <CANTIDAD_MENSAJES>' + str(ers[er]) + '<CANTIDAD_MENSAJES>' + '\n')
                    re.write('          <ERROR>' + '\n')
            re.write('      </ERRORES>' + '\n')
            re.write('  </ESTADISTICA>' + '\n')
        re.write('</ESTADISTICAS>' + '\n')
        re.close()

    repuesta_nueva = open(os.getcwd()+'/server/uploads/salida.xml', 'r')
    for valores in repuesta_nueva.readlines():
        cad += valores
    return cad

"""
@app.route("/graf")
def grafico():
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()
    return 'Funciona'
"""

@app.route("/grafico_errores", methods=['GET', 'POST'])
def graf():
    cod = request.form['codigo']
    cod = str(cod)
    fechas = []
    valores = []
    titulo = 'Error: ' + str(cod)
    #cont_err = {'15/01/20':[{'2001': 2}, {'1001': 1}], '16/01/20':[{'2001': 1}, {'1001': 1}]}
    for fecha in cont_err:
        for errores in cont_err[fecha]:
            inde1x = -1
            for err in errores:
                inde1x += 1
                if cod in err:
                    valores.append(errores[cod])
                    fechas.append(fecha)

    plt.title(titulo)
    plt.bar(fechas, valores)
    plt.show()
    return 'Grafica Realizada'

@app.route("/graficar_fechas", methods=['GET', 'POST'])
def frag():
    date = request.form['fecha']
    date = str(date)
    ususarios = []
    valores1 = []
    titulo1 = 'Fecha: ' + str(date)
    for user in cont_repor[date]:
        for val in user:
            ususarios.append(val)
            valores1.append(user[val])

    plt.title(titulo1)
    plt.bar(ususarios, valores1)
    plt.show()
    return 'Grafica Generada'

@app.route("/reset")
def borrar():
    eventos.clear()
    filtro_fecha.clear()
    cont_repor.clear()
    cont_err.clear()
    fechas.clear()
    return jsonify({'message': 'Servidor reseteado'})


if __name__ == '__main__':
    app.run(debug = True, port= 8800)