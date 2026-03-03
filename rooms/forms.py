from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form for creating a Booking.

    Accepts guest_name, nights, and check_in from user input.
    Does not apply any time-dilation logic itself; the view handles
    calling apply_time_dilation() before saving the Booking instance.
    """

    class Meta:
        model = Booking
        fields = ["guest_name", "check_in", "nights"]
