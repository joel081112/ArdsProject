# Generated by Django 3.1.5 on 2021-03-05 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0056_auto_20210305_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batting',
            name='member',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.member'),
        ),
    ]
