from django import forms
from .models import Note, Task

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'larger_goal']
