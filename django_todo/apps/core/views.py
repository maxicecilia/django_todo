from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView

from django_todo.apps.core.forms import TaskForm
from django_todo.apps.core.models import Task


class CurrentTaskView(FormView):
    form_class = TaskForm
    success_url = '/'
    template_name = 'core/current_tasks.html'

    def get(self, request):
        return self._return_tasks()

    def form_valid(self, form):
        form.save()
        return super(CurrentTaskView, self).form_valid(form)

    def form_invalid(self, form):
        return self._return_tasks(form)

    def _return_tasks(self, form=None):
        tasks = Task.objects.pending_tasks()
        return render_to_response(self.template_name,
                                  RequestContext(self.request, {'tasks': tasks, 'form': form, }))


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
