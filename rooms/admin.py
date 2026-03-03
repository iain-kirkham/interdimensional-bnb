from django.contrib import admin
from .models import Room, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "dimension_code", "price_per_night")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "room", "check_in", "nights", "created_at")
    list_filter = ("room", "check_in")
