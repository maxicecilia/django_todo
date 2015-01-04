from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from django_todo.apps.core.views import CurrentTaskView, CompleteTaskView

urlpatterns = patterns(
    '',
    url(r'^$', CurrentTaskView.as_view(), name='home'),
    url(r'create/$', CurrentTaskView.as_view(), name='create_task'),
    url(r'complete/(?P<id>\d+)/$', csrf_exempt(CompleteTaskView.as_view()), name='complete_task'),

    url(r'^admin/', include(admin.site.urls)),
)
