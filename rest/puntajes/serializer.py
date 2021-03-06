from .models import postulante, autores
from rest_framework import serializers

class postulanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = postulante
        fields = '__all__'

class codigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = postulante
        fields = ('Codigo',)

class autoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = autores
        fields = '__all__'
