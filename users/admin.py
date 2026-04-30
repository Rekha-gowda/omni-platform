from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, LoginHistory

from shopping.models import ShoppingOrder
from foods.models import FoodOrder
from movies.models import MovieTicket
from travellers.models import BusBooking

class ShoppingOrderInline(admin.TabularInline):
    model = ShoppingOrder
    extra = 0
    show_change_link = True
    fields = ('total_amount', 'status', 'created_at')
    readonly_fields = ('total_amount', 'created_at')
    can_delete = False

class FoodOrderInline(admin.TabularInline):
    model = FoodOrder
    extra = 0
    show_change_link = True
    fields = ('restaurant', 'total_amount', 'status', 'created_at')
    readonly_fields = ('restaurant', 'total_amount', 'created_at')
    can_delete = False

class MovieTicketInline(admin.TabularInline):
    model = MovieTicket
    extra = 0
    show_change_link = True
    fields = ('show', 'seats', 'total_price', 'booking_time')
    readonly_fields = ('show', 'total_price', 'booking_time')
    can_delete = False

class BusBookingInline(admin.TabularInline):
    model = BusBooking
    extra = 0
    show_change_link = True
    fields = ('trip', 'no_of_seats', 'total_cost', 'booking_time')
    readonly_fields = ('trip', 'total_cost', 'booking_time')
    can_delete = False

admin.site.unregister(Group)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ShoppingOrderInline, FoodOrderInline, MovieTicketInline, BusBookingInline)

admin.site.site_header = "Omni Platform Admin"
admin.site.index_title = "Omni Platform Management"
admin.site.site_title = "Omni Admin"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'ip_address', 'user_agent')
    list_filter = ('login_time', 'user')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'login_time', 'ip_address', 'user_agent')

