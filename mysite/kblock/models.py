from django.db import models

# Create your models here.

class Stack(models.Model):
    name = models.CharField(max_length=200)
    balance = models.FloatField(default=0.0)
    goal = models.FloatField(default=0.0)
    owner = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default='none')



