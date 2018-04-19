from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..usuario.models import Usuario
from django.contrib.auth.models import User
from django.template import loader

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
