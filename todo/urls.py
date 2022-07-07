"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from account.account import login
from apps.task_list.task_list import TaskList
from apps.task_list.task_lists import TaskLists
from apps.task.task import Task
from apps.task.tasks import Tasks
# from apps.stream.views import stream, send

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', login),
    path('api/task_list/task_list',TaskList.as_view()),
    path('api/task_list/task_lists',TaskLists.as_view()),
    path('api/task/task',Task.as_view()),
    path('api/task/tasks',Tasks.as_view()),
    # path('api/stream',stream),
    # path('api/send', send),
]
