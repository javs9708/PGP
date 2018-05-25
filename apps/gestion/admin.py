from django.contrib import admin

from .models import *

@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):
	list_display = ('nombre','numero_tarjeta')
