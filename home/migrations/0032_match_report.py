# Generated by Django 3.1.5 on 2021-03-01 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_overview'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='report',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
    ]