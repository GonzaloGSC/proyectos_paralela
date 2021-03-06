
######################################################################## SECTOR DE IMPORTS ########################################################################

from mimetypes import guess_type, guess_extension # Utilizado para trabajar el MIME de archivos, comprobacion.
import re # Utilizado para .search(), busqueda de extencion en archivos
import base64 # Utilizado para trabajar con la codificación y decodificación del archivo
import csv # Utilizado para revisar el archivo decodificado, para detectar separadores y demas
import platform # Utilizado para detectar el SO
import os # Utilizado para eliminar archivo temporal de revisión
import pandas #Libreria open source, utilizada para crear xlsx
# import xlrd
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

######################################################################## SECTOR DE FUNCIONES ########################################################################


def codificar(textoSinCodificar):
    base64_cadena_bytes = base64.b64encode(textoSinCodificar.encode('ascii'))
    texto_base64 = base64_cadena_bytes.decode('ascii')
    return texto_base64

def decodificar(textoCodificado): # Decodifica el archivo de ingreso, utilizando en primera instancia, la codificacion ascii para luego decodificar correctamente la informacion desde base64
    try:
        cadena_bytes = base64.b64decode(textoCodificado.encode('ascii'))
        textoDecode = cadena_bytes.decode('ascii')
        return textoDecode
    except:
        print("Error: Falla inesperada en decodificación, revise la codificacion base64 del archivo, esta puede haber sido cortada.")

def revisarMime(nombreDelArchivo): # Revisa el mime del nombre de archivo ingresado. Retorna el MIME de csv cuando es correcto. fuente: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    resultado=guess_type(nombreDelArchivo)
    if(resultado[0]=="application/vnd.ms-excel" and re.search(".csv$" , nombreDelArchivo)): #Detecta Mime del archivo
        print("MIME detectado = text/csv ("+str(resultado[0])+")")
        return "text/csv"
    else:
        print("MIME detectado = "+str(resultado[0]))
        print("Error: MIME Incorrecto, debe utilizar text/csv. El archivo no corresponde al formato admitido, por favor, reintentar.")
        return resultado[0]

def revisarContenidoBase64(TextoCodificado): # Revisa el contenido del archivo para detectar si es efectivamente un CSV o no.
    contador = 0
    try:
        revision = csv.Sniffer().sniff(decodificar(TextoCodificado),";") #Realiza varios testeos sobre el archivo (separadores, delimitadores, etc.) archivo.read(1024) Fuente: https://docs.python.org/3/library/csv.html
        mensaje = decodificar(TextoCodificado).split("\n")
        for linea in mensaje: #Revision de cada linea ingresada
            for caracter in linea: #Revision de cada caracter ingresado
                contador = contador + 1
                if (contador>32): # Detecta si la fila de ingreso es mas larga de lo debido, el largo correcto es de 32 caracteres (Ej. 19291586;123;123;123;123;123;123)
                    print("Error: Excedido tamaño de filas, existe al menos una fila mal ingresada en el archivo. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
                if ((caracter!=";" and caracter.isnumeric()) or caracter==";"): # Detecta si el archivo ingresado contiene algun caracter que no sea numeros o punto y coma (;), si es así, detecta la falla
                    pass
                else:
                    print("Error: Letras detectadas en contenido, el archivo debe contener solo numeros y separadores. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
            if (contador!=0 and contador<32): # Detecta si la fila de ingreso es corta, el largo correcto es de 32 caracteres (Ej. 19291586;123;123;123;123;123;123)
                print("Error: Insuficiente tamaño de filas, existe al menos una fila mal ingresada en el archivo. El archivo no corresponde al formato admitido, por favor, reintentar.")
                return 0
            else:
                contador = 0
        print("El archivo es correcto.") # Si finalmente el archivo ingresado pasa todos los filtros, es aceptado.
        return 1 #Aprovechando la instancia, devuelve la informacion ya decodificada
    except csv.Error:
        print("Error: Separadores y delimitadores no corresponden. El archivo no corresponde al formato admitido, por favor, reintentar.") # Excepcion preparada para la deteccion de otro separador en el csv o un error en la revision de este.
        return 0

def generarXlsx(rutss,puntajess,nombreXlsx):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    writer = pandas.ExcelWriter(dir_path+"/"+nombreXlsx) # pylint: disable=abstract-class-instantiated
    for i in range(0,28):
        ordenarEsto = []
        for j in range(len(puntajess[i])):
            ordenarEsto.append([rutss[i][j],puntajess[i][j]])
        ordenarEsto.sort(key=lambda x: x[1], reverse=1)
        r=[]
        p=[]
        for k in range(len(ordenarEsto)):
            r.append(ordenarEsto[k][0])
            p.append(ordenarEsto[k][1])

        df = pandas.DataFrame({
            "Nº": [int(j)+1 for j in range(len(puntajess[i]))],
            "RUT Matriculado": r,
            "Puntaje": p})
        df = df[["Nº", "RUT Matriculado", "Puntaje"]]
        if (i==0):
            df.to_excel(writer, "Administración Pública", index=False)
        if (i==1):
            df.to_excel(writer, "Bibliotecología y Documentación", index=False)
        if (i==2):
            df.to_excel(writer, "Contador Público y Auditor", index=False)
        if (i==3):
            df.to_excel(writer, "Ing. Comercial", index=False)
        if (i==4):
            df.to_excel(writer, "Ing. en Adm. Agroindustrial", index=False)
        if (i==5):
            df.to_excel(writer, "Ing. en Comercio Inter.", index=False)
        if (i==6):
            df.to_excel(writer, "Ing. en Gestión Turística", index=False)
        if (i==7):
            df.to_excel(writer, "Arquitectura", index=False)
        if (i==8):
            df.to_excel(writer, "Ing. Civil en Obras Civiles", index=False)
        if (i==9):
            df.to_excel(writer, "Ing. en Construcción", index=False)
        if (i==10):
            df.to_excel(writer, "Ing. Civil en Prev. de R.", index=False)
        if (i==11):
            df.to_excel(writer, "Ing.en Biotecnología", index=False)
        if (i==12):
            df.to_excel(writer, "Ing. en Ind. Alimentaria", index=False)
        if (i==13):
            df.to_excel(writer, "Ing. en Química", index=False)
        if (i==14):
            df.to_excel(writer, "Química Ind.", index=False)
        if (i==15):
            df.to_excel(writer, "Diseño en Comunicación Visual", index=False)
        if (i==16):
            df.to_excel(writer, "Diseño Ind.", index=False)
        if (i==17):
            df.to_excel(writer, "Trabajo Social", index=False)
        if (i==18):
            df.to_excel(writer, "Bach. en Ciencias de la Ing.", index=False)
        if (i==19):
            df.to_excel(writer, "Dibujante Proyectista", index=False)
        if (i==20):
            df.to_excel(writer, "Ing. Civil en Comp.", index=False)
        if (i==21):
            df.to_excel(writer, "Ing. Civil Ind.", index=False)
        if (i==22):
            df.to_excel(writer, "Ing. Civil en Ciencia de Datos", index=False)
        if (i==23):
            df.to_excel(writer, "Ing. Civil Electrónica", index=False)
        if (i==24):
            df.to_excel(writer, "Ing. Civil en Mecánica", index=False)
        if (i==25):
            df.to_excel(writer, "Ing. en Geomensura", index=False)
        if (i==26):
            df.to_excel(writer, "Ing. en Informática", index=False)
        if (i==27):
            df.to_excel(writer, "Ing. Ind.", index=False)
    writer.save()

######################################################################## Programa principal  ########################################################################

class servicios(ServiceBase):

    @rpc(Unicode, Unicode, Unicode, _returns = Iterable(Unicode))
    def programaPrincipal(ctx,mime,nombreDelArchivo,datosBase64):#Funcion de consumo

        ########### DECLARACION DE VARIABLES

        matriculadosPorCarreraRuts=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # Contendrá todos los RUTS de estudiantes ya matriculados en una carrera, ordenados segun carrera
        matriculadosPorCarreraPuntajes=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # Contendrá todos los PUNTAJES de estudiantes ya matriculados en una carrera, ordenados segun carrera
        lista = [] # contiene los grupos de carrera segun criterios de ingreso a ellas.

        # IMPORTANTE: Se separaron las ponderaciones exigidas de las carreras en 12 grupos, ya que habian carreras con la misma exigencia, a continuacion se describen:
        # grupo1 Contendrá los mejores puntajes ordenados de las carreras: 21089
        # grupo2 Contendrá los mejores puntajes ordenados de las carreras: 21002
        # grupo3 Contendrá los mejores puntajes ordenados de las carreras: 21012
        # grupo4 Contendrá los mejores puntajes ordenados de las carreras: 21048, 21015, 21081 y 21082
        # grupo5 Contendrá los mejores puntajes ordenados de las carreras: 21047
        # grupo6 Contendrá los mejores puntajes ordenados de las carreras: 21074 y 21032
        # grupo7 Contendrá los mejores puntajes ordenados de las carreras: 21087
        # grupo8 Contendrá los mejores puntajes ordenados de las carreras: 21073 y 21039
        # grupo9 Contendrá los mejores puntajes ordenados de las carreras: 21080 y 21083
        # grupo10 Contendrá los mejores puntajes ordenados de las carreras: 21024 y 21023
        # grupo11 Contendrá los mejores puntajes ordenados de las carreras: 21043
        # grupo12 Contendrá los mejores puntajes ordenados de las carreras: 21046, 21071, 21041, 21076, 21049, 21075, 21096, 21031, 21030 y 21045

        ########### VALIDACION DE DATOS INGRESADOS
        print("Validando datos ingresados...")
 
        if (not (revisarContenidoBase64(datosBase64)) or revisarMime(nombreDelArchivo)!="text/csv" or mime!="text/csv"):# Comprueba datos de ingreso (nombre del archivo, mime, e informacion codifiada en base64)
            if (mime!="text/csv"):
                print("Recepcion de MIME incorrecto, usar text/csv.")
            return "Finalizando ejecucion..."

        ########### OPERACION SOBRE DATOS

        arregloDePuntajesPsu = decodificar(datosBase64).split("\n") # Separa el string en los saltos de linea
        contadorPostulante = 0
        print("Obteniendo ponderaciones por estudiante a cada carrera...")
        for datosPostulante in arregloDePuntajesPsu:
            
            arregloDePuntajesPsu[contadorPostulante]=datosPostulante.split(";")
            
            if (len(arregloDePuntajesPsu[contadorPostulante])==7):
                arregloDePuntajesPsu[contadorPostulante][0]=str(arregloDePuntajesPsu[contadorPostulante][0])
                arregloDePuntajesPsu[contadorPostulante][1]=float(arregloDePuntajesPsu[contadorPostulante][1])
                arregloDePuntajesPsu[contadorPostulante][2]=float(arregloDePuntajesPsu[contadorPostulante][2])
                arregloDePuntajesPsu[contadorPostulante][3]=float(arregloDePuntajesPsu[contadorPostulante][3])
                arregloDePuntajesPsu[contadorPostulante][4]=float(arregloDePuntajesPsu[contadorPostulante][4])
                arregloDePuntajesPsu[contadorPostulante][5]=float(arregloDePuntajesPsu[contadorPostulante][5])
                arregloDePuntajesPsu[contadorPostulante][6]=float(arregloDePuntajesPsu[contadorPostulante][6])
                np = arregloDePuntajesPsu[contadorPostulante]

                ponderacionesDelAlumno=[]
                if (np[5]>=np[6] and (np[3]+np[4])/2>450): # Verifica que el puntaje de Ciencias sea mayor o igual al de Historia (np[5]>=np[6]) y que el promedio de matematicas y lenguaje sea mayor a 450
                    ponderacionesDelAlumno.append(np[0]) # Agrega el rut
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.2+np[3]*0.25+np[4]*0.3+np[5]*0.1,2)) # Calculo de ponderaciones por grupo de carreras (comparar con excel)
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.2+np[3]*0.1+np[4]*0.4+np[5]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.2+np[3]*0.15+np[4]*0.3+np[5]*0.15,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.2+np[3]*0.3+np[4]*0.3+np[5]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.25+np[3]*0.2+np[4]*0.2+np[5]*0.2,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.2+np[3]*0.35+np[4]*0.15+np[5]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.35+np[3]*0.2+np[4]*0.2+np[5]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.25+np[3]*0.3+np[4]*0.2+np[5]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.25+np[3]*0.3+np[4]*0.15+np[5]*0.2,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.4+np[3]*0.1+np[4]*0.3+np[5]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.3+np[3]*0.1+np[4]*0.2+np[5]*0.2,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.25+np[3]*0.35+np[4]*0.2+np[5]*0.1,2))
                elif((np[3]+np[4])/2>450): # Si lo anterior no es ejecutado, revisa que la razon de ello sea que ciencias es menor a historia en puntaje, si es el caso, considera historia en el calculo (np[6])
                    ponderacionesDelAlumno.append(np[0])
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.2+np[3]*0.25+np[4]*0.3+np[6]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.2+np[3]*0.1+np[4]*0.4+np[6]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.2+np[3]*0.15+np[4]*0.3+np[6]*0.15,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.2+np[3]*0.3+np[4]*0.3+np[6]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.25+np[3]*0.2+np[4]*0.2+np[6]*0.2,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.2+np[3]*0.35+np[4]*0.15+np[6]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.35+np[3]*0.2+np[4]*0.2+np[6]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.25+np[3]*0.3+np[4]*0.2+np[6]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.25+np[3]*0.3+np[4]*0.15+np[6]*0.2,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.4+np[3]*0.1+np[4]*0.3+np[6]*0.1,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.2+np[2]*0.3+np[3]*0.1+np[4]*0.2+np[6]*0.2,2))
                    ponderacionesDelAlumno.append(round(np[1]*0.1+np[2]*0.25+np[3]*0.35+np[4]*0.2+np[6]*0.1,2))
                lista.append(ponderacionesDelAlumno) # Se guarda el rut del estudiante junto a todas sus ponderaciones a cada grupo de carreras
            contadorPostulante = contadorPostulante + 1  
        print("Asignando carreras a los mejores postulantes y a su vez, mejor opcion por postulante...")
        # Las carreras a continuacion estan ordenadas bajo la prioridad del puntaje mas alto de ingreso del año 2019, y en secundario, bajo tamaño menor de cupos
        print("Carrera: Ingeniería en Construcción...")
        lista.sort(key=lambda x: x[6], reverse=1) # Se ordena el array lista en base al dato lista[n](Puntaje de grupo de carreras, esto varia por cada una), de esta forma, se guardan los matriculados por orden de puntaje.
        b=0 # Contador de matriculados
        a=0 # Contador de postulantes revisados
        c=0 # Interruptor para añadir rechazados
        while(b<100): # While que se repite segun numero de matriculas de la carrera
            # if maravilloso que hace cumplir 2 condiciones antes de agregar un estudiante a una carrera, 
            # 1era: (lista[a][6]>=max(lista[a][1:12]); que el puntaje ponderado de la carrera que se revisa sea el mejor ponderado del alumno, esto evita el re-posicionamiento de los matriculados
            # 2da: lista[a][0]!=0; que el alumno no este matriculado en una carrera (eso significaria que el Rut=0)
            # 3ro c and lista[a][0]!=0); esto representa la activacion de relleno de cupos entre los mejores posibles para la carrera, si y solo si, con las dos condiciones anteriores no se llegan a llenar los cupos. Esto tiene relacion con el orden de prioridad de carreras (las de mas arriba en este codigo, mas prioridad, por lo tanto, se llenan antes.)
            if ((lista[a][6]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)): 
                matriculadosPorCarreraRuts[9].append(lista[a][0]) # Se guarda el rut del matriculado
                matriculadosPorCarreraPuntajes[9].append(lista[a][6]) # Se guarda el puntaje del matriculado
                lista[a][0] = 0 # Se cambia el rut por 0, asi se detectan los ya matriculados
                b=b+1 # Nuevo matriculado
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<100): # Si se revisaron todos los postulantes, y no se llenan los cupos, activa proceso de relleno de mejores postulantes
                c=1
                a=0
            else:
                a=a+1 # Pasa al siguiente postulante para revision
            

        # Se repite todo el proceso anterior por cada carrera....

        print("Carrera: Diseño en Comunicación Visual...")
        lista.sort(key=lambda x: x[10], reverse=1) 
        b=0
        a=0
        c=0
        while(b<100):
            if ((lista[a][10]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[15].append(lista[a][0])
                matriculadosPorCarreraPuntajes[15].append(lista[a][10])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<100):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Trabajo Social...")
        lista.sort(key=lambda x: x[11], reverse=1) 
        b=0
        a=0
        c=0
        while(b<95):
            if ((lista[a][11]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[17].append(lista[a][0])
                matriculadosPorCarreraPuntajes[17].append(lista[a][11])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<95):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ingeniería en Informática...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<105):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[26].append(lista[a][0])
                matriculadosPorCarreraPuntajes[26].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<105):
                c=1
                a=0
            else:
                a=a+1
            
        
        print("Carrera: Ingeniería Civil en Mecánica...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<90):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[24].append(lista[a][0])
                matriculadosPorCarreraPuntajes[24].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<90):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Dibujante Proyectista...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<25):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[19].append(lista[a][0])
                matriculadosPorCarreraPuntajes[19].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<25):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ingeniería en Industria Alimentaria...")
        lista.sort(key=lambda x: x[8], reverse=1) 
        b=0
        a=0
        c=0
        while(b<30):
            if ((lista[a][8]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[12].append(lista[a][0])
                matriculadosPorCarreraPuntajes[12].append(lista[a][8])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<30):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Ingeniería en Biotecnología...")
        lista.sort(key=lambda x: x[8], reverse=1) 
        b=0
        a=0
        c=0
        while(b<60):
            if ((lista[a][8]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[11].append(lista[a][0])
                matriculadosPorCarreraPuntajes[11].append(lista[a][8])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<60):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Bibliotecología y Documentación...") 
        lista.sort(key=lambda x: x[2], reverse=1)
        b=0
        a=0
        c=0
        while(b<35):
            if ((lista[a][2]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[1].append(lista[a][0])
                matriculadosPorCarreraPuntajes[1].append(lista[a][2])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<35):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Ingeniería Civil en Computación, mención Informática...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<130):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[20].append(lista[a][0])
                matriculadosPorCarreraPuntajes[20].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<130):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ingeniería Civil en Ciencia de Datos...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<60):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[22].append(lista[a][0])
                matriculadosPorCarreraPuntajes[22].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<60):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ingeniería Civil Industrial...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<200):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[21].append(lista[a][0])
                matriculadosPorCarreraPuntajes[21].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<200):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ing. en Gestión Turística...")
        lista.sort(key=lambda x: x[4], reverse=1) 
        b=0
        a=0
        c=0
        while(b<25):
            if ((lista[a][4]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[6].append(lista[a][0])
                matriculadosPorCarreraPuntajes[6].append(lista[a][4])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<25):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Ingeniería Civil Electrónica...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<80):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[23].append(lista[a][0])
                matriculadosPorCarreraPuntajes[23].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<80):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ing. Comercial...")
        lista.sort(key=lambda x: x[4], reverse=1)
        b=0
        a=0
        c=0
        while(b<125):
            if ((lista[a][4]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[3].append(lista[a][0])
                matriculadosPorCarreraPuntajes[3].append(lista[a][4])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<125):
                c=1
                a=0
            else:
                a=a+1
                
        print("Carrera: Diseño Industrial...")
        lista.sort(key=lambda x: x[10], reverse=1) 
        b=0
        a=0
        c=0
        while(b<65):
            if ((lista[a][10]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[16].append(lista[a][0])
                matriculadosPorCarreraPuntajes[16].append(lista[a][10])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<65):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Arquitectura...")
        lista.sort(key=lambda x: x[5], reverse=1) 
        b=0
        a=0
        c=0
        while(b<100):
            if ((lista[a][5]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[7].append(lista[a][0])
                matriculadosPorCarreraPuntajes[7].append(lista[a][5])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<100):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ing. en Comercio Inter...")
        lista.sort(key=lambda x: x[4], reverse=1) 
        b=0
        a=0
        c=0
        while(b<90):
            if ((lista[a][4]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[5].append(lista[a][0])
                matriculadosPorCarreraPuntajes[5].append(lista[a][4])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<90):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Contador Público y Auditor...")
        lista.sort(key=lambda x: x[3], reverse=1)
        b=0
        a=0
        c=0
        while(b<80):
            if ((lista[a][3]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[2].append(lista[a][0])
                matriculadosPorCarreraPuntajes[2].append(lista[a][3])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<80):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ing. en Adm. Agroindustrial...")
        lista.sort(key=lambda x: x[4], reverse=1) 
        b=0
        a=0
        c=0
        while(b<30):
            if ((lista[a][4]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[4].append(lista[a][0])
                matriculadosPorCarreraPuntajes[4].append(lista[a][4])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<30):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Administración Pública...")
        lista.sort(key=lambda x: x[1], reverse=1) 
        b=0 
        a=0
        c=0
        while(b<35):
            if ((lista[a][1]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[0].append(lista[a][0])
                matriculadosPorCarreraPuntajes[0].append(lista[a][1])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<35):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Ingeniería Civil en Obras Civiles...")
        lista.sort(key=lambda x: x[6], reverse=1) 
        b=0
        a=0
        c=0
        while(b<100):
            if ((lista[a][6]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[8].append(lista[a][0])
                matriculadosPorCarreraPuntajes[8].append(lista[a][6])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<100):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Ingeniería Civil en Prevención de Riesgos y Medioambiente...")
        lista.sort(key=lambda x: x[7], reverse=1) 
        b=0
        a=0
        c=0
        while(b<30):
            if ((lista[a][7]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[10].append(lista[a][0])
                matriculadosPorCarreraPuntajes[10].append(lista[a][7])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<30):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ingeniería en Geomensura...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<60):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[25].append(lista[a][0])
                matriculadosPorCarreraPuntajes[25].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<60):
                c=1
                a=0
            else:
                a=a+1

        print("Carrera: Ingeniería en Química...")
        lista.sort(key=lambda x: x[9], reverse=1) 
        b=0
        a=0
        c=0
        while(b<80):
            if ((lista[a][9]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[13].append(lista[a][0])
                matriculadosPorCarreraPuntajes[13].append(lista[a][9])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<80):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Quimica Industrial...")
        lista.sort(key=lambda x: x[9], reverse=1) 
        b=0
        a=0
        c=0
        while(b<60):
            if ((lista[a][9]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[14].append(lista[a][0])
                matriculadosPorCarreraPuntajes[14].append(lista[a][9])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<60):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Bachillerato en Ciencias de la Ingeniería...")
        lista.sort(key=lambda x: x[12], reverse=1) 
        b=0
        a=0
        c=0
        while(b<25):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[18].append(lista[a][0])
                matriculadosPorCarreraPuntajes[18].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<25):
                c=1
                a=0
            else:
                a=a+1
        
        print("Carrera: Ingeniería Industrial...")
        b=0
        a=0
        c=0
        lista.sort(key=lambda x: x[12], reverse=1) 
        while(b<60):
            if ((lista[a][12]>=max(lista[a][1:12]) and lista[a][0]!=0) or (c and lista[a][0]!=0)):
                matriculadosPorCarreraRuts[27].append(lista[a][0])
                matriculadosPorCarreraPuntajes[27].append(lista[a][12])
                lista[a][0] = 0
                b=b+1
            if(a==len(lista)-1 and c==1):
                break
            if (a==len(lista)-1 and b<60):
                c=1
                a=0
            else:
                a=a+1
        
        ########### RESPUESTA DEL SERVIDOR AL CLIENTE

        yield "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        yield "Matriculados Utem.xlsx"
        generarXlsx(matriculadosPorCarreraRuts,matriculadosPorCarreraPuntajes,"Matriculados UTEM.xlsx")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        contenidoArchivoCreado=open(dir_path+"/"+"Matriculados UTEM.xlsx", 'rb').read()  
        # print(contenidoArchivoCreado)
        contenidoArchivoCreado64=base64.b64encode(contenidoArchivoCreado)#.decode('UTF-8')
        os.remove(dir_path+"/"+"Matriculados UTEM.xlsx") 
        yield contenidoArchivoCreado64

######################################################################## Programa principal, DECLARACION DE APLICACION  ########################################################################

application = Application([servicios], 'spyne.servicio.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    #El servidor esta escuchando por el puerto 8000
    #El documento wsdl estara alojado en http://localhost:8000/?wsdl
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")
    wsgi_app = WsgiApplication(application, chunked = True, max_content_length = 2097152*1000, block_length = 1024*1024*5000)
    server = make_server('127.0.0.1', 8000, wsgi_app)
    server.serve_forever()