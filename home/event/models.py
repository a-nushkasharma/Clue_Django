from django.db import models

class Department(models.Model):
    department_name = models.CharField(max_length=25, primary_key=True)
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.department_name

class Club(models.Model):
    club_name = models.CharField(max_length=25, primary_key=True)
    department_name = models.ForeignKey(Department,null=True,on_delete=models.CASCADE)
    club_description = models.TextField()
    club_poster = models.ImageField(upload_to='club_posters/', blank=True)


    def __str__(self):
        return self.club_name
class Event(models.Model):
    event_name = models.CharField(max_length=25)
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    department_name = models.ForeignKey('Department', on_delete=models.CASCADE)
    event_poster = models.ImageField(upload_to='event_posters/', blank=True)
    event_venue = models.CharField(max_length = 40)
    registration_link = models.URLField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.event_name
   