# Generated by Django 3.1.5 on 2021-03-05 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20210305_1438'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='batting',
            unique_together={('member', 'match')},
        ),
        migrations.AlterUniqueTogether(
            name='bowling',
            unique_together={('member', 'match')},
        ),
    ]