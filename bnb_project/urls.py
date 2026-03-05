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
from rooms.views import ProfileView

urlpatterns = [
        path("rooms/", TemplateView.as_view(template_name="rooms/rooms.html"), name="browse_rooms"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('about/', TemplateView.as_view(template_name='about/about.html'), name='about'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', RedirectView.as_view(pattern_name='account_login', permanent=False), name='login'),
    path('signup/', RedirectView.as_view(pattern_name='account_signup', permanent=False), name='signup'),

    # All room-related URLs live here
    path("", include("rooms.urls")),
]
