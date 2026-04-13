from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from shopping.models import ShoppingOrder
from foods.models import FoodOrder
from movies.models import MovieTicket
from travellers.models import BusBooking
import itertools
from operator import attrgetter

def home(request):
    return render(request, 'core/home.html')

def offline(request):
    return render(request, 'offline.html')


def payment_confirmation(request):
    amount = request.GET.get('amount', '0.00')
    module = request.GET.get('module', 'Omni System')
    ref = request.GET.get('ref', '')
    
    # If we already have the details, just go to success to avoid "asking again"
    if amount and module:
        return redirect(f"/payment/success/?amount={amount}&module={module}&ref={ref}")
        
    if request.method == 'POST':
        return redirect('payment_success')
    return render(request, 'core/payment_confirmation.html', {'amount': amount, 'module': module})

def payment_success(request):
    amount = request.GET.get('amount', '0.00')
    module = request.GET.get('module', 'Omni System')
    ref = request.GET.get('ref', '')
    return render(request, 'core/payment_success.html', {'amount': amount, 'module': module, 'ref': ref})

@login_required
def download_ticket_pdf(request):
    module = request.GET.get('module', '')
    ref = request.GET.get('ref', '')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{module}_Ticket.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    
    # Header
    p.setFont("Helvetica-Bold", 24)
    p.setStrokeColorRGB(0.9, 0.18, 0.44) # Omni Pink
    p.drawString(100, 750, "Omni Platform E-Ticket")
    p.line(100, 740, 500, 740)
    
    p.setFont("Helvetica-Bold", 16)
    p.setStrokeColorRGB(0, 0, 0)
    p.drawString(100, 710, f"Service: {module}")
    
    p.setFont("Helvetica", 12)
    y = 680
    
    if module == 'Movies':
        try:
            ticket = MovieTicket.objects.get(id=ref, user=request.user)
            p.drawString(100, y, f"Movie: {ticket.show.movie.title}")
            y -= 20
            p.drawString(100, y, f"Theater: {ticket.show.theater_name}")
            y -= 20
            p.drawString(100, y, f"Show Time: {ticket.show.show_time.strftime('%b %d, %Y - %I:%M %p')}")
            y -= 20
            p.drawString(100, y, f"Seats: {ticket.seats}")
            y -= 20
            p.drawString(100, y, f"Total Amount: ₹{ticket.total_price}")
            y -= 20
            p.drawString(100, y, f"Customer: {ticket.customer_name}")
        except MovieTicket.DoesNotExist:
            p.drawString(100, y, f"Reference: {ref}")
            p.drawString(100, y-20, "Detail retrieval failed.")
            
    elif module == 'Travellers':
        try:
            booking = BusBooking.objects.get(id=ref, user=request.user)
            p.drawString(100, y, f"Bus: {booking.trip.bus.name}")
            y -= 20
            p.drawString(100, y, f"Route: {booking.trip.source} to {booking.trip.destination}")
            y -= 20
            p.drawString(100, y, f"Departure: {booking.trip.departure_date} at {booking.trip.departure_time if hasattr(booking.trip, 'departure_time') else booking.trip.timing_shift}")
            y -= 20
            p.drawString(100, y, f"Number of Seats: {booking.no_of_seats}")
            y -= 20
            p.drawString(100, y, f"Total Amount: ₹{booking.total_cost}")
            y -= 20
            p.drawString(100, y, f"Customer: {booking.customer_name}")
        except BusBooking.DoesNotExist:
            p.drawString(100, y, f"Reference: {ref}")
            p.drawString(100, y-20, "Detail retrieval failed.")
    
    else:
        p.drawString(100, y, f"Reference Number: {ref}")
        y -= 20
        p.drawString(100, y, f"Issued To: {request.user.username}")
    
    y -= 40
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, y, "Thank you for choosing Omni Platform! Enjoy your experience.")
    
    p.showPage()
    p.save()
    return response

def robots_txt(request):
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /accounts/\nSitemap: http://localhost:8000/sitemap.xml"
    return HttpResponse(content, content_type="text/plain")

@login_required
def unified_history(request):
    shopping_orders = ShoppingOrder.objects.filter(user=request.user)
    food_orders = FoodOrder.objects.filter(user=request.user)
    movie_tickets = MovieTicket.objects.filter(user=request.user)
    bus_bookings = BusBooking.objects.filter(user=request.user)
    
    # Add a timestamp attribute to each for consistent sorting
    for o in shopping_orders: 
        o.timestamp = o.created_at
        o.type = 'shopping'
    for o in food_orders:
        o.timestamp = o.created_at
        o.type = 'food'
    for t in movie_tickets:
        t.timestamp = t.booking_time
        t.type = 'movie'
    for b in bus_bookings:
        b.timestamp = b.booking_time
        b.type = 'bus'
        
    activities = sorted(
        itertools.chain(shopping_orders, food_orders, movie_tickets, bus_bookings),
        key=attrgetter('timestamp'),
        reverse=True
    )
    
    return render(request, 'core/unified_history.html', {'activities': activities})
