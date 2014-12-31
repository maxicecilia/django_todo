import json
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django_todo.apps.core.forms import TaskForm
from django_todo.apps.core.models import Task


def current_tasks(request):
    tasks = Task.objects.filter(is_checked=False).order_by('-date_created')
    return render_to_response('core/current_tasks.html',
                              RequestContext(request, {'tasks': tasks, 'form': TaskForm(), }))


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            Task.objects.create(description=form.cleaned_data['description'])
            return HttpResponseRedirect('/')
    else:
        return HttpResponseForbidden('Forbidden')
