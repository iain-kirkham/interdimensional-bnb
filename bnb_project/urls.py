from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from bnb_project.views import account_login, account_signup, home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/login/", account_login, name="account_login"),
    path("accounts/signup/", account_signup, name="account_signup"),
    path(
        "about/", TemplateView.as_view(template_name="about/about.html"), name="about"
    ),
    path("home/", home, name="home"),
    # Rooms app lives under /rooms/
    path("rooms/", include("rooms.urls")),
    # The URL name used in the navbar
    path(
        "browse_rooms/",
        RedirectView.as_view(url="/rooms/", permanent=False),
        name="browse_rooms",
    ),
    # Root URL directs to the home page
    path("", home, name="root_home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
