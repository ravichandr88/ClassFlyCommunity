from django.urls import path
from . import views


urlpatterns = [
    path('search',views.searchpage),
    path('prologin',views.login_view,name='login_new'),
    path('prohome',views.homepage, name='pro_home'),
    path('profile',views.profile_card),
    path('project',views.project_detail),
    path('prosignup',views.signup),
    path('task',views.run_task) ,
    path('otp_verify',views.otp_verify_view, name='otp_verify'),
    path('resend_otp',views.resend_otp),
    path('logout_pro',views.logout_view),
    path('reset_pro_password',views.forgot_password),   #to request otp
    path('reset_password_pro',views.password_reset,name='password_reset_pro') #to enter password
]