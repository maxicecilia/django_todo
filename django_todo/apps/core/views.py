import json
from django.shortcuts import render_to_response

from django_todo.apps.core.models import Task


def current_tasks(request):
    tasks = Task.objects.filter(is_checked=False)
    return render_to_response('core/current_tasks.html', {'tasks': tasks, })
