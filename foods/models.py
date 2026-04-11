from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} at {self.restaurant.name}"

class FoodOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_name = models.CharField(max_length=200, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    delivery_phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')
    payment_method = models.CharField(max_length=50, default='COD')

    def __str__(self):
        return f"Order {self.id} from {self.restaurant.name} by {self.user.username}"

class FoodCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_total(self):
        return sum(item.menu_item.price * item.quantity for item in self.items.all())

class FoodCartItem(models.Model):
    cart = models.ForeignKey(FoodCart, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class FoodComplaint(models.Model):
    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='complaints')
    reason_text = models.TextField()
    image = models.ImageField(upload_to='food_complaints/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending verification')

class FoodReview(models.Model):
    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    review_text = models.TextField()
    image = models.ImageField(upload_to='food_reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
