from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from .models import Tarjeta,Prestamo, Inversion
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required(login_url='/ingresar/')
def gestionMenu(request):
    username = request.GET.get('username')
    template = loader.get_template('gestion/Gestion.html')
    user = User.objects.filter(username=username)
    usuario = Usuario.objects.filter(user_id=user[0].id)
    usuario = usuario[0]
    ctx = {
        	'usuario': usuario,
    }
    return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def gestionCuentas(request):

    mensaje_cuenta = (False,"")
    template = loader.get_template('gestion/gestionCuentas.html')
    if request.method == 'GET':
        username = request.GET.get('username')
        user =  User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)

        ctx = {
            	'usuario': usuario,
                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones':inversiones,
        }
        return HttpResponse(template.render(ctx,request))


    if request.method == 'POST':
        if 'bc1' in request.POST:
            nombre = request.POST.get('c_name')
            numero_tarjeta = request.POST.get('c_num')
            saldo_inicial = request.POST.get('c_saldo')
            entidad = request.POST.get('c_entidad')
            numero_cuenta = request.POST.get('c_numCuenta')
            fecha_vencimiento_mm = request.POST.get('mm')
            fecha_vencimiento_aa = request.POST.get('aa')
            tipo_divisa = request.POST.get('divisa')

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            tarjetas = Tarjeta.objects.filter(user_id=user[0].id)

            error=False
            for tarjeta in tarjetas:
                if str(tarjeta.numero_tarjeta) == str(numero_tarjeta):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una tarjeta registrada con este número")

                else:
                    if str(tarjeta.numero_cuenta) == str(numero_cuenta):
                        error=True
                        mensaje_cuenta = (True,"Ya existe una cuenta registrada con este número")

            if not error:
                tarjeta = Tarjeta.objects.create(
                        nombre= nombre,
                        numero_tarjeta = numero_tarjeta,
                        numero_cuenta = numero_cuenta,
                        entidad = entidad,
                        fecha_vencimiento_mm = fecha_vencimiento_mm,
                        fecha_vencimiento_aa = fecha_vencimiento_aa,
                        tipo_divisa = tipo_divisa,
                        user_id= user[0].id
                )

                tarjeta.save()
                tarjetas = Tarjeta.objects.filter(user_id=user[0].id)



        if 'bc2' in request.POST:
            nombre = request.POST.get('c_name')
            entidad = request.POST.get('c_entidad')
            monto = request.POST.get('c_mon')
            interes = request.POST.get('interes')
            fecha_prestamo = request.POST.get('fecha_prestamo')
            fecha_limite = request.POST.get('fecha_limite')
            tipo_divisa = request.POST.get('divisa')
            tipo_pago = request.POST.get('pago')

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            prestamos = Prestamo.objects.filter(user_id=user[0].id)

            prestamo = Prestamo.objects.create(
                    nombre = nombre,
                    entidad = entidad,
                    monto = monto,
                    interes = interes,
                    fecha_prestamo = fecha_prestamo,
                    fecha_limite = fecha_limite,
                    tipo_divisa = tipo_divisa,
                    tipo_pago = tipo_pago,
                    user_id= user[0].id,
            )

            prestamo.save()
            prestamos = Prestamo.objects.filter(user_id=user[0].id)

        if 'bc3' in request.POST:
            nombre = request.POST.get('c_name')
            entidad = request.POST.get('c_entidad')
            numero_cuenta = request.POST.get('c_numCuenta')
            monto = request.POST.get('c_mon')
            interes = request.POST.get('interes')
            fecha_prestamo = request.POST.get('fecha_prestamo')
            fecha_limite = request.POST.get('fecha_limite')
            tipo_divisa = request.POST.get('divisa')

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            inversiones = Inversion.objects.filter(user_id=user[0].id)


            num_cuenta_exist = False
            for num_cuenta in inversiones:
                if str(num_cuenta.numero_cuenta) == str(numero_cuenta):
                    num_cuenta_exist = True

            if not num_cuenta_exist:
                inversion = Inversion.objects.create(
                        nombre= nombre,
                        entidad = entidad,
                        numero_cuenta = numero_cuenta,
                        monto = monto,
                        interes = interes,
                        fecha_prestamo = fecha_prestamo,
                        fecha_limite = fecha_limite,
                        tipo_divisa = tipo_divisa,
                        user_id= user[0].id
                )

                inversion.save()
                inversiones = Inversion.objects.filter(user_id=user[0].id)

            else:
                mensaje_cuenta = (True,"Ya existe una cuenta con este numero de cuenta")



        template = loader.get_template('gestion/gestionCuentas.html')

        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)

        ctx = {
                'usuario': usuario,
                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones':inversiones,
                'mensaje_cuenta': mensaje_cuenta
        }
        return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def gestionTransacciones(request):
    username = request.GET.get('username')
    template = loader.get_template('gestion/gestionTransacciones.html')
    user = User.objects.filter(username=username)
    usuario = Usuario.objects.filter(user_id=user[0].id)
    usuario = usuario[0]
    ctx = {
        	'usuario': usuario,
    }
    return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def gestionPresupuesto(request):
    username = request.GET.get('username')
    template = loader.get_template('gestion/gestionPresupuesto.html')
    user = User.objects.filter(username=username)
    usuario = Usuario.objects.filter(user_id=user[0].id)
    usuario = usuario[0]
    ctx = {
        	'usuario': usuario,
    }
    return HttpResponse(template.render(ctx,request))
