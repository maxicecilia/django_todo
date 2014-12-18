import json
from django.http import HttpResponse
from django_todo.apps.core.models import Task


def current_tasks(request):
    tasks = Task.objects.filter(is_checked=False)
    response = ''
    for task in tasks:
        response += task.description + '<br/>'
    return HttpResponse(response)
