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
    list_display = ('id', 'user', 'user_email', 'restaurant', 'ordered_items', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'restaurant')
    search_fields = ('id', 'user__username', 'user__email', 'delivery_name', 'delivery_phone')
    inlines = [FoodComplaintInline]
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        from django.utils import timezone
        now = timezone.now()
        for order in qs:
            hours_passed = (now - order.created_at).total_seconds() / 3600.0
            if hours_passed >= 1 and order.status in ['Pending', 'Preparing (Arriving in 1 Hour)']:
                order.status = 'Delivered'
                order.save(update_fields=['status'])
            elif order.status == 'Pending':
                order.status = 'Preparing (Arriving in 1 Hour)'
                order.save(update_fields=['status'])
        return qs

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

@admin.register(FoodComplaint)
class FoodComplaintAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(FoodReview)
class FoodReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
