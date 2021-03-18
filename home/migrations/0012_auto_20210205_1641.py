# Generated by Django 3.1.5 on 2021-02-05 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20210205_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bowling',
            name='match_format',
        ),
        migrations.AddField(
            model_name='bowling',
            name='match_format',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, to='home.matchformat'),
            preserve_default=False,
        ),
    ]