
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , authenticate, logout

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect

from .models import Usuario
from apps.gestion.models import Tarjeta
from django.contrib.auth.decorators import login_required
from .funciones.validadores import *




def RegistroUsuario(request):
    error2=(False,"")
    error3=(False,"")
    error=(False,"")
    erroresCampos = []
    errores = (False , erroresCampos )
    datos = request.POST
    if request.method == 'GET':

        username=None
        username=request.user.username
        usuario = User.objects.filter(username=username).exists()
        if usuario:
            usuario = User.objects.get(username=username)
        if len(username)!=0 and not usuario.is_superuser:
            return redirect('/gestion/menu?username='+username)

        template = loader.get_template('usuario/index.html')
        ctx = {
        }
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

            usuario = User.objects.filter(username=username)
            cedula = Usuario.objects.filter(cc=cc)

            flag = False

            erroresCampos = []
            errores = (False , erroresCampos )
            datos = request.POST

            if validar_nombre(first_name):
                flag = True
                error = "Nombre (Ingrese unicamente caracteres alfabéticos)"
                erroresCampos.append(error)
                errores = (True , erroresCampos)

            if validar_apellido(last_name):
                flag = True
                error = "Apellido (Ingrese unicamente caracteres alfabéticos)"
                erroresCampos.append(error)
                errores = (True , erroresCampos)

            if validar_cc(cc):
                flag = True
                error = "Documento de identidad (Ingrese unicamente caracteres numericos y un rango de 6 a 14 digitos)"
                erroresCampos.append(error)
                errores = (True , erroresCampos)
            """
            if validar_password(password1):
                flag = True
                error = "Contraseña (Debe tener 8 Digitos a lo menos)"
                erroresCampos.append(error)
                errores = (True , erroresCampos)
            """
            if validar_fecha(fecha_nacimiento):
                flag = True
                error = "Fecha de nacimiento (Ingrese un año de nacimiento valido)"
                erroresCampos.append(error)
                errores = (True , erroresCampos)
            """
            if validar_email(email):
                flag = True
                error = "Correo Electronico"
                erroresCampos.append(error)
                errores = (True , erroresCampos)
            """
            if len(usuario)!=0:
                flag= True
                error = "Nombre de usuario (Ya existe un nombre de usuario asociado)"
                erroresCampos.append(error)
                errores = (True , erroresCampos)


            if len(cedula)!=0:
                flag= True
                error = "Documento de identidad (Ya existe un documento asociado)"
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
            usuario = User.objects.filter(username=username).exists()
            if usuario:
                usuario = User.objects.get(username=username)
                if not usuario.is_superuser:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request,user)
                        return redirect('/gestion/menu?username='+username)

                    else:
                        error = (True, "Contraseña invalida")
                else:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request,user)
                        return redirect('/usuario/gestionAdmin?username='+username)

                    else:
                        error = (True, "Contraseña invalida")
                    #error = (True, "El usuario "+username+" es superusuario")

            else:
                error = (True, "No existe el usuario " + username)



    template = loader.get_template('usuario/index.html')
    ctx = {'error':error,
            'error2':error2,
            'error3':error3,
            'errores':errores,
            'datos':datos,
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
def gestionAdmin(request):

    if request.method == 'GET':
        username = request.GET.get('username')
        user =  User.objects.filter(username=username)
        usuario = user[0]

        username=request.user.username
        usuario = User.objects.filter(username=username).exists()
        if usuario:
            usuario = User.objects.get(username=username)
        if len(username)!=0 and usuario.is_superuser:

            tarjeta =  Tarjeta.objects.all()

            template = loader.get_template('usuario/gestionAdmin.html')

            ctx = {
                	'usuario': usuario,
                    'tarjeta': tarjeta,
            }
            return HttpResponse(template.render(ctx,request))

        return redirect('inicio')


@login_required(login_url='/ingresar/')
def editarPerfil(request):
    erroresCampos = []
    errores = (False , erroresCampos )
    datos = request.POST

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

        #usuario = User.objects.filter(username=username)
        cedula = Usuario.objects.filter(cc=cc)
        flag = False

        erroresCampos = []
        errores = (False , erroresCampos )
        datos = request.POST

        if validar_nombre(first_name):
            flag = True
            error = "Nombre (Ingrese unicamente caracteres alfabéticos)"
            erroresCampos.append(error)
            errores = (True , erroresCampos)

        if validar_apellido(last_name):
            flag = True
            error = "Apellido (Ingrese unicamente caracteres alfabéticos)"
            erroresCampos.append(error)
            errores = (True , erroresCampos)

        if validar_cc(cc):
            flag = True
            error = "Documento de identidad (Ingrese unicamente caracteres numericos y 10 digitos)"
            erroresCampos.append(error)
            errores = (True , erroresCampos)

        if validar_fecha(fecha_nacimiento):
            flag = True
            error = "Fecha de nacimiento (Ingrese un año de nacimiento valido)"
            erroresCampos.append(error)
            errores = (True , erroresCampos)
        """
        if validar_email(email):
            flag = True
            error = "Correo Electronico"
            erroresCampos.append(error)
            errores = (True , erroresCampos)



        if len(usuario)!=0 and (usuario[0])!=(username):
            flag= True
            print (usuario[0])
            print(username)
            error = "Nombre de usuario (Ya existe un nombre de usuario asociado)"
            erroresCampos.append(error)
            errores = (True , erroresCampos)
            """

        if flag == False:

            username = request.GET.get('username')
            user = User.objects.filter(username=username)
            usuario = Usuario.objects.filter(user_id=user[0].id)
            usuario = usuario[0]


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

    template = loader.get_template('usuario/EPerfil.html')
    ctx = {'errores':errores,
            'datos':datos,
            'usuario': usuario
            }
    return HttpResponse(template.render(ctx,request))
