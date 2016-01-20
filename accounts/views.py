from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register_page(request):
    form = UserCreationForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'register.html', {'form': UserCreationForm()})
