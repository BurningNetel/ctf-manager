from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.http import HttpResponse


def register_page(request):
    form = UserCreationForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'registration/register.html', {'form': UserCreationForm()})
