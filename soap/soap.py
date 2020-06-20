
######################################################################## SECTOR DE IMPORTS ########################################################################

from mimetypes import guess_type, guess_extension # Utilizado para trabajar el MIME de archivos, comprobacion.
import re # Utilizado para .search(), busqueda de extencion en archivos
import base64 # Utilizado para trabajar con la codificación y decodificación del archivo
import csv # Utilizado para revisar el archivo decodificado, para detectar separadores y demas
import platform # Utilizado para detectar el SO
import os # Utilizado para eliminar archivo temporal de revisión


######################################################################## SECTOR DE FUNCIONES ########################################################################

# def codificar(nombreDelArchivo):
#     # Lectura de archivo de puntajes sin codificar
#     archivoPuntajes = open("puntajesNoEncode.csv", "r")
#     texto=archivoPuntajes.read()
#     archivoPuntajes.close()
#     # Codificacion
#     base64_cadena_bytes = base64.b64encode(texto.encode('ascii'))
#     texto_base64 = base64_cadena_bytes.decode('ascii')
#     return texto_base64
    
def decodificar(textoCodificado): # Decodifica el archivo de ingreso, utilizando en primera instancia, la codificacion ascii para luego decodificar correctamente la informacion desde base64
    try:
        cadena_bytes = base64.b64decode(textoCodificado.encode('ascii'))
        textoDecode = cadena_bytes.decode('ascii')
        textoDecode = textoDecode.split("\n") # Separa el string en los saltos de linea
        return textoDecode
    except:
        print("Error: Falla inesperada en decodificación, revise la codificacion base64 del archivo, esta puede haber sido cortada. Otra opcion, es modificar la cantidad de bytes aceptados en la funcion: revisarContenidoBase64, linea: mensaje = archivo64.read(100012)")

# programaPrincipal("ctx","text/csv","puntajes.csv","puntajesEncode.txt")
def revisarMime(nombreDelArchivo): # Revisa el mime del nombre de archivo ingresado. Retorna el MIME de csv cuando es correcto. fuente: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    resultado=guess_type(nombreDelArchivo)
    if(resultado[0]=="application/vnd.ms-excel" and re.search(".csv$" , nombreDelArchivo)): #Detecta Mime del archivo
        print("MIME detectado = text/csv ("+str(resultado[0])+")")
        return "text/csv"
    else:
        print("MIME detectado = "+str(resultado[0]))
        print("Error: MIME Incorrecto, debe utilizar text/csv. El archivo no corresponde al formato admitido, por favor, reintentar.")
        return resultado[0]

def revisarContenidoBase64(ArchivoCodificado): # Revisa el contenido del archivo para detectar si es efectivamente un CSV o no.
    dir_path = os.path.dirname(os.path.realpath(__file__)) #Detecta la posicion real del archivo soap.py, para evitar errores de busqueda de archivos en el mismo directorio.
    archivo64 = open(dir_path+"/"+ArchivoCodificado,"r")
    mensaje = archivo64.read(100012)# Tamaño de lectura en bytes para revisar, recomendado = 100012
    archivo64.close()
    mensaje = decodificar(mensaje)
    salida = open("temporalRevisionIngreso.txt", "w")
    a = salida.write(str(mensaje))
    salida.close()
    archivoTemporal = open("temporalRevisionIngreso.txt","r")
    contador = 0
    # print(mensaje)
    try:
        revision = csv.Sniffer().sniff(archivoTemporal.read(),";") #Realiza varios testeos sobre el archivo (separadores, delimitadores, etc.) archivo.read(1024) Fuente: https://docs.python.org/3/library/csv.html
        archivoTemporal.close()
        wea=mensaje[1900:]
        # print(str(wea))
        # print("LARGO = "+ str(len(mensaje)))
        if (len(mensaje)<2055):
            print("Error: El numero de datos es menor al minimo aceptado, se necesitan al menos 2055 lineas de ruts y puntajes. El archivo no corresponde al formato admitido, por favor, reintentar.")
            return 0
        if (platform.system()=="Linux"): # En base al SO elimina el archivo creado para revision
            try:
                os.unlink("temporalRevisionIngreso.txt")
            except OSError as e:
                print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        elif (platform.system()=="Windows"):
            try:
                os.remove("temporalRevisionIngreso.txt")
            except OSError as e:
                print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        for linea in mensaje: #Revision de cada linea ingresada
            for caracter in linea: #Revision de cada caracter ingresado
                contador = contador + 1
                if (contador>32):
                    print("Error: Excedido tamaño de filas, existe al menos una fila mal ingresada en el archivo. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
                if ((caracter!=";" and caracter.isnumeric()) or caracter==";"):
                    pass
                else:
                    print("Error: Letras detectadas en contenido, el archivo debe contener solo numeros y separadores. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
            if (contador!=0 and contador<32):
                print("Error: Insuficiente tamaño de filas, existe al menos una fila mal ingresada en el archivo. El archivo no corresponde al formato admitido, por favor, reintentar.")
                return 0
            else:
                contador = 0
        print("El archivo es correcto.")
        return 1
    except csv.Error:
        archivoTemporal.close()
        if (platform.system()=="Linux"): # En base al SO elimina el archivo creado para revision
            try:
                os.unlink("temporalRevisionIngreso.txt")
            except OSError as e:
                print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        elif (platform.system()=="Windows"):
            try:
                os.remove("temporalRevisionIngreso.txt")
            except OSError as e:
                print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        print("Error: Separadores y delimitadores no corresponden. El archivo no corresponde al formato admitido, por favor, reintentar.")
        return 0

######################################################################## Programa principal  ########################################################################

# TAMAÑO MINIMO DE 2055 ESTUDIANTES EN EL INGRESO DE DATOS

def programaPrincipal(ctx,mime,nombreDelArchivo,datosBase64):#FUNCION QUE DEBE ESTAR DENTRO DE LA CLASE SERVIDOR O SERVICIO

    #Declaracion de variables

    matriculadosPorCarrera=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # Contendrá todos los estudiantes ya matriculados en una carrera, ordenados segun carrera
    ponderacionCarreras = [] # contiene los grupos de carrera segun criterios de ingreso a ellas.
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

    #Comprobacion de datos ingresados

    if (not (revisarContenidoBase64(datosBase64)) or revisarMime(nombreDelArchivo)!="text/csv" or mime!="text/csv"):# Comprueba datos de ingreso (nombre del archivo, mime, e informacion codifiada en base64)
        if (mime!="text/csv"):
            print("Recepcion de MIME incorrecto, usar text/csv.")
        return print("Finalizando ejecucion...")

    #Operacion sobre datos

    dir_path = os.path.dirname(os.path.realpath(__file__)) #Detecta la posicion real del archivo soap.py, para evitar errores de busqueda de archivos en el mismo directorio.
    archivo64 = open(dir_path+"/"+datosBase64,"r")
    mensaje = archivo64.read()
    archivo64.close()
    arregloDePuntajesPsu = decodificar(mensaje)
    contadorPostulante = 0
    print("Obteniendo ponderaciones por estudiante a cada carrera...")
    for datosPostulante in arregloDePuntajesPsu:
        
        arregloDePuntajesPsu[contadorPostulante]=datosPostulante.split(";")
        
        if (len(arregloDePuntajesPsu[contadorPostulante])==7):
            arregloDePuntajesPsu[contadorPostulante][0]=int(arregloDePuntajesPsu[contadorPostulante][0])
            arregloDePuntajesPsu[contadorPostulante][1]=float(arregloDePuntajesPsu[contadorPostulante][1])
            arregloDePuntajesPsu[contadorPostulante][2]=float(arregloDePuntajesPsu[contadorPostulante][2])
            arregloDePuntajesPsu[contadorPostulante][3]=float(arregloDePuntajesPsu[contadorPostulante][3])
            arregloDePuntajesPsu[contadorPostulante][4]=float(arregloDePuntajesPsu[contadorPostulante][4])
            arregloDePuntajesPsu[contadorPostulante][5]=float(arregloDePuntajesPsu[contadorPostulante][5])
            arregloDePuntajesPsu[contadorPostulante][6]=float(arregloDePuntajesPsu[contadorPostulante][6])
            np = arregloDePuntajesPsu[contadorPostulante]

            ponderacionesDelAlumno=[]
            if (np[5]>=np[6] and (np[3]+np[4])/2>450):
                ponderacionesDelAlumno.append(np[0])
                ponderacionesDelAlumno.append(round(np[1]*0.15+np[2]*0.2+np[3]*0.25+np[4]*0.3+np[5]*0.1,2))
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
            elif((np[3]+np[4])/2>450):
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
            ponderacionCarreras.append(ponderacionesDelAlumno) 
        contadorPostulante = contadorPostulante + 1  
    print("Asignando carreras a los mejores postulantes...")
    print("Carrera 1...")
    largo=len(ponderacionCarreras)
    c1=int(35/2055*largo)
    c2=int(80/2055*largo)
    c3=int(125/2055*largo)
    c4=int(30/2055*largo)
    c5=int(90/2055*largo)
    c6=int(25/2055*largo)
    c7=int(100/2055*largo)
    c8=int(60/2055*largo)
    c9=int(40/2055*largo)
    c10=int(65/2055*largo)
    c11=int(95/2055*largo)
    c12=int(130/2055*largo)
    c13=int(200/2055*largo)
    c14=int(105/2055*largo)
    lista = ponderacionCarreras[0:c1]
    s=len(lista)
    lista.sort(key=lambda x: x[1], reverse=1)
    b=0
    while(b<35):
        matriculadosPorCarrera[0].append([lista[b][0],lista[b][1]])
        b=b+1
    print("Carrera 2...")
    lista = ponderacionCarreras[s:s+c1]
    s=s+len(lista)
    lista.sort(key=lambda x: x[2], reverse=1)
    b=0
    while(b<35):
        matriculadosPorCarrera[1].append([lista[b][0],lista[b][2]])
        b=b+1
    print("Carrera 3...")
    lista = ponderacionCarreras[s:s+c2]
    s=s+len(lista)
    lista.sort(key=lambda x: x[3], reverse=1)
    b=0
    while(b<80):
        matriculadosPorCarrera[2].append([lista[b][0],lista[b][3]])
        b=b+1
    print("Carrera 4...")
    lista = ponderacionCarreras[s:s+c3]
    s=s+len(lista)
    lista.sort(key=lambda x: x[4], reverse=1)
    b=0
    while(b<125):
        matriculadosPorCarrera[3].append([lista[b][0],lista[b][4]])
        b=b+1
    print("Carrera 5...")
    lista = ponderacionCarreras[s:s+c4]
    s=s+len(lista)
    lista.sort(key=lambda x: x[4], reverse=1)
    b=0
    while(b<30):
        matriculadosPorCarrera[4].append([lista[b][0],lista[b][4]])
        b=b+1
    print("Carrera 6...")
    lista = ponderacionCarreras[s:s+c5]
    s=s+len(lista)
    lista.sort(key=lambda x: x[4], reverse=1)
    b=0
    while(b<90):
        matriculadosPorCarrera[5].append([lista[b][0],lista[b][4]])
        b=b+1
    print("Carrera 7...")
    lista = ponderacionCarreras[s:s+c6]
    s=s+len(lista)
    lista.sort(key=lambda x: x[4], reverse=1)
    b=0
    while(b<25):
        matriculadosPorCarrera[6].append([lista[b][0],lista[b][4]])
        b=b+1
    print("Carrera 8...")
    lista = ponderacionCarreras[s:s+c7]
    s=s+len(lista)
    lista.sort(key=lambda x: x[5], reverse=1)
    b=0
    while(b<100):
        matriculadosPorCarrera[7].append([lista[b][0],lista[b][5]])
        b=b+1
    print("Carrera 9...")
    lista = ponderacionCarreras[s:s+c7]
    s=s+len(lista)
    lista.sort(key=lambda x: x[6], reverse=1)
    b=0
    while(b<100):
        matriculadosPorCarrera[8].append([lista[b][0],lista[b][6]])
        b=b+1
    print("Carrera 10...")
    lista = ponderacionCarreras[s:s+c7]
    s=s+len(lista)
    lista.sort(key=lambda x: x[6], reverse=1)
    b=0
    while(b<100):
        matriculadosPorCarrera[9].append([lista[b][0],lista[b][6]])
        b=b+1
    print("Carrera 11...")
    lista = ponderacionCarreras[s:s+c4]
    s=s+len(lista)
    lista.sort(key=lambda x: x[7], reverse=1)
    b=0
    while(b<30):
        matriculadosPorCarrera[10].append([lista[b][0],lista[b][7]])
        b=b+1    
    print("Carrera 12...")
    lista = ponderacionCarreras[s:s+c8]
    s=s+len(lista)
    lista.sort(key=lambda x: x[8], reverse=1)
    b=0
    while(b<60):
        matriculadosPorCarrera[11].append([lista[b][0],lista[b][8]])
        b=b+1
    print("Carrera 13...")
    lista = ponderacionCarreras[s:s+c4]
    s=s+len(lista)
    lista.sort(key=lambda x: x[8], reverse=1)
    b=0
    while(b<30):
        matriculadosPorCarrera[12].append([lista[b][0],lista[b][8]])
        b=b+1 
    print("Carrera 14...")
    lista = ponderacionCarreras[s:s+c2]
    s=s+len(lista)
    lista.sort(key=lambda x: x[9], reverse=1)
    b=0
    while(b<80):
        matriculadosPorCarrera[13].append([lista[b][0],lista[b][9]])
        b=b+1    
    print("Carrera 15...")
    lista = ponderacionCarreras[s:s+c9]
    s=s+len(lista)
    lista.sort(key=lambda x: x[9], reverse=1)
    b=0
    while(b<40):
        matriculadosPorCarrera[14].append([lista[b][0],lista[b][9]])
        b=b+1    
    print("Carrera 16...")
    lista = ponderacionCarreras[s:s+c7]
    s=s+len(lista)
    lista.sort(key=lambda x: x[10], reverse=1)
    b=0
    while(b<100):
        matriculadosPorCarrera[15].append([lista[b][0],lista[b][10]])
        b=b+1
    print("Carrera 17...")
    lista = ponderacionCarreras[s:s+c10]
    s=s+len(lista)
    lista.sort(key=lambda x: x[10], reverse=1)
    b=0
    while(b<65):
        matriculadosPorCarrera[16].append([lista[b][0],lista[b][10]])
        b=b+1
    print("Carrera 18...")
    lista = ponderacionCarreras[s:s+c11]
    s=s+len(lista)
    lista.sort(key=lambda x: x[11], reverse=1)
    b=0
    while(b<95):
        matriculadosPorCarrera[17].append([lista[b][0],lista[b][11]])
        b=b+1
    print("Carrera 19...")
    lista = ponderacionCarreras[s:s+c6]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<25):
        matriculadosPorCarrera[18].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 20...")
    lista = ponderacionCarreras[s:s+c6]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<25):
        matriculadosPorCarrera[19].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 21...")
    lista = ponderacionCarreras[s:s+c12]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<130):
        matriculadosPorCarrera[20].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 22...")
    lista = ponderacionCarreras[s:s+c13]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<200):
        matriculadosPorCarrera[21].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 23...")
    lista = ponderacionCarreras[s:s+c8]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<60):
        matriculadosPorCarrera[22].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 24...")
    lista = ponderacionCarreras[s:s+c2]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<80):
        matriculadosPorCarrera[23].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 25...")
    lista = ponderacionCarreras[s:s+c5]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<90):
        matriculadosPorCarrera[24].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 26...")
    lista = ponderacionCarreras[s:s+c8]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<60):
        matriculadosPorCarrera[25].append([lista[b][0],lista[b][12]])
        b=b+1
    print("Carrera 27...")
    lista = ponderacionCarreras[s:s+c14]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    b=0
    while(b<105):
        matriculadosPorCarrera[26].append([lista[b][0],lista[b][12]])
        b=b+1
    b=0
    print("Carrera 28...")
    lista = ponderacionCarreras[s:s+c8]
    s=s+len(lista)
    lista.sort(key=lambda x: x[12], reverse=1)
    while(b<60):
        matriculadosPorCarrera[27].append([lista[b][0],lista[b][12]])
        b=b+1
    print(matriculadosPorCarrera)

programaPrincipal("ctx","text/csv","puntajes.csv","puntajesEncode.txt")
