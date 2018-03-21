
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.template import loader
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import Usuario


def RegistroUsuario(request):
    if request.method == 'GET':
        template = loader.get_template('usuario/index.html')
        ctx = {}
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1= request.POST.get('password1')
        password2= request.POST.get('password2')
        cc = request.POST.get('cc')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        user = User(
				username=username,
				first_name=first_name,
				last_name=last_name,
				email=email
				)
        user.save()

        usuario = Usuario(
                user = user,
                cc = cc,
                fecha_nacimiento = fecha_nacimiento
        )

        usuario.save()

        template = loader.get_template('usuario/index.html')
        ctx = {}
        return HttpResponse(template.render(ctx,request))
