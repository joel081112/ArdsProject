# Generated by Django 3.1.5 on 2021-04-16 13:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0104_auto_20210416_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bowling',
            name='runs',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
