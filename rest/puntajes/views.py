from django.shortcuts import render
#clases para vistas
from rest_framework import viewsets, views, filters
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
# Create your views here.

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
        carrera = postulante.objects.filter(Codigo = '21041')
        seria = postulanteSerializer(carrera, many=True)
        return Response(seria.data)
    #    carrera = postulante.objects.get(Codigo = 21041)
    #    print(carrera)
    #    return Response("hola")
    
