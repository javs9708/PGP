from django.db import models
from django.contrib.auth.models import User

TYPE = (
    ('ceremonia','Ceremonia'),
    ('fiesta', 'Fiesta')
)

#------------Cuentas--------------------#

class Tarjeta(models.Model):
    nombre = models.CharField(max_length=50)
    numero_tarjeta = models.BigIntegerField(null=True)
    saldo_inicial = models.BigIntegerField(null=True)
    entidad = models.CharField(max_length=50, null=True)
    numero_cuenta = models.BigIntegerField(null=True)
    fecha_vencimiento_mm = models.IntegerField()
    fecha_vencimiento_aa = models.IntegerField()
    tipo_divisa = models.CharField(max_length=5, null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    tipo = models.CharField(default="tarjeta" , max_length=50)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50, null=True)
    monto = models.BigIntegerField(null=True)
    interes = models.BigIntegerField(null=True)
    fecha_prestamo = models.DateField()
    fecha_limite = models.DateField()
    tipo_divisa = models.CharField(max_length=5, null=True)
    tipo_pago = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    tipo = models.CharField(default="prestamos" , max_length=50)

class Inversion(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50)
    numero_cuenta = models.BigIntegerField(null=True)
    monto = models.BigIntegerField(null=True)
    interes = models.BigIntegerField(null=True)
    fecha_prestamo = models.DateField()
    fecha_limite = models.DateField()
    tipo_divisa = models.CharField(max_length=5, null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    tipo = models.CharField(default="inversion" , max_length=50)

class Chequera(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50)
    tipo_divisa = models.CharField(max_length=5)
    numero_cuenta = models.BigIntegerField(null=True)
    monto = models.BigIntegerField(null=True)
    numero_cheques = models.BigIntegerField(null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    tipo = models.CharField(default="chequera" , max_length=50)

#------------Transacciones--------------------#
class Ingreso(models.Model):
    nombre = models.CharField(max_length=50)
    monto = models.BigIntegerField(null=True)
    tipo_divisa = models.CharField(max_length=5)
    cuenta_ingresar = models.CharField(max_length=50)
    fecha_ingreso = models.DateField()
    notas_adicionales = models.TextField()

    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

class Gasto(models.Model):
    nombre = models.CharField(max_length=50)
    monto = models.BigIntegerField(null=True)
    tipo_divisa = models.CharField(max_length=5)
    cuenta_retirar = models.CharField(max_length=50)
    fecha_gasto = models.DateField()
    notas_adicionales = models.TextField()

    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

class Transferencia(models.Model):
    nombre = models.CharField(max_length=50)
    monto = models.BigIntegerField(null=True)
    cuenta_fuente = models.CharField(max_length=50)
    cuenta_destino = models.CharField(max_length=50)
    notas_adicionales = models.TextField()

    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

#------------Presupuestos--------------------#

class Presupuesto(models.Model):
    nombre = models.CharField(max_length=50)
    monto = models.BigIntegerField(null=True)
    tipo_divisa = models.CharField(max_length=5)
    cuenta = models.CharField(max_length=50)
    saldo_reinversion = models.BigIntegerField(null=True)
    periodo_recurrencia = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)

    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
