# Generated by Django 3.1.5 on 2021-04-07 15:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0084_auto_20210407_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]