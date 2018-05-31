from django.contrib import admin

from .models import *

@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):
	list_display = ('nombre','numero_tarjeta')

@admin.register(Chequera)
class ChequeraAdmin(admin.ModelAdmin):
	list_display = ('nombre','monto')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
	list_display = ('nombre','monto')

@admin.register(Inversion)
class InversionAdmin(admin.ModelAdmin):
	list_display = ('nombre','monto')
