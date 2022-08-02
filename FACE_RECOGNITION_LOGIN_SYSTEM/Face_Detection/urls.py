from django.contrib import admin
from django.urls import path
from . import views
from . views import *
urlpatterns = [
    path('',home,name = "home"),
    path('register/',register,name = 'register'),
    path('login/',login,name = 'login'),
    path('greeting/<face_id>/',Greeting,name='greeting'),
    path('greeting/<face_id>/', views.home2, name='home2'),
    path('greeting/<face_id>/speaktosearch', views.speech, name='speechToText'),
    path('greeting/<face_id>/texttosearch', views.text, name='texttoweb'),
]
