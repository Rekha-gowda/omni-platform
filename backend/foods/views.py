from django.http import JsonResponse

def food_list(request):
    return JsonResponse({"message":"Food API working"})

def add_food_cart(request):
    return JsonResponse({"message":"Food added to cart"})

def view_food_cart(request,user_id):
    return JsonResponse({"message":"Food cart view"})

def place_food_order(request):
    return JsonResponse({"message":"Food order placed"})
# Create your views here.
