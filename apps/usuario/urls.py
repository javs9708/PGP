from django.conf.urls import url, include
from apps.usuario.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [

    url(r'^perfil/',visualizarPerfil, name='perfil'),
    url(r'^editar_perfil/',editarPerfil, name='EPerfil')
] 
