from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
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
    username = request.GET.get('username')
    template = loader.get_template('gestion/gestionCuentas.html')
    user = User.objects.filter(username=username)
    usuario = Usuario.objects.filter(user_id=user[0].id)
    usuario = usuario[0]
    ctx = {
        	'usuario': usuario,
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
