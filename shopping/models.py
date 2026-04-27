from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('grocery', 'Grocery'),
    ('clothing_female', 'Clothing - Female'),
    ('clothing_male', 'Clothing - Male'),
    ('clothing_kids', 'Clothing - Kids'),
    ('other', 'Other'),
)

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    color = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Red, Blue, Black")
    available_sizes = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. S, M, L, XL (Comma separated)")

    def __str__(self):
        return self.name

class ShoppingOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    delivery_name = models.CharField(max_length=200, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    delivery_phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')
    delivered_at = models.DateTimeField(null=True, blank=True)
    is_fast_delivery = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, default='COD')
    current_location = models.CharField(max_length=255, blank=True, null=True, help_text="Order tracking status (e.g. 'At Hyderabad Hub')")
    agent_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Delivery agent contact number")
    expected_delivery = models.DateTimeField(null=True, blank=True, help_text="Expected date and time of delivery")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class ShoppingOrderItem(models.Model):
    order = models.ForeignKey(ShoppingOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_total(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)

class ShoppingReturn(models.Model):
    order_item = models.ForeignKey(ShoppingOrderItem, on_delete=models.CASCADE, related_name='returns')
    return_type = models.CharField(max_length=20, choices=[('Return', 'Return'), ('Replace', 'Replace')])
    reason_text = models.TextField()
    image = models.ImageField(upload_to='returns/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ShoppingReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    review_text = models.TextField()
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
