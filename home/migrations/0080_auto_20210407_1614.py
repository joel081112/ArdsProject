# Generated by Django 3.1.5 on 2021-04-07 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0079_auto_20210407_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2021, 4, 7), null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(16, 14, 39, 777274), null=True),
        ),
    ]
