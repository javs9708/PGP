from django.conf.urls import url, include
from apps.gestion.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^menu/',login_required(gestionMenu), name='menu')

]
