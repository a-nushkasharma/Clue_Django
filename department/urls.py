from django.urls import path
from .views import home, department_fests, fest_detail,  devent_detail
from django.conf import settings
from .import views 
from django.conf.urls.static import static

urlpatterns = [

# Department-wise fests
    path('dept/', home, name='dept'),
    path('department/<str:department_name>/', views.department_fests, name='department_fests'),

    # Specific fest details
    path('department/<str:department_name>/<str:fest_name>/', fest_detail, name='fest_detail'),

    # Standalone event details (without a fest)
    path('department/event/<str:department_name>/<str:event_name>/', views.devent_detail, name='devent_detail'),

    # Specific event in a fest
    path('department/event/<str:department_name>/<str:fest_name>/<str:event_name>/', views.devent_detail, name='devent_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)