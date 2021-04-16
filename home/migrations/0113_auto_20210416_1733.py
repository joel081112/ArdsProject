# Generated by Django 3.1.5 on 2021-04-16 16:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0112_auto_20210416_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='ards_overs_batted',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='match',
            name='ards_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='ards_wickets',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='match',
            name='opponent_overs_batted',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='match',
            name='opponent_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='opponent_wickets',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
