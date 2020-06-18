
######################################################################## SECTOR DE IMPORTS ########################################################################

from mimetypes import guess_type, guess_extension
import re
import base64 
import csv
import platform # Usado para detectar el SO
import os # Usado para eliminar archivo temporal de revisión



######################################################################## SECTOR DE FUNCIONES ########################################################################

def codificar(nombreDelArchivo):
    # Lectura de archivo de puntajes sin codificar
    archivoPuntajes = open("puntajesNoEncode.csv", "r")
    texto=archivoPuntajes.read()
    archivoPuntajes.close()
    # Codificacion
    base64_cadena_bytes = base64.b64encode(texto.encode('ascii'))
    texto_base64 = base64_cadena_bytes.decode('ascii')
    return texto_base64
    
def decodificar(textoCodificado):
    try:
        cadena_bytes = base64.b64decode(textoCodificado.encode('ascii'))
        textoDecode = cadena_bytes.decode('ascii')
        textoDecode = textoDecode.split("\n") 
        return textoDecode
    except:
        print("Error: Falla inesperada en codificación.")
        return 0


def revisarMime(nombreDelArchivo): # Revisa el mime del nombre de archivo ingresado. Retorna el MIME de csv cuando es correcto. fuente: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    resultado=guess_type(nombreDelArchivo)
    if(resultado[0]=="application/vnd.ms-excel" and re.search(".csv$" , nombreDelArchivo) ): #Detecta Mime del archivo
        print("MIME detectado = text/csv("+str(resultado[0])+")")
        return "text/csv"
    else:
        print("MIME detectado = "+str(resultado[0]))
        print("Error: MIME Incorrecto, debe utilizar text/csv. El archivo no corresponde al formato admitido, por favor, reintentar.")
        return resultado[0]

def revisarContenidoCSV(ArchivoCodificado): # Revisa el contenido del archivo para detectar si es efectivamente un CSV o no.
    archivo64 = open(ArchivoCodificado,"r")
    mensaje = archivo64.read(1024)
    archivo64.close()
    mensaje = decodificar(mensaje)
    salida = open("temporalRevisionIngreso.txt", "w")
    a=salida.write(str(mensaje))
    salida.close()
    archivoTemporal = open("temporalRevisionIngreso.txt","r")
    contador = 0
    try:
        revision = csv.Sniffer().sniff(archivoTemporal.read(),";") #Realiza varios testeos sobre el archivo (separadores, delimitadores, etc.) archivo.read(1024) Fuente: https://docs.python.org/3/library/csv.html
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
        for linea in mensaje: #Revision de cada linea ingresada
            for caracter in linea: #Revision de cada caracter ingresado
                contador = contador + 1
                if (contador>32):
                    print("Error: Excedido tamaño de filas. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
                if ((caracter!=";" and caracter.isnumeric()) or caracter==";"):
                    pass
                else:
                    print("Error: Letras detectadas en contenido. El archivo no corresponde al formato admitido, por favor, reintentar.")
                    return 0
            if (contador!=0 and contador<32):
                print("Error: Insuficiente tamaño de filas. El archivo no corresponde al formato admitido, por favor, reintentar.")
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

######################################################################## Definicion de variables ########################################################################



######################################################################## SECTOR DE PRUEBAS ########################################################################

# archivo64 = open("puntajesEncode.txt","r")
# mensaje = archivo64.read()

revisarMime("puntajes.csv")
revisarContenidoCSV("puntajesEncode.txt")

