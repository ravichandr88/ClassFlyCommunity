from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('video.urls')),
    path('',include('exam.urls')),
    path('',include('upload.urls')),
    path('',include('pro.urls')),
    path('',include('chatt.urls')),
    path('',include('internship.urls')),
    path('',include('interview.urls')),
    path('',include('fresher.urls')),
    path('',include('call.urls')),
    path('',include('intervideo.urls')),

]
