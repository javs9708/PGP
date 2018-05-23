from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from .models import Tarjeta,Prestamo, Inversion, Chequera, Ingreso, Gasto, Transferencia, Presupuesto
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

            saldo_inicial=int(saldo_inicial)
            numero_tarjeta=int(numero_tarjeta)
            numero_cuenta=int(numero_cuenta)

            error=False
            for tarjeta in tarjetas:
                if str(tarjeta.numero_tarjeta) == str(numero_tarjeta):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una tarjeta registrada con este número")

                else:
                    if str(tarjeta.numero_cuenta) == str(numero_cuenta):
                        error=True
                        mensaje_cuenta = (True,"Ya existe una cuenta registrada con este número")
                    else:
                        if str(tarjeta.nombre) == str(nombre):
                            error=True
                            mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")
                        else:
                            if (saldo_inicial<0) or (numero_tarjeta<0) or (numero_cuenta<0):
                                error=True
                                mensaje_cuenta = (True,"No puede ingresar numeros negativos")
                            else:
                                if (saldo_inicial==0) or (numero_tarjeta==0) or (numero_cuenta==0):
                                    error=True
                                    mensaje_cuenta = (True,"Ingrese un numero valido")


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

            monto=int(monto)
            interes=int(interes)

            error=False
            for prestamo in prestamos:
                if str(prestamo.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe un prestamo registrado con este nombre")
                else:
                    if (monto<0) or (interes<0):
                        error=True
                        mensaje_cuenta = (True,"No puede ingresar numeros negativos")
                    else:
                        if (monto==0) or (interes==0):
                            error=True
                            mensaje_cuenta = (True,"Ingrese un numero valido")

            if not error:
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

            monto=int(monto)
            interes=int(interes)
            numero_cuenta=int(numero_cuenta)

            num_cuenta_exist = False
            for num_cuenta in inversiones:
                if str(num_cuenta.numero_cuenta) == str(numero_cuenta):
                    num_cuenta_exist = True
                    mensaje_cuenta = (True,"Ya existe una inversion registrada con este número")

                else:
                    if str(num_cuenta.nombre) == str(nombre):
                        num_cuenta_exist=True
                        mensaje_cuenta = (True,"Ya existe una inversion registrada con este nombre")

                    else:
                        if (monto<0) or (interes<0) or (numero_cuenta<0):
                            num_cuenta_exist=True
                            mensaje_cuenta = (True,"No puede ingresar numeros negativos")

                        else:
                            if (monto==0) or (interes==0) or (numero_cuenta==0):
                                num_cuenta_exist=True
                                mensaje_cuenta = (True,"Ingrese un numero valido")

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

            monto=int(monto)
            numero_cheques=int(numero_cheques)
            numero_cuenta=int(numero_cuenta)


            num_cuenta_exist = False
            for num_cuenta in chequeras:
                if str(num_cuenta.numero_cuenta) == str(numero_cuenta):
                    num_cuenta_exist = True
                    mensaje_cuenta = (True,"Ya existe una chequera registrada con este número")
                else:
                    if str(num_cuenta.nombre) == str(nombre):
                        num_cuenta_exist=True
                        mensaje_cuenta = (True,"Ya existe una chequera registrada con este nombre")

                    else:
                        if (monto<0) or (numero_cheques<0) or (numero_cuenta<0):
                            num_cuenta_exist=True
                            mensaje_cuenta = (True,"No puede ingresar numeros negativos")
                        else:
                            if (monto==0) or (numero_cheques==0) or (numero_cuenta==0):
                                num_cuenta_exist=True
                                mensaje_cuenta = (True,"Ingrese un numero valido")

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

        if 'delete_tarjeta' in request.POST:
            id_tarjeta = request.POST.get('id_tarjeta')        
            tarjeta = Tarjeta.objects.get(id=id_tarjeta)

            if tarjeta is not None:
                tarjeta.delete()

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]


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

            error = False
            for ingreso in ingresos:
                if str(ingreso.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una transacción con este nombre")

            if not error:
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



            tarjeta = Tarjeta.objects.filter(nombre=cuenta_ingresar).exists()
            prestamo = Prestamo.objects.filter(nombre=cuenta_ingresar).exists()
            inversion = Inversion.objects.filter(nombre=cuenta_ingresar).exists()
            chequera = Chequera.objects.filter(nombre=cuenta_ingresar).exists()

            if tarjeta:
                tarjeta = Tarjeta.objects.get(nombre=cuenta_ingresar)
                monto=int(monto)
                tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                tarjeta.saldo_inicial+=monto
                tarjeta.save()

            if prestamo:
                prestamo = Prestamo.objects.get(nombre=cuenta_ingresar)
                monto=int(monto)
                prestamo.monto=int(prestamo.monto)
                prestamo.monto+=monto
                prestamo.save()

            if inversion:
                inversion = Inversion.objects.get(nombre=cuenta_ingresar)
                monto=int(monto)
                inversion.monto=int(inversion.monto)
                inversion.monto+=monto
                inversion.save()

            if chequera:
                chequera = Chequera.objects.get(nombre=cuenta_ingresar)
                monto=int(monto)
                chequera.monto=int(chequera.monto)
                chequera.monto+=monto
                chequera.save()


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

            error=False
            for gasto in gastos:
                if str(gasto.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una transacción con este nombre")


            if not error:
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

            tarjeta = Tarjeta.objects.filter(nombre=cuenta_retirar).exists()
            prestamo = Prestamo.objects.filter(nombre=cuenta_retirar).exists()
            inversion = Inversion.objects.filter(nombre=cuenta_retirar).exists()
            chequera = Chequera.objects.filter(nombre=cuenta_retirar).exists()

            if tarjeta:
                tarjeta = Tarjeta.objects.get(nombre=cuenta_retirar)
                monto=int(monto)
                tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                tarjeta.saldo_inicial-=monto
                tarjeta.save()

            if prestamo:
                prestamo = Prestamo.objects.get(nombre=cuenta_retirar)
                monto=int(monto)
                prestamo.monto=int(prestamo.monto)
                prestamo.monto-=monto
                prestamo.save()

            if inversion:
                inversion = Inversion.objects.get(nombre=cuenta_retirar)
                monto=int(monto)
                inversion.monto=int(inversion.monto)
                inversion.monto-=monto
                inversion.save()

            if chequera:
                chequera = Chequera.objects.get(nombre=cuenta_retirar)
                monto=int(monto)
                chequera.monto=int(chequera.monto)
                chequera.monto-=monto
                chequera.save()

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

            error=False
            for transferencia in transferencias:
                if str(transferencia.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una transacción con este nombre")

            if not error:
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

            tarjeta = Tarjeta.objects.filter(nombre=cuenta_fuente).exists()
            tarjetaD = Tarjeta.objects.filter(nombre=cuenta_destino).exists()

            prestamo = Prestamo.objects.filter(nombre=cuenta_fuente).exists()
            prestamoD = Prestamo.objects.filter(nombre=cuenta_destino).exists()

            inversion = Inversion.objects.filter(nombre=cuenta_fuente).exists()
            inversionD = Inversion.objects.filter(nombre=cuenta_destino).exists()

            chequera = Chequera.objects.filter(nombre=cuenta_fuente).exists()
            chequeraD = Chequera.objects.filter(nombre=cuenta_destino).exists()

            if tarjeta:
                tarjeta = Tarjeta.objects.get(nombre=cuenta_fuente)
                monto=int(monto)
                tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                tarjeta.saldo_inicial-=monto
                tarjeta.save()

            if tarjetaD:
                tarjeta = Tarjeta.objects.get(nombre=cuenta_destino)
                monto=int(monto)
                tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                tarjeta.saldo_inicial+=monto
                tarjeta.save()

            if prestamo:
                prestamo = Prestamo.objects.get(nombre=cuenta_fuente)
                monto=int(monto)
                prestamo.monto=int(prestamo.monto)
                prestamo.monto-=monto
                prestamo.save()

            if prestamoD:
                prestamo = Prestamo.objects.get(nombre=cuenta_destino)
                monto=int(monto)
                prestamo.monto=int(prestamo.monto)
                prestamo.monto+=monto
                prestamo.save()

            if inversion:
                inversion = Inversion.objects.get(nombre=cuenta_fuente)
                monto=int(monto)
                inversion.monto=int(inversion.monto)
                inversion.monto-=monto
                inversion.save()

            if inversionD:
                inversion = Inversion.objects.get(nombre=cuenta_destino)
                monto=int(monto)
                inversion.monto=int(inversion.monto)
                inversion.monto+=monto
                inversion.save()

            if chequera:
                chequera = Chequera.objects.get(nombre=cuenta_fuente)
                monto=int(monto)
                chequera.monto=int(chequera.monto)
                chequera.monto-=monto
                chequera.save()

            if chequeraD:
                chequera = Chequera.objects.get(nombre=cuenta_destino)
                monto=int(monto)
                chequera.monto=int(chequera.monto)
                chequera.monto+=monto
                chequera.save()

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
    mensaje_cuenta = (False,"")
    template = loader.get_template('gestion/gestionPresupuesto.html')

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

        presupuestos = Presupuesto.objects.filter(user_id=user[0].id)

        ctx = {
                'usuario': usuario,

                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones': inversiones,
                'chequeras': chequeras,

                'ingresos': ingresos,
                'gastos': gastos,
                'transferencias': transferencias,

                'presupuestos':presupuestos,

                'mensaje_cuenta': mensaje_cuenta,
        }
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':
        if 'bc1' in request.POST:
            nombre = request.POST.get('c_name')
            monto = request.POST.get('c_mon')
            tipo_divisa = request.POST.get('divisa')
            cuenta = request.POST.get('cuenta')
            saldo_reinversion = request.POST.get('c_saldoR')
            periodo_recurrencia_num = request.POST.get('c_periodoRecurrenciaD')
            periodo_recurrencia_tiem = request.POST.get('c_periodoRecurrenciaT')
            categoria = request.POST.get('c_categoria')

            periodo_recurrencia_num=str(periodo_recurrencia_num)
            periodo_recurrencia_tiem=str(periodo_recurrencia_tiem)

            periodo_recurrencia=periodo_recurrencia_num+" "+periodo_recurrencia_tiem

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            presupuestos = Presupuesto.objects.filter(user_id=user[0].id)

            error=False
            for presupuesto in presupuestos:
                if str(presupuesto.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe un presupuesto con este nombre")

            if not error:
                presupuesto = Presupuesto.objects.create(
                        nombre = nombre,
                        monto = monto,
                        tipo_divisa = tipo_divisa,
                        cuenta = cuenta,
                        saldo_reinversion = saldo_reinversion,
                        periodo_recurrencia = periodo_recurrencia,
                        categoria = categoria,
                        user_id= user[0].id,
                )
                presupuesto.save()
                presupuestos = Presupuesto.objects.filter(user_id=user[0].id)

        template = loader.get_template('gestion/gestionPresupuesto.html')

        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)
        chequeras = Chequera.objects.filter(user_id=user[0].id)

        ingresos = Ingreso.objects.filter(user_id=user[0].id)
        gastos = Gasto.objects.filter(user_id=user[0].id)
        transferencias = Transferencia.objects.filter(user_id=user[0].id)

        presupuestos = Presupuesto.objects.filter(user_id=user[0].id)



        ctx = {
                'usuario': usuario,

                'tarjetas': tarjetas,
                'prestamos': prestamos,
                'inversiones': inversiones,
                'chequeras': chequeras,

                'ingresos': ingresos,
                'gastos': gastos,
                'transferencias':transferencias,

                'presupuestos':presupuestos,

                'mensaje_cuenta': mensaje_cuenta,
        }
        return HttpResponse(template.render(ctx,request))

def paginacion(request):
    tarjetas= Tarjeta.objects.all()
    paginator = Paginator(tarjetas, 1) # Show 25 contacts per page
    page = request.GET.get('page')
    # ?page=1
    tarjetas = paginator.get_page(page)
    return render(request, 'gestion/gestionCuentas.html', {'tarjetas': tarjetas})
