from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from ..gestion.models import Tarjeta,Prestamo, Inversion, Chequera, Ingreso, Gasto, Transferencia, Presupuesto
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required(login_url='/ingresar/')
def visualizarMenu(request):
    template = loader.get_template('visualizar/Visualizar.html')
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]
        ctx = {
            	'usuario': usuario,
        }
        return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def visualizarCuentas(request):
    template = loader.get_template('visualizar/visualizar_cuentas.html')
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        tarjeta = Tarjeta.objects.filter(user_id=user[0].id)
        prestamo = Prestamo.objects.filter(user_id=user[0].id)
        inversion = Inversion.objects.filter(user_id=user[0].id)
        chequera = Chequera.objects.filter(user_id=user[0].id)

        ctx = {
            	'usuario': usuario,

                'tarjeta': tarjeta,
                'prestamo': prestamo,
                'inversion': inversion,
                'chequera': chequera,
        }
        return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def visualizarTransacciones(request):
    template = loader.get_template('visualizar/visualizar_transacciones.html')
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        ingreso = Ingreso.objects.filter(user_id=user[0].id)
        gasto = Gasto.objects.filter(user_id=user[0].id)
        transferencia = Transferencia.objects.filter(user_id=user[0].id)


        ctx = {
            	'usuario': usuario,

                'ingreso': ingreso,
                'gasto': gasto,
                'transferencia': transferencia,

        }
        return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def visualizarPresupuestos(request):
    username = request.GET.get('username')
    template = loader.get_template('visualizar/visualizar_transacciones.html')
    user = User.objects.filter(username=username)
    usuario = Usuario.objects.filter(user_id=user[0].id)
    usuario = usuario[0]
    ctx = {
        	'usuario': usuario,
    }
    return HttpResponse(template.render(ctx,request))
