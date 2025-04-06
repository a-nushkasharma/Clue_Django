from django import forms
from event.models import Event

class EventForm1(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'event_name',
            'event_start_date',
            'event_end_date',
            'event_time',
            'club_name',
            'event_poster',
            'event_venue',
            'registration_link' 
        ]
        widgets = {
            'event_start_date': forms.DateInput(attrs={'type': 'date'}),
            'event_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

