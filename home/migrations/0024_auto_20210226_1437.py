# Generated by Django 3.1.5 on 2021-02-26 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20210226_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='ards_runs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='opponent_runs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='overs_played',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=4),
        ),
    ]
