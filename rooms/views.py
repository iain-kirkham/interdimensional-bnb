from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        bookings = Booking.objects.filter(guest=user)
        context['user'] = user
        context['bookings'] = bookings.distinct()
        return context


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            if request.user.is_authenticated:
                booking.guest = request.user
                booking.guest_name = request.user.get_username()
            booking.save()
            return redirect("booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, "booking/booking.html", {
        "room": room,
        "form": form,
    })


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    return render(request, "booking/booking_confirmation.html", {
        "booking": booking,
    })
