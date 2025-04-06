from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import  Fest, dEvent
from event.models import Department
from event.models import Event
from django.contrib.auth.decorators import login_required

# Home page - Lists all departments
def home(request):
    departments = Department.objects.all()
    return render(request, 'page_01.html', {'departments': departments})

# List of fests under a department
def department_fests(request, department_name):
    department = get_object_or_404(Department, department_name=department_name)
    
    # Fetch all fests under this department
    fests = Fest.objects.filter(department_name=department)
    
    # Fetch standalone events (events with no fest)
    standalone_events = dEvent.objects.filter(department_name=department, fest_name__isnull=True)

    return render(request, 'department_detail.html', {
        'department': department,
        'fests': fests,
        'standalone_events': standalone_events  # Pass standalone events to the template
    })

def fest_detail(request, department_name, fest_name):
    try:
        department = get_object_or_404(Department, department_name=department_name)
        fest = get_object_or_404(Fest, fest_name=fest_name, department_name=department)
        
        # Fetch events related to the fest
        events = dEvent.objects.filter(fest_name=fest)

        return render(request, 'fest_detail.html', {
            'department': department,
            'fest': fest,
            'events': events  # Empty if no events exist
        })
    except (Department.DoesNotExist, Fest.DoesNotExist):
        return HttpResponse("Fest not found", status=404)


# Event detail view

def devent_detail(request, department_name, fest_name=None, event_name=None):
    department = get_object_or_404(Department, department_name=department_name)

    if fest_name == "None":  # Convert 'None' (string) to actual NoneType
        fest_name = None

    if fest_name:
        fest = get_object_or_404(Fest, fest_name=fest_name, department_name=department)
        event = get_object_or_404(dEvent, event_name=event_name, fest_name=fest)
    else:
        event = get_object_or_404(dEvent, event_name=event_name, department_name=department, fest_name__isnull=True)
        fest = None

    return render(request, 'event.html', {'department': department, 'fest': fest, 'event': event})
