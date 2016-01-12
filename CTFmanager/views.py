from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Event
from .forms import EventForm


def events_page(request):
    _events = Event.objects.filter(date__gt=timezone.now())
    return render(request, 'events.html', {'events': _events})


def new_event_page(request):
    form = EventForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('events')
    else:
        return render(request, 'add_event.html', {'form': EventForm()})
