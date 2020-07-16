from django.db import models

# Create your models here.

class postulante(models.Model):
    Nombre = models.CharField(max_length = 50)
    Codigo = models.IntegerField()
    Nem = models.DecimalField(max_digits = 5, decimal_places = 2)
    Ranking = models.DecimalField(max_digits = 5, decimal_places = 2)
    Lenguaje = models.DecimalField(max_digits = 5, decimal_places = 2)
    Matematicas = models.DecimalField(max_digits = 5, decimal_places = 2)
    Historia = models.DecimalField(max_digits = 5, decimal_places = 2)
    Ciencias = models.DecimalField(max_digits = 5, decimal_places = 2)
    PuntajePromedio = models.DecimalField(max_digits = 5, decimal_places = 2)
    PuntajeMinimo = models.DecimalField(max_digits = 5, decimal_places = 2)
    Vacantes = models.IntegerField()
    PrimerMatriculado = models.DecimalField(max_digits = 5, decimal_places = 2)
    UltimoMatriculado = models.DecimalField(max_digits = 5, decimal_places = 2)


class autores(models.Model):
    integrante = models.CharField(max_length = 50)
