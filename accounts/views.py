from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse


def register_page(request):
    form = UserCreationForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'register.html', {'form': UserCreationForm()})


def login_page(request):
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username,
                            password=_password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': AuthenticationForm()})
