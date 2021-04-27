vuelos = [
    {"nombre": "España", "hora": "10:10", "precio": 100},
    {"nombre": "Argentina", "hora": "10:10", "precio": 100},
    {"nombre": "Marruecos", "hora": "10:10", "precio": 100}
]

direccion = r'C:\Users\Rodrigo\Desktop\3er año\IPC2\Laboratorio\Proyect3\Proyect_3\server\entrada.xml'
arc = open(direccion, encoding="utf-8")
for lineas in arc:
    print(lineas)