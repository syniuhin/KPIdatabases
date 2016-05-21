# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-21 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab02', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photographer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lab02.Photographer'),
        ),
        migrations.AlterField(
            model_name='photographer',
            name='cameras',
            field=models.ManyToManyField(null=True, to='lab02.Camera'),
        ),
        migrations.AlterField(
            model_name='photographer',
            name='locations',
            field=models.ManyToManyField(null=True, to='lab02.Location'),
        ),
    ]