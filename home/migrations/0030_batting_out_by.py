# Generated by Django 3.1.5 on 2021-02-27 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_bowling_bowler_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='batting',
            name='out_by',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]