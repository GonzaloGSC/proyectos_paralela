from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class servicios(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def validarusuario(ctx, name, con):
        
        usuario= "usuario"
        contra = 12345
        if (name == usuario and con == contra):
            valido = "valido"
            return valido
        else:
            valido = "invalido"
            return valido
        
       # for i in range(times):
        #    yield u'Hello, %s' % name


application = Application([servicios], 'spyne.servicio.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
