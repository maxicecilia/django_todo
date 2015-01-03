import json
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext

from django_todo.apps.core.forms import TaskForm
from django_todo.apps.core.models import Task


def current_tasks(request):
    tasks = Task.objects.pending_tasks()
    return render_to_response('core/current_tasks.html',
                              RequestContext(request, {'tasks': tasks, }))


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            tasks = Task.objects.pending_tasks()
            return render_to_response('core/current_tasks.html',
                                      RequestContext(request, {'tasks': tasks, 'form': form, }))
    else:
        return HttpResponseForbidden('Forbidden')


def complete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(pk=task_id)
            task.is_checked = True
            task.save()
            return HttpResponseRedirect('/')
        except:
            raise HttpResponseNotFound("Cant find task id {0}".format(task_id))
    else:
        return HttpResponseForbidden('Forbidden')
