
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , authenticate, logout

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect

from .models import Usuario
from django.contrib.auth.decorators import login_required
from .funciones.validadores import *


def RegistroUsuario(request):
    error2=(False,"")
    error3=(False,"")
    error=(False,"")
    if request.method == 'GET':
        template = loader.get_template('usuario/index.html')
        ctx = {}
        return HttpResponse(template.render(ctx,request))


    if request.method == 'POST':
        if 'bc1' in request.POST:

            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1= request.POST.get('password1')
            password2= request.POST.get('password2')
            cc = request.POST.get('cc')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')

            flag = False

            erroresCampos = []
            errores = (False , erroresCampos )

            if validar_nombre(first_name):
                flag = True
                error = "Nombre"
                erroresCampos.append(error)
                errores = (True , erroresCampos)

            if validar_apellido(last_name):
                flag = True
                error = "Apellido"
                erroresCampos.append(error)
                errores = (True , erroresCampos)

            if validar_cc(cc):
                flag = True
                error = "Documento de identidad"
                erroresCampos.append(error)
                errores = (True , erroresCampos)

            if validar_fecha(fecha_nacimiento):
                flag = True
                error = "Fecha Nacimiento"
                erroresCampos.append(error)
                errores = (True , erroresCampos)

            if validar_email(email):
                flag = True
                error = "Correo Electronico"
                erroresCampos.append(error)
                errores = (True , erroresCampos)


            if flag == False:
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
                            fecha_nacimiento = fecha_nacimiento,
                            foto_perfil = None
                    )

                    usuario.save()

                    error2=(True, "Registro exitoso")

                else:
                    error3=(True, "Las contraseñas deben ser iguales")
            else:
                error = (False , "")


        if 'bc2' in request.POST:

            username = request.POST['username']
            password = request.POST['password']
            usuario = User.objects.filter(username=username)

            if len(usuario) != 0:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request,user)
                    return redirect('/gestion/menu?username='+username)

                else:
                    error = (True, "Contraseña invalida")

            else:
                error = (True, "No existe el usuario " + username)



    template = loader.get_template('usuario/index.html')
    ctx = {'error':error,
            'error2':error2,
            'error3':error3,
            'errores':errores,
            }
    return HttpResponse(template.render(ctx,request))

def inicio(request):
    return render(request, 'usuario/inicio.html')

@login_required(login_url='/ingresar/')
def cerrarSesion(request):
	if request.user is not None:
		logout(request)

	return redirect('inicio')

@login_required(login_url='/ingresar/')
def visualizarPerfil(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]
        template = loader.get_template('usuario/Perfil.html')
        print(usuario.foto_perfil)
        ctx = {'usuario':usuario,
                }
        return HttpResponse(template.render(ctx,request))


@login_required(login_url='/ingresar/')
def editarPerfil(request):

    if request.method == 'GET': 
        username = request.GET.get('username')
        template = loader.get_template('usuario/EPerfil.html')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]
        fecha = usuario.fecha_nacimiento
        fecha = str(fecha)
        ctx = {'usuario':usuario,
                'fecha' : fecha,
                    }
        return HttpResponse(template.render(ctx,request))

    if request.method == 'POST':
        template = loader.get_template('usuario/Perfil.html')
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        usuario = Usuario.objects.filter(user_id=user[0].id)
        usuario = usuario[0]

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cc = request.POST.get('cc')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        if len(username) != 0:
            usuario.user.username = username
            usuario.user.save()

        if len(first_name) != 0:
            usuario.user.first_name = first_name
            usuario.user.save()

        if len(last_name) != 0:
            usuario.user.last_name = last_name
            usuario.user.save() 

        if len(email) != 0:
            usuario.user.email = email
            usuario.user.save()

        if len(cc) != 0:
            usuario.cc = cc
            usuario.save()

        if len(fecha_nacimiento) != 0:
            usuario.fecha_nacimiento = fecha_nacimiento
            usuario.save()

        if len(request.FILES) != 0:
            foto_perfil = request.FILES['foto_perfil']
        else:
            foto_perfil = None

        if foto_perfil is not None:
            usuario.foto_perfil.delete()
            usuario.foto_perfil = foto_perfil
            usuario.save()

        return redirect('/usuario/perfil?username='+usuario.user.username)





