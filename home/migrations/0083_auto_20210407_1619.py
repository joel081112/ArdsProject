# Generated by Django 3.1.5 on 2021-04-07 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0082_auto_20210407_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
