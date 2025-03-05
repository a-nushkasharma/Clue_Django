from django.contrib import admin
from .models import Department, Club,Event
# Register your models here.
admin.site.register(Department)
admin.site.register(Club)
admin.site.register(Event)