from django.urls import path
from . import views

urlpatterns = [

    path('', views.product_list, name='products'),

    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.view_cart, name='view_cart'),

    path('order/', views.place_order, name='place_order'),

    path('orders/', views.order_history, name='order_history'),
]
