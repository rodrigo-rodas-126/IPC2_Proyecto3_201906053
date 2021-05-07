import re
from evento import Error, Evento
import matplotlib.pyplot as plt
eventos = []
filtro_fecha = {}
cont_repor = {}
cont_err = {}
fechas = []
import os



"""
names = ['group_a', 'group_b', 'group_c']
values = [1, 2, 5]
plt.title('Fechas')
plt.bar(names, values)
plt.show()

input()

cad = {'<hola>': 0}
print('hola' in cad)
input()

fehnn = ['Guatemala, 15/01/20', 'Guatemala, 16/01/20']
a = {'Guatemala, 15/01/20': [{'user1@ing.usac.edu.gt': 1}, {'<user2@ing.usac.edu.gt>': 1}], 'Guatemala, 16/01/20': [{'user1@ing.usac.edu.gt': 1}, {'<user2@ing.usac.edu.gt>': 1}]}
for fech in fehnn:
    for reportes in a[fech]:
        for reporte in reportes:
            print(reporte)
            print(reportes[reporte])

input()

for el in a:
    print('user1@ing.usac.edu.gt' in el)
input()
a = {'Guatemala, 15/01/20': [{'user1@ing.usac.edu.gt': 1}, {'<user2@ing.usac.edu.gt>': 1}]}
for k in a:
    #print(a[k])
    for m in a[k]:
        print('user1@ing.usac.edu.gt' in m)
input()
#mo = {'uno': {'hola': 5}, 'dos': 2, 're': 1}
#mo = {'uno': 0, 'dos': 2, 're': 1}
#for eo in mo:
#    print(mo[eo])
#input()
"""
entrada1 = """
<EVENTOS>
	<EVENTO>
    Guatemala, 15/01/2021
    Reportado por: user1@ing.usac.edu.gt
    Usuarios afectados: user2@ing.usac.edu.gt, user3@ing.usac.edu.gt
    Error: 20001 - Desbordamiento de búfer de memoria RAM
    en el servidor de correo electrónico.
	</EVENTO>
	<EVENTO>
    Guatemala, 16/01/2021
    Reportado por: <user4@ing.usac.edu.gt>
    Usuarios afectados: user1@ing.usac.edu.gt, <"usuario3" user3@ing.usac.edu.gt>
    Error: 30001 - Excepción en pila
	</EVENTO>
	<EVENTO>
    Guatemala, 17/01/2021
    Reportado por: <coordinador@ing.usac.edu.gt>
    Usuarios afectados: user2@ing.usac.edu.gt, <user3@ing.usac.edu.gt>
    Error: 30001 - Servicio no encontrado
	</EVENTO>
	<EVENTO>
    Guatemala, 15/01/2021
    Reportado por: <user2@ing.usac.edu.gt>
    Usuarios afectados: coordinador@ing.usac.edu.gt, user1@ing.usac.edu.gt
    Error: 20001 - Desbordamiento de búfer de memoria RAM
    en el servidor de correo electrónico.
	</EVENTO>
	<EVENTO>
    Guatemala, 16/01/2021
    Reportado por: user1@ing.usac.edu.gt
    Usuarios afectados: user2@ing.usac.edu.gt, user4@ing.usac.edu.gt, <"coordinador" coordinador@ing.usac.edu.gt>
    Error: 30001 - Servicio no encontrado
	</EVENTO>
	<EVENTO>
    Guatemala, 16/01/2021
    Reportado por: user1@ing.usac.edu.gt
    Usuarios afectados: user2@ing.usac.edu.gt, <user3@ing.usac.edu.gt>
    Error: 10001 - Excepción en pila
	</EVENTO>
</EVENTOS>"""

entrada = """
<EVENTOS>
	<EVENTO>
        Guatemala, 15/01/2021
        Reportado por: <"coordinador" coordinador@ing.usac.edu.gt>
        Usuarios afectados: user2@edu.gt, user3@ing.usac.edu.gt
        Error: 20001 - Desbordamiento de búfer de memoria RAM
        en el servidor de correo electrónico.
	</EVENTO>
	<EVENTO>
        Guatemala, 16/01/2021
        Reportado por: <user4@ing.usac.edu.gt>
        Usuarios afectados: user1@ing.usac.edu.gt, <"usuario3" user3@ing.usac.edu.gt>
        Error: 10001 - Excepción en pila
	</EVENTO>
	<EVENTO>
        Guatemala, 17/01/2021
        Reportado por: <coordinador@ing.usac.edu.gt>
        Usuarios afectados: user2@ing.usac.edu.gt, <user3@ing.usac.edu.gt>
        Error: 30001 - Servicio no encontrado
	</EVENTO>
	<EVENTO>
        Guatemala, 15/01/2021
        Reportado por: <user2@ing.usac.edu.gt>
        Usuarios afectados: coordinador@ing.usac.edu.gt, user1@ing.usac.edu.gt
        Error: 20001 - Desbordamiento de búfer de memoria RAM
        en el servidor de correo electrónico.
	</EVENTO>
	<EVENTO>
        Guatemala, 16/01/2021
        Reportado por: user1@ing.usac.edu.gt
        Usuarios afectados: user2@edu.gt, user4@ing.usac.edu.gt, <"coordinador" coordinador@ing.usac.edu.gt>
        Error: 30001 - Servicio no encontrado
	</EVENTO>
	<EVENTO>
        Guatemala, 16/01/2021
        Reportado por: user1@ing.usac.edu.gt
        Usuarios afectados: user2@ing.usac.edu.gt, <user3@ing.usac.edu.gt>
        Error: 30001 - Excepción en pila
	</EVENTO>
</EVENTOS>
"""

entradass = """
<EVENTOS>
    <EVENTO>
    Guatemala, 15/01/2021
    Reportado por: xx@ing.usac.edu.gt
    Usuarios afectados: aa@ing.usac.edu.gt, bb@ing.usac.edu.gt
    Error: 20001 - Desbordamiento de búfer de memoria RAM
    en el servidor de correo electrónico.
    </EVENTO>
</EVENTOS>
"""

#putb = {'Guatemala, 15/01/2021': []}
#cf = 'Guatemala, 15/01/2021'
#print(cf in putb)
#input()
"""
aux_entrada = []
entrada = entrada.split('\n')
for el in entrada:
    aux_entrada.append(el.strip())
print(aux_entrada)
input()
"""

correo_re_1 = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
reportado_re = r'Reportado\spor:\s"[a-zA-Z|\s]+[0-9]"\s[a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+'
afectados_re = r'Usuarios\safectados:\s([a-zA-Z]+@([a-zA-Z]|.)+[a-zA-Z]+,?)+'
correo_re = r'[a-zA-Z0-9]+@([a-zA-Z]|.)+[a-zA-Z]+,?'
evento_re = r'<EVENTO>'
evento1_re = r'</EVENTO>'
eventos_re = r'<EVENTOS>'
fecha_re = r'[a-zA-Z]+[,]\s[0-9][0-9]/[0-9][0-9]/[0-9][0-9]'
error_re = r'Error:\s[0-9]*\s-\s([a-zA-Z]|\s)+'

print(re.search(correo_re, 'coordinador@gt'))
input()

#print(re.search(pattern, 'Error: 20001 - Desbordamiento de bufer de memoria RAM').group())
def leer(entarad):
    nuevo = False

    aux_entrada = []
    f = entarad.split('\n')
    for el in f:
        aux_entrada.append(el.strip())

    for el in aux_entrada:
        if re.search(eventos_re, el):
            continue
        elif re.search(evento_re, el):
            nuevo = True
        elif re.search(fecha_re, el):
            aux_fecha = el.replace('\t', '')
            #aux_fecha = aux_fecha.replace('    ', '')
            #print('Fecha: ', aux_fecha)
        #elif re.search(reportado_re, el):
        elif re.search('Reportado\spor:\s', el):
            #aux_repor = el.split(', ')
            aux_repor_1 = ''
            aux_repor = el
            aux_repor = aux_repor.replace('Reportado por: ', '')
            #aux_repor = aux_repor.replace('    ', '')
            aux_repor = aux_repor.replace('<', '')
            aux_repor = aux_repor.replace('>', '')
            aux_repor = aux_repor.replace('"', '')
            aux_repor = aux_repor.replace('"', '')
            aux_repor = aux_repor.replace('\t', '')
            if re.search(correo_re, aux_repor):
                aux_repor_1 = re.search(correo_re, aux_repor).group()
            #print(aux_repor)
            #input()
            #aux_repor = re.search(reportado_re, el).group()
            #aux_repor = aux_repor.replace('Reportado por: ', '')
            #aux_repor = aux_repor.split('"')
            #aux_repor.remove('')
            #print(aux_repor)
        elif re.search('Usuarios\safectados:\s', el):
            aux_afec_re = []
            aux_afec = el
            aux_afec = aux_afec.replace('Usuarios afectados: ', '')
            #aux_fecha = aux_fecha.replace('    ', '')
            aux_afec = aux_afec.replace('\t', '')
            aux_afec = aux_afec.split(', ')
            for mint in aux_afec:
                mint = mint.replace('<', '')
                mint = mint.replace('>', '')
                if re.search(correo_re, mint):
                    aux_afec_re.append(re.search(correo_re, mint).group())
            #print(aux_afec)
            #input()
            #aux_afec = re.search(afectados_re, el).group()
            #aux_afec = aux_afec.replace('Usuarios afectados: ', '')
            #aux_afec = aux_afec.split(' ')
            #print(aux_afec)
        elif re.search('Error: ', el):
            aux_err = el
            aux_err = aux_err.replace('Error: ', '')
            #aux_err = aux_err.replace('    ', '')
            aux_err = aux_err.replace('\t', '')
            aux_err = aux_err.split(' - ')
            #print(aux_err)
            #input()
            #aux_err = re.search(error_re, el).group()
            #print('Error: ', aux_err)
        elif re.search(evento1_re, el):
            if nuevo == True:            
                eventos.append(Evento(aux_fecha, str(aux_repor_1), aux_afec_re, Error(aux_err[0], aux_err[1])))
                nuevo = False

def estad(eventos):
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
    
    #print(filtro_fecha)
    #print(fechas)

    conta = -1

    # Contadores de personas que reportaron
    for fe in fechas:
        cont1 = -1
        eventos1 = filtro_fecha[fe]
        cont_repor[fe] = []
        aox = cont_repor[fe]
        #print(aox)
        #input()

        for even1 in eventos1:
            
            cont1 += 1
            if cont1 == 0:
                aox.append({even1.empleado: 1})
                #print(aox)
                #input()
            else:
                #print(aox)
                #input()
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

    print(cont_repor)

    # Contadores de errores que se reportaron
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

    print('\n')
    print(cont_err)


def graficar_errores(cod):
    fechas = []
    valores = []
    titulo = 'Error: ' + str(cod)

    for fecha in cont_err:
        for errores in cont_err[fecha]:
            inde1x = -1
            for err in errores:
                inde1x += 1
                if cod in err:
                    valores.append(errores[cod])
                    fechas.append(fecha)
    print(fechas)
    print(valores)

    plt.title(titulo)
    plt.bar(fechas, valores)
    plt.show()


def graficar_fechas(date):
    ususarios = []
    valores1 = []
    titulo1 = 'Fecha: ' + str(date)

    for user in cont_repor[date]:
        #print(user)
        for val in user:
            #print(val)
            #print(user[val])
            ususarios.append(val)
            valores1.append(user[val])

    plt.title(titulo1)
    plt.bar(ususarios, valores1)
    plt.show()
    


def generar(filtros):
    with open(os.getcwd()+'/server/uploads/salida.xml', 'w') as re:
        re.write('<ESTADISTICAS>' + '\n')
        for fech in filtros:
            re.write('  <ESTADISTICA>' + '\n')
            re.write('      <FECHA>' + str(fech) + '<FECHA>' + '\n')
            re.write('      <CANTIDAD_MENSAJES>' + str(len(filtros[fech])) + '<CANTIDAD_MENSAJES>' + '\n')
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

leer(entrada)
"""
for ev in eventos:
    ev.imprimir()
    print('\n')
"""

estad(eventos)

generar(filtro_fecha)

#graficar_errores('30001')

graficar_fechas('Guatemala, 15/01/2021')





#hola = ['<EVENTOS>\n', '    <EVENTO>\n', '        Guatemala, 15/01/2021\n', '        Reportado por: "Nombre Empleado 1" xx@ing.usac.edu.gt\n', '        Usuarios afectados: aa@ing.usac.edu.gt, bb@ing.usac.edu.gt\n', '        Error: 20001 - Desbordamiento de bÃºfer de memoria RAM\n', '        en el servidor de correo electrÃ³nico.\n', '    </EVENTO>\n', '</EVENTOS>']
#print("".join(hola))

#op = r'Proyect_3\app\Proyecto3'