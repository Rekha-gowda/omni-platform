from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):

    CATEGORY = (
        ('men','Men'),
        ('women','Women'),
        ('kids','Kids')
    )

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20,choices=CATEGORY)
    price = models.FloatField()
    image = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
