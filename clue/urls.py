from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include  # ✅ Include is necessary
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('signup.urls')),  # ✅ Correct path
    path('home/', include('home.urls')),  # If home is also in signup
    path('',include('home.urls')),
    path('event/',include('event.urls') ),
    path('department/',include('department.urls')),
    path('admin_handling/',include('admin_handling.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)