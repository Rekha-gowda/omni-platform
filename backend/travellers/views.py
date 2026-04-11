from django.shortcuts import render
from django.http import JsonResponse


def bus_list(request):
    return JsonResponse({"message": "Bus list working"})


def book_bus(request):
    return JsonResponse({"message": "Bus seat booked"})
# Create your views here.
