from django.shortcuts import render, redirect

from .forms import EventForm


def events_page(request):
    return render(request, 'events.html')


def new_event_page(request):
    form = EventForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('events')
    else:
        return render(request, 'add_event.html', {'form': EventForm()})
