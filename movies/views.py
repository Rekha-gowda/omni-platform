from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Movie, Show, MovieTicket, MovieSeat, MovieCart, MovieCartItem
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def movie_list(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies, 'query': query})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

@login_required
def book_ticket(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    # Release expired locks
    MovieSeat.objects.filter(show=show, lock_expires_at__lt=timezone.now()).update(is_booked=False, locked_by=None, lock_expires_at=None)
    
    if not show.seats.exists():
        rows = ['A', 'B', 'C', 'D']
        seats = [MovieSeat(show=show, seat_identifier=f"{r}{c}") for r in rows for c in range(1, 9)]
        MovieSeat.objects.bulk_create(seats)

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')
        if selected_seat_ids:
            cart, _ = MovieCart.objects.get_or_create(user=request.user)
            for sid in selected_seat_ids:
                seat = get_object_or_404(MovieSeat, pk=sid)
                if not seat.is_locked():
                    seat.is_booked = True
                    seat.locked_by = request.user
                    seat.lock_expires_at = timezone.now() + timezone.timedelta(hours=3)
                    seat.save()
                    MovieCartItem.objects.create(cart=cart, seat=seat)
            return redirect('movie_cart_view')
    
    seats = show.seats.all()
    return render(request, 'movies/book_ticket.html', {'show': show, 'seats': seats})

@login_required
def movie_cart_view(request):
    cart, _ = MovieCart.objects.get_or_create(user=request.user)
    # Release all expired locks for this show or generally
    MovieSeat.objects.filter(lock_expires_at__lt=timezone.now()).update(is_booked=False, locked_by=None, lock_expires_at=None)
    # Remove corresponding cart items
    MovieCartItem.objects.filter(seat__lock_expires_at__isnull=True, seat__is_booked=False).delete() # This is a bit complex, let's keep it simple
    cart.items.filter(seat__is_booked=False).delete()
    return render(request, 'movies/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(MovieCartItem, id=item_id, cart__user=request.user)
        item.seat.is_booked = False
        item.seat.locked_by = None
        item.seat.lock_expires_at = None
        item.seat.save()
        item.delete()
    return redirect('movie_cart_view')

@login_required
def checkout_movie_cart(request):
    cart, _ = MovieCart.objects.get_or_create(user=request.user)
    total = cart.get_total()
    if request.method == 'POST' and total > 0:
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        payment_method = request.POST.get('payment_method', 'COD')
        
        shows_seats = {}
        for item in cart.items.all():
            show = item.seat.show
            if show not in shows_seats:
                shows_seats[show] = []
            shows_seats[show].append(item.seat)
            item.seat.lock_expires_at = None
            item.seat.save()
            
        for show, seats in shows_seats.items():
            MovieTicket.objects.create(
                user=request.user,
                show=show,
                seats=len(seats),
                total_price=sum(s.show.price for s in seats),
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                payment_method=payment_method
            )

        cart.items.all().delete()
        if payment_method == 'UPI':
            return redirect(f"/payment/success/?amount={total}&module=Movies")
        return redirect(f"/payment/confirm/?amount={total}&module=Movies")
    return redirect('movie_cart_view')

@login_required
def ticket_history(request):
    tickets = MovieTicket.objects.filter(user=request.user).order_by('-booking_time')
    return render(request, 'movies/history.html', {'tickets': tickets})

@login_required
def download_ticket_pdf(request, ticket_id):
    ticket = get_object_or_404(MovieTicket, pk=ticket_id, user=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="MovieTicket_{ticket.id}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 750, "Omni Platform - Movie Ticket")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Ticket ID: {ticket.id}")
    p.drawString(100, 700, f"Customer: {ticket.customer_name}")
    p.drawString(100, 680, f"Movie: {ticket.show.movie.title}")
    p.drawString(100, 660, f"Theater: {ticket.show.theater_name}")
    p.drawString(100, 640, f"Show Time: {ticket.show.time}")
    p.drawString(100, 620, f"Number of Seats: {ticket.seats}")
    p.drawString(100, 600, f"Total Amount: ₹{ticket.total_price}")
    p.drawString(100, 580, f"Status: {ticket.payment_method} - Confirmed")
    
    p.showPage()
    p.save()
    return response
