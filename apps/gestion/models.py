from django.db import models
from django.contrib.auth.models import User

class Tarjeta(models.Model):
    nombre = models.CharField(max_length=50)
    numero_tarjeta = models.BigIntegerField()
    saldo_inicial = models.BigIntegerField(null=True)
    entidad = models.CharField(max_length=50, null=True)
    numero_cuenta = models.IntegerField()
    fecha_vencimiento_mm = models.IntegerField()
    fecha_vencimiento_aa = models.IntegerField()
    tipo_divisa = models.CharField(max_length=5, null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

class Prestamo(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50, null=True)
    monto = models.BigIntegerField()
    interes = models.IntegerField()
    fecha_prestamo = models.DateField()
    fecha_limite = models.DateField()
    tipo_divisa = models.CharField(max_length=5, null=True)
    tipo_pago = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

class Inversion(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50)
    numero_cuenta = models.IntegerField()
    monto = models.BigIntegerField()
    interes = models.IntegerField()
    fecha_prestamo = models.DateField()
    fecha_limite = models.DateField()
    tipo_divisa = models.CharField(max_length=5, null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

class Chequera(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50)
    tipo_divisa = models.CharField(max_length=5)
    numero_cuenta = models.IntegerField()
    monto = models.BigIntegerField()
