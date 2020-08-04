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
from rest_framework import generics #import para utilizar los tipos de vistas 
import json
from django.http import JsonResponse #import para las respuestas del servicio


class autores(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = autores.objects.all()
        serializador = autoresSerializer(queryset, many=True)
        return JsonResponse({'ok':True,'data':serializador.data}, status=200)

class buscarcodigo(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if ('Codigo' in request.GET):
            if (request.GET.get('Codigo').isdigit()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'Codigo' presenta un tipo de dato incorrecto."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'Codigo'."}, status=400)
        cod = request.GET.get('Codigo')
        carrera = postulante.objects.filter(Codigo = cod)
        serializador = postulanteSerializer(carrera, many=True)
        return JsonResponse({'ok':True,'data':serializador.data}, status=200)
    
class buscarcarrera(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if ('Nombre' in request.GET):
            if (request.GET.get('Nombre').isalpha()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'Nombre' presenta un tipo de dato incorrecto."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'Nombre'."}, status=400)
        consulta = request.GET.get('Nombre')
        resultado = postulante.objects.filter(Nombre__icontains = consulta)
        serializador = postulanteSerializer(resultado, many=True)
        return JsonResponse({'ok':True,'data':serializador.data}, status=200)

class postular(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = postulante.objects.all()
    serializer_class = postulanteSerializer
    def post(self, request):
        ################################# SE REVISA EL JSON DE INGRESO
        if ('nem' in request.POST):
            if (request.POST['nem'].isdigit()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'nem' presenta un tipo de dato incorrecto."}, status=400)
            if (int(request.POST['nem'])>850):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'nem' presenta un numero superior 850pts."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'nem'."}, status=400)
        if ('ciencias' in request.POST != True):
            if (request.POST['ciencias'].isdigit()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'ciencias' presenta un tipo de dato incorrecto."}, status=400)
            if (int(request.POST['ciencias'])>850):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'ciencias' presenta un numero superior 850pts."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'ciencias'."}, status=400)
        if ('historia' in request.POST != True):
            if (request.POST['historia'].isdigit()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'historia' presenta un tipo de dato incorrecto."}, status=400)
            if (int(request.POST['historia'])>850):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'historia' presenta un numero superior 850pts."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'historia'."}, status=400)
        if ('matematicas' in request.POST != True):
            if (request.POST['matematicas'].isdigit()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'matematicas' presenta un tipo de dato incorrecto."}, status=400)
            if (int(request.POST['matematicas'])>850):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'matematicas' presenta un numero superior 850pts."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'matematicas'."}, status=400)
        if ('lenguaje' in request.POST != True):
            if (request.POST['lenguaje'].isdigit()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'lenguaje' presenta un tipo de dato incorrecto."}, status=400)
            if (int(request.POST['lenguaje'])>850):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'lenguaje' presenta un numero superior 850pts."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'lenguaje'."}, status=400)
        if ('ranking' in request.POST != True):
            if (request.POST['ranking'].isdigit()==False):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'ranking' presenta un tipo de dato incorrecto."}, status=400)
            if (int(request.POST['ranking'])>850):
                return JsonResponse({'ok':False,'data':"json mal ingresado, la llave 'ranking' presenta un numero superior 850pts."}, status=400)
        else:
            return JsonResponse({'ok':False,'data':"json mal ingresado, falta la llave 'ranking'."}, status=400)
        ################################# SE PREPARA LA RESPUESTA
        bdddato = postulante.objects.all()
        opciones = []
        if (float((json.loads(request.POST['lenguaje']))+float(json.loads(request.POST['matematicas'])))/2<450):
            return JsonResponse({'ok':True,'data':"Lo sentimos, tu puntaje promedio entre matematicas y lenguaje es inferior a 450pts, por lo que no cumples con el minimo exigido."}, status=200)
        for i in bdddato:
            p0 = (float(i.Nem)/100)*float(json.loads(request.POST['nem']))
            p1 = (float(i.Ranking)/100)*float(json.loads(request.POST['ranking']))
            p2 = (float(i.Lenguaje)/100)*float(json.loads(request.POST['lenguaje']))
            p3 = (float(i.Matematicas)/100)*float(json.loads(request.POST['matematicas']))
            if (float(json.loads(request.POST['historia']))>=float(json.loads(request.POST['ciencias']))):
                p4 = (float(i.Historia)/100)*float(json.loads(request.POST['historia']))
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
        data = []
        for carrera in mejoresdiez:
            data.append({
            'codigo_carrera': carrera[2],
            'nombre_carrera': carrera[0],
            'puntaje_postulacion': carrera[1],
            'lugar_tentativo': carrera[3]})
        return JsonResponse({'ok':True,'data':data}, status=200)

