class Evento:
    def __init__(self, fecha, empleado, afectados, error):
        self.fecha = fecha
        self.empleado = empleado
        self.afectados = afectados
        self.error = error

    def imprimir(self):
        cadena = 'Evento = \nFecha: '+ str(self.fecha) + '\nReportado por: ' + str(self.empleado) + ',\nAfectados: ' + str(self.afectados) + ',\nError: ' + str(self.error.num) + ' - ' + str(self.error.name)
        print(cadena)
        return cadena

class Error:
    def __init__(self, num, name):
        self.num = num
        self.name = name
