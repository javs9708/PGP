# Generated by Django 2.0.3 on 2018-05-24 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0023_auto_20180523_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chequera',
            name='numero_cheques',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='chequera',
            name='numero_cuenta',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='inversion',
            name='numero_cuenta',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='saldo_reinversion',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='numero_cuenta',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='numero_tarjeta',
            field=models.BigIntegerField(null=True),
        ),
    ]