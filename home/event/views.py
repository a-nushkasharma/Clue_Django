from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Club ,Event

# Create your views here.
def club_event(request):
    return render(request,'club_event.html')

def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'event_page.html', {'clubs': clubs})
def club_detail(request, club_name):
    # Get the specific club
    club = get_object_or_404(Club, club_name=club_name)
    events = Event.objects.filter(department_name=club.department_name).order_by('-event_start_date')
    return render(request, 'club_event.html', {'club': club, 'events': events})

def event_detail(request, club_name, event_id):
    club = get_object_or_404(Club, club_name=club_name)
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event.html', {'club': club, 'event': event})


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})
