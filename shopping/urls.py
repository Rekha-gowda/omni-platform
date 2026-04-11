from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('buy/<int:pk>/', views.buy_product, name='buy_product'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/checkout/', views.checkout_cart, name='checkout_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='shopping_remove_from_cart'),
    path('history/', views.order_history, name='shopping_history'),
    path('history/return/<int:item_id>/', views.submit_return, name='submit_shopping_return'),
    path('history/review/<int:product_id>/', views.submit_review, name='submit_shopping_review'),
]
