
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , authenticate

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect

from .models import Usuario





def RegistroUsuario(request):
    if request.method == 'GET':
        template = loader.get_template('usuario/index.html')
        ctx = {}
        return HttpResponse(template.render(ctx,request))


    if request.method == 'POST':
        if 'bc1' in request.POST:
            error=(False,"")
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1= request.POST.get('password1')
            password2= request.POST.get('password2')
            cc = request.POST.get('cc')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')

            if password1 == password2:
                user = User.objects.create_user(
        				username=username,
        				first_name=first_name,
        				last_name=last_name,
        				email=email,
                        password=password1
        				)
                user.save()

                usuario = Usuario.objects.create(
                        user = user,
                        cc = cc,
                        fecha_nacimiento = fecha_nacimiento
                )

                usuario.save()

                error=(True, "Registro exitoso")

            else:
                error=(True, "Las contraseñas deben ser iguales")


        if 'bc2' in request.POST:
            error=(False,"")
            username = request.POST['username']
            password = request.POST['password']
            usuario = User.objects.filter(username=username)

            if len(usuario) != 0:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request,user)
                    error = (True, "Bien")
                else:
                    error = (True, "Contraseña invalida")

            else:
                error = (True, "No existe el usuario " + username)



    template = loader.get_template('usuario/index.html')
    ctx = {'error':error}
    return HttpResponse(template.render(ctx,request))
