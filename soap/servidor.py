from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import fun

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