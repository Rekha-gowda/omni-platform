from django.db import models

class Bus(models.Model):

    name=models.CharField(max_length=200)
    from_city=models.CharField(max_length=200)
    to_city=models.CharField(max_length=200)
    time=models.CharField(max_length=100)
# Create your models here.
