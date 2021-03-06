# Generated by Django 2.0.3 on 2018-05-22 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestion', '0020_transferencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('monto', models.BigIntegerField()),
                ('tipo_divisa', models.CharField(max_length=5)),
                ('cuenta', models.CharField(max_length=50)),
                ('saldo_reinversion', models.BigIntegerField()),
                ('periodo_recurrencia', models.IntegerField()),
                ('categoria', models.CharField(max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
