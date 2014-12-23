import json
from django.http import HttpResponse
from django.template import RequestContext, loader

from django_todo.apps.core.models import Task


def current_tasks(request):
    tasks = Task.objects.filter(is_checked=False)
    template = loader.get_template('core/current_tasks.html')
    context = RequestContext(request, {
        'tasks': tasks,
    })
    return HttpResponse(template.render(context))
