# Generated by Django 2.0.3 on 2018-05-21 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0008_auto_20180521_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarjeta',
            old_name='numero',
            new_name='numero_tarjeta',
        ),
    ]
