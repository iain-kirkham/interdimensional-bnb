"""
URL configuration for bnb_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from rooms.views import RoomListView, RoomDetailView, ProfileView, book_room, booking_confirmation
from bnb_project.views import account_login, account_signup

urlpatterns = [
        path("rooms/", TemplateView.as_view(template_name="rooms/rooms.html"), name="browse_rooms"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path(
        "about/", TemplateView.as_view(template_name="about/about.html"), name="about"
    ),
    path("", RoomListView.as_view(), name="home"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "login/",
        RedirectView.as_view(pattern_name="account_login", permanent=False),
        name="login",
    ),
    path(
        "signup/",
        RedirectView.as_view(pattern_name="account_signup", permanent=False),
        name="signup",
    ),
    path("booking/<int:room_id>/", book_room, name="booking"),
    path("booking/confirmation/<int:booking_id>/", booking_confirmation, name="booking_confirmation"),


    path("accounts/login/", account_login, name="account_login"),
    path('accounts/signup/', account_signup, name='account_signup'),
    path("", include("rooms.urls")),
]
