# Generated by Django 3.0.8 on 2020-07-16 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puntajes', '0002_auto_20200712_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='autores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('integrante_1', models.CharField(max_length=50)),
                ('integrante_2', models.CharField(max_length=50)),
                ('integrante_3', models.CharField(max_length=50)),
            ],
        ),
    ]
