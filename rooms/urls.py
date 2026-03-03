from django.urls import path
from .views import RoomListView, book_room, booking_confirmation

app_name = 'rooms'

urlpatterns = [
    path('', RoomListView.as_view(), name='home'),
    path("<int:room_id>/book/", book_room, name="book_room"),
    path(
        "booking/<int:booking_id>/confirmation/",
        booking_confirmation,
        name="booking_confirmation",
    ),
]
