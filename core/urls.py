from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('offline/', views.offline, name='offline'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('payment/confirm/', views.payment_confirmation, name='payment_confirmation'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('download-pdf/', views.download_ticket_pdf, name='download_ticket_pdf'),
    path('account/history/', views.unified_history, name='unified_history'),
]
