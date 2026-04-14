from django.contrib import admin
from .models import Restaurant, MenuItem, FoodOrder, FoodComplaint, FoodReview

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')

class FoodComplaintInline(admin.TabularInline):
    model = FoodComplaint
    extra = 0
    readonly_fields = ('reason_text', 'image', 'created_at', 'status')

@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_name', 'delivery_phone', 'restaurant', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'restaurant')
    search_fields = ('id', 'user__username', 'delivery_name', 'delivery_phone')
    inlines = [FoodComplaintInline]
    readonly_fields = ('created_at',)

@admin.register(FoodComplaint)
class FoodComplaintAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(FoodReview)
class FoodReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
