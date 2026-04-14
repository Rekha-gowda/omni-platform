from django.contrib import admin
from .models import Bus, BusBooking, Trip

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('bus', 'source', 'destination', 'departure_date', 'timing_shift', 'price_per_seat')
    list_filter = ('bus', 'source', 'destination', 'departure_date')

@admin.register(BusBooking)
class BusBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'no_of_seats', 'total_cost', 'booking_time', 'customer_name', 'customer_phone', 'payment_method')
    list_filter = ('trip__bus__name', 'booking_time', 'payment_method')
    search_fields = ('user__username', 'customer_name', 'customer_phone', 'trip__bus__name')
