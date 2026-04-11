from reportlab.pdfgen import canvas

def generate_ticket(user,movie,seat):

    file=f"{user}_ticket.pdf"

    c=canvas.Canvas(file)

    c.drawString(100,750,"Movie Ticket")
    c.drawString(100,700,f"User: {user}")
    c.drawString(100,680,f"Movie: {movie}")
    c.drawString(100,660,f"Seat: {seat}")

    c.save()

    return file
