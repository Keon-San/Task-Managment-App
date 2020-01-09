from django.urls import path
from django.conf.urls import include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'taskmanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('viewlist', views.getList, name='viewlist'),
    path('viewtask', views.getTask, name='viewtask'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout')
]