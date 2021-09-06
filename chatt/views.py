from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TwoGroup, Messages


# class ChatView(TemplateView):
#     template_name = 'chat/chat.html'

@login_required
def index(request):
    user = User.objects.get(username = request.user)
    print(request.session.session_key)
    # Check wether the user is have an Chat group , If not redirect user for professional search page
    if TwoGroup.objects.filter(Q(prof__username = user.username) | Q(fresher__username = user.username)).count() == 0:
        return HttpResponse('No chatting account found')

    groups = TwoGroup.objects.filter(prof__id = user.id) | TwoGroup.objects.filter(fresher__id = user.id)

    return render(request, 'chat/index.html', {'groups':groups})



def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
