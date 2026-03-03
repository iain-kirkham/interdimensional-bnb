from django.urls import path
from .views import RoomListView, RoomDetailView, book_room, booking_confirmation

app_name = 'rooms'

urlpatterns = [
    path('', RoomListView.as_view(), name='home'),
    path('home/', RoomListView.as_view(), name='home_page'),
    path('index/', RoomListView.as_view(), name='index'),
    path('<int:pk>/', RoomDetailView.as_view(), name='detail'),
    path("<int:room_id>/book/", book_room, name="book_room"),
    path(
        "booking/<int:booking_id>/confirmation/",
        booking_confirmation,
        name="booking_confirmation",
    ),
]
