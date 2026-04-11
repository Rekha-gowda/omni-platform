from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from .models import Restaurant, MenuItem, FoodOrder, FoodCart, FoodCartItem, FoodReview, FoodComplaint

def get_previous_addresses(user):
    return FoodOrder.objects.filter(user=user).values_list('delivery_address', flat=True).distinct().order_by('-created_at')[:5]

def restaurant_list(request):
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) | Q(menu__name__icontains=query)
        ).distinct()
    else:
        restaurants = Restaurant.objects.all()
    return render(request, 'foods/restaurant_list.html', {'restaurants': restaurants, 'query': query})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'foods/restaurant_detail.html', {'restaurant': restaurant})

@login_required
def order_food(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('delivery_name')
        address = request.POST.get('delivery_address')
        phone = request.POST.get('delivery_phone')
        payment_method = request.POST.get('payment_method', 'COD')
        order = FoodOrder.objects.create(
            user=request.user,
            restaurant=item.restaurant,
            total_amount=item.price,
            delivery_name=name,
            delivery_address=address,
            delivery_phone=phone,
            payment_method=payment_method
        )
        if payment_method in ['UPI', 'Card']:
            return redirect(f"/payment/success/?amount={order.total_amount}&module=Foods&ref={order.id}")
        return redirect(f"/payment/confirm/?amount={order.total_amount}&module=Foods&ref={order.id}")
    
    prev_addresses = get_previous_addresses(request.user) if request.user.is_authenticated else []
    return render(request, 'foods/order_food.html', {'item': item, 'prev_addresses': prev_addresses})

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    cart, _ = FoodCart.objects.get_or_create(user=request.user)
    cart_item, created = FoodCartItem.objects.get_or_create(cart=cart, menu_item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    from django.contrib import messages
    messages.success(request, f"Added {item.name} to your food cart!")
    return redirect(request.META.get('HTTP_REFERER', 'restaurant_list'))

@login_required
def cart_view(request):
    cart, _ = FoodCart.objects.get_or_create(user=request.user)
    return render(request, 'foods/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(FoodCartItem, id=item_id, cart__user=request.user)
        item.delete()
    return redirect('food_cart_view')

@login_required
def checkout_cart(request):
    cart, _ = FoodCart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('delivery_name')
        address = request.POST.get('delivery_address')
        phone = request.POST.get('delivery_phone')
        
        items = cart.items.all()
        if not items:
            return redirect('food_cart_view')
            
        from collections import defaultdict
        restaurant_items = defaultdict(list)
        for item in items:
            restaurant_items[item.menu_item.restaurant].append(item)
            
        total_overall = 0
        ref_ids = []
        payment_method = request.POST.get('payment_method', 'COD')
        for restaurant, r_items in restaurant_items.items():
            r_total = sum(i.menu_item.price * i.quantity for i in r_items)
            total_overall += r_total
            order = FoodOrder.objects.create(
                user=request.user,
                restaurant=restaurant,
                total_amount=r_total,
                delivery_name=name,
                delivery_address=address,
                delivery_phone=phone,
                payment_method=payment_method
            )
            ref_ids.append(str(order.id))
            
        cart.items.all().delete()
        refs = ",".join(ref_ids)
        total_overall_str = f"{total_overall:.2f}"
        if payment_method in ['UPI', 'Card']:
            return redirect(f"/payment/success/?amount={total_overall_str}&module=Foods&ref={refs}")
        return redirect(f"/payment/confirm/?amount={total_overall_str}&module=Foods&ref={refs}")
        
    prev_addresses = get_previous_addresses(request.user) if request.user.is_authenticated else []
    return render(request, 'foods/checkout.html', {'cart': cart, 'prev_addresses': prev_addresses})

@login_required
def order_history(request):
    orders = FoodOrder.objects.filter(user=request.user).order_by('-created_at')
    now = timezone.now()
    for order in orders:
        hours_passed = (now - order.created_at).total_seconds() / 3600.0
        if hours_passed >= 1:
            order.status = 'Delivered'
            order.is_delivered = True
            order.can_review = True
            # can_complain is True up to 1 hour AFTER delivery (total 2 hours)
            order.can_complain = hours_passed < 2.0
        else:
            order.status = 'Preparing (Arriving in 1 Hour)'
            order.is_delivered = False
            order.can_review = False
            order.can_complain = True
            
        order.has_complaint = order.complaints.exists()
        # Check for review specifically for THIS order
        order.has_review = order.reviews.exists()
        
        # Hide "No Returns" message if already reviewed OR if more than 1h passed since delivery (T+2h)
        order.show_no_return_warning = order.is_delivered and not order.has_review and hours_passed < 2.0
            
    return render(request, 'foods/history.html', {'orders': orders})

@login_required
def submit_complaint(request, order_id):
    if request.method == 'POST':
        from .models import FoodComplaint
        order = get_object_or_404(FoodOrder, id=order_id, user=request.user)
        reason_text = request.POST.get('reason_text')
        image = request.FILES.get('image')
        FoodComplaint.objects.create(order=order, reason_text=reason_text, image=image)
    return redirect('foods_history')

@login_required
def submit_food_review(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        order_id = request.POST.get('order_id')
        order = None
        if order_id:
            order = FoodOrder.objects.filter(id=order_id, user=request.user).first()
            
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        image = request.FILES.get('image')
        FoodReview.objects.create(
            restaurant=restaurant,
            user=request.user,
            order=order,
            rating=rating,
            review_text=review_text,
            image=image
        )
    return redirect('foods_history')
