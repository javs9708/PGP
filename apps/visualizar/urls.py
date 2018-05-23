from django.conf.urls import url, include
from apps.visualizar.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^menu/',visualizarMenu, name='menu'),
    url(r'^cuentas/',visualizarCuentas, name='cuentas'),
    url(r'^transacciones/',visualizarTransacciones, name='transacciones'),
    url(r'^presupuestos/',visualizarPresupuestos, name='presupuesto'),
]
