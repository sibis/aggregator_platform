from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from authentication.views import signup, login, test, logout

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^test/$', test, name='test'),
    url(r'^logout/$', logout, name='logout')
]