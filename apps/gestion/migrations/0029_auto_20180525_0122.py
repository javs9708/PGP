# Generated by Django 2.0.3 on 2018-05-25 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0028_auto_20180525_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inversion',
            name='interes',
            field=models.BigIntegerField(null=True),
        ),
    ]
