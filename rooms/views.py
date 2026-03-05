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
    template_name = "rooms/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """
        Return non-collapsing Room objects filtered by GET parameters.

        Supported query parameters:
        - gravity - substring match against
          reality_rules['physics']['gravity'].
        - min_dilation / max_dilation — numeric bounds on
          reality_rules['time']['dilation_factor'].
        - dimension — substring match against dimension_code.

        Malformed or non-numeric values for numeric filters are ignored.
        """
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
                    reality_rules__time__dilation_factor__gte=float(
                        min_dilation
                    )
                )
            except (ValueError, TypeError):
                pass

        max_dilation = params.get("max_dilation")
        if max_dilation:
            try:
                qs = qs.filter(
                    reality_rules__time__dilation_factor__lte=float(
                        max_dilation
                    )
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
    template_name = "rooms/room_detail.html"
    context_object_name = "room"

    def get_object(self, queryset=None):
        """
        Return the Room instance for this view.

        If the room is marked is_collapsing it is treated as not found
        and Http404 is raised to prevent access.
        """

        obj = super().get_object(queryset)
        if getattr(obj, "is_collapsing", False):
            raise Http404("Room not found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = context["room"]
        rules = room.reality_rules or {}
        time_rules = rules.get("time", {})

        context.update({
            "physics": rules.get("physics", {}),
            "warnings": rules.get("warnings", []),
            "min_nights": time_rules.get("min_nights"),
            "max_nights": time_rules.get("max_nights"),
        })

        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        """
        Add the authenticated user and their bookings to the context.

        Adds user and bookings (distinct queryset) for use in the
        profile template.
        """

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
        # Pass Room into the form for min/max validation
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
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
            return redirect("rooms:booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm(room=room)

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
