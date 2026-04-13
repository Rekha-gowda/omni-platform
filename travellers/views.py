from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Bus, Trip, BusBooking, BusSeat


def bus_list(request):
    query = request.GET.get('q', '')
    
    buses = Bus.objects.all()
    
    if query:
        buses = buses.filter(
            Q(name__icontains=query) |
            Q(trips__source__icontains=query) |
            Q(trips__destination__icontains=query)
        ).distinct()
        
    return render(request, 'travellers/bus_list.html', {
        'buses': buses, 
        'query': query
    })

def bus_trips(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    # Release expired locks for all trips of this bus
    BusSeat.objects.filter(trip__bus=bus, lock_expires_at__lt=timezone.now()).update(is_booked=False, locked_by=None, lock_expires_at=None)
    
    trips = bus.trips.all().order_by('departure_date', 'timing_shift')
    return render(request, 'travellers/bus_trips.html', {'bus': bus, 'trips': trips})

@login_required
def book_bus(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    if not trip.seats.exists():
        rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        cols = ['A', 'B', 'C', 'D']
        seats = [BusSeat(trip=trip, seat_identifier=f"{r}{c}") for r in rows for c in cols]
        BusSeat.objects.bulk_create(seats)

    # Release expired locks/bookings (3-hour rule)
    # The user specifically said "releasing after 3 hours"
    expired_seats = trip.seats.filter(lock_expires_at__lt=timezone.now())
    if expired_seats.exists():
        expired_seats.update(is_booked=False, locked_by=None, lock_expires_at=None)

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        
        payment_method = request.POST.get('payment_method', 'COD')
        
        if selected_seat_ids and customer_name and customer_email and customer_phone:
            total = len(selected_seat_ids) * trip.price_per_seat
            for sid in selected_seat_ids:
                seat = get_object_or_404(BusSeat, pk=sid)
                if not seat.is_locked():
                    seat.is_booked = True
                    seat.locked_by = request.user
                    seat.lock_expires_at = timezone.now() + timezone.timedelta(hours=3)
                    seat.save()

            booking = BusBooking.objects.create(
                user=request.user, 
                trip=trip, 
                no_of_seats=len(selected_seat_ids), 
                total_cost=total,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                payment_method=payment_method
            )

            # CLEAR EXPIRY ON CONFIRMED BOOKING
            for sid in selected_seat_ids:
                seat = get_object_or_404(BusSeat, pk=sid)
                seat.lock_expires_at = None
                seat.save()
            amount_str = f"{total:.2f}"
            if payment_method == 'UPI':
                return redirect(f"/payment/success/?amount={amount_str}&module=Travellers&ref={booking.id}")
            return redirect(f"/payment/confirm/?amount={amount_str}&module=Travellers&ref={booking.id}")
            
    seats = trip.seats.all()
    return render(request, 'travellers/book_bus.html', {'trip': trip, 'seats': seats})

@login_required
def booking_history(request):
    bookings = BusBooking.objects.filter(user=request.user).order_by('-booking_time').select_related('trip__bus')
    return render(request, 'travellers/history.html', {'bookings': bookings})

@login_required
def download_ticket_pdf(request, booking_id):
    booking = get_object_or_404(BusBooking, pk=booking_id, user=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="BusTicket_{booking.id}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 750, "Omni Platform - Bus Ticket")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Booking ID: {booking.id}")
    p.drawString(100, 700, f"Customer: {booking.customer_name}")
    p.drawString(100, 680, f"Bus: {booking.trip.bus.name}")
    p.drawString(100, 660, f"Route: {booking.trip.source} to {booking.trip.destination}")
    p.drawString(100, 640, f"Travel Date: {booking.trip.departure_date}")
    p.drawString(100, 620, f"Reporting Time: {booking.trip.departure_time}")
    p.drawString(100, 600, f"Number of Seats: {booking.no_of_seats}")
    p.drawString(100, 580, f"Total Amount: ₹{booking.total_cost}")
    p.drawString(100, 560, f"Status: {booking.payment_method} - Confirmed")
    
    p.showPage()
    p.save()
    return response
