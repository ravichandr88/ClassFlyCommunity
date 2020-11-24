from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
	path('about',views.about,name='about-us'),
	path('community',views.lib,name='home'),
	path('community/home',views.lib,name='home'),
	path('community/v1',views.lib,name='home'),


	path('communityhome',views.home,name='community'),
	path('community/player/<int:sub>',views.community,name='player'),		#for mobile app
	
	path('community/player/<int:sub>/<int:chp>',views.community,name='player'),# for mobile app
	path('community/player',views.community,name='player'),	#for mobile app
	
	path('player/<int:sub>',views.community,name='player'),
	
	path('player/<int:sub>/<int:chp>',views.community,name='player'),
	path('player',views.communityn,name='player'),
	
	path('library',views.lib,name='library'),
	path('default',views.default,name='default'),
	# path('upload',views.upload),
	path('training.pdf',views.generate_PDF), 
	path('training_details.pdf',views.generate_detailsPDF),
	path('playlist',views.playlist),
	path('videoslist',views.videos_list),
	path('dept_dashboard',views.depthead_dashboard,name='dept_dashboard'),	#link for dept head dashboard
	path('dept_dashboard/<slug:page>',views.depthead_dashboard),
	path('video_upload',views.video_uploader),
	path('videos_list',views.videos_uploaded_list,name='videom_dashboard'),	#link for video maker dashboard
	path('ap_rj_vd',views.approve_reject_video),
	path('reader/<slug:id>',views.reader),	#page for all the pdf's display
	path('notes_upload',views.notes_upload),#page to submit notes
	path('notes_list',views.notes_uploaded_list),  #page to see all the submitted by the user
    path('notes_dept_dash',views.depthead_notes_dashboard), #dashboard for dept head to validate notes uplaoded by video makers
	path('notes_dept_dash/<slug:page>',views.depthead_notes_dashboard), #dashboard for dept head to validate notes uplaoded by video makers
	path('ap_rj_vd_notes',views.approve_reject_notes)
	]
