from django.forms import ModelForm
from django_todo.apps.core.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']
