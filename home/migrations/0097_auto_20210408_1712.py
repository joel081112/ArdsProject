# Generated by Django 3.1.5 on 2021-04-08 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0096_auto_20210408_1711'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='batting',
            unique_together={('member', 'match'), ('batter_number', 'match')},
        ),
    ]