from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Usuario(models.Model):

    class Meta:
        verbose_name = u"Usuario"
        verbose_name_plural = u"Usuarios"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cc = models.CharField(max_length=15, null=False, blank=False)
    fecha_nacimiento = models.DateField()


    def __str__(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)
