from django.urls import path
from .views import RoomListView

app_name = 'rooms'

urlpatterns = [
    path('', RoomListView.as_view(), name='home'),
]
