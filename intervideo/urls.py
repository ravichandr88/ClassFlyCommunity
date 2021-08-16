from django.urls import path, include
from . import views

 

urlpatterns = [

    path('player_now/<int:pfmid>',views.video_player),
    path('hr_dash/<int:id>',views.hr_dashboard),
    path('hr_dash/<int:id>/<str:skill>',views.hr_dashboard),
    path('hr_dash/<int:id>/<str:skill>/<int:status>',views.hr_dashboard), 
    path('hr_dash',views.hr_dashboard),
    path('jobpost',views.jobpost) ,
    path('job/<int:id>',views.jobdetails),
    path('jobs/search',views.job_search),   #Job Search
    path('jobs/search/<str:desig>/<str:city>/<str:salary>',views.job_search),
    path('position/<str:key>',views.autocompleteModel),  #Auto complete api to provide suggesstions for job positions
    path('change/status/<int:id>/<str:status>',views.change_status),
    path('videocalling',views.videocall),
    path('applicants/<int:id>',views.applicants_search), #Applicants can be searched with respect to the same id and skils they have posted job for.
    path('applicants/<int:id>/',views.applicants_search), #Applicants can be searched with respect to the same id and skils they have posted job for.
    path('applicants/<int:id>/<str:skill>',views.applicants_search), #Applicants can be searched with respect to the same id and skils they have posted job for.
    path('invite/<int:fid>/<int:jobid>',views.invite_fresher)  #URL for HR to invite fresher for their JOB

]