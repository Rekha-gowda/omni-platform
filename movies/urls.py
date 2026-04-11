from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('book/<int:show_id>/', views.book_ticket, name='book_ticket'),
    path('cart/', views.movie_cart_view, name='movie_cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='movie_remove_from_cart'),
    path('cart/checkout/', views.checkout_movie_cart, name='checkout_movie_cart'),
    path('history/', views.ticket_history, name='ticket_history'),
    path('ticket/<int:ticket_id>/pdf/', views.download_ticket_pdf, name='download_movie_ticket_pdf'),
]
