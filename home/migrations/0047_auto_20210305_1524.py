# Generated by Django 3.1.5 on 2021-03-05 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_auto_20210305_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bowling',
            name='byes',
        ),
        migrations.RemoveField(
            model_name='bowling',
            name='leg_byes',
        ),
    ]
