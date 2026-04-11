from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    image = models.URLField()

    def __str__(self):
        return self.name
