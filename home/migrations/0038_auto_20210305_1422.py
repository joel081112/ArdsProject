# Generated by Django 3.1.5 on 2021-03-05 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_auto_20210305_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='badge',
            field=models.ImageField(blank=True, default='original_images/default_logo.png', null=True, upload_to=''),
        ),
    ]
