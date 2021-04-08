# Generated by Django 3.1.5 on 2021-04-08 09:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0091_auto_20210408_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battingopponents',
            name='batter_name',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='home.oppositionnames'),
        ),
        migrations.AlterField(
            model_name='bowlingopponents',
            name='bowler_number',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(11), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='club',
            name='home_venue',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cointoss',
            name='decision',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='extras',
            name='ards',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('player_link',)},
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together={('user',)},
        ),
        migrations.RemoveField(
            model_name='member',
            name='ards',
        ),
    ]
