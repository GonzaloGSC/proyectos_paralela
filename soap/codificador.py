import base64
import os

#Detecta la posicion real del archivo soap.py, para evitar errores de busqueda de archivos en el mismo directorio.
dir_path = os.path.dirname(os.path.realpath(__file__)) 

# Lectura de archivo de puntajes sin codificar
archivoPuntajes=open(dir_path+"/"+"puntajesBloq.csv", "r")
texto=archivoPuntajes.read()
archivoPuntajes.close()

# Codificacion
base64_cadena_bytes = base64.b64encode(texto.encode('ascii'))
base64_message = base64_cadena_bytes.decode('ascii')

# Escritura de datos codificados
salida=open(dir_path+"/"+"puntajesEncode.txt", "w")
a=salida.write(base64_message)
salida.close()