from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('order/<int:pk>/', views.order_food, name='order_food'),
    path('history/', views.order_history, name='foods_history'),
    path('history/complaint/<int:order_id>/', views.submit_complaint, name='submit_food_complaint'),
    path('history/review/<int:restaurant_id>/', views.submit_food_review, name='submit_food_review'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='food_add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='food_remove_from_cart'),
    path('cart/', views.cart_view, name='food_cart_view'),
    path('cart/checkout/', views.checkout_cart, name='food_checkout_cart'),
]
