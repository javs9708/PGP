# Generated by Django 2.0.3 on 2018-05-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0022_auto_20180522_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chequera',
            name='monto',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='monto',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='monto',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='inversion',
            name='monto',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='monto',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='monto',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='saldo_inicial',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transferencia',
            name='monto',
            field=models.FloatField(null=True),
        ),
    ]
