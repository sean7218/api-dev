# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('cuisine', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=50)),
            ],
        ),
    ]
