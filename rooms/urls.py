from django.urls import path
from .views import (
    RoomListView,
    RoomDetailView,
    ProfileView,
    book_room,
    booking_confirmation,
)

app_name = "rooms"

urlpatterns = [
    path("", RoomListView.as_view(), name="room_list"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
    path("room/<int:room_id>/book/", book_room, name="book_room"),
    path(
        "booking/<int:booking_id>/confirmation/",
        booking_confirmation,
        name="booking_confirmation",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
]
