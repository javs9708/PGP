# Generated by Django 2.0.3 on 2018-05-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0013_inversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjeta',
            name='saldo_inicial',
            field=models.BigIntegerField(null=True),
        ),
    ]
