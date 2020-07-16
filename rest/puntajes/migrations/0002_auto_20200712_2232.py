# Generated by Django 3.0.8 on 2020-07-13 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puntajes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postulante',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='postulante',
            name='tittle',
        ),
        migrations.AddField(
            model_name='postulante',
            name='Ciencias',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Codigo',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Historia',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Lenguaje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Matematicas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Nem',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Nombre',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='PrimerMatriculado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='PuntajeMinimo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='PuntajePromedio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Ranking',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='UltimoMatriculado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postulante',
            name='Vacantes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]