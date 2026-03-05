from django import forms
from django.core.exceptions import ValidationError
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form for creating a Booking.

    Accepts guest_name, nights, and check_in from user input.
    Does not apply any time-dilation logic itself; the view handles
    calling apply_time_dilation() before saving the Booking instance.

    Validates nights against optional min_nights and max_nights
    defined in room.reality_rules["time"].
    """

    class Meta:
        model = Booking
        fields = ["guest_name", "check_in", "nights"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        # The view will pass room=room into the form
        self.room = kwargs.pop("room", None)
        super().__init__(*args, **kwargs)

    def clean_nights(self):
        nights = self.cleaned_data.get("nights")

        if not self.room:
            return nights  # safety fallback

        rules = self.room.reality_rules or {}
        time_rules = rules.get("time", {})

        min_nights = time_rules.get("min_nights")
        max_nights = time_rules.get("max_nights")

        # Validate minimum
        if min_nights is not None and nights < min_nights:
            raise ValidationError(
                f"Minimum stay in this dimension is {min_nights} nights."
            )

        # Validate maximum
        if max_nights is not None and nights > max_nights:
            raise ValidationError(
                f"The maximum stay in this dimension is {max_nights} nights."
            )

        return nights
