from django.db import models

class Theatre(models.Model):

    name=models.CharField(max_length=200)
    location=models.CharField(max_length=200)


class Movie(models.Model):

    title=models.CharField(max_length=200)
    image=models.URLField()
    theatre=models.ForeignKey(Theatre,on_delete=models.CASCADE)
    timing=models.CharField(max_length=100)


class Seat(models.Model):

    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    seat_number=models.CharField(max_length=5)
    booked=models.BooleanField(default=False)
# Create your models here.
