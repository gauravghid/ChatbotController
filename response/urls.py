from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
   path('',  views.input, name='input'),
   url(r'^(?P<inputString>.*)/$', views.getChatbotResponse, name='getChatbotResponse'),
]


