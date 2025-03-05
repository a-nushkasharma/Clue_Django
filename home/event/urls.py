from django.urls import path
from event.views import club_event
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns= [
    path('club_event/',club_event,name ="club_event"),
    path('', club_list, name='club_list'),
    path('club/<str:club_name>/', club_detail, name='club_detail'),
    path('club/<str:club_name>/<int:event_id>/',event_detail, name='event_detail'),
    # path('events/', event_list, name='event_list'),
    # path('club/<str:club_name>/events/', club_event_list, name='club_event_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)