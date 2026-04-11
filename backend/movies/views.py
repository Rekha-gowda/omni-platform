from django.shortcuts import render
from django.http import JsonResponse


def movie_list(request):
    return JsonResponse({"message": "Movies list working"})


def book_seat(request):
    return JsonResponse({"message": "Seat booked"})


def my_tickets(request, user_id):
    return JsonResponse({"message": "User tickets"})
# Create your views here.
