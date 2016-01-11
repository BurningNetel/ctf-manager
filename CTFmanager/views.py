from django.shortcuts import render


def events_page(request):

    return render(request, 'events.html')
