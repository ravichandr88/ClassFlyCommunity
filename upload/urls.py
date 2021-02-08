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
    path('url_multi',views.presigned_url_multipart),
    path('upload_raw',views.upload_raw),
    path('complete_upload',views.complete_upload),
    path('tempurl',views.create_presigned_url) 
]