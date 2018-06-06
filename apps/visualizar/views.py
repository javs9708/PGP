from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from ..gestion.models import Tarjeta,Prestamo, Inversion, Chequera, Ingreso, Gasto, Transferencia, Presupuesto
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.auth.decorators import login_required
from .funciones.validadores import *

@login_required(login_url='/ingresar/')
def visualizarMenu(request):
    template = loader.get_template('visualizar/Visualizar.html')
    if request.method == 'GET':
        username = request.GET.get('username')
        user =  User.objects.filter(username=username)
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

        tarjeta = Tarjeta.objects.filter(user_id=user[0].id)
        prestamo = Prestamo.objects.filter(user_id=user[0].id)
        inversion = Inversion.objects.filter(user_id=user[0].id)
        chequera = Chequera.objects.filter(user_id=user[0].id)


        ctx = {
            	'usuario': usuario,

                'ingreso': ingreso,
                'gasto': gasto,
                'transferencia': transferencia,

                'tarjeta': tarjeta,
                'prestamo': prestamo,
                'inversion': inversion,
                'chequera': chequera,

        }
        return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def visualizarPresupuestos(request):
    template = loader.get_template('visualizar/visualizar_presupuesto.html')
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        presupuesto= Presupuesto.objects.filter(user_id=user[0].id)

        ctx = {
            	'usuario': usuario,

                'presupuesto':presupuesto,
        }
        return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def editarTarjeta(request):

    if request.method == 'GET':

        template = loader.get_template('visualizar/editar_tarjeta.html')
        tarjeta_id =  request.GET.get('tarjeta_id')
        tarjetas = Tarjeta.objects.filter(id=tarjeta_id)
        tarjetas = Tarjeta.objects.get(id=tarjeta_id)

        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]



        ctx = {
        'usuario': usuario,
        'tarjetas': tarjetas,
        }
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':

        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        tarjeta_id =  request.GET.get('tarjeta_id')
        tarjetas = Tarjeta.objects.filter(id=tarjeta_id)
        tarjetas = Tarjeta.objects.get(id=tarjeta_id)

        nombre = request.POST.get('nombre')
        entidad = request.POST.get('entidad')


        tarjetas.nombre=nombre
        tarjetas.entidad = entidad

        tarjetas.save()
        return redirect('/visualizar/cuentas?username='+usuario.user.username)

    template = loader.get_template('visualizar/editar_tarjeta.html')
    ctx = {
            'usuario': usuario,
            'tarjetas': tarjetas,

            }
    return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def editarInversiones(request):
    if request.method == 'GET':
        template = loader.get_template('visualizar/editar_inversiones.html')
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]
        inversion_id =  request.GET.get('inversion_id')
        inversiones = Inversion.objects.filter(id=inversion_id)
        inversiones = Inversion.objects.get(id=inversion_id)

        fecha_prestamo=inversiones.fecha_prestamo
        fecha_prestamo=str(fecha_prestamo)

        fecha_limite=inversiones.fecha_limite
        fecha_limite=str(fecha_limite)


        ctx = {
            	'usuario': usuario,
                'inversiones':inversiones,
                'fecha_prestamo': fecha_prestamo,
                'fecha_limite': fecha_limite,
        }
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':
        error=(False,"")
        errorM=False
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        inversion_id =  request.GET.get('inversion_id')
        inversiones = Inversion.objects.filter(id=inversion_id)
        inversiones = Inversion.objects.get(id=inversion_id)

        fecha_prestamo=inversiones.fecha_prestamo
        fecha_prestamo=str(fecha_prestamo)

        fecha_limite=inversiones.fecha_limite
        fecha_limite=str(fecha_limite)

        nombre = request.POST.get('nombre')
        entidad = request.POST.get('entidad')
        fecha_prestamo = request.POST.get('fecha_prestamo')
        fecha_limite = request.POST.get('fecha_limite')

        if validar_fecha_prestamo(fecha_prestamo):
            error=(True,"Ingrese una fecha de prestamo valida")
            errorM=True
        if validar_fecha_limite(fecha_limite):
            error=(True,"Ingrese una fecha de limite valida")
            errorM=True

        if not errorM:
            inversiones.nombre=nombre
            inversiones.entidad = entidad
            inversiones.fecha_prestamo = fecha_prestamo
            inversiones.fecha_limite = fecha_limite

            inversiones.save()
            return redirect('/visualizar/cuentas?username='+usuario.user.username)

    template = loader.get_template('visualizar/editar_inversiones.html')
    ctx = {
            'usuario': usuario,
            'inversiones': inversiones,
            'fecha_prestamo': fecha_prestamo,
            'fecha_limite': fecha_limite,
            'error':error,

            }
    return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def editarPrestamos(request):
    if request.method == 'GET':

        template = loader.get_template('visualizar/editar_prestamos_hipotecas.html')
        prestamo_id =  request.GET.get('prestamo_id')
        prestamos = Prestamo.objects.filter(id=prestamo_id)
        prestamos = Prestamo.objects.get(id=prestamo_id)

        fecha_prestamo=prestamos.fecha_prestamo
        fecha_prestamo=str(fecha_prestamo)

        fecha_limite=prestamos.fecha_limite
        fecha_limite=str(fecha_limite)

        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]



        ctx = {
        'usuario': usuario,
        'fecha_prestamo': fecha_prestamo,
        'fecha_limite': fecha_limite,
        'prestamos': prestamos,
        }
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':
        errorM=False
        error=(False,"")
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        prestamo_id =  request.GET.get('prestamo_id')
        prestamos = Prestamo.objects.filter(id=prestamo_id)
        prestamos = Prestamo.objects.get(id=prestamo_id)

        fecha_prestamo=prestamos.fecha_prestamo
        fecha_prestamo=str(fecha_prestamo)

        fecha_limite=prestamos.fecha_limite
        fecha_limite=str(fecha_limite)

        nombre = request.POST.get('nombre')
        entidad = request.POST.get('entidad')
        interes= request.POST.get('interes')
        fecha_prestamo = request.POST.get('fecha_prestamo')
        fecha_limite = request.POST.get('fecha_limite')
        tipo_pago = request.POST.get('pago')

        if validar_fecha_prestamo(fecha_prestamo):
            error=(True,"Ingrese una fecha de prestamo valida")
            errorM=True
        if validar_fecha_limite(fecha_limite):
            error=(True,"Ingrese una fecha de limite valida")
            errorM=True

        if not errorM:
            prestamos.nombre=nombre
            prestamos.entidad = entidad
            prestamos.interes= interes
            prestamos.fecha_prestamo=fecha_prestamo
            prestamos.fecha_limite=fecha_limite
            prestamos.tipo_pago=tipo_pago

            prestamos.save()
            return redirect('/visualizar/cuentas?username='+usuario.user.username)

    template = loader.get_template('visualizar/editar_prestamos_hipotecas.html')
    ctx = {'error':error,
            'usuario': usuario,
            'fecha_prestamo': fecha_prestamo,
            'fecha_limite': fecha_limite,
            'prestamos': prestamos,

            }
    return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def editarChequeras(request):
    if request.method == 'GET':
        template = loader.get_template('visualizar/editar_chequera.html')

        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        chequera_id =  request.GET.get('chequera_id')
        chequeras = Chequera.objects.filter(id=chequera_id)
        chequeras = Chequera.objects.get(id=chequera_id)


        ctx = {
            	'usuario': usuario,

                'chequeras':chequeras,
        }
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':

        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        chequera_id =  request.GET.get('chequera_id')
        chequeras = Chequera.objects.filter(id=chequera_id)
        chequeras = Chequera.objects.get(id=chequera_id)

        nombre = request.POST.get('nombre')
        entidad = request.POST.get('entidad')
        numero_cheques = request.POST.get('numero_cheques')

        chequeras.nombre=nombre
        chequeras.entidad = entidad
        chequeras.numero_cheques= numero_cheques


        chequeras.save()
        return redirect('/visualizar/cuentas?username='+usuario.user.username)

    template = loader.get_template('visualizar/editar_prestamos_hipotecas.html')
    ctx = {
            'usuario': usuario,

            'chequeras': chequeras,

            }
    return HttpResponse(template.render(ctx,request))
