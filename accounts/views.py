from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


def register_page(request):
    ucf = UserCreationForm(data=request.POST)
    if request.method == 'POST':
        ucf.save()
    return render(request, 'register.html', {'form': UserCreationForm()})
