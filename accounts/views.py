from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

def register_page(request):
    form = UserCreationForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'register.html', {'form': UserCreationForm()})


def login_page(request):
    return render(request, 'login.html')
