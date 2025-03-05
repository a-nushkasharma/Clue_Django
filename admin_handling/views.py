from django.shortcuts import render, redirect
from event.models import Event
from django.core.files.storage import FileSystemStorage

def create_event(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        time = request.POST["time"]
        venue = request.POST["venue"]
        registration_url= request.POST["registration_url"]
        
        # Handle file upload
        poster = request.FILES.get("poster")
        if poster:
            fs = FileSystemStorage()
            filename = fs.save(poster.name, poster)
            poster_url = fs.url(filename)
        else:
            poster_url = None
        
        # Save data to database
        Event.objects.create(
            event_name=title,
            description=description,
            event_start_date=start_date,
            event_end_date=end_date,
            event_time=time,
            venue=venue,
            poster=poster_url,
            registration_url=registration_url
        )
        return redirect("event_success")  # Redirect after form submission

    return render(request, 'event_creation_form/event_creation_form.html')
def event_success(request):
    return render(request, 'event_success.html')