from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import EventForm, ChallengeForm
from .models import Event, Challenge


@login_required
def home_page(request):
    return render(request, 'home.html')


@login_required
def events_page(request):
    _events = Event.objects.filter(date__gt=timezone.now())
    archive = Event.objects.filter(date__lte=timezone.now())
    return render(request, 'event/events.html', {'events': _events,
                                           'archive': archive})


@login_required
def new_event_page(request):
    form = EventForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('events')
        else:
            return render(request, 'event/add_event.html', {'form': form})
    return render(request, 'event/add_event.html', {'form': EventForm()})


@login_required
def view_event(request, event_id):
    _event = Event.objects.get(pk=event_id)
    return render(request, 'event/event_detail.html', {'event': _event})


@login_required
def new_challenge(request, event_id):
    _event = Event.objects.get(pk=event_id)
    form = ChallengeForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save(for_event=_event)
            return redirect(_event.get_absolute_url())
        else:
            return render(request, 'event/add_challenge.html', {'form': form, 'event': _event})
    return render(request, 'event/add_challenge.html', {'form': ChallengeForm(), 'event': _event})


def challenge_pad(request, event_id, challenge_name):
    _challenge = Challenge.objects.get(name=challenge_name)
    return render(request, 'event/challenge_pad.html', {'challenge': _challenge})
