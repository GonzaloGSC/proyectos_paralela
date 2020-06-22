from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from mimetypes import guess_type, guess_extension # Utilizado para trabajar el MIME de archivos, comprobacion.
import re # Utilizado para .search(), busqueda de extencion en archivos
import base64 # Utilizado para trabajar con la codificación y decodificación del archivo
import csv # Utilizado para revisar el archivo decodificado, para detectar separadores y demas
import platform # Utilizado para detectar el SO
import os # Utilizado para eliminar archivo temporal de revisión
import pandas #Libreria open source, utilizada para crear xlsx

def revisarContenidoBase64(ArchivoCodificado): # Revisa el contenido del archivo para detectar si es efectivamente un CSV o no.
    dir_path = os.path.dirname(os.path.realpath(__file__)) #Detecta la posicion real del archivo soap.py, para evitar errores de busqueda de archivos en el mismo directorio.
    archivo64 = open(dir_path+"/"+ArchivoCodificado,"r")
    mensaje = archivo64.read(100012)# Tamaño de lectura en bytes para revisar, recomendado = 100012
    
    mensaje = decodificar(mensaje)
    salida = open("temporalRevisionIngreso.txt", "w")
    a = salida.write(str(mensaje))
    salida.close()
    archivoTemporal = open("temporalRevisionIngreso.txt","r")
    contador = 0
    # # print(mensaje)
    try:
        revision = csv.Sniffer().sniff(archivoTemporal.read(),";") #Realiza varios testeos sobre el archivo (separadores, delimitadores, etc.) archivo.read(1024) Fuente: https://docs.python.org/3/library/csv.html
        mensaje = archivo64.read()
        mensaje = decodificar(mensaje)
        archivo64.close()
        archivoTemporal.close()
        # if (len(mensaje)<2055): # Verifica el largo mini aceptado de los datos de entrada
        # #     print("Error: El numero de datos es menor al minimo aceptado, se necesitan al menos 2055 lineas de ruts y puntajes. El archivo no corresponde al formato admitido, por favor, reintentar.")
        #     return 0
        if (platform.system()=="Linux"): # En base al SO elimina el archivo creado para revision
            try:
                os.unlink("temporalRevisionIngreso.txt") # Eliminacion del archivo temporal
            except OSError as e:
                # print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        elif (platform.system()=="Windows"):
            try:
                os.remove("temporalRevisionIngreso.txt") # Eliminacion del archivo temporal
            except OSError as e:
                # print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        for linea in mensaje: #Revision de cada linea ingresada
            for caracter in linea: #Revision de cada caracter ingresado
                contador = contador + 1
                if (contador>32): # Detecta si la fila de ingreso es mas larga de lo debido, el largo correcto es de 32 caracteres (Ej. 19291586;123;123;123;123;123;123)
                    # print("Error: Excedido tamaño de filas, existe al menos una fila mal ingresada en el archivo. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
                if ((caracter!=";" and caracter.isnumeric()) or caracter==";"): # Detecta si el archivo ingresado contiene algun caracter que no sea numeros o punto y coma (;), si es así, detecta la falla
                    pass
                else:
                    # print("Error: Letras detectadas en contenido, el archivo debe contener solo numeros y separadores. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
            if (contador!=0 and contador<32): # Detecta si la fila de ingreso es corta, el largo correcto es de 32 caracteres (Ej. 19291586;123;123;123;123;123;123)
                # print("Error: Insuficiente tamaño de filas, existe al menos una fila mal ingresada en el archivo. El archivo no corresponde al formato admitido, por favor, reintentar.")
                return 0
            else:
                contador = 0
        # print("El archivo es correcto.") # Si finalmente el archivo ingresado pasa todos los filtros, es aceptado.
        return 1 #Aprovechando la instancia, devuelve la informacion ya decodificada
    except csv.Error:
        archivo64.close()
        archivoTemporal.close()
        if (platform.system()=="Linux"): # En base al SO elimina el archivo creado para revision
            try:
                os.unlink("temporalRevisionIngreso.txt")
            except OSError as e:
                # print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        elif (platform.system()=="Windows"):
            try:
                os.remove("temporalRevisionIngreso.txt")
            except OSError as e:
                # print("Error: %s : %s" % ("temporalRevisionIngreso.txt", e.strerror))
        # print("Error: Separadores y delimitadores no corresponden. El archivo no corresponde al formato admitido, por favor, reintentar.") # Excepcion preparada para la deteccion de otro separador en el csv o un error en la revision de este.
        return mensaje

class servicios(ServiceBase):
    @rpc(Integer, Integer, _returns = Integer)#Define el tipo de variables que entran y las que retorna
    def sumar(ctx, num1, num2):
        resultado = num1 + num2
        return resultado

    @rpc(Unicode, Unicode, Unicode, _returns = Unicode)
    def multi(ctx, mime, nombreDelArchivo, datosBase64):
        multi = mime + nombreDelArchivo + datosBase64
         ########### DECLARACION DE VARIABLES

        matriculadosPorCarreraRuts=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # Contendrá todos los RUTS de estudiantes ya matriculados en una carrera, ordenados segun carrera
        matriculadosPorCarreraPuntajes=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] # Contendrá todos los PUNTAJES de estudiantes ya matriculados en una carrera, ordenados segun carrera
        lista = []

        arregloDePuntajesPsu = revisarContenidoBase64(datosBase64)
        return multi