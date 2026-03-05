from django.urls import path
from .views import RoomListView, RoomDetailView, book_room, booking_confirmation

app_name = 'rooms'

urlpatterns = [
    path('', RoomListView.as_view(), name='home'),
    # Aliases for the homepage kept for backward compatibility
    path('home/', RoomListView.as_view(), name='home_page'),
    path('index/', RoomListView.as_view(), name='index'),
    path("rooms/booking/<int:room_id>/", book_room, name="book_room"),
    path(
        "booking/<int:booking_id>/confirmation/",
        booking_confirmation,
        name="booking_confirmation",
    ),
]
