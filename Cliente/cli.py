from suds.client import Client
sumarservicio = Client('http://localhost:8000/?wsdl')
print (sumaservicio.sumar(2, 5))

