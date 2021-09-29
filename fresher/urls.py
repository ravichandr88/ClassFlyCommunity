from django.urls import path
from . import views
 
urlpatterns = [
    path('searchpage',views.search_professional, name='pro_search'),
    path('searchpage/<int:page>',views.search_professional, name='pro_search'), 
    path('f_dashh', views.fresher_dash, name = 'f_dashboard'),
    path('pro/<int:pro>',views.pro_profile), 
    path('book/<str:prof>',views.book_interview),
    path('pro_dashboard', views.pro_dash ,name = 'pro_dashboard'),
    path('fresher/<int:fre>',views.fresher_profile),
    path('reject/<int:mid>',views.reject_meeting),
    path('chat_now/<int:fid>',views.hr_fresher_chat),
    path('hr_fresher_profile/<int:fre>',views.hr_fresher_profile)
	] 


