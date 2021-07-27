from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
	
	path('video_prepare/<str:id>',views.video_prepare),
    path('videocall',views.videocall,name= 'videocall'),
	path('audiocall',views.audio_testing),
	path('record/<int:fid>/<int:mid>', views.record),
	path('record', views.record)
	path('play',views.video_play),
	path('pro_join/<int:pid>/<int:mid>',   views.connect_to_call_pro),
	path('pro_joined/<int:mid>/<int:fid>', views.pro_joined),	# call to get into video rrom from waiting room
	path('fre_join/<int:fid>/<int:mid>',   views.connect_to_call_fresh),
	
]