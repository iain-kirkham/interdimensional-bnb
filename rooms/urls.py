from django.urls import path
from .views import (
    RoomListView,
    RoomDetailView,
    book_room,
    booking_confirmation,
)

app_name = 'rooms'

urlpatterns = [
    # Homepage → room list
    path('', RoomListView.as_view(), name='home'),

    # Optional aliases (keep if UX wants them)
    path('home/', RoomListView.as_view(), name='home_page'),
    path('index/', RoomListView.as_view(), name='index'),

    # Canonical room list URL
    path('rooms/', RoomListView.as_view(), name='room_list'),

    # Room detail (slug-based)
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),

    # Booking flow
    path('room/<int:room_id>/book/', book_room, name='book_room'),
    path('booking/<int:booking_id>/confirmation/', booking_confirmation, name='booking_confirmation'),
]
