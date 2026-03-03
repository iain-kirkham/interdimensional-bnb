from django.shortcuts import render
from django.views.generic import ListView
from .models import Room

class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
