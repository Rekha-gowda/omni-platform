from django.urls import path
from . import views

urlpatterns = [

    path('buses/', views.bus_list),
    path('book-seat/', views.book_bus),
]
