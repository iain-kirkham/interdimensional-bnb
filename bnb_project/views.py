from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from rooms.models import Room


def account_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    return render(request, "accounts/login.html", {"form": form})


def account_signup(request):
    return render(request, "accounts/signup.html")


def home(request):
    """Render the homepage with a list of non-collapsing rooms.

    This replaces the previous TemplateView so the `home/index.html`
    template receives a `rooms` context variable used by the template.
    """
    rooms = Room.objects.filter(is_collapsing=False)
    return render(request, "home/index.html", {"rooms": rooms})
