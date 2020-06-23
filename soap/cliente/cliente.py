from suds.client import Client
import base64, os, io

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

######################SOLICITUD Y RESPUESTA DE SERVIDOR

respuesta = wsdl.service.programaPrincipal("text/csv","puntajes.csv",codificar("puntajes.csv"))
if (respuesta[0][0]=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    arregloDatos = base64.b64decode(respuesta[0][2])
    toread = io.BytesIO()
    toread.write(arregloDatos)  # pass your `decrypted` string as the argument here
    toread.seek(0)  # reset the pointer
    with open(dir_path+"/"+respuesta[0][1], "wb") as f:
        f.write(toread.read())
    f.close()
else:
    print("Error: Falla en MIME... ")
