# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-22 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworkapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]