import re
eventos = []

entrada = """<EVENTOS>
    <EVENTO>
        Guatemala, 15/01/2021
        Reportado por: <"Nombre Empleado 1" xx@ing.usac.edu.gt>
        Usuarios afectados: aa@ing.usac.edu.gt, <bb@ing.usac.edu.gt>
        Error: 20001 - Desbordamiento de búfer de memoria RAM
        en el servidor de correo electrónico.
    </EVENTO>
</EVENTOS>"""
s = '[a-zA-Z]@[[a-zA-Z].]+[a-zA-Z]+>'
pattern = r'Reportado\spor:\s<"[a-zA-Z|\s]+[0-9]"\s[a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+>'
patterna = r'[a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+'
evento_re = r'<Evento>'
eventos_re = r'<Eventos>'
fecha_re = r'[a-zA-Z]+[,]\s[0-9][0-9]/[0-9][0-9]/[0-9][0-9]'

#print(entrada)

entry = 'xx@ing.usac.edu.gt'

print(re.search(pattern, 'Reportado por: <"Nombre Empleado 1" xx@ing.usac.edu.gt>').group())