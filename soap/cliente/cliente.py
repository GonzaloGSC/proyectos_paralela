from suds.client import Client
import base64
import os
import pandas
wsdl = Client('http://localhost:8000/?wsdl')


def codificar(nombreArchivo):
    #Detecta la posicion real del archivo soap.py, para evitar errores de busqueda de archivos en el mismo directorio.
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    # Lectura de archivo de puntajes sin codificar
    archivoPuntajes=open(dir_path+"/"+nombreArchivo, "r")
    texto=archivoPuntajes.read()
    archivoPuntajes.close()
    # Codificacion
    base64_cadena_bytes = base64.b64encode(texto.encode('ascii'))
    base64_message = base64_cadena_bytes.decode('ascii')
    return base64_message

def decodificar(textoCodificado): # Decodifica el archivo de ingreso, utilizando en primera instancia, la codificacion ascii para luego decodificar correctamente la informacion desde base64
    try:
        cadena_bytes = base64.b64decode(textoCodificado.encode('ascii'))
        textoDecode = cadena_bytes.decode('ascii')
        textoDecode = textoDecode.split("\n") # Separa el string en los saltos de linea
        return textoDecode
    except:
        print("Error: Falla inesperada en decodificación de respuesta del servidor, revise la codificacion base64 del archivo, esta puede haber sido cortada.")



# Envio de archivo en solicitud de procesamiento al servidor
respuesta = wsdl.service.programaPrincipal("text/csv","puntajes.csv",codificar("puntajes.csv"))

print(respuesta[0][2])
arregloDatos = base64.b64decode(respuesta[0][2])
print(arregloDatos)