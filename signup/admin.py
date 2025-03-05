from django.contrib import admin
from .models import PasswordReset
from .models import Coordinator

admin.site.register(PasswordReset)
admin.site.register(Coordinator)