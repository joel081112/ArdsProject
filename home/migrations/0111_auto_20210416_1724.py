# Generated by Django 3.1.5 on 2021-04-16 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0110_auto_20210416_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='match',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]