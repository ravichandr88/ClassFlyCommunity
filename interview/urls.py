from django.urls import path
from . import views



urlpatterns = [
    path('applicant',views.student,name= 'student'),    #2nd form for fresher to fill his details, colleg to skills
    path('resume',views.resumeview, name='resume'),
    path('pro/signup',views.prosignup, name= 'professional'),
    path('pro/signup/<int:edit>',views.prosignup, name= 'professional'),
    path('pro/exp',views.proexp),
    path('pro/exp/<int:edit>',views.proexp),
    path('resume/<int:edit>',views.resumeview, name='resume'),
    path('pro/meet',views.prof_initial_meet),   
    path('pro/profile',views.profile_pic),
    path('pro/waiting',views.pro_waiting, name='pro_waiting'),
    path('company',views.company_singup, name = 'company'), 
    path('company/<int:edit>',views.company_singup, name = 'company'), 
    path('hraccount',views.hr_account_creation, name ='hr_account_creation' ),
    path('hraccount/<int:edit>',views.hr_account_creation, name ='hr_account_creation' ),
    path('hridcard',views.hr_id_card, name='hr_id_card'), 
    path('hrprofile',views.hr_profile_pic), 
    path('pro/timetable',views.pro_timetable, name='pro_time_table'),
    path('pro/timetable/<int:edit>',views.pro_timetable, name='pro_time_table'),
    path('pro/bank', views.pro_bank, name = 'banking'),
    path('pro/bank/<int:edit>', views.pro_bank, name = 'banking'),
    path('hr/dashboard',views.hr_dashboard),
    path('hr/waiting',views.hr_waiting, name='hr_waiting') 
    # path('pro/dashboard',views.prof_dashboard,name='pro_dashboard'),
    # path('applicant/dashboard',views.applicant_dashboard)

]