# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-08 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170108_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='year',
            field=models.CharField(choices=[('SY_A', 'SY_A'), ('SY_B', 'SY_B'), ('TY_A', 'TY_A'), ('TY_B', 'TY_B')], max_length=52),
        ),
    ]