from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
from tkinter import filedialog
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from Database import archivos_cargados

path_media = r'C:\Users\Rodrigo\Desktop\3er año\IPC2\Laboratorio\Proyect3\Proyect_3\app\Proyecto3'

"""
def inicio(request):

    main = loader.get_template('index.html')

    documento = main.render({"nombre": 'hola'})

    return HttpResponse(documento)
"""
def home(request):
    main = loader.get_template('index.html')
    documento = main.render()
    return HttpResponse(documento)

def home1(request):
    archivos_cargados.clear()
    response = requests.get('http://127.0.0.1:8800/reset').json()
    main = loader.get_template('index.html')
    documento = main.render()
    return HttpResponse(documento)

def inicio(request):
    response = requests.get('http://127.0.0.1:8800/inicio').json()
    
    return render(request, 'index.html', {'respuesta':response})

@csrf_exempt 
def archivo(request):
    archivo_entrada = ''
    if request.method == 'POST':
        myfile = request.FILES['ourfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        aux_file = open(str(path_media)+uploaded_file_url, 'r')
        for el in aux_file.readlines():
            archivo_entrada += el
        # Consumiendo la API
        url = 'http://127.0.0.1:8800/cargar'
        archivo_xml = {'texto': "".join(archivo_entrada)}
        x = requests.post(url, data = archivo_xml)
        print(x.text)
        archivos_cargados.append(archivo_entrada)
        # Retornando Templeate
        main = loader.get_template('index.html')
        documento = main.render({'respuesta': "".join(archivo_entrada)})
        return HttpResponse(documento)

@csrf_exempt
def consultar(request):
    main = loader.get_template('index.html')
    documento = main.render({"respuesta": archivos_cargados[0], "respuesta_estadistica": archivos_cargados[1]})
    return HttpResponse(documento)
