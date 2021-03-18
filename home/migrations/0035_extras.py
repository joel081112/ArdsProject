# Generated by Django 3.1.5 on 2021-03-04 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_team_abr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wides', models.IntegerField(blank=True, null=True)),
                ('no_balls', models.IntegerField(blank=True, null=True)),
                ('byes', models.IntegerField(blank=True, null=True)),
                ('leg_byes', models.IntegerField(blank=True, null=True)),
                ('match', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.match')),
            ],
        ),
    ]
