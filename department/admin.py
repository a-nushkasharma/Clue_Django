from django.contrib import admin
# Register your models here.
from .models import Fest, dEvent

admin.site.register(Fest)
admin.site.register(dEvent)