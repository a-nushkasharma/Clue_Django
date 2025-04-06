from django import forms
from department.models import dEvent  

class dEventForm(forms.ModelForm):
    class Meta:
        model = dEvent
        fields = [
            "event_name", 
            "fest_name",  
            "event_time", 
            "event_start_date", 
            "event_end_date", 
            "event_venue", 
            "event_poster", 
            "registration_link",
            "department_name"
        ]
        widgets = {
            "event_name": forms.TextInput(attrs={"class": "w-full p-3 border border-gray-300 rounded-md"}),
            "fest_name": forms.Select(attrs={"class": "w-full p-3 border border-gray-300 rounded-md"}),
            "event_time": forms.TextInput(attrs={"class": "w-full p-3 border border-gray-300 rounded-md"}),
            "event_start_date": forms.DateInput(attrs={"type": "date", "class": "w-full p-3 border border-gray-300 rounded-md"}),
            "event_end_date": forms.DateInput(attrs={"type": "date", "class": "w-full p-3 border border-gray-300 rounded-md"}),
            "event_venue": forms.TextInput(attrs={"class": "w-full p-3 border border-gray-300 rounded-md"}),
            "event_poster": forms.ClearableFileInput(attrs={"class": "w-full p-3 border border-gray-300 rounded-md"}),
            "registration_link": forms.URLInput(attrs={"class": "w-full p-3 border border-gray-300 rounded-md"}),
        }
