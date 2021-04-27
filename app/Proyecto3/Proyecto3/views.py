from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
from tkinter import filedialog
import os
import requests

"""
def inicio(request):

    main = loader.get_template('index.html')

    documento = main.render({"nombre": 'hola'})

    return HttpResponse(documento)
"""
def home(request):
    main = loader.get_template('index.html')

    documento = main.render({"nombre": 'hola'})

    return HttpResponse(documento)

def inicio(request):
    response = requests.get('http://127.0.0.1:8800/inicio').json()
    return render(request, 'index.html', {'respuesta':response})

