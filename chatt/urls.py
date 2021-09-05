from django.urls import path

from . import views

urlpatterns = [
    # path('chat/', views.ChatView.as_view(), name='chat'),
    path('index', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
]
