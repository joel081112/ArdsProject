# Generated by Django 3.1.5 on 2021-03-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_extras_ards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='badge',
            field=models.ImageField(blank=True, default='default_logo.png', null=True, upload_to=''),
        ),
    ]
