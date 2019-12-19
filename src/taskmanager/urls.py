from django.urls import path

from . import views

app_name = 'taskmanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('viewlist', views.getList, name='viewlist'),
    path('viewtask', views.getTask, name='viewtask')
]