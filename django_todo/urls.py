from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'django_todo.apps.core.views.current_tasks', name='home'),
    url(r'create/$', 'django_todo.apps.core.views.create_task', name='create_task'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
