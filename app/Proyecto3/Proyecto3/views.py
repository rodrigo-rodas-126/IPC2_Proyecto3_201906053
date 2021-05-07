from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.template import Template, Context, loader
from django.shortcuts import render
from tkinter import filedialog
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from Database import archivos_cargados

path_media = r'C:\Users\lolig\Desktop\3semestre\IPC2\Proyect3\app\Proyecto3'

def home(request):
    main = loader.get_template('index.html')
    documento = main.render()
    return HttpResponse(documento)

def home1(request):
    archivos_cargados.clear()
    response = requests.get('http://127.0.0.1:8800/reset').json()
    print(archivos_cargados)
    return HttpResponseRedirect('http://127.0.0.1:8000')

@csrf_exempt 
def filtros(request):
    main = loader.get_template('home.html')
    # {"respuesta": archivos_cargados[0], "respuesta_estadistica": archivos_cargados[1]}
    documento = main.render({"respuesta": archivos_cargados[0], "respuesta_estadistica": archivos_cargados[1]})
    return HttpResponse(documento)

@csrf_exempt 
def filtros1(request):
    if request.method == 'POST':
        parametro1 = request.POST['codigo']
        #print(parametro1)
        url = 'http://127.0.0.1:8800/grafico_errores'
        codigo = {'codigo': parametro1}
        x = requests.post(url, data = codigo)
        print(x.text)
        return HttpResponseRedirect('http://127.0.0.1:8000/filtros')

@csrf_exempt
def filtros2(request):
    if request.method == 'POST':
        parametro = request.POST['fecha']
        #print(parametro)
        url = 'http://127.0.0.1:8800/graficar_fechas'
        fecha = {'fecha': parametro}
        x1 = requests.post(url, data = fecha)
        print(x1.text)
        return HttpResponseRedirect('http://127.0.0.1:8000/filtros')

def inicio(request):
    response = requests.get('http://127.0.0.1:8800/inicio')
    return render(request, 'index.html', {'respuesta':response.text})

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

        """
        # Consumiendo la API
        url = 'http://127.0.0.1:8800/cargar'
        archivo_xml = {'texto': "".join(archivo_entrada)}
        x = requests.post(url, data = archivo_xml)
        print(x.text)
        """

        archivos_cargados.append(archivo_entrada)
        # Retornando Templeate
        main = loader.get_template('index.html')
        documento = main.render({'respuesta': "".join(archivo_entrada)})
        return HttpResponse(documento)

@csrf_exempt
def archivo2(request):
    # Consumiendo la API
    url = 'http://127.0.0.1:8800/cargar'
    archivo_xml = {'texto': "".join(archivos_cargados[0])}
    x = requests.post(url, data = archivo_xml)
    print(x.text)
    main = loader.get_template('index.html')
    documento = main.render({'respuesta': "".join(archivos_cargados[0])})
    return HttpResponse(documento)

@csrf_exempt
def consultar(request):
    response = requests.get('http://127.0.0.1:8800/generar')
    main = loader.get_template('index.html')
    archivos_cargados.append(response.text)
    documento = main.render({"respuesta": archivos_cargados[0], "respuesta_estadistica": response.text})
    return HttpResponse(documento)

@csrf_exempt
def docu(request):
    try:
        return FileResponse(open('C:/Users/lolig/Desktop/3semestre/IPC2/Proyect3/Documentacion/EnsayoIPC2.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()