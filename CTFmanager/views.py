from django.shortcuts import render


def events_page(request):

    return render(request, 'events.html')

def new_event_page(request):

    return render(request, 'add_event.html')