from django.urls import path
from . import views
 
urlpatterns = [
    path('searchpage',views.search_professional),
    path('f_dashh', views.fresher_dash, name = 'f_dashboard'),
    path('pro/<str:pro>',views.pro_profile),
    path('book/<str:prof>',views.book_interview),
    path('pro_dashboard', views.pro_dash,name = 'pro_dashboard'),
    
]

