from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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

        username = user.get_username()
        full_name = f"{user.first_name} {user.last_name}".strip()
        bookings = Booking.objects.none()
        if username and full_name:
            bookings = Booking.objects.filter(guest_name__in=[username, full_name])
        elif username:
            bookings = Booking.objects.filter(guest_name=username)
        elif full_name:
            bookings = Booking.objects.filter(guest_name=full_name)
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
    booking = get_object_or_404(Booking, id=booking_id)
    user = request.user
    username = user.get_username()
    full_name = f"{user.first_name} {user.last_name}".strip()
    if booking.guest_name not in ([username] if username else []) + ([full_name] if full_name else []):
        return HttpResponseForbidden("You do not have permission to view this booking.")

    return render(request, "booking/booking_confirmation.html", {
        "booking": booking,
    })
