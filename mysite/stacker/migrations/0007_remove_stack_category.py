# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 22:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacker', '0006_auto_20171216_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stack',
            name='category',
        ),
    ]