from django.db import models
from event.models import Department
from event.models import Club
from django.contrib.auth.models import User
import uuid  ##unique id is generated through this for reset password 

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) #each id is unquely generated 
    created_when = models.DateTimeField(auto_now_add=True)  #used to help store timestamp when i was created 

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
    

class Coordinator(models.Model):
    COORDINATOR_TYPES = [
        ('club', 'Club Coordinator'),
        ('department', 'Department Coordinator'),
    ]

    coordinator_name = models.CharField(max_length=25, primary_key=True, null=False, blank=False)
    coordinator_type = models.CharField(max_length=10, choices=COORDINATOR_TYPES, null=False, blank=False)
    
    club_name = models.ForeignKey(Club, on_delete=models.CASCADE, to_field="club_name", null=True, blank=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, to_field="department_name", null=True, blank=True)
    
    email = models.CharField(max_length=25, null=False, blank=False)
    password = models.CharField(max_length=25, null=False, blank=False)
    phone_no = models.CharField(max_length=15, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.coordinator_name} ({self.get_coordinator_type_display()})"