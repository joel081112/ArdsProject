# Generated by Django 3.1.5 on 2021-02-05 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20210205_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batting',
            name='out',
        ),
        migrations.AddField(
            model_name='batting',
            name='out',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.wicket'),
        ),
    ]
