from django.urls import path
from .views import create_event, create_dept_event,modify_event,delete_event,events_page1

urlpatterns = [
    path('create_event', create_event, name='create_event'),  # This handles /create-event/
    path('create_dept_event/', create_dept_event, name='create_dept_event'),
  # path('dashboard_events/',events_page1, name="dashboard_events"),
    path('eventspage1/', events_page1, name='eventspage1'), 
    path('delete/<int:event_id>/', delete_event, name='delete_event'),
    path('modify-event/<int:event_id>/', modify_event, name='modify_event'),

]