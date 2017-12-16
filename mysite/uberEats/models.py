# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models



















































class UbereatsVendor(models.Model):
    name = models.CharField(max_length=40)
    cuisine = models.CharField(max_length=50)
    price = models.CharField(max_length=30)
    location = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'uberEats_vendor'


class Vendor(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    cuisine = models.CharField(max_length=30, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor'
