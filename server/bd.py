import re
from evento import Evento
eventos = []
import os
entrada = """
<EVENTOS>
    <EVENTO>
        Guatemala, 15/01/2021
        Reportado por: "Nombre Empleado 1" xx@ing.usac.edu.gt
        Usuarios afectados: aa@ing.usac.edu.gt, bb@ing.usac.edu.gt
        Error: 20001 - Desbordamiento de bufer de memoria RAM
        en el servidor de correo electrónico.
    </EVENTO>
</EVENTOS>"""

entrada = entrada.split('\n')
entrada.remove('')

reportado_re = r'Reportado\spor:\s"[a-zA-Z|\s]+[0-9]"\s[a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+'
afectados_re = r'Usuarios\safectados:\s([a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+,?)+'
evento_re = r'<EVENTO>'
evento1_re = r'</EVENTO>'
eventos_re = r'<EVENTOS>'
fecha_re = r'[a-zA-Z]+[,]\s[0-9][0-9]/[0-9][0-9]/[0-9][0-9]'
error_re = r'Error:\s[0-9]*\s-\s([a-zA-Z]|\s)+'

#print(re.search(pattern, 'Error: 20001 - Desbordamiento de bufer de memoria RAM').group())
"""
nuevo = False
for el in entrada:
    if re.search(eventos_re, el):
        eventos = []
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
    ev.imprimir()
"""

hola = ['<EVENTOS>\n', '    <EVENTO>\n', '        Guatemala, 15/01/2021\n', '        Reportado por: "Nombre Empleado 1" xx@ing.usac.edu.gt\n', '        Usuarios afectados: aa@ing.usac.edu.gt, bb@ing.usac.edu.gt\n', '        Error: 20001 - Desbordamiento de bÃºfer de memoria RAM\n', '        en el servidor de correo electrÃ³nico.\n', '    </EVENTO>\n', '</EVENTOS>']
print("".join(hola))

op = r'Proyect_3\app\Proyecto3'