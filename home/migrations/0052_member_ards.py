# Generated by Django 3.1.5 on 2021-03-05 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0051_auto_20210305_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='ards',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
