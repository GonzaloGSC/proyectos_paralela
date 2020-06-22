from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import fun

#clase servicios aqui se encuentran alojados todos los posibles servicios
# class servicios(ServiceBase):
#     @rpc(Unicode, Integer, _returns=Unicode)
    #Define el tipo de variables que entran y las que retorna
    #Los valores dados por el cliente se encuentran en name y con
    #ctx es un valor necesario para que el servicio funcione correctamente
    # def validarusuario(ctx, name, con):
        
    #     usuario= "usuario"
    #     contra = 12345
    #     if (name == usuario and con == contra):
    #         valido = "valido"
    #         return valido
    #     else:
    #         valido = "invalido"
    #         return valido
    #realiza una suma simple entre dos enteros
    # @rpc(Integer, Integer, _returns = Integer)
    #Define el tipo de variables que entran y las que retorna
    # def sumara(ctx, num1, num2):
    #     tata = fun.sumar(num1,num2)
    #     return tata
    #suma dos string en una variable cadena
    # @rpc(Unicode, Unicode, _returns=Unicode)
    # def cadena(ctx, cad1, cad2):
    #     cadena1 = cad1 + cad2
        
        # return cadena
    #Compara dos numeros y devuelve un bool
    # @rpc(Unicode, Unicode, _returns = bool)
    # def verdaderofalso(ctx, num1, num2):
    #     if num1 > num2:
    #         verdadero= True
    #         return verdadero
    #     else:
    #         verdadero = False
    #         return verdadero

    # @rpc(Unicode, _returns = Unicode)
    # def webarchivo(ctx, documento):
    #     return "hola"



application = Application([fun.servicios], 'spyne.servicio.soap',
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
    wsgi_app = WsgiApplication(application, chunked = True, max_content_length = 2097152*100, block_length = 1024*1024*500)
    server = make_server('127.0.0.1', 8000, wsgi_app)
    server.serve_forever()

    #
    #