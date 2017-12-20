from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=250)
    age = models.IntegerField()
