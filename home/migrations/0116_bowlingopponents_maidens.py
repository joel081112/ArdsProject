# Generated by Django 3.1.5 on 2021-04-26 09:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0115_auto_20210426_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='bowlingopponents',
            name='maidens',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]