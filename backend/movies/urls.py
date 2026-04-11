from django.urls import path
from . import views

urlpatterns = [

    path('movies/', views.movie_list),
    path('book-seat/', views.book_seat),
    path('my-tickets/<int:user_id>/', views.my_tickets),

]
