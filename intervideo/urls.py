from django.urls import path, include
from . import views

 

urlpatterns = [

    path('player_now/<int:pfmid>',views.video_player),
    path('player_now',views.video_player),
    path('hr_dash/<int:id>',views.hr_dashboard),
    path('hr_dash/<int:id>/<str:skill>',views.hr_dashboard),
    path('hr_dash/<int:id>/<str:skill>/<int:status>',views.hr_dashboard), 
    path('hr_dash',views.hr_dashboard, name='hrdashboard'),
    path('jobpost',views.jobpost),
    path('jobpost/<int:job_id>/<int:edit>',views.jobpost),
    path('job/<int:id>',views.jobdetails),
    path('jobs/search',views.job_search, name='jobsearh'),   #Job Search
    path('jobs/search/<str:desig>/<str:city>/<str:salary>',views.job_search),
    path('position/<str:key>',views.autocompleteModel),  #Auto complete api to provide suggesstions for job positions
    path('change/status/<int:id>/<str:status>',views.change_status),
    path('videocalling',views.videocall),
    path('applicants/<int:id>',views.applicants_search), #Applicants can be searched with respect to the same id and skils they have posted job for.
    path('applicants/',views.applicants_search), #Applicants can be searched with respect to the same id and skils they have posted job for.
    path('applicants/<int:id>/',views.applicants_search), #Applicants can be searched with respect to the same id and skils they have posted job for.
    path('applicants/<int:id>/<str:skill>',views.applicants_search), #Applicants can be searched with respect to the same id and skils they have posted job for.
    path('invite/<int:fid>/<int:jobid>',views.invite_fresher),  #URL for HR to invite fresher for their JOB
    path('jobs_applied',views.jobs_applied),
    path('jobpost_delete/<int:id>',views.delete_jobpost),     #API call for deleting the jobpost
    path('payment',views.payment),
    path('video_buy/<int:vdo_id>',views.video_buying),
    path('interview_buy/<int:pfmid>',views.purchase_interview) ,
    path('resume_buy/<int:skills>',views.resume_purchase),
    path('paid_service',views.paid_services)
]