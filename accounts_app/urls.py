from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('home', views.home, name='home'),


]