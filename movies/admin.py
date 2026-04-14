from django.contrib import admin
from .models import Movie, Show, MovieTicket

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater_name', 'show_time', 'price')
    list_filter = ('theater_name', 'show_time')
    search_fields = ('movie__title', 'theater_name')

@admin.register(MovieTicket)
class MovieTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'seats', 'total_price', 'booking_time', 'customer_name', 'customer_phone', 'payment_method')
    list_filter = ('show__movie__title', 'booking_time', 'payment_method')
    search_fields = ('user__username', 'customer_name', 'customer_phone', 'show__movie__title')
