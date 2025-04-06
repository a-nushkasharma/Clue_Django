from django.urls import path,include
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('event/', views.event_page, name='event_page'),
    path('club_event/', views.club_event, name='club_event'),
    path('calendar/', views.calendar_view, name='calendar_view'),
]

