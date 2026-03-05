from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def account_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    return render(request, 'accounts/login.html', {'form': form})

def account_signup(request):
    return render(request, 'accounts/signup.html')
