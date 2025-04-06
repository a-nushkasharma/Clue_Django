from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from .models import *
from department.models import *
from signup.models import *
from django.utils.timezone import now
from django.contrib import messages
# Create your views here.
def club_event(request):
    return render(request,'club_event.html')

def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'event_page.html', {'clubs': clubs})
def club_detail(request, club_name):
    # Get the specific club
    club = get_object_or_404(Club, club_name=club_name)
    events = Event.objects.filter(club_name=club).order_by('-event_start_date')
    return render(request, 'club_event.html', {'club': club, 'events': events})

def event_detail(request, club_name, event_id):
    club = get_object_or_404(Club, club_name=club_name)
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event.html', {'club': club, 'event': event})

def notice_view(request):
    """Show notices for the respective coordinator (Club/Department)."""

    # Check if the coordinator is logged in
    if "coordinator_name" not in request.session:
        return redirect("coordinator_login")

    try:
        # Fetch the coordinator based on session
        coordinator = Coordinator.objects.get(coordinator_name=request.session["coordinator_name"])
    except Coordinator.DoesNotExist:
        messages.error(request, "Coordinator not found.")
        return redirect("coordinator_login")

    # Determine whether coordinator is for a club or a department
    if coordinator.coordinator_type == "club" and coordinator.club_name:
        notices = Notice.objects.filter(club_name=coordinator.club_name)
    elif coordinator.coordinator_type == "department" and coordinator.department_name:
        notices = Notice.objects.filter(department_name=coordinator.department_name)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("coordinator_login")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # Create a new notice for the respective club/department
        notice = Notice(
            title=title,
            description=description,
            date_posted=now(),
        )

        if coordinator.coordinator_type == "club":
            notice.club_name = coordinator.club_name
        elif coordinator.coordinator_type == "department":
            notice.department_name = coordinator.department_name

        notice.save()
        return redirect("notices")

    return render(request, "notice.html", {"notices": notices, "coordinator": coordinator})

def delete_notice(request, notice_id):
    """Allow a coordinator to delete only their own notices."""

    # Check if the coordinator is logged in
    if "coordinator_name" not in request.session:
        return redirect("coordinator_login")

    try:
        coordinator = Coordinator.objects.get(coordinator_name=request.session["coordinator_name"])
    except Coordinator.DoesNotExist:
        messages.error(request, "Coordinator not found.")
        return redirect("coordinator_login")

    notice = get_object_or_404(Notice, id=notice_id)

    # Ensure the coordinator can delete only their own notices
    if (coordinator.coordinator_type == "club" and notice.club_name != coordinator.club_name) or \
       (coordinator.coordinator_type == "department" and notice.department_name != coordinator.department_name):
        messages.error(request, "You are not authorized to delete this notice.")
        return redirect("notices")

    notice.delete()
    return redirect("notices")
