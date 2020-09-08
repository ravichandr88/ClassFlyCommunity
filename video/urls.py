from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
	path('about',views.about,name='about-us'),
	path('cfhome',views.home,name='home'),
	path('community',views.community,name='community'),
	path('library',views.lib,name='library'),
	path('default',views.default,name='default'),


    ]