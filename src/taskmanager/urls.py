from django.urls import path
from django.conf.urls import include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'taskmanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('viewlist', views.getList, name='viewlist'),
    path('viewtask', views.getTask, name='viewtask'),
    path('addnote', views.addNote, name='addnote'),
    path('addtask', views.addTask, name='addtask'),
    path('addrole', views.giveRole, name='addrole'),
    path('editend', views.editEndDate, name='editend'),
    path('claimtask', views.claimTask, name='claimtask'),
    path('deletenote', views.deleteNote, name='deletenote'),
    path('deletetask', views.deleteTask, name='deletetask'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout')
]
