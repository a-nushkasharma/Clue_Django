from django.urls import path
from .views import home, department_fests, fest_detail,  event_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dept/', home, name='dept'),
# Department-wise fests
    path('department/<str:department_name>/fests/', department_fests, name='department_fests'),
    
    # Specific fest details
    #path('department/<str:department_name>/fest/<str:fest_name>/', fest_detail, name='fest_detail'),
    #path('department/<str:department_name>/<str:fest_name>/', fest_detail, name='fest_detail'),
    
    # List of events in a fest
    path('department/<str:department_name>/fest/<str:fest_name>/events/', fest_detail, name='fest_detail'),
    
    # Specific event details
    path('department/<str:department_name>/fest/<str:fest_name>/event/<str:event_name>/', event_detail, name='event_detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)