# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stacker', '0008_auto_20171216_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='stack',
            name='category',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
