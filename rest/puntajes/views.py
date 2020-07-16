from django.shortcuts import render
#clases para vistas
from rest_framework import viewsets, views, filters
#modelos BBDD
from .models import postulante
#serializador transforma el formato
from .serializer import postulanteSerializer
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
    

class buscarcodigo(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print (hola)
        #carrera = postulante.objects.filter(Nombre=request)
        #seriealizer = postulanteSerializer(carrera)
        return Response(request)

    #def get(self, request):
    #    return "trasero"