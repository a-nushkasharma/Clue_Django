from django.shortcuts import render


def home(request):
    return render(request, 'index.html')  # Render the home page

def clubs(request):
    return render(request, 'club_event.html')  # Render the clubs page

def dept_page(request):
    return render(request,"dept_page.html")

def profile(request):
    return render(request, 'profile.html')

def dept(request):
    return render(request, 'dept_page.html')

def event_page(request):
    return render(request, 'event_page.html')

def club_event(request):
    return render(request, 'club_event.html')