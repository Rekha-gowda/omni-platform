from django.urls import path
from . import views

urlpatterns = [
    path('', views.bus_list, name='bus_list'),
    path('bus/<int:bus_id>/trips/', views.bus_trips, name='bus_trips'),
    path('book/<int:trip_id>/', views.book_bus, name='book_bus'),
    path('history/', views.booking_history, name='booking_history'),
    path('ticket/<int:booking_id>/pdf/', views.download_ticket_pdf, name='download_bus_ticket_pdf'),
]
