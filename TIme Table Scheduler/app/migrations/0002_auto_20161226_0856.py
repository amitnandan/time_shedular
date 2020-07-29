# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-26 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='classroom',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='is_lab',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='units',
        ),
        migrations.AddField(
            model_name='lecture',
            name='lecture_practical',
            field=models.CharField(choices=[('LECTURE_', 'Lecture_'), ('PRACTICAL_', 'Practical_')], default='', max_length=52),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='year',
            field=models.CharField(choices=[('Second_Year_A', 'SY_A'), ('Second_Year_B', 'SY_B'), ('Third_Year_A', 'TY_A'), ('Third_Year_B', 'TY_B')], max_length=52),
        ),
    ]
