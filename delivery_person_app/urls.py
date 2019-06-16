from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from delivery_person_app.views import list_tasks, decline_task, complete_task, accept_task, priority_task

urlpatterns = [
    url(r'^list_tasks/$', list_tasks, name='list_tasks'),
    url(r'^decline_task/$', decline_task, name='decline_task'),
    url(r'^complete_task/$', complete_task, name='complete_task'),
    url(r'^accept_task/$', accept_task, name='accept_task'),
    url(r'^priority_task/$', priority_task, name='priority_task')
]