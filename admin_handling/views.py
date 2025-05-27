from django.contrib.auth import logout
from signup.models import Coordinator
from event.models import Event,Department
from department.models import Fest,dEvent
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .forms1 import EventForm1
from .forms2 import dEventForm

def create_event(request):
    if "coordinator_name" not in request.session:
        return redirect("coordinator_login")  # Redirect to login if not authenticated

    try: 
        coordinator = Coordinator.objects.get(coordinator_name=request.session["coordinator_name"])

        if coordinator.coordinator_type != "club" or not coordinator.club_name:
             messages.error(request, "You are not authorized to access this page.")

        club_instance = coordinator.club_name
        department_instance = coordinator.department_name  # Get department

    except Coordinator.DoesNotExist:
        return redirect("coordinator_login")

    if request.method == "POST":
        title = request.POST["title"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        time = request.POST["time"]
        venue = request.POST["venue"]
        registration_url = request.POST.get("registration_url", "")
        poster = request.FILES.get("poster")

        Event.objects.create(
            event_name=title,
            event_start_date=start_date,
            event_end_date=end_date,
            event_time=time,
            event_venue=venue,
            event_poster=poster,
            registration_link=registration_url,
            club_name=club_instance,
            department_name=department_instance
        )
        return redirect("coordinator_dashboard")  # Redirect after form submission

    return render(request, "event_creation_form.html")

def create_dept_event(request):
    if "coordinator_name" not in request.session:
        return redirect("coordinator_login")

    try:
        # Get coordinator and ensure they have a department
        coordinator = Coordinator.objects.get(coordinator_name=request.session["coordinator_name"])
        if not coordinator.department_name:
            return render(request, "fest_event_form.html", {"error": "You are not linked to a department."})

        department_name = coordinator.department_name.department_name
        
        # Fetch department and its related fests
        department = Department.objects.get(department_name=department_name)
        fests = Fest.objects.filter(department_name=department)

        if request.method == "POST":
            event_name = request.POST["event_name"]
            event_start_date = request.POST["event_start_date"]
            event_end_date = request.POST["event_end_date"]
            event_time = request.POST["event_time"]
            event_venue = request.POST["event_venue"]
            registration_link = request.POST["registration_link"]
            fest_name = request.POST["fest_name"]

            # Check if fest exists
            fest = None
            if fest_name != "non-fest":
                try:
                    fest = Fest.objects.get(fest_name=fest_name)
                except Fest.DoesNotExist:
                    return render(request, "fest_event_form.html", {"error": "Selected fest does not exist!", "fests": fests})

            # Create the event
            dEvent.objects.create(
                event_name=event_name,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                event_time=event_time,
                fest_name=fest,
                department_name=department,
                event_venue=event_venue,
                registration_link=registration_link,
            )

            return redirect("coordinator_dashboard_dept")

        # Render form with fests dropdown
        return render(request, "fest_event_form.html", {"fests": fests})

    except Exception as e:
        return render(request, "fest_event_form.html", {"error": str(e)})




def events_page1(request):
    if "coordinator_name" not in request.session:
        return redirect("coordinator_login")  # Redirect to login if not authenticated

    try:
        coordinator = Coordinator.objects.get(coordinator_name=request.session["coordinator_name"])
    except Coordinator.DoesNotExist:
        messages.error(request, "Coordinator not found.")
        return redirect("coordinator_login")

    # Determine the coordinator type and fetch corresponding events
    if coordinator.coordinator_type == "club" and coordinator.club_name:
        events = Event.objects.filter(club_name=coordinator.club_name)
    elif coordinator.coordinator_type == "department" and coordinator.department_name:
        events = dEvent.objects.filter(department_name=coordinator.department_name)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("coordinator_login")

    return render(request, "eventspage1.html", {"eve": events, "coordinator": coordinator})

def modify_event(request, event_id):
    if "coordinator_name" not in request.session:
        return redirect("coordinator_login")  # Redirect if not authenticated

    try:
        coordinator = Coordinator.objects.get(coordinator_name=request.session["coordinator_name"])
    except Coordinator.DoesNotExist:
        messages.error(request, "Coordinator not found.")
        return redirect("coordinator_login")

    # Check coordinator type and use the correct form and event model
    if coordinator.coordinator_type == "club" and coordinator.club_name:
        event = get_object_or_404(Event, id=event_id, club_name=coordinator.club_name)
        form_class = EventForm
        template_name = "event_creation_form_modify.html"  # Club coordinators use modifyform1.html
    elif coordinator.coordinator_type == "department" and coordinator.department_name:
        event = get_object_or_404(dEvent, id=event_id, department_name=coordinator.department_name)
        form_class = dEventForm  # Use dEventForm for department events
        template_name = "modifyform2.html"  # Department coordinators use modifyform2.html
    else:
        messages.error(request, "You are not authorized to modify this event.")
        return redirect("eventspage1")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect("eventspage1")  # Redirect to events page after modification
        else:
            print(form.errors)  # Debugging: Print form errors if validation fails

    else:
        form = form_class(instance=event)

    return render(request, template_name, {"form": form, "event": event, "coordinator": coordinator})

def delete_event(request, event_id):
    if "coordinator_name" not in request.session:
        return redirect("coordinator_login")  # Redirect to login if not authenticated

    try:
        coordinator = Coordinator.objects.get(coordinator_name=request.session["coordinator_name"])
    except Coordinator.DoesNotExist:
        messages.error(request, "Coordinator not found.")
        return redirect("coordinator_login")

    # Determine the event type based on the coordinator's type
    if coordinator.coordinator_type == "club" and coordinator.club_name:
        event = get_object_or_404(Event, id=event_id, club_name=coordinator.club_name)
    elif coordinator.coordinator_type == "department" and coordinator.department_name:
        event = get_object_or_404(dEvent, id=event_id, department_name=coordinator.department_name)
    else:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect("eventspage1")

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect("eventspage1")  

    return redirect("eventspage1")
