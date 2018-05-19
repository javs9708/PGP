from django.conf.urls import url, include
from apps.visualizar.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^menu/',visualizarMenu, name='menu'),
]
