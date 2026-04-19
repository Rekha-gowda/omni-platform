from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from .models import Product, ShoppingOrder, ShoppingOrderItem, ShoppingCart, ShoppingCartItem

def product_list(request):
    category = request.GET.get('category')
    query = request.GET.get('q')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
        
    if query:
        products = products.filter(name__icontains=query)
        
    categories = [{'key': k, 'label': v} for k, v in Product._meta.get_field('category').choices]
    return render(request, 'shopping/product_list.html', {'products': products, 'categories': categories, 'selected_category': category, 'query': query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:10]
    return render(request, 'shopping/product_detail.html', {'product': product, 'related_products': related_products})

@login_required
def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    previous_addresses = ShoppingOrder.objects.filter(user=request.user).values_list('delivery_address', flat=True).distinct()[:5]
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        name = request.POST.get('delivery_name')
        address = request.POST.get('delivery_address')
        phone = request.POST.get('delivery_phone')
        size = request.POST.get('size')
        is_fast = request.POST.get('is_fast_delivery') == 'on'
        payment_method = request.POST.get('payment_method', 'COD')
        
        total = product.price * quantity
        if is_fast:
            total += 50
            
        order = ShoppingOrder.objects.create(
            user=request.user, 
            total_amount=total, 
            is_paid=(payment_method != 'COD'), # Assume paid if not COD for simplicity in this flow
            delivery_name=name,
            delivery_address=address,
            delivery_phone=phone,
            is_fast_delivery=is_fast,
            payment_method=payment_method
        )
        ShoppingOrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price, size=size)
        
        total_str = f"{total:.2f}"
        if payment_method in ['UPI', 'Card']:
            return redirect(f"/payment/success/?amount={total_str}&module=Shopping&ref={order.id}")
        return redirect(f"/payment/confirm/?amount={total_str}&module=Shopping&ref={order.id}")
    return render(request, 'shopping/buy_product.html', {'product': product, 'previous_addresses': previous_addresses})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
    
    size = None
    if request.method == 'POST':
        size = request.POST.get('size')
        
    item, created = ShoppingCartItem.objects.get_or_create(cart=cart, product=product, size=size)
    if not created:
        item.quantity += 1
        item.save()
    from django.contrib import messages
    messages.success(request, f"Added {product.name} to your cart!")
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def cart_view(request):
    cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
    return render(request, 'shopping/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingCartItem, id=item_id, cart__user=request.user)
        item.delete()
    return redirect('cart_view')

@login_required
def checkout_cart(request):
    cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
    previous_addresses = ShoppingOrder.objects.filter(user=request.user).values_list('delivery_address', flat=True).distinct()[:5]
    
    if request.method == 'POST':
        name = request.POST.get('delivery_name')
        address = request.POST.get('delivery_address')
        phone = request.POST.get('delivery_phone')
        is_fast = request.POST.get('is_fast_delivery') == 'on'
        payment_method = request.POST.get('payment_method', 'COD')
        
        total = cart.get_total()
        if is_fast:
            total += 50
            
        if total > 0:
            order = ShoppingOrder.objects.create(
                user=request.user,
                total_amount=total,
                is_paid=(payment_method != 'COD'),
                delivery_name=name,
                delivery_address=address,
                delivery_phone=phone,
                is_fast_delivery=is_fast,
                payment_method=payment_method
            )
            for item in cart.items.all():
                ShoppingOrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price, size=item.size)
                
            cart.items.all().delete()
            
            total_str = f"{total:.2f}"
            if payment_method in ['UPI', 'Card']:
                return redirect(f"/payment/success/?amount={total_str}&module=Shopping&ref={order.id}")
            return redirect(f"/payment/confirm/?amount={total_str}&module=Shopping&ref={order.id}")
        return redirect('cart_view')
        
    return render(request, 'shopping/checkout.html', {'cart': cart, 'previous_addresses': previous_addresses})

@login_required
def order_history(request):
    orders = ShoppingOrder.objects.filter(user=request.user).order_by('-created_at')
    now = timezone.now()
    for order in orders:
        days_passed = (now - order.created_at).days
        delivery_threshold = 3 if order.is_fast_delivery else 7
        
        if days_passed >= delivery_threshold:
            if order.status == 'Pending':
                order.status = 'Delivered'
                order.save(update_fields=['status'])
            order.is_delivered = (order.status == 'Delivered')
            order.can_return = (order.is_delivered and days_passed <= (delivery_threshold + 3))
            order.can_review = order.is_delivered
        else:
            if order.status == 'Pending':
                order.expected_date = order.created_at + datetime.timedelta(days=delivery_threshold)
            order.is_delivered = (order.status == 'Delivered')
            order.can_return = False
            order.can_review = order.is_delivered
            
        for item in order.items.all():
            item.has_return = item.returns.exists()
            item.has_review = item.product.reviews.filter(user=request.user).exists()
            
            # Per-item return logic
            if order.is_delivered:
                if item.product.category.startswith('clothing_'):
                    # Clothing items have a 3-day return window after delivery (days 7 to 10)
                    item.can_return = (days_passed >= 7 and days_passed <= 10)
                else:
                    # Non-clothing items (like grocery) have no return window after delivery
                    item.can_return = False
            else:
                item.can_return = False
            
            item.can_review = order.is_delivered
            
    return render(request, 'shopping/history.html', {'orders': orders})

@login_required
def submit_return(request, item_id):
    if request.method == 'POST':
        from .models import ShoppingReturn
        item = get_object_or_404(ShoppingOrderItem, id=item_id, order__user=request.user)
        return_type = request.POST.get('return_type')
        reason_text = request.POST.get('reason_text')
        image = request.FILES.get('image')
        ShoppingReturn.objects.create(order_item=item, return_type=return_type, reason_text=reason_text, image=image)
    return redirect('shopping_history')

@login_required
def submit_review(request, product_id):
    if request.method == 'POST':
        from .models import ShoppingReview
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating', 5)
        review_text = request.POST.get('review_text')
        image = request.FILES.get('image')
        ShoppingReview.objects.create(product=product, user=request.user, rating=rating, review_text=review_text, image=image)
    return redirect('shopping_history')
