from django.urls import path
from event.views import club_event
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns= [
    path('club_event/',club_event,name ="club_event"),
    path('clubs/', club_list, name='clubs'),
    path('club/<str:club_name>/', club_detail, name='club_detail'),
    path('club/<str:club_name>/<int:event_id>/',event_detail, name='event_detail'),
    path('notices/',notice_view, name='notices'),
    path('notices/delete/<int:notice_id>/', delete_notice, name='delete_notice'),
  


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)