from django.urls import path
from . import views

urlpatterns = [

    path('foods/', views.food_list),
    path('add-cart/', views.add_food_cart),
    path('view-cart/<int:user_id>/', views.view_food_cart),
    path('place-order/', views.place_food_order),

]
