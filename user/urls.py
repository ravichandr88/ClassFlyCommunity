from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

 
urlpatterns = [
		path('signup',views.signup,name='signup'),
    path('login',views.loginview,name='login'),
    path('password_reset',views.password_reset,name='password_reset'),
    path('video',views.videoupload),
    path('',views.home,name='cfhome'),
    path('php',views.php),
    path('eh',views.eh),
    path('ds',views.ds),
    path('sql',views.sql),
    path('java',views.java),
    path('web',views.web),
    path('ml',views.ml),
    path('angular',views.angular),
    path('python',views.python),
    path('home',views.home),
    path('subscribe',views.subsignup),
    path('example',views.example),
    path('logout',views.logout_request,name='logout'),
    path('register',views.webinar),
    path('register_email',views.save_email,name='register_email')
 
    ] 