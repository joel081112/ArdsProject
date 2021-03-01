# Generated by Django 3.1.5 on 2021-02-27 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('home', '0030_batting_out_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Overview',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('banner_title', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Overview Page',
                'verbose_name_plural': 'Overview Pages',
            },
            bases=('wagtailcore.page',),
        ),
    ]
