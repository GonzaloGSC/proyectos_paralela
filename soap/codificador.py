import base64

# Lectura de archivo de puntajes sin codificar
archivoPuntajes=open("pruebas.txt", "r")
texto=archivoPuntajes.read()
archivoPuntajes.close()

# Codificacion
base64_cadena_bytes = base64.b64encode(texto.encode('ascii'))
base64_message = base64_cadena_bytes.decode('ascii')

# Escritura de datos codificados
salida=open("puntajesEncode.txt", "w")
a=salida.write(base64_message)
salida.close()