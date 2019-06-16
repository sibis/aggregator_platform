from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from store_manager_app.views import create_task, cancel_task, list_tasks, list_task_transactions

urlpatterns = [
    url(r'^create_task/$', create_task, name='create_task'),
    url(r'^cancel_task/$', cancel_task, name='cancel_task'),
    url(r'^list_tasks/$', list_tasks, name='list_tasks'),
    url(r'^list_task_transactions/$', list_task_transactions, name='list_task_transactions')
]