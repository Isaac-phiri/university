# Generated by Django 5.1.7 on 2025-03-25 08:32

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentapplication',
            name='country',
            field=django_countries.fields.CountryField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
