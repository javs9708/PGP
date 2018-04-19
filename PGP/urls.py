"""PGP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from apps.usuario.views import *

from apps.usuario.views import RegistroUsuario, inicio, cerrarSesion
from apps.gestion.views import gestionMenu
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^usuario/', include ('apps.usuario.urls')),
	url(r'^gestion/', include ('apps.gestion.urls')),
	url(r'^ingresar/',RegistroUsuario , name='index'),
	url(r'^$',inicio , name='inicio'),

	url(r'^logout/$',cerrarSesion,name="logout"),

	url(r'^reiniciar/reiniciar_contraseña$',password_reset,
       {'template_name':'registration/password_reset_form.html',
       'email_template_name':'registration/password_reset_email.html'},
        name='password_reset'),
    url(r'^reiniciar/contraseña_reiniciada$',password_reset_done,
       {'template_name':'registration/password_reset_done.html'},
       name='password_reset_done'),
    url(r'^reiniciar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
       password_reset_confirm,
       {'template_name':'registration/password_reset_confirm.html'},
       name='password_reset_confirm'),
    url(r'^reiniciar/hecho$',password_reset_complete,
       {'template_name':'registration/password_reset_complete.html'},
       name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
