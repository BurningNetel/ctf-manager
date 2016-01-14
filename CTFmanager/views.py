from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import EventForm
from .models import Event


def home_page(request):
    return render(request, 'home.html')


def events_page(request):
    _events = Event.objects.filter(date__gt=timezone.now())
    return render(request, 'events.html', {'events': _events})


def new_event_page(request):
    form = EventForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('events')
        else:
            return render(request, 'add_event.html', {'form': form})
    return render(request, 'add_event.html', {'form': EventForm()})


def view_event(request, event_id):
    _event = Event.objects.get(pk=event_id)
    return render(request, 'event_detail.html', {'event': _event})


def new_challenge(request, event_id):
    _event = Event.objects.get(pk=event_id)
    return render(request, 'add_challenge.html', {'event': _event})
