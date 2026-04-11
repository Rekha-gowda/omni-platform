from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/',admin.site.urls),
    path('shopping/',include('shopping.urls')),
    path('foods/',include('foods.urls')),
    path('movies/',include('movies.urls')),
    path('travellers/',include('travellers.urls')),
]
