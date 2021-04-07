# Generated by Django 3.1.5 on 2021-04-07 16:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0087_auto_20210407_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battingopponents',
            name='batter_number',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(11), django.core.validators.MinValueValidator(1)]),
        ),
    ]
