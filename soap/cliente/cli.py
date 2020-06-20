from suds.client import Client
import base64
import os
wsdl = Client('http://localhost:8000/?wsdl')
print (wsdl.service.sumar(2, 5))


# cad = wsdl.service.verdaderofalso(2,3)
# print (cad)

dir_path = os.path.dirname(os.path.realpath(__file__))
archivo = open(dir_path+"/"+"doc.csv","r")
narchivo = archivo.read()

hola= base64.encodestring(narchivo.encode('ascii'))

#print (hola)
documento = wsdl.service.webarchivo(hola)
# print (documento)

#from zeep import Client

#client = Client('http://localhost:8000/?wsdl')

#resultas = client.service.webarchivo(hola)