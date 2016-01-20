from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


def register_page(request):
    return render(request, 'register.html', {'form': UserCreationForm()})
