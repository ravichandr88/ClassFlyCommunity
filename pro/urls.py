from django.urls import path
from . import views
from . import projects
 

urlpatterns = [
    path('startpage',views.startpage),
    path('community/v1',views.startpage),
    path('search_now',views.searchpage),
    path('prologin',views.login_view,name='login_new'),
    path('prohome',views.homepage, name='pro_home'),
    path('profile',views.profile_card),
    path('project_now',views.project_detail),
    path('prosignup/<str:type>',views.signup),
    path('task',views.run_task),
    path('otp_verify',views.otp_verify_view, name='otp_verify'),
    path('email',views.email_function, name='emailpage'),
    path('email/otp',views.email_otp, name='email_otp_verify'),
    path('email/otp/resend',views.resend_email_otp),
    path('resend_otp',views.resend_otp),
    path('logout_pro',views.logout_view),
    path('reset_pro_password',views.forgot_password),   #to request otp
    path('reset_password_pro',views.password_reset,name='password_reset_pro'), #to enter password
    path('send_otp/<str:phone>/<str:otp>',views.temp_otp),   #temp url for stuednt door opening porject
    path('search',projects.search),     #Dynamic search page for projects
    path('project',projects.project_review),
    path('videoplayer/<int:video_id>',projects.videoplayer),
    path('dashboard',projects.dashboard)
]