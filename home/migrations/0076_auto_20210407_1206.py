# Generated by Django 3.1.5 on 2021-04-07 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0075_customeruser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customeruser',
            old_name='department',
            new_name='weblink',
        ),
    ]