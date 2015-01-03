from django.conf.urls import patterns, include, url
from django.contrib import admin

from django_todo.apps.core.views import CurrentTaskView

urlpatterns = patterns(
    '',
    url(r'^$', CurrentTaskView.as_view(), name='home'),
    url(r'create/$', CurrentTaskView.as_view(), name='create_task'),
    url(r'complete/(\d+)/$', 'django_todo.apps.core.views.complete_task', name='complete_task'),

    url(r'^admin/', include(admin.site.urls)),
)
