from django.conf.urls import url, include
from apps.visualizar.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^menu/',visualizarMenu, name='menu'),
    
    url(r'^cuentas/',visualizarCuentas, name='cuentas'),
    url(r'^transacciones/',visualizarTransacciones, name='transacciones'),
    url(r'^presupuesto/',visualizarPresupuestos, name='presupuesto'),

    url(r'^editar_tarjeta/',editarTarjeta, name='editar_tarjeta'),
    url(r'^editar_prestamos/',editarPrestamos, name='editar_prestamos'),
    url(r'^editar_inversiones/',editarInversiones, name='editar_inversiones'),
    url(r'^editar_chequeras/',editarChequeras, name='editar_chequeras'),
]
