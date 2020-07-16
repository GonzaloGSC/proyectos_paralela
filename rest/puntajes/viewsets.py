from rest_framework import viewsets
from .models import postulante
from .serializer import postulanteSerializer

class postulanteViewSet(viewsets.ModelViewSet):
    queryset = postulante.objects.all()
    serializer_class = postulanteSerializer