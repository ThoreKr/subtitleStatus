﻿from django.urls import reverse_lazy, path, re_path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.conf import settings
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.start, name='home'),
    path('event/<slug:acronym>/', views.event, name='event'),
    path('event/<slug:acronym>/day/<int:day>', views.event, name='event'),
    path('event/<slug:acronym>/day/<int:day>/lang/<str:language>', views.event, name='event'),
    path('talk/<int:id>/', views.talk, name='talk'),
    path('talk/frab-id/<int:frab_id>/', views.talk_by_frab),
    path('talk/guid/<uuid:guid>/', views.talk_by_guid),
    path('subtitle/<int:id>/', views.updateSubtitle, name='subtitle'),
    path('speaker/<int:speaker_id>/', views.speaker, name="speaker"),
    path('statistics/talks/', views.statistics_talks),
    path('statistics/speakers/', views.statistics_speakers),
    path('statistics/speakers_in_talks/', views.statistics_speakers_in_talks),
    re_path('^workflow/transforms/(?P<subtitle_id>[0-9]+)/(?P<next_ids>[0-9]+(,[0-9]+)*)?$', views.text_transforms_dwim, name='workflowTransforms'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
