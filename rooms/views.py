from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Room, Booking
from .forms import BookingForm


class RoomListView(ListView):
    model = Room
    template_name = 'home/index.html'
    context_object_name = 'rooms'


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail/room_detail.html'
    context_object_name = 'room'


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.save()
            return redirect("booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, "booking/booking.html", {
        "room": room,
        "form": form,
    })


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "booking/booking.html", {
        "booking": booking,
    })
