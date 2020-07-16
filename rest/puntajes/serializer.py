from .models import postulante
from rest_framework import serializers

class postulanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = postulante
        fields = '__all__'