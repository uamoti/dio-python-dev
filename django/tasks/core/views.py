from django.shortcuts import render, HttpResponse
from core.models import Event

# Create your views here.
def list_events(request):
    events = Event.objects.all()
    response = {'events': events}

    return HttpResponse(events)
