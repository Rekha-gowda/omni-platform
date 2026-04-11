from django.shortcuts import render, redirect
from .models import Product, Cart, Order, OrderItem
from django.contrib.auth.models import User


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopping/products.html', {'products': products})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'shopping/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect('order_history')


def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shopping/orders.html', {'orders': orders})
