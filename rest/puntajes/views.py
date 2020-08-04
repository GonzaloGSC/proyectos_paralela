from django.shortcuts import render
#clases para vistas
from rest_framework import viewsets, views, filters, generics
#modelos BBDD
from .models import postulante, autores
#serializador transforma el formato
from .serializer import postulanteSerializer, autoresSerializer,codigoSerializer
#mensaje de error
from django.shortcuts import get_object_or_404
#autentificacion por token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.

class postulanteViewSet(viewsets.ModelViewSet):
    
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
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        consulta = request.GET.get('Nombre')
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
        numero1 = request.query_params['numero']
        obj = postulante.objects.get(pk=1)
        num1=1
        seria=codigoSerializer(num1)
        print(numero1)
        print(obj)
        return Response(seria.data)