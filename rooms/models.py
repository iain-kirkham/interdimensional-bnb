from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Room(models.Model):
    """
    Represents an interdimensional room with optional reality rules.

    reality_rules schema (convention, not enforced):

    {
        "time": {
            "dilation_factor": <number>,   # Multiplier for nights
            "offset_hours": <number>,      # Extra hours added to checkout
            "min_nights": <number>,        # Optional constraint
            "max_nights": <number>         # Optional constraint
        },
        "physics": {
            "gravity": "<string>",         # Optional flavour text
            "notes": "<string>"
        },
        "warnings": [
            "<string>",                    # Optional warnings shown to user
            "<string>"
        ]
    }
    """

    name = models.CharField(max_length=100)
    dimension_code = models.CharField(max_length=50)
    # Flag for unsafe/removed rooms — hide from public listings when True
    is_collapsing = models.BooleanField(default=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    reality_rules = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name} ({self.dimension_code})"


class Booking(models.Model):
    """
    Stores both the original and dimension-adjusted stay details.

    adjusted_nights and adjusted_checkout are computed using the room's
    reality_rules, based on the following logic:

    - adjusted_nights = nights * time.dilation_factor (default: 1)
    - adjusted_checkout = check_in + adjusted_nights (days)
                          + time.offset_hours (hours)

    Any warnings defined in reality_rules["warnings"] may be displayed
    on the confirmation page. Missing keys fall back to safe defaults.
    """

    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    guest_name = models.CharField(max_length=100)
    check_in = models.DateField()
    nights = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    # issue-6 - add additional fields for dilation adjusted booking values.
    adjusted_nights = models.FloatField(null=True, blank=True)
    adjusted_checkout = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} - {self.room.name} ({self.check_in})"
