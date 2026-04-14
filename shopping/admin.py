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
    readonly_fields = ('product', 'quantity', 'price', 'size')

class ShoppingReturnInline(admin.TabularInline):
    model = ShoppingReturn
    extra = 0
    readonly_fields = ('return_type', 'reason_text', 'image', 'created_at')

@admin.register(ShoppingOrder)
class ShoppingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_name', 'delivery_phone', 'total_amount', 'status', 'current_location', 'agent_phone', 'expected_delivery', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'status', 'created_at')
    search_fields = ('id', 'user__username', 'delivery_name', 'delivery_phone', 'current_location', 'agent_phone')
    inlines = [ShoppingOrderItemInline]
    fields = ('user', 'total_amount', 'status', 'current_location', 'agent_phone', 'expected_delivery', 'is_paid', 'delivery_name', 'delivery_address', 'delivery_phone', 'delivered_at', 'is_fast_delivery', 'payment_method')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ShoppingReturn)
class ShoppingReturnAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'return_type', 'created_at')
    list_filter = ('return_type', 'created_at')

@admin.register(ShoppingReview)
class ShoppingReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
