# Generated by Django 3.1.5 on 2021-04-12 13:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0100_auto_20210412_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bowling',
            name='overs',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0.05)]),
        ),
    ]
