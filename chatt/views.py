from django.contrib import messages
from django.views.generic import TemplateView

# chat/views.py
from django.shortcuts import render


class ChatView(TemplateView):
    template_name = 'chat/chat.html'

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })