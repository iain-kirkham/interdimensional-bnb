from django.contrib import admin
from .models import Room, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin for Room.

    Shows name, dimension code, and price; allows toggling
    is_collapsing from the changelist.
    """

    list_display = ("name", "dimension_code", "price_per_night", "is_collapsing")
    list_display_links = ("name",)
    list_editable = ("is_collapsing",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin for Booking.

    Displays primary booking fields and provides filters for
    quick lookup by room and check-in date.
    """

    list_display = ("guest_name", "room", "check_in", "nights", "created_at")
    list_filter = ("room", "check_in")
