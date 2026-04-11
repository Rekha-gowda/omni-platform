from django.contrib import admin
from .models import Movie, Show, MovieTicket

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater_name', 'show_time', 'price')

@admin.register(MovieTicket)
class MovieTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'seats', 'total_price', 'booking_time')
