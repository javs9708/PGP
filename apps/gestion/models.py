from django.db import models
from django.contrib.auth.models import User

class Tarjeta(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.IntegerField()
    csc = models.IntegerField()
    fecha_vencimiento_mm = models.IntegerField()
    fecha_vencimiento_aa = models.IntegerField()
    tipo_divisa = models.CharField(max_length=5, null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
