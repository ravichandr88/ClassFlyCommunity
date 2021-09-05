from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
  
urlpatterns = [
    path('fileurl',views.fileupload),
    path('api/imgurl',views.fileupload),
    path('upload',views.upload),
    path('initiate_upload',views.initiate_upload),
    path('initiate',csrf_exempt(views.initiate)),
    path('url_multi/<int:key>',views.presigned_url_multipart),
    path('upload_raw',views.upload_raw),
    path('complete_upload',views.complete_upload),
    path('signurl/<str:filename>',views.classfly_create_presigned_url),
    path('classfly/initiate_upload',views.classfly_initiate_upload),
    path('classfly/url_multi',views.classfly_presigned_url_multipart), 
    path('classfly/complete_upload',views.classfly_complete_upload),
    path('get_url/<int:id>',views.create_presigned_url)
]