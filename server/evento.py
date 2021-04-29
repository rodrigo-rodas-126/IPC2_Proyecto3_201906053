class Evento:
    def __init__(self, fecha, empleado, afectados, error):
        self.fecha = fecha
        self.empleado = empleado
        self.afectados = afectados
        self.error = error

    def imprimir(self):
        cadena = 'Fecha: '+ str(self.fecha) + ' Reportado por: ' + str(self.empleado) + ', Afectados: ' + str(self.afectados) + ', ' + str(self.error)
        print(cadena)
        return cadena