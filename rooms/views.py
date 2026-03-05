from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from .models import Room, Booking
from .forms import BookingForm
from .utils import apply_time_dilation


class RoomListView(ListView):
    model = Room
    template_name = "home/index.html"
    context_object_name = "rooms"

    def get_queryset(self):
        # Start with non-collapsing rooms
        qs = Room.objects.filter(is_collapsing=False)

        params = self.request.GET

        # Filter by gravity (JSONField lookup)
        gravity = params.get("gravity")
        if gravity:
            qs = qs.filter(reality_rules__physics__gravity__icontains=gravity)

        # Filter by dilation factor range
        min_dilation = params.get("min_dilation")
        if min_dilation:
            try:
                qs = qs.filter(
                    reality_rules__time__dilation_factor__gte=float(min_dilation)
                )
            except (ValueError, TypeError):
                pass

        max_dilation = params.get("max_dilation")
        if max_dilation:
            try:
                qs = qs.filter(
                    reality_rules__time__dilation_factor__lte=float(max_dilation)
                )
            except (ValueError, TypeError):
                pass

        # Filter by dimension code
        dimension = params.get("dimension")
        if dimension:
            qs = qs.filter(dimension_code__icontains=dimension)

        return qs


class RoomDetailView(DetailView):
    model = Room
    template_name = "room_detail/room_detail.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if getattr(obj, "is_collapsing", False):
            raise Http404("Room not found")
        return obj


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        bookings = Booking.objects.filter(guest=user)
        context["user"] = user
        context["bookings"] = bookings.distinct()
        return context


@login_required
def book_room(request, room_id):
    """
    Handles the booking form for a specific room.

    - Loads the Room instance.
    - Validates and saves the Booking form.
    - Applies time-dilation rules via apply_time_dilation().
    - Stores adjusted_nights and adjusted_checkout on the Booking.
    - Redirects to the confirmation page on success.

    Expects POST data containing guest_name, nights, and check_in.
    """

    room = get_object_or_404(Room, id=room_id)

    # Prevent direct booking of collapsing rooms
    if getattr(room, "is_collapsing", False):
        raise Http404("Room not available")


    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Validate min_nights and max_nights from reality_rules JSON
            nights = form.cleaned_data.get("nights")
            rules = room.reality_rules or {}
            time_rules = rules.get("time", {})
            min_nights = time_rules.get("min_nights")
            max_nights = time_rules.get("max_nights")
            error = None
            if min_nights is not None and nights < min_nights:
                error = f"Minimum stay for this dimension is {min_nights} nights."
            if max_nights is not None and nights > max_nights:
                error = f"Maximum stay for this dimension is {max_nights} nights."
            if error:
                return render(
                    request,
                    "booking/booking.html",
                    {
                        "room": room,
                        "form": form,
                        "error": error,
                    },
                )

            booking = form.save(commit=False)
            booking.room = room
            booking.guest = request.user
            if not booking.guest_name:
                booking.guest_name = request.user.get_username()

            # Apply time dilation
            data = apply_time_dilation(booking)
            booking.adjusted_nights = data["adjusted_nights"]
            booking.adjusted_checkout = data["adjusted_checkout"]

            booking.save()
            return redirect("booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(
        request,
        "booking/booking.html",
        {
            "room": room,
            "form": form,
        },
    )


@login_required
def booking_confirmation(request, booking_id):
    """
    Displays the final booking details, including both the original and
    dimension-adjusted values. Also surfaces any warnings or physics data
    defined in the room's reality_rules JSON.
    """
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    rules = booking.room.reality_rules or {}

    return render(
        request,
        "booking/booking_confirmation.html",
        {
            "booking": booking,
            "warnings": rules.get("warnings", []),
            "physics": rules.get("physics", {}),
        },
    )
