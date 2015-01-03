from django import forms
from django_todo.apps.core.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', ]

    def clean_description(self):
        if self.cleaned_data['description'].lower() == 'nothing':
            raise forms.ValidationError("You can't do nothing!!")

        return self.cleaned_data['description']
