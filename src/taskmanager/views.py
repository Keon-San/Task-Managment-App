from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Task, List

# Create your views here.

def index(request):
	return HttpResponse("Hello, world. You're at the index.")
    
def getList(request):
    task_list = List.objects.filter(name=request.GET.get('name', ''))[0].tasks.all()
    template = loader.get_template('taskmanager/view_list.html')
    context = {
        'list_name': request.GET.get('name', ''),
        'tasks_list': task_list,
    }
    return HttpResponse(template.render(context, request))
    
def getTask(request):
    task = Task.objects.filter(id=request.GET.get('id', ''))[0]
    template = loader.get_template('taskmanager/view_task.html')
    context = {
        'task': task,
    }
    return HttpResponse(template.render(context, request))