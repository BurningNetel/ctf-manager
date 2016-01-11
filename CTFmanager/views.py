from django.http import HttpResponse

# Create your views here.

def events_page(request):
    return HttpResponse('<html><title>CTFman - Events</title></html>')