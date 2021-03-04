from django.urls import path
from . import views


urlpatterns = [
    path('search',views.searchpage),
    path('pronlogin',views.login),
    path('pronhome',views.homepage),
    path('profile',views.profile_card),
    path('project',views.project_detail),
    path('prosignup',views.signup),
    path('task',views.run_task)  
]