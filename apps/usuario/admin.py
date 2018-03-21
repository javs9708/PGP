from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class Usuario(admin.ModelAdmin):
    list_display = ['user','cc','fecha_nacimiento']
