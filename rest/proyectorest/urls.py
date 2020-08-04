"""proyectorest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from puntajes import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0.01/', include('puntajes.urls')),
    path('api/v0.01/codigo',views.buscarcodigo.as_view()),
    path('api/v0.01/search',views.CarrerasListView.as_view()),
    path('api/v0.01/carrera',views.buscarcarrera.as_view()),
    path('api/v0.01/postular',views.postular.as_view()),

    # path('consulta1View', views.Consulta1ListView.as_view()),#wea magica

    path('api/v1/auth/',
        include('rest_auth.urls')),
    path('api/v1/auth/registration/', 
        include('rest_auth.registration.urls')),
]
