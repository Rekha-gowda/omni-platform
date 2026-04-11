from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bus(models.Model):
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    image = models.ImageField(upload_to='buses/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Rating: {self.rating})"

class Trip(models.Model):
    bus = models.ForeignKey(Bus, related_name='trips', on_delete=models.CASCADE, null=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField(default=timezone.now)
    timing_shift = models.CharField(max_length=100, help_text="e.g. 6:00 AM, Morning, Night")
    arrival_time = models.DateTimeField(null=True, blank=True)
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
    total_seats = models.IntegerField(default=40)

    def __str__(self):
        return f"{self.bus.name if self.bus else 'No Bus'}: {self.source} to {self.destination} ({self.departure_date} - {self.timing_shift})"

class BusBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True)
    no_of_seats = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    booking_time = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='COD')

    def __str__(self):
        return f"Booking {self.id} for {self.user.username} on {self.trip}"

class BusSeat(models.Model):
    trip = models.ForeignKey(Trip, related_name='seats', on_delete=models.CASCADE, null=True)
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
        return f"{self.trip.bus.name} - {self.trip.source} to {self.trip.destination} - {self.seat_identifier}"
