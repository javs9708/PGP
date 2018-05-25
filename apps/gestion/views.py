from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from .models import Tarjeta,Prestamo, Inversion, Chequera, Ingreso, Gasto, Transferencia, Presupuesto
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.auth.decorators import login_required
from .funciones.validadores import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
from itertools import chain



@login_required(login_url='/ingresar/')
def gestionMenu(request):
    template = loader.get_template('gestion/Gestion.html')
    if request.method == 'GET':
        username = request.GET.get('username')
        user =  User.objects.filter(username=username)
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
        page = request.GET.get('page')
        user =  User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)
        chequeras = Chequera.objects.filter(user_id=user[0].id)

        objetos = list(chain(tarjetas , prestamos , inversiones , chequeras))
        objetos , paginator = paginacion(objetos,page)


        ctx = {
            	'usuario': usuario,
                'objetos': objetos,
                'paginator': paginator,
                'num_pages': int(paginator.num_pages),
                'page': int(page)
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
            prestamos = Prestamo.objects.filter(user_id=user[0].id)
            inversiones = Inversion.objects.filter(user_id=user[0].id)
            cheques = Chequera.objects.filter(user_id=user[0].id)

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
                        mensaje_cuenta = (True,"Ya existe una tarjeta registrada con este número de cuenta")
                    else:
                        if str(tarjeta.nombre)==str(nombre):
                            error=True
                            mensaje_cuenta = (True,"Ya existe una tarjeta registrada con este nombre")

            for prestamo in prestamos:
                if str(prestamo.nombre)==str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")
            for inversion in inversiones:
                if str(inversion.nombre)==str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")
            for cheque in cheques:
                if str(cheque.nombre)==str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")


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
            tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
            inversiones = Inversion.objects.filter(user_id=user[0].id)
            cheques = Chequera.objects.filter(user_id=user[0].id)


            error=False
            for prestamo in prestamos:
                if str(prestamo.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe un prestamo registrado con este nombre")

            for tarjeta in tarjetas:
                if str(tarjeta.nombre)==str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")
            for inversion in inversiones:
                if str(inversion.nombre)==str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")
            for cheque in cheques:
                if str(cheque.nombre)==str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")

            if validar_fecha_prestamo(fecha_prestamo):
                error=True
                mensaje_cuenta = (True,"Ingrese una fecha de prestamo valida")

            if validar_fecha_limite(fecha_limite):
                error=True
                mensaje_cuenta = (True,"Ingrese una fecha limite valida")

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

            tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
            prestamos = Prestamo.objects.filter(user_id=user[0].id)
            inversiones = Inversion.objects.filter(user_id=user[0].id)
            cheques = Chequera.objects.filter(user_id=user[0].id)

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

            for tarjeta in tarjetas:
                if str(tarjeta.nombre)==str(nombre):
                    num_cuenta_exist=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")
            for cheque in cheques:
                if str(cheque.nombre)==str(nombre):
                    num_cuenta_exist=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")

            for prestamo in prestamos:
                if str(prestamo.nombre)==str(nombre):
                    num_cuenta_exist=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")

            if validar_fecha_prestamo(fecha_prestamo):
                num_cuenta_exist=True
                mensaje_cuenta = (True,"Ingrese una fecha de deposito valida")

            if validar_fecha_limite(fecha_limite):
                num_cuenta_exist=True
                mensaje_cuenta = (True,"Ingrese una fecha limite valida")

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

            tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
            prestamos = Prestamo.objects.filter(user_id=user[0].id)
            inversiones = Inversion.objects.filter(user_id=user[0].id)
            chequeras = Chequera.objects.filter(user_id=user[0].id)


            num_cuenta_exist = False
            for num_cuenta in chequeras:
                if str(num_cuenta.numero_cuenta) == str(numero_cuenta):
                    num_cuenta_exist = True
                    mensaje_cuenta = (True,"Ya existe una chequera registrada con este número")
                else:
                    if str(num_cuenta.nombre) == str(nombre):
                        num_cuenta_exist=True
                        mensaje_cuenta = (True,"Ya existe una chequera registrada con este nombre")

            for tarjeta in tarjetas:
                if str(tarjeta.nombre)==str(nombre):
                    num_cuenta_exist=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")


            for prestamo in prestamos:
                if str(prestamo.nombre)==str(nombre):
                    num_cuenta_exist=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")

            for inversion in inversiones:
                if str(inversion.nombre)==str(nombre):
                    num_cuenta_exist=True
                    mensaje_cuenta = (True,"Ya existe una cuenta registrada con este nombre")

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

        if 'delete_prestamo' in request.POST:
            id_prestamo = request.POST.get('id_prestamo')
            prestamo = Prestamo.objects.get(id=id_prestamo)
            if prestamo is not None:
                prestamo.delete()

        if 'delete_inversion' in request.POST:
            id_inversion = request.POST.get('id_inversion')
            inversion = Inversion.objects.get(id=id_inversion)
            if inversion is not None:
                inversion.delete()

        if 'delete_chequera' in request.POST:
            id_chequera = request.POST.get('id_chequera')
            chequera = Chequera.objects.get(id=id_chequera)
            if chequera is not None:
                chequera.delete()

        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]


        template = loader.get_template('gestion/gestionCuentas.html')

        page = request.GET.get('page')
        prestamos = Prestamo.objects.filter(user_id=user[0].id)
        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)
        inversiones = Inversion.objects.filter(user_id=user[0].id)
        chequeras = Chequera.objects.filter(user_id=user[0].id)

        objetos = list(chain(tarjetas , prestamos , inversiones , chequeras))
        objetos , paginator = paginacion(objetos,page)

        ctx = {
                'usuario': usuario,
                'objetos': objetos,
                'paginator': paginator,
                'num_pages': int(paginator.num_pages),
                'page': int(page),
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

            cuenta_ingresar=str(cuenta_ingresar)
            sin_cuentas= "Sin cuentas"

            error = False
            for ingreso in ingresos:
                if str(ingreso.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe una transacción con este nombre")

            if cuenta_ingresar == sin_cuentas:
                error=True
                mensaje_cuenta = (True,"No hay cuentas existentes para realizar la acción")

            if validar_fecha_prestamo(fecha_ingreso):
                error=True
                mensaje_cuenta = (True,"Ingrese una fecha de ingreso valida")



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

                tipo_divisa=str(tipo_divisa)

                if tarjeta:
                    tarjeta = Tarjeta.objects.get(nombre=cuenta_ingresar)
                    tipo_divisa_tarjeta=str(tarjeta.tipo_divisa)

                    #--------------- Cuenta Colombiana ----------------#
                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*2851
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*3358
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*26
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    #---------------- Cuenta Americana -----------------------#

                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.00035000
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*1.1701
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.0090800
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    #---------------- Cuenta Europea -----------------------#

                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.00030000
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.85488
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.0077700
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    #---------------- Cuenta Japonesa -----------------------#

                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.038260
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*110.01
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*128.68
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial+=monto
                        tarjeta.save()

                if prestamo:
                    prestamo = Prestamo.objects.get(nombre=cuenta_ingresar)
                    tipo_divisa_prestamo=str(prestamo.tipo_divisa)

                    #--------------------Cuenta Colombiana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*2851
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*3358
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*26
                        prestamo.monto+=monto
                        prestamo.save()
                    #--------------------Cuenta Americana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.00035000
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*1.1701
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.0090800
                        prestamo.monto+=monto
                        prestamo.save()
                    #--------------------Cuenta Europea---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.00030000
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.85488
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.0077700
                        prestamo.monto+=monto
                        prestamo.save()
                    #--------------------Cuenta Japonesa---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.038260
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*110.01
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*128.68
                        prestamo.monto+=monto
                        prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto+=monto
                        prestamo.save()

                if inversion:
                    inversion = Inversion.objects.get(nombre=cuenta_ingresar)
                    tipo_divisa_inversion=str(inversion.tipo_divisa)

                    #--------------------Cuenta Colombiana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*3358
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*2851
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*26
                        inversion.monto+=monto
                        inversion.save()
                    #--------------------Cuenta Americana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.00035000
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*1.1701
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.0090800
                        inversion.monto+=monto
                        inversion.save()
                    #--------------------Cuenta Europea---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.00030000
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.85488
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.0077700
                        inversion.monto+=monto
                        inversion.save()
                    #--------------------Cuenta Japonesa---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.038260
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*128.68
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*110.01
                        inversion.monto+=monto
                        inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto+=monto
                        inversion.save()

                if chequera:
                    chequera = Chequera.objects.get(nombre=cuenta_ingresar)
                    tipo_divisa_chequera=str(chequera.tipo_divisa)

                    #--------------------Cuenta Colombiana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*3358
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*2851
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*26
                        chequera.monto+=monto
                        chequera.save()
                    #--------------------Cuenta Americana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.00035000
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*1.1701
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.0090800
                        chequera.monto+=monto
                        chequera.save()
                    #--------------------Cuenta Europea---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.00030000
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.85488
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.0077700
                        chequera.monto+=monto
                        chequera.save()
                    #--------------------Cuenta Japonesa---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="YEN":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.038260
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="YEN":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*128.68
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="YEN":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*110.01
                        chequera.monto+=monto
                        chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="YEN":
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

            cuenta_retirar=str(cuenta_retirar)
            sin_cuentas= "Sin cuentas"

            error=False
            error2=False
            for gasto in gastos:
                if str(gasto.nombre) == str(nombre):
                    error2=True
                    error=True
                    mensaje_cuenta = (True,"Ya existe una transacción con este nombre")

            if cuenta_retirar == sin_cuentas:
                error2=True
                error=True
                mensaje_cuenta = (True,"No hay cuentas existentes para realizar la acción")

            if validar_fecha_prestamo(fecha_gasto):
                error=True
                error2=True
                mensaje_cuenta = (True,"Ingrese una fecha de gasto valida")



            if not error2:

                tarjeta = Tarjeta.objects.filter(nombre=cuenta_retirar).exists()
                prestamo = Prestamo.objects.filter(nombre=cuenta_retirar).exists()
                inversion = Inversion.objects.filter(nombre=cuenta_retirar).exists()
                chequera = Chequera.objects.filter(nombre=cuenta_retirar).exists()

                if tarjeta:
                    tarjeta = Tarjeta.objects.get(nombre=cuenta_retirar)
                    tipo_divisa_tarjeta=str(tarjeta.tipo_divisa)

                    #--------------------Cuenta Colombiana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*2851
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*3358
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="COP":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*26
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()

                    #--------------------Cuenta Americana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.00035000
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*1.1701
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="DOL":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.0090800
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()

                    #--------------------Cuenta Europea---------------#
                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.00030000
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.85488
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="EUR":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.0077700
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()

                    #--------------------Cuenta Japonesa---------------#
                    if tipo_divisa=="COP" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*0.038260
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="DOL" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*110.01
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="EUR" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        monto=monto*128.68
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()
                    if tipo_divisa=="YEN" and tipo_divisa_tarjeta=="YEN":
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.saldo_inicial-=monto
                        if tarjeta.saldo_inicial<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            tarjeta.save()

                if prestamo:
                    prestamo = Prestamo.objects.get(nombre=cuenta_retirar)
                    tipo_divisa_prestamo=str(prestamo.tipo_divisa)

                    #--------------------Cuenta Colombiana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*2851
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*3358
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="COP":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*26
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    #--------------------Cuenta Americana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.00035000
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*1.1701
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="DOL":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.0090800
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    #--------------------Cuenta Europea---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.00030000
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.85488
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="EUR":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.0077700
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    #--------------------Cuenta Japonesa---------------#
                    if tipo_divisa=="COP" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*0.038260
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="DOL" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*110.01
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="EUR" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        monto=monto*128.68
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()
                    if tipo_divisa=="YEN" and tipo_divisa_prestamo=="YEN":
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.monto-=monto
                        if prestamo.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            prestamo.save()

                if inversion:
                    inversion = Inversion.objects.get(nombre=cuenta_retirar)
                    tipo_divisa_inversion=str(inversion.tipo_divisa)

                    #--------------------Cuenta Colombiana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*3358
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*2851
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="COP":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*26
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    #--------------------Cuenta Americana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.00035000
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*1.1701
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="DOL":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.0090800
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    #--------------------Cuenta Europea---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.00030000
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.85488
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="EUR":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.0077700
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()

                    #--------------------Cuenta Japonesa---------------#
                    if tipo_divisa=="COP" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*0.038260
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="EUR" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*128.68
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="DOL" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        monto=monto*110.01
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()
                    if tipo_divisa=="YEN" and tipo_divisa_inversion=="YEN":
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.monto-=monto
                        if inversion.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            inversion.save()

                if chequera:
                    chequera = Chequera.objects.get(nombre=cuenta_retirar)
                    tipo_divisa_chequera=str(chequera.tipo_divisa)

                    #--------------------Cuenta Colombiana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*3358
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*2851
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="COP":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*26
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    #--------------------Cuenta Americana---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.00035000
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*1.1701
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="DOL":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.0090800
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    #--------------------Cuenta Europea---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.00030000
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.85488
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="EUR":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.0077700
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()

                    #--------------------Cuenta Japonesa---------------#
                    if tipo_divisa=="COP" and tipo_divisa_chequera=="YEN":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*0.038260
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="EUR" and tipo_divisa_chequera=="YEN":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*128.68
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="DOL" and tipo_divisa_chequera=="YEN":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        monto=monto*110.01
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()
                    if tipo_divisa=="YEN" and tipo_divisa_chequera=="YEN":
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.monto-=monto
                        if chequera.monto<0:
                            error=True
                            mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                        else:
                            chequera.save()

            if not error:
                monto = request.POST.get('c_mon')
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
            cuenta_fuente = request.POST.get('cuentaF')
            cuenta_destino = request.POST.get('cuentaD')
            notas_adicionales = request.POST.get('notas')

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]

            transferencias = Transferencia.objects.filter(user_id=user[0].id)

            cuenta_fuente=str(cuenta_fuente)
            sin_cuentas= "Sin cuentas"

            error=False
            error2=False
            sonIguales=False
            for transferencia in transferencias:
                if str(transferencia.nombre) == str(nombre):
                    error2=True
                    error=True
                    mensaje_cuenta = (True,"Ya existe una transacción con este nombre")

            if cuenta_fuente == sin_cuentas:
                error2=True
                error=True
                mensaje_cuenta = (True,"No hay cuentas existentes para realizar la acción")

            if not error:
                tarjeta = Tarjeta.objects.filter(nombre=cuenta_fuente).exists()
                tarjetaD = Tarjeta.objects.filter(nombre=cuenta_destino).exists()
                if tarjeta and tarjetaD:
                    tarjetaFuente = Tarjeta.objects.get(nombre=cuenta_fuente)
                    tarjetaDestino = Tarjeta.objects.get(nombre=cuenta_destino)
                    tarjetaFuente = str(tarjetaFuente.nombre)
                    tarjetaDestino = str(tarjetaDestino.nombre)
                    if tarjetaFuente==tarjetaDestino:
                        mensaje_cuenta = (True,"No puede hacer una transferencia entre una misma cuenta")
                        error2=True
                        sonIguales=True


                prestamo = Prestamo.objects.filter(nombre=cuenta_fuente).exists()
                prestamoD = Prestamo.objects.filter(nombre=cuenta_destino).exists()
                if prestamo and prestamoD:
                    prestamoFuente = Prestamo.objects.get(nombre=cuenta_fuente)
                    prestamoDestino = Prestamo.objects.get(nombre=cuenta_destino)
                    prestamoFuente = str(prestamoFuente.nombre)
                    prestamoDestino = str(prestamoDestino.nombre)
                    if prestamoFuente==prestamoDestino:
                        mensaje_cuenta = (True,"No puede hacer una transferencia entre una misma cuenta")
                        error2=True
                        sonIguales=True

                inversion = Inversion.objects.filter(nombre=cuenta_fuente).exists()
                inversionD = Inversion.objects.filter(nombre=cuenta_destino).exists()
                if inversion and inversionD:
                    inversionFuente = Inversion.objects.get(nombre=cuenta_fuente)
                    inversionDestino = Inversion.objects.get(nombre=cuenta_destino)
                    inversionFuente = str(inversionFuente.nombre)
                    inversionDestino = str(inversionDestino.nombre)
                    if inversionFuente==inversionDestino:
                        mensaje_cuenta = (True,"No puede hacer una transferencia entre una misma cuenta")
                        error2=True
                        sonIguales=True

                chequera = Chequera.objects.filter(nombre=cuenta_fuente).exists()
                chequeraD = Chequera.objects.filter(nombre=cuenta_destino).exists()
                if chequera and chequeraD:
                    chequeraFuente = Chequera.objects.get(nombre=cuenta_fuente)
                    chequeraDestino = Chequera.objects.get(nombre=cuenta_destino)
                    chequeraFuente = str(chequeraFuente.nombre)
                    chequeraDestino = str(chequeraDestino.nombre)
                    if chequeraFuente==chequeraDestino:
                        mensaje_cuenta = (True,"No puede hacer una transferencia entre una misma cuenta")
                        error2=True
                        sonIguales=True

                if not sonIguales:
                    if tarjeta:
                        tarjeta = Tarjeta.objects.get(nombre=cuenta_fuente)
                        monto=int(monto)
                        tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                        tarjeta.tipo_divisa=str(tarjeta.tipo_divisa)
                        tarjeta.saldo_inicial-=monto
                        tarjeta.save()
                        if tarjetaD:
                            tarjetaD = Tarjeta.objects.get(nombre=cuenta_destino)
                            tarjetaD.saldo_inicial=int(tarjetaD.saldo_inicial)
                            tarjetaD.tipo_divisa=str(tarjetaD.tipo_divisa)
                            if tarjeta.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*3358
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*2851
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*26
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="COP":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="DOL":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="EUR":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="YEN":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if tarjeta.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()

                        if prestamoD:
                            prestamoD = Prestamo.objects.get(nombre=cuenta_destino)
                            prestamoD.monto=int(prestamoD.monto)
                            prestamoD.tipo_divisa=str(prestamoD.tipo_divisa)
                            if tarjeta.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="COP":
                                monto=monto*3358
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="COP":
                                monto=monto*2851
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="COP":
                                monto=monto*26
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="COP" and prestamoD.tipo_divisa=="COP":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="DOL":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="COP" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="EUR":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="COP" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="YEN":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if tarjeta.tipo_divisa=="COP" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                prestamoD.monto+=monto
                                prestamoD.save()

                        if inversionD:
                            inversionD = Inversion.objects.get(nombre=cuenta_destino)
                            inversionD.monto=int(inversionD.monto)
                            inversionD.tipo_divisa=str(inversionD.tipo_divisa)
                            if tarjeta.tipo_divisa=="EUR" and inversionD.tipo_divisa=="COP":
                                monto=monto*3358
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="DOL" and inversionD.tipo_divisa=="COP":
                                monto=monto*2851
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="YEN" and inversionD.tipo_divisa=="COP":
                                monto=monto*26
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="COP" and inversionD.tipo_divisa=="COP":
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and inversionD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="DOL" and inversionD.tipo_divisa=="DOL":
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="YEN" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="COP" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and inversionD.tipo_divisa=="EUR":
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="DOL" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="YEN" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="COP" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and inversionD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="DOL" and inversionD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="YEN" and inversionD.tipo_divisa=="YEN":
                                inversionD.monto+=monto
                                inversionD.save()
                            if tarjeta.tipo_divisa=="COP" and inversionD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                inversionD.monto+=monto
                                inversionD.save()

                        if chequeraD:
                            chequeraD = Chequera.objects.get(nombre=cuenta_destino)
                            chequeraD.monto=int(chequeraD.monto)
                            chequeraD.tipo_divisa=str(chequeraD.tipo_divisa)
                            if tarjeta.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="COP":
                                monto=monto*3358
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="COP":
                                monto=monto*2851
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="COP":
                                monto=monto*26
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="COP" and chequeraD.tipo_divisa=="COP":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="DOL":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="COP" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="EUR":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="COP" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if tarjeta.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="YEN":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if tarjeta.tipo_divisa=="COP" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                chequeraD.monto+=monto
                                chequeraD.save()

                    if prestamo:
                        prestamo = Prestamo.objects.get(nombre=cuenta_fuente)
                        monto=int(monto)
                        prestamo.monto=int(prestamo.monto)
                        prestamo.tipo_divisa=str(prestamo.tipo_divisa)
                        prestamo.monto-=monto
                        prestamo.save()
                        if tarjetaD:
                            tarjetaD = Tarjeta.objects.get(nombre=cuenta_destino)
                            tarjetaD.saldo_inicial=int(tarjetaD.saldo_inicial)
                            tarjetaD.tipo_divisa=str(tarjetaD.tipo_divisa)
                            if prestamo.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*3358
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*2851
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*26
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="COP":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="DOL":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="EUR":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="YEN":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if prestamo.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()

                        if prestamoD:
                            prestamoD = Prestamo.objects.get(nombre=cuenta_destino)
                            prestamoD.monto=int(prestamoD.monto)
                            prestamoD.tipo_divisa=str(prestamoD.tipo_divisa)
                            if prestamo.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="COP":
                                monto=monto*3358
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="COP":
                                monto=monto*2851
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="COP":
                                monto=monto*26
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="COP" and prestamoD.tipo_divisa=="COP":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="DOL":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="COP" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="EUR":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="COP" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="YEN":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if prestamo.tipo_divisa=="COP" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                prestamoD.monto+=monto
                                prestamoD.save()

                        if inversionD:
                            inversionD = Inversion.objects.get(nombre=cuenta_destino)
                            inversionD.monto=int(inversionD.monto)
                            inversionD.tipo_divisa=str(inversionD.tipo_divisa)
                            if prestamo.tipo_divisa=="EUR" and inversionD.tipo_divisa=="COP":
                                monto=monto*3358
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="DOL" and inversionD.tipo_divisa=="COP":
                                monto=monto*2851
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="YEN" and inversionD.tipo_divisa=="COP":
                                monto=monto*26
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="COP" and inversionD.tipo_divisa=="COP":
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and inversionD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="DOL" and inversionD.tipo_divisa=="DOL":
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="YEN" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="COP" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and inversionD.tipo_divisa=="EUR":
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="DOL" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="YEN" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="COP" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and inversionD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="DOL" and inversionD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="YEN" and inversionD.tipo_divisa=="YEN":
                                inversionD.monto+=monto
                                inversionD.save()
                            if prestamo.tipo_divisa=="COP" and inversionD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                inversionD.monto+=monto
                                inversionD.save()

                        if chequeraD:
                            chequeraD = Chequera.objects.get(nombre=cuenta_destino)
                            chequeraD.monto=int(chequeraD.monto)
                            chequeraD.tipo_divisa=str(chequeraD.tipo_divisa)
                            if prestamo.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="COP":
                                monto=monto*3358
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="COP":
                                monto=monto*2851
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="COP":
                                monto=monto*26
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="COP" and chequeraD.tipo_divisa=="COP":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="DOL":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="COP" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="EUR":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="COP" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if prestamo.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="YEN":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if prestamo.tipo_divisa=="COP" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                chequeraD.monto+=monto
                                chequeraD.save()

                    if inversion:
                        inversion = Inversion.objects.get(nombre=cuenta_fuente)
                        monto=int(monto)
                        inversion.monto=int(inversion.monto)
                        inversion.tipo_divisa=str(inversion.tipo_divisa)
                        inversion.monto-=monto
                        inversion.save()
                        if tarjetaD:
                            tarjetaD = Tarjeta.objects.get(nombre=cuenta_destino)
                            tarjetaD.saldo_inicial=int(tarjetaD.saldo_inicial)
                            tarjetaD.tipo_divisa=str(tarjetaD.tipo_divisa)
                            if inversion.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*3358
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*2851
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*26
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="COP":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="DOL":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="EUR":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="YEN":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if inversion.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()

                        if prestamoD:
                            prestamoD = Prestamo.objects.get(nombre=cuenta_destino)
                            prestamoD.monto=int(prestamoD.monto)
                            prestamoD.tipo_divisa=str(prestamoD.tipo_divisa)
                            if inversion.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="COP":
                                monto=monto*3358
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="COP":
                                monto=monto*2851
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="COP":
                                monto=monto*26
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="COP" and prestamoD.tipo_divisa=="COP":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="DOL":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="COP" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="EUR":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="COP" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="YEN":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if inversion.tipo_divisa=="COP" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                prestamoD.monto+=monto
                                prestamoD.save()

                        if inversionD:
                            inversionD = Inversion.objects.get(nombre=cuenta_destino)
                            inversionD.monto=int(inversionD.monto)
                            inversionD.tipo_divisa=str(inversionD.tipo_divisa)
                            if inversion.tipo_divisa=="EUR" and inversionD.tipo_divisa=="COP":
                                monto=monto*3358
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="DOL" and inversionD.tipo_divisa=="COP":
                                monto=monto*2851
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="YEN" and inversionD.tipo_divisa=="COP":
                                monto=monto*26
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="COP" and inversionD.tipo_divisa=="COP":
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and inversionD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="DOL" and inversionD.tipo_divisa=="DOL":
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="YEN" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="COP" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and inversionD.tipo_divisa=="EUR":
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="DOL" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="YEN" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="COP" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and inversionD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="DOL" and inversionD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="YEN" and inversionD.tipo_divisa=="YEN":
                                inversionD.monto+=monto
                                inversionD.save()
                            if inversion.tipo_divisa=="COP" and inversionD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                inversionD.monto+=monto
                                inversionD.save()

                        if chequeraD:
                            chequeraD = Chequera.objects.get(nombre=cuenta_destino)
                            chequeraD.monto=int(chequeraD.monto)
                            chequeraD.tipo_divisa=str(chequeraD.tipo_divisa)
                            if inversion.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="COP":
                                monto=monto*3358
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="COP":
                                monto=monto*2851
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="COP":
                                monto=monto*26
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="COP" and chequeraD.tipo_divisa=="COP":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="DOL":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="COP" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="EUR":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="COP" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if inversion.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="YEN":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if inversion.tipo_divisa=="COP" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                chequeraD.monto+=monto
                                chequeraD.save()

                    if chequera:
                        chequera = Chequera.objects.get(nombre=cuenta_fuente)
                        monto=int(monto)
                        chequera.monto=int(chequera.monto)
                        chequera.tipo_divisa=str(chequera.tipo_divisa)
                        chequera.monto-=monto
                        chequera.save()
                        if tarjetaD:
                            tarjetaD = Tarjeta.objects.get(nombre=cuenta_destino)
                            tarjetaD.saldo_inicial=int(tarjetaD.saldo_inicial)
                            tarjetaD.tipo_divisa=str(tarjetaD.tipo_divisa)
                            if chequera.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*3358
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*2851
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="COP":
                                monto=monto*26
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="COP":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="DOL":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="EUR":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="DOL" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="YEN" and tarjetaD.tipo_divisa=="YEN":
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()
                            if chequera.tipo_divisa=="COP" and tarjetaD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                tarjetaD.saldo_inicial+=monto
                                tarjetaD.save()

                        if prestamoD:
                            prestamoD = Prestamo.objects.get(nombre=cuenta_destino)
                            prestamoD.monto=int(prestamoD.monto)
                            prestamoD.tipo_divisa=str(prestamoD.tipo_divisa)
                            if chequera.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="COP":
                                monto=monto*3358
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="COP":
                                monto=monto*2851
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="COP":
                                monto=monto*26
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="COP" and prestamoD.tipo_divisa=="COP":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="DOL":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="COP" and prestamoD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="EUR":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="COP" and prestamoD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                prestamoD.monto+=monto
                                prestamoD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="DOL" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="YEN" and prestamoD.tipo_divisa=="YEN":
                                prestamoD.monto+=monto
                                prestamoD.save()
                            if chequera.tipo_divisa=="COP" and prestamoD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                prestamoD.monto+=monto
                                prestamoD.save()

                        if inversionD:
                            inversionD = Inversion.objects.get(nombre=cuenta_destino)
                            inversionD.monto=int(inversionD.monto)
                            inversionD.tipo_divisa=str(inversionD.tipo_divisa)
                            if chequera.tipo_divisa=="EUR" and inversionD.tipo_divisa=="COP":
                                monto=monto*3358
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="DOL" and inversionD.tipo_divisa=="COP":
                                monto=monto*2851
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="YEN" and inversionD.tipo_divisa=="COP":
                                monto=monto*26
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="COP" and inversionD.tipo_divisa=="COP":
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and inversionD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="DOL" and inversionD.tipo_divisa=="DOL":
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="YEN" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="COP" and inversionD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and inversionD.tipo_divisa=="EUR":
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="DOL" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="YEN" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="COP" and inversionD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                inversionD.monto+=monto
                                inversionD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and inversionD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="DOL" and inversionD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="YEN" and inversionD.tipo_divisa=="YEN":
                                inversionD.monto+=monto
                                inversionD.save()
                            if chequera.tipo_divisa=="COP" and inversionD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                inversionD.monto+=monto
                                inversionD.save()

                        if chequeraD:
                            chequeraD = Chequera.objects.get(nombre=cuenta_destino)
                            chequeraD.monto=int(chequeraD.monto)
                            chequeraD.tipo_divisa=str(chequeraD.tipo_divisa)
                            if chequera.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="COP":
                                monto=monto*3358
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="COP":
                                monto=monto*2851
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="COP":
                                monto=monto*26
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="COP" and chequeraD.tipo_divisa=="COP":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*1.17
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="DOL":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.0090
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="COP" and chequeraD.tipo_divisa=="DOL":
                                monto=monto*0.00035
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="EUR":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.854
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.007
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="COP" and chequeraD.tipo_divisa=="EUR":
                                monto=monto*0.00030
                                chequeraD.monto+=monto
                                chequeraD.save()
                            #----------------------------------------------------#
                            if chequera.tipo_divisa=="EUR" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*128.68
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="DOL" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*110.01
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="YEN" and chequeraD.tipo_divisa=="YEN":
                                chequeraD.monto+=monto
                                chequeraD.save()
                            if chequera.tipo_divisa=="COP" and chequeraD.tipo_divisa=="YEN":
                                monto=monto*0.038
                                chequeraD.monto+=monto
                                chequeraD.save()




            if not error2:
                monto = request.POST.get('c_mon')
                tipo_divisa = request.POST.get('divisa')
                transferencia = Transferencia.objects.create(
                        nombre = nombre,
                        monto = monto,
                        cuenta_fuente = cuenta_fuente,
                        cuenta_destino= cuenta_destino,
                        notas_adicionales = notas_adicionales,
                        user_id= user[0].id,
                )
                transferencia.save()
                transferencias = Transferencia.objects.filter(user_id=user[0].id)

        if 'delete_ingreso' in request.POST:
            id_ingreso = request.POST.get('id_ingreso')
            ingreso = Ingreso.objects.get(id=id_ingreso)
            if ingreso is not None:
                ingreso.delete()

        if 'delete_gasto' in request.POST:
            id_gasto = request.POST.get('id_gasto')
            gasto = Gasto.objects.get(id=id_gasto)
            if gasto is not None:
                gasto.delete()

        if 'delete_transferencia' in request.POST:
            id_transferencia = request.POST.get('id_transferencia')
            transferencia = Transferencia.objects.get(id=id_transferencia)
            if transferencia is not None:
                transferencia.delete()



        template = loader.get_template('gestion/gestionTransacciones.html')

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

            cuenta=str(cuenta)
            sin_cuentas= "Sin cuentas"

            error=False
            for presupuesto in presupuestos:
                if str(presupuesto.nombre) == str(nombre):
                    error=True
                    mensaje_cuenta = (True,"Ya existe un presupuesto con este nombre")

            if cuenta==sin_cuentas:
                error=True
                mensaje_cuenta = (True,"No hay cuentas existentes para realizar la acción")

            tarjeta = Tarjeta.objects.filter(nombre=cuenta).exists()
            prestamo = Prestamo.objects.filter(nombre=cuenta).exists()
            inversion = Inversion.objects.filter(nombre=cuenta).exists()
            cheque = Chequera.objects.filter(nombre=cuenta).exists()

            if tarjeta:
                tarjeta = Tarjeta.objects.get(nombre=cuenta)
                tipo_divisa=str(tarjeta.tipo_divisa)
                tarjeta.saldo_inicial=int(tarjeta.saldo_inicial)
                monto=int(monto)
                tarjeta.saldo_inicial-=monto
                if tarjeta.saldo_inicial<0:
                    error=True
                    mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                else:
                    tarjeta.save()

            if prestamo:
                prestamo = Prestamo.objects.get(nombre=cuenta)
                tipo_divisa=str(prestamo.tipo_divisa)
                prestamo.monto=int(prestamo.monto)
                monto=int(monto)
                prestamo.monto-=monto
                if prestamo.monto<0:
                    error=True
                    mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                else:
                    prestamo.save()

            if inversion:
                inversion = Inversion.objects.get(nombre=cuenta)
                tipo_divisa=str(inversion.tipo_divisa)
                inversion.monto=int(inversion.monto)
                monto=int(monto)
                inversion.monto-=monto
                if inversion.monto<0:
                    error=True
                    mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                else:
                    inversion.save()

            if cheque:
                cheque = Chequera.objects.get(nombre=cuenta)
                tipo_divisa=str(cheque.tipo_divisa)
                cheque.monto=int(cheque.monto)
                monto=int(monto)
                cheque.monto-=monto
                if cheque.monto<0:
                    error=True
                    mensaje_cuenta = (True,"No puede realizar la acción, fondos insuficientes")
                else:
                    cheque.save()


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

        if 'delete_presupuesto' in request.POST:
            id_presupuesto = request.POST.get('id_presupuesto')
            presupuesto = Presupuesto.objects.get(id=id_presupuesto)
            if presupuesto is not None:
                presupuesto.delete()

        template = loader.get_template('gestion/gestionPresupuesto.html')

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
                'transferencias':transferencias,

                'presupuestos':presupuestos,

                'mensaje_cuenta': mensaje_cuenta,
        }
        return HttpResponse(template.render(ctx,request))


def paginacion(tarjetas,page):
    paginator = Paginator(tarjetas, 4)
    tarjetas = paginator.page(page)
    return tarjetas , paginator
