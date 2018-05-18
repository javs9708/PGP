from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from .models import Tarjeta
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
    if request.method == 'GET':
        username = request.GET.get('username')
        template = loader.get_template('gestion/gestionCuentas.html')
        user =  User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]
        tarjetas = Tarjeta.objects.filter(user_id=user[0].id)



        ctx = {
            	'usuario': usuario,
                'tarjetas': tarjetas,
        }
        return HttpResponse(template.render(ctx,request))


    if request.method == 'POST':
        nombre = request.POST.get('c_name')
        numero = request.POST.get('c_num')
        csc = request.POST.get('csc')
        fecha_vencimiento_mm = request.POST.get('mm')
        fecha_vencimiento_aa = request.POST.get('aa')
        tipo_divisa = request.POST.get('divisa')

        username = request.GET.get('username')
        user = User.objects.filter(username=username)


        tarjeta = Tarjeta.objects.create(
                nombre= nombre,
                numero = numero,
                csc = csc,
                fecha_vencimiento_mm = fecha_vencimiento_mm,
                fecha_vencimiento_aa = fecha_vencimiento_aa,
                tipo_divisa = tipo_divisa,
                user_id= user[0].id
        )

        tarjeta.save()

    template = loader.get_template('gestion/gestionCuentas.html')
    ctx = {
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
