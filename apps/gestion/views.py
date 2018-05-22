from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from .models import Tarjeta,Prestamo, Inversion, Chequera, Ingreso, Gasto, Transferencia
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        chequeras = Chequera.objects.filter(user_id=user[0].id)

        ctx = {
            	'usuario': usuario,
                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones':inversiones,
                'chequeras':chequeras,
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
                        saldo_inicial = saldo_inicial,
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
                mensaje_cuenta = (True,"Ya existe una cuenta registrada con este número")

        if 'bc4' in request.POST:
            nombre = request.POST.get('c_name')
            entidad = request.POST.get('c_entidad')
            tipo_divisa = request.POST.get('divisa')
            numero_cuenta = request.POST.get('c_numCuenta')
            monto = request.POST.get('c_mon')
            numero_cheques = request.POST.get('c_numCheques')



            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            chequeras = Chequera.objects.filter(user_id=user[0].id)


            num_cuenta_exist = False
            for num_cuenta in chequeras:
                if str(num_cuenta.numero_cuenta) == str(numero_cuenta):
                    num_cuenta_exist = True

            if not num_cuenta_exist:
                chequera = Chequera.objects.create(
                        nombre= nombre,
                        entidad = entidad,
                        tipo_divisa = tipo_divisa,
                        numero_cuenta = numero_cuenta,
                        monto = monto,
                        numero_cheques = numero_cheques,
                        user_id= user[0].id
                )

                chequera.save()
                chequeras = Chequera.objects.filter(user_id=user[0].id)

            else:
                mensaje_cuenta = (True,"Ya existe una cuenta registrada con este número")

        template = loader.get_template('gestion/gestionCuentas.html')

        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)
        chequeras = Chequera.objects.filter(user_id=user[0].id)

        ctx = {
                'usuario': usuario,
                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones':inversiones,
                'chequeras':chequeras,
                'mensaje_cuenta': mensaje_cuenta,
        }
        return HttpResponse(template.render(ctx,request))

@login_required(login_url='/ingresar/')
def gestionTransacciones(request):

    mensaje_cuenta = (False,"")
    template = loader.get_template('gestion/gestionTransacciones.html')

    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]


        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)
        chequeras = Chequera.objects.filter(user_id=user[0].id)

        ingresos = Ingreso.objects.filter(user_id=user[0].id)
        gastos = Gasto.objects.filter(user_id=user[0].id)
        transferencias = Transferencia.objects.filter(user_id=user[0].id)

        ctx = {
                'usuario': usuario,

                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones': inversiones,
                'chequeras': chequeras,

                'ingresos': ingresos,
                'gastos': gastos,
                'transferencias': transferencias,

                'mensaje_cuenta': mensaje_cuenta,
        }
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':
        if 'bc1' in request.POST:
            nombre = request.POST.get('c_name')
            monto = request.POST.get('c_mon')
            tipo_divisa = request.POST.get('divisa')
            cuenta_ingresar = request.POST.get('cuenta')
            fecha_ingreso = request.POST.get('fechai')
            notas_adicionales = request.POST.get('notas')

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            ingresos = Ingreso.objects.filter(user_id=user[0].id)

            ingreso = Ingreso.objects.create(
                    nombre = nombre,
                    monto = monto,
                    tipo_divisa = tipo_divisa,
                    cuenta_ingresar = cuenta_ingresar,
                    fecha_ingreso = fecha_ingreso,
                    notas_adicionales = notas_adicionales,
                    user_id= user[0].id,
            )



            ingreso.save()
            ingresos = Ingreso.objects.filter(user_id=user[0].id)

        if 'bc2' in request.POST:
            nombre = request.POST.get('c_name')
            monto = request.POST.get('c_mon')
            tipo_divisa = request.POST.get('divisa')
            cuenta_retirar = request.POST.get('cuenta')
            fecha_gasto = request.POST.get('fechag')
            notas_adicionales = request.POST.get('notas')

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            gastos = Gasto.objects.filter(user_id=user[0].id)

            gasto = Gasto.objects.create(
                    nombre = nombre,
                    monto = monto,
                    tipo_divisa = tipo_divisa,
                    cuenta_retirar = cuenta_retirar,
                    fecha_gasto = fecha_gasto,
                    notas_adicionales = notas_adicionales,
                    user_id= user[0].id,
            )



            gasto.save()
            gastos = Gasto.objects.filter(user_id=user[0].id)

        if 'bc3' in request.POST:
            nombre = request.POST.get('c_name')
            monto = request.POST.get('c_mon')
            tipo_divisa = request.POST.get('divisa')
            cuenta_fuente = request.POST.get('cuentaF')
            cuenta_destino = request.POST.get('cuentaD')
            notas_adicionales = request.POST.get('notas')

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            transferencias = Transferencia.objects.filter(user_id=user[0].id)

            transferencia = Transferencia.objects.create(
                    nombre = nombre,
                    monto = monto,
                    tipo_divisa = tipo_divisa,
                    cuenta_fuente = cuenta_fuente,
                    cuenta_destino= cuenta_destino,
                    notas_adicionales = notas_adicionales,
                    user_id= user[0].id,
            )



            transferencia.save()
            transferencias = Transferencia.objects.filter(user_id=user[0].id)

        template = loader.get_template('gestion/gestionTransacciones.html')

        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)
        chequeras = Chequera.objects.filter(user_id=user[0].id)

        ingresos = Ingreso.objects.filter(user_id=user[0].id)
        gastos = Gasto.objects.filter(user_id=user[0].id)
        transferencias = Transferencia.objects.filter(user_id=user[0].id)



        ctx = {
                'usuario': usuario,

                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones': inversiones,
                'chequeras': chequeras,

                'ingresos': ingresos,
                'gastos': gastos,
                'transferencias':transferencias,

                'mensaje_cuenta': mensaje_cuenta,
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

def paginacion(request):
    tarjetas= Tarjeta.objects.all()
    paginator = Paginator(tarjetas, 1) # Show 25 contacts per page
    page = request.GET.get('page')
    # ?page=1
    tarjetas = paginator.get_page(page)
    return render(request, 'gestion/gestionCuentas.html', {'tarjetas': tarjetas})
