# Generated by Django 3.1.5 on 2021-03-05 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0059_remove_batting_out_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='batting',
            name='out_by',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='home.oppositionnames'),
        ),
    ]
