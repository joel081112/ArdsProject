# Generated by Django 3.1.5 on 2021-04-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0066_auto_20210405_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='store_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]