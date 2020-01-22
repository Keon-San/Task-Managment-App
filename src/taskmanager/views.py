from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import sys

from .models import Task, List, User, Role, Note
from .forms import NoteForm, TaskForm

# Create your views here.

def index(request):
        lists = []
        if request.user.is_authenticated:
                if User.objects.filter(email=request.user.email).count() == 0:
                        newUser = User(email=request.user.email, name=(request.user.first_name + request.user.last_name))
                        newUser.save()
                user = User.objects.filter(email=request.user.email)[0]
                print("found user")
                print(user.roles.all())
                for x in user.roles.all():
                        lists.extend(list(List.objects.filter(team=x.role_team, can_read__lte=x.access_level)))
       
        template = loader.get_template('taskmanager/view_lists.html')
        context = {
                'lists': lists,
                'authed': request.user.is_authenticated,
        }
        return HttpResponse(template.render(context, request))
                
                
def getList(request):
    ourList = List.objects.filter(name=request.GET.get('name', ''))[0]
    can_view = False
    can_add = False
    can_admin = False
    if request.user.is_authenticated:
            user = User.objects.filter(email=request.user.email)[0]
            for x in user.roles.all():
                if x.role_team == ourList.team:
                        if x.access_level >= ourList.can_read:
                                can_view = True
                        if x.access_level >= ourList.can_add:
                                can_add = True
                        if x.access_level >= ourList.can_admin:
                                can_admin = True

    task_list = ourList.tasks.all()
    template = loader.get_template('taskmanager/view_list.html')
    context = {
        'list_name': request.GET.get('name', ''),
        'tasks_list': task_list,
        'authed': request.user.is_authenticated,
        'can_view': can_view,
        'can_add': can_add,
        'can_admin': can_admin,
        'user': user,
    }
    return HttpResponse(template.render(context, request))
    
def getTask(request):
    task = Task.objects.filter(id=request.GET.get('id', ''))[0]
    ourList = task.task_list
    can_view = False
    can_claim = False
    can_admin = False
    if request.user.is_authenticated:
            user = User.objects.filter(email=request.user.email)[0]
            for x in user.roles.all():
                if x.role_team == ourList.team:
                        if x.access_level >= ourList.can_read:
                                can_view = True
                        if x.access_level >= ourList.can_claim:
                                can_claim = True
                        if x.access_level >= ourList.can_admin:
                                can_admin = True

    template = loader.get_template('taskmanager/view_task.html')
    context = {
        'task': task,
        'authed': request.user.is_authenticated,
        'can_view': can_view,
        'can_claim': can_claim,
        'can_admin': can_admin,
        'user': user,
    }
    return HttpResponse(template.render(context, request))

def addNote(request):
        can_claim = False
        if request.method == 'POST':
                ourList = Task.objects.filter(id=request.POST.get('task', ''))[0].task_list
                if request.user.is_authenticated:
                        user = User.objects.filter(email=request.user.email)[0]
                        for x in user.roles.all():
                                if x.role_team == ourList.team:
                                        if x.access_level >= ourList.can_claim:
                                                can_claim = True
                if not can_claim:
                        context = {
                                'authed': request.user.is_authenticated,
                        }

                        template = loader.get_template('taskmanager/denied.html')
                        return HttpResponse(template.render(context, request))
                else:
                        form = NoteForm(request.POST)
                        if form.is_valid():
                                print(form.cleaned_data, sys.stderr)
                                newNote = form.save(commit=False)
                                newNote.poster = User.objects.filter(email=request.user.email)[0]
                                newNote.task = Task.objects.filter(id=request.POST.get("task"))[0]
                                newNote.save()
                                return HttpResponseRedirect('/taskmanager/viewtask?id=' + request.POST.get("task"))
        else:
                ourList = Task.objects.filter(id=request.GET.get('task', ''))[0].task_list
                if request.user.is_authenticated:
                        user = User.objects.filter(email=request.user.email)[0]
                        for x in user.roles.all():
                                if x.role_team == ourList.team:
                                        if x.access_level >= ourList.can_claim:
                                                can_claim = True

                if not can_claim:
                        context = {
                                'authed': request.user.is_authenticated,
                        }

                        template = loader.get_template('taskmanager/denied.html')
                        return HttpResponse(template.render(context, request))
                else:
                        noteForm = NoteForm()
                        
                        context = {
                                'task': request.GET.get('task', ''),
                                'form': noteForm,
                                'authed': request.user.is_authenticated,
                        }

                        template = loader.get_template('taskmanager/add_note.html')
                        return HttpResponse(template.render(context, request))

def addTask(request):
        can_add = False
        if request.method == 'POST':
                ourList = List.objects.filter(name=request.POST.get('list', ''))[0]
                if request.user.is_authenticated:
                        user = User.objects.filter(email=request.user.email)[0]
                        for x in user.roles.all():
                                if x.role_team == ourList.team:
                                        if x.access_level >= ourList.can_add:
                                                can_add = True
                if not can_add:
                        context = {
                                'authed': request.user.is_authenticated,
                        }

                        template = loader.get_template('taskmanager/denied.html')
                        return HttpResponse(template.render(context, request))
                else:
                        form = TaskForm(request.POST)
                        if form.is_valid():
                                newTask = form.save(commit=False)
                                newTask.creator = User.objects.filter(email=request.user.email)[0]
                                newTask.task_list = List.objects.filter(name=request.POST.get('list'))[0]
                                newTask.save()
                                return HttpResponseRedirect('/taskmanager/viewlist?name=' + request.POST.get('list'))
                        else:
                             context = {
                                'authed': False,
                             }

                             template = loader.get_template('taskmanager/denied.html')
                             return HttpResponse(template.render(context, request))   
        else:
                ourList = List.objects.filter(name=request.GET.get('list', ''))[0]
                if request.user.is_authenticated:
                        user = User.objects.filter(email=request.user.email)[0]
                        for x in user.roles.all():
                                if x.role_team == ourList.team:
                                        if x.access_level >= ourList.can_add:
                                                can_add = True

                if not can_add:
                        context = {
                                'authed': request.user.is_authenticated,
                        }

                        template = loader.get_template('taskmanager/denied.html')
                        return HttpResponse(template.render(context, request))
                else:
                        taskForm = TaskForm()
                        
                        context = {
                                'list': request.GET.get('list', ''),
                                'form': taskForm,
                                'authed': request.user.is_authenticated,
                        }

                        template = loader.get_template('taskmanager/add_task.html')
                        return HttpResponse(template.render(context, request))

def deleteNote(request):
        if request.method == 'POST':
                user = User.objects.filter(email=request.user.email)[0]
                note = Note.objects.filter(id=request.POST.get('id', ''))
                can_delete = False
                ourList = Note.objects.filter(id=request.POST.get('id', ''))[0].task.task_list
                if request.user.is_authenticated:
                        for x in user.roles.all():
                                if x.role_team == ourList.team:
                                        if x.access_level >= ourList.can_admin or note.poster == user:
                                                can_delete = True

                if can_delete:
                        note.delete()

                return HttpResponse('')


def deleteTask(request):
        if request.method == 'POST':
                user = User.objects.filter(email=request.user.email)[0]
                task = Task.objects.filter(id=request.POST.get('id', ''))
                can_delete = False
                ourList = Task.objects.filter(id=request.POST.get('id', ''))[0].task_list
                if request.user.is_authenticated:
                        for x in user.roles.all():
                                if x.role_team == ourList.team:
                                        if x.access_level >= ourList.can_admin or task.creator == user:
                                                can_delete = True

                if can_delete:
                        task.delete()

                return HttpResponse('')
