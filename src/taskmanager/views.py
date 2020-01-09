from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Task, List, User, Role

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
