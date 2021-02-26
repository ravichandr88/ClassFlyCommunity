from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf.urls import (
  handler400, handler403, handler404, handler500)

from django.conf.urls import url
from django.http import HttpResponse

# handler404 = views.error404

urlpatterns = [
		# path('signup',views.signup,name='signup'),
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
    path('privacy',views.privacy),
    path('angular',views.angular),
    path('python',views.python),
    path('home',views.home),
    path('signup',views.subsignup,name='signup'),
    path('example',views.example),
    path('logout',views.logout_request,name='logout'),
    path('register',views.webinar,name='register'),
    path('register_email',views.save_email,name='register_email'),
    path('event',views.redirect_event),
    path('resend',views.resend_otp),
    path('renew/<slug:code>',views.session_renew),
    path('home_pro',views.pro_home),
    # path('robots.txt',)
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"), name="robots_file"),
 
    ] 