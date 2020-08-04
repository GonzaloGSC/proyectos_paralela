from django.shortcuts import render
#clases para vistas
from rest_framework import viewsets, views, filters, generics
#modelos BBDD
from .models import postulante, autores
#serializador transforma el formato
from .serializer import postulanteSerializer, autoresSerializer
#mensaje de error
from django.shortcuts import get_object_or_404
#autentificacion por token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Imports de las weas magicas
from django_filters.rest_framework import DjangoFilterBackend # imports de filtros para realizar busquedas.
from rest_framework.filters import OrderingFilter, SearchFilter # imports para ordenar la busqueda.
from rest_framework import generics #import para utilizar los tipos de vistas 
import json
class postulanteViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = postulante.objects.all()
    serializer_class = postulanteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['Nombre','Codigo']

class autoresViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = autores.objects.all()
    serializer_class = autoresSerializer
    

class buscarcodigo(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cod = request.GET['Codigo']
        print(cod)
        carrera = postulante.objects.filter(Codigo = cod)
        seria = postulanteSerializer(carrera, many=True)
        return Response(seria.data)
    #    carrera = postulante.objects.get(Codigo = 21041)
    #    print(carrera)
    #    return Response("hola")
    
class buscarcarrera(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        consulta = request.GET['Nombre']
        print(consulta)
        resultado = postulante.objects.filter(Nombre__icontains = consulta)
        serializador = postulanteSerializer(resultado, many=True)
        return Response(serializador.data)

class CarrerasListView(generics.ListAPIView):
    queryset = postulante.objects.all()
    serializer_class = postulanteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['Nombre','Codigo']

class postular(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = postulante.objects.all()
    serializer_class = postulanteSerializer
    def post(self, request):
        # postulante.objects.filter(id=1).delete()
        # ingreso = request.GET['nem']
        bdddato = postulante.objects.all()
        opciones = []
        for i in bdddato:
            p0 = (float(i.Nem)/100)*float(json.loads(request.POST['nem']))#['nem']
            p1 = (float(i.Ranking)/100)*float(json.loads(request.POST['ranking']))
            p2 = (float(i.Lenguaje)/100)*float(json.loads(request.POST['lenguaje']))
            p3 = (float(i.Matematicas)/100)*float(json.loads(request.POST['matematicas']))
            if (float(json.loads(request.POST['historia']))>=float(json.loads(request.POST['ciencias']))):
                p4 = (float(i.Historia)/100)*float(json.loads(request.POST['histoia']))
            else:
                p4 = (float(i.Ciencias)/100)*float(json.loads(request.POST['ciencias']))
            ponderacion = p0+p1+p2+p3+p4
            posicion = 0
            contador = 0
            while(True):
                puntajexposicion = (i.PrimerMatriculado-i.UltimoMatriculado)/i.Vacantes
                if (ponderacion>=i.PrimerMatriculado):
                    posicion = 1
                    break
                if (ponderacion<=i.UltimoMatriculado):
                    posicion = int(i.Vacantes)
                    break
                if (ponderacion>=i.PrimerMatriculado-(puntajexposicion*contador)):
                    posicion = contador+1
                    break
                contador = contador+1
            opciones.append([i.Nombre,ponderacion,i.Codigo,posicion])
        opciones.sort(key=lambda x: x[1], reverse=1)
        mejoresdiez = opciones[0:10]
        print(mejoresdiez)
        data = {}
        data['MejoresOpcionesPostulacion'] = []
        for carrera in mejoresdiez:
            data['MejoresOpcionesPostulacion'].append({
            'codigo_carrera': carrera[2],
            'nombre_carrera': carrera[0],
            'puntaje_postulacion': carrera[1],
            'lugar_tentativo': carrera[3]})

        # data = json.loads(request.POST['nem'])
        # print(data)

        
        return Response(data)
    


####################################################


# class Consulta1ListView(generics.ListAPIView): #Listado para busquedas sobre proyectos GENERAL
#     serializer_class = postulanteSerializer
#     queryset=postulante.objects.all()
#     filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, )
#     data= (
#         'Nombre',
#         'Codigo',
#         'Nem',
#         'Ranking',
#         'Lenguaje',
#         'Matematicas',
#         'Historia',
#         'Ciencias',
#         'PuntajePromedio',
#         'PuntajeMinimo',
#         'Vacantes',
#         'PrimerMatriculado',
#         'UltimoMatriculado'
#     )
#     filter_fields = data #Campos por los que filtra los datos.
#     ordering_fields = data  #Campos por los que ordena los datos, falta estadoProyecto.
#     ordering = ('Nombre',) # Prioridad de orden por defecto.
#     search_fields = data #Busqueda general de toda la vida en los campos indicados.