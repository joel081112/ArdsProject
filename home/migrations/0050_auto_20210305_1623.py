# Generated by Django 3.1.5 on 2021-03-05 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_auto_20210305_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='report',
            field=models.TextField(blank=True, default='', max_length=600, null=True),
        ),
    ]
