from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    release_date = models.DateField()
    duration_minutes = models.IntegerField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Theater(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    location_url = models.URLField(blank=True, null=True, help_text="Google Maps link or similar")
    
    def __str__(self):
        return self.name

class Show(models.Model):
    movie = models.ForeignKey(Movie, related_name='shows', on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, related_name='shows', on_delete=models.CASCADE, null=True, blank=True)
    theater_name = models.CharField(max_length=200, help_text="Legacy field, use 'theater' for new entries")
    show_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        t_name = self.theater.name if self.theater else self.theater_name
        return f"{self.movie.title} at {t_name} ({self.show_time})"

class MovieTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    booking_time = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='COD')

    def __str__(self):
        return f"Ticket {self.id} for {self.show.movie.title} by {self.user.username}"

class MovieSeat(models.Model):
    show = models.ForeignKey(Show, related_name='seats', on_delete=models.CASCADE)
    seat_identifier = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    locked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    lock_expires_at = models.DateTimeField(null=True, blank=True)

    def is_locked(self):
        if self.is_booked:
            return True
        if self.lock_expires_at and self.lock_expires_at > timezone.now():
            return True
        return False

    def __str__(self):
        return f"{self.show.movie.title} - {self.seat_identifier}"

class MovieCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_total(self):
        return sum(item.seat.show.price for item in self.items.all())

class MovieCartItem(models.Model):
    cart = models.ForeignKey(MovieCart, related_name='items', on_delete=models.CASCADE)
    seat = models.ForeignKey(MovieSeat, on_delete=models.CASCADE)
