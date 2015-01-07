from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import FormView

from django_todo.apps.core.forms import TaskForm
from django_todo.apps.core.models import Task


class CurrentTaskView(FormView):
    form_class = TaskForm
    success_url = '/'
    template_name = 'core/current_tasks.html'

    def get(self, request):
        return self._return_tasks(self.request.user, TaskForm())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(CurrentTaskView, self).form_valid(form)

    def form_invalid(self, form):
        return self._return_tasks(self.request.user, form)

    def _return_tasks(self, user, form=None):
        tasks = Task.objects.pending_tasks(user)
        return render_to_response(self.template_name,
                                  RequestContext(self.request, {'tasks': tasks, 'form': form, }))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CurrentTaskView, self).dispatch(*args, **kwargs)


class CompleteTaskView(View):
    def post(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(pk=kwargs['id'])
            task.is_checked = True
            task.save()
            return HttpResponseRedirect('/')
        except Task.DoesNotExist:
            raise HttpResponseNotFound("Cant find task id {0}".format(kwargs['id']))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CompleteTaskView, self).dispatch(*args, **kwargs)
