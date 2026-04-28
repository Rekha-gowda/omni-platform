from django.contrib import admin
from .models import Bus, BusBooking, Trip, BusSeat

@admin.register(Bus)

class BusAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('bus', 'source', 'destination', 'departure_date', 'timing_shift', 'price_per_seat')
    list_filter = ('bus', 'source', 'destination', 'departure_date')

@admin.register(BusBooking)
class BusBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'trip', 'no_of_seats', 'total_cost', 'booking_time', 'customer_name', 'customer_phone', 'payment_method')
    list_filter = ('trip__bus__name', 'booking_time', 'payment_method')
    search_fields = ('user__username', 'user__email', 'customer_name', 'customer_phone', 'trip__bus__name')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
@admin.register(BusSeat)
class BusSeatAdmin(admin.ModelAdmin):
    list_display = ('trip', 'seat_identifier', 'is_booked', 'locked_by', 'lock_expires_at')
    list_filter = ('is_booked', 'trip__bus__name')
    search_fields = ('seat_identifier', 'trip__bus__name')
