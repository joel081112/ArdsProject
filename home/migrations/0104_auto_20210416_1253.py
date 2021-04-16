# Generated by Django 3.1.5 on 2021-04-16 11:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0103_auto_20210415_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bowling',
            name='overs',
            field=models.DecimalField(decimal_places=1, default=0.1, max_digits=4, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0.05)]),
        ),
    ]
