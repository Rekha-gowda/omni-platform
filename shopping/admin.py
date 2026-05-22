from django.contrib import admin
from .models import Product, ShoppingOrder, ShoppingOrderItem, ShoppingReturn, ShoppingReview

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'description')

class ShoppingOrderItemInline(admin.TabularInline):
    model = ShoppingOrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'quantity_unit')

class ShoppingReturnInline(admin.TabularInline):
    model = ShoppingReturn
    extra = 0
    readonly_fields = ('return_type', 'reason_text', 'image', 'created_at')

@admin.register(ShoppingOrder)
class ShoppingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_email', 'delivery_name', 'delivery_phone', 'total_amount', 'status', 'current_location', 'agent_phone', 'expected_delivery', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'status', 'created_at')
    search_fields = ('id', 'user__username', 'user__email', 'delivery_name', 'delivery_phone', 'current_location', 'agent_phone')
    inlines = [ShoppingOrderItemInline]
    fields = ('user', 'total_amount', 'status', 'current_location', 'agent_phone', 'expected_delivery', 'is_paid', 'delivery_name', 'delivery_address', 'delivery_phone', 'delivered_at', 'is_fast_delivery', 'payment_method')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        from django.utils import timezone
        import datetime
        now = timezone.now()
        for order in qs:
            days_passed = (now - order.created_at).days
            delivery_threshold = 3 if order.is_fast_delivery else 7
            
            if days_passed >= delivery_threshold:
                if order.status == 'Pending':
                    order.status = 'Delivered'
                    order.delivered_at = now
                    order.save(update_fields=['status', 'delivered_at'])
            else:
                if order.status == 'Pending' and not order.expected_delivery:
                    order.expected_delivery = order.created_at + datetime.timedelta(days=delivery_threshold)
                    order.save(update_fields=['expected_delivery'])
        return qs

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

@admin.register(ShoppingReturn)
class ShoppingReturnAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'return_type', 'created_at')
    list_filter = ('return_type', 'created_at')

@admin.register(ShoppingReview)
class ShoppingReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
