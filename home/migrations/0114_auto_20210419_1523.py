# Generated by Django 3.1.5 on 2021-04-19 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0113_auto_20210416_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oppositionnames',
            name='name',
            field=models.CharField(default='', max_length=40),
        ),
    ]
