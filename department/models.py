from django.db import models
from event.models import Department


class Fest(models.Model):
    fest_name = models.CharField(max_length=25,primary_key=True)
    department_name = models.ForeignKey(Department,null=True,on_delete=models.CASCADE)
    event_start_date = models.DateField()
    event_end_date = models.DateField()     
    fest_poster = models.ImageField(upload_to='fest_posters/', blank=True)
    def __str__(self):
        return self.fest_name

    
class dEvent(models.Model):
    event_name = models.CharField(max_length=25)
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    event_time = models.CharField(max_length=100)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    event_poster = models.ImageField(upload_to='event_posters/', blank=True)
    event_venue = models.CharField(max_length = 40)
    registration_link = models.URLField(max_length=200, blank=True, null=True)
    fest_name = models.ForeignKey(Fest,null=True,blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.event_name
   