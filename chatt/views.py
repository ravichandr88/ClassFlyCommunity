from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, Http404
from django.contrib.auth.models import User
from django.db.models import Q
from interview.models import Prfessional, Fresher, HRaccount


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



def get_img_url(user):
    img_url = ''

    # get the img_url for the opposite user
    if Prfessional.objects.filter(user = user).count() == 1:
        img_url = Prfessional.objects.get(user = user).profile_pic

    elif Fresher.objects.filter(user = user).count()  == 1:
        img_url = Fresher.objects.get(user = user).profile_pic

    elif HRaccount.objects.filter(user = user).count() == 1:
        img_url = HRaccount.objects.get(user = user).profilepic
    else:
        return ''
    
    return img_url



# Chating function 
@login_required
def chatting(request, room_name):
    # Fetch user details 
    user = User.objects.get(username = request.user)
    
    
    if TwoGroup.objects.filter(channel_name = room_name).count() == 0:
        raise Http404

    room = TwoGroup.objects.get(channel_name = room_name)

    user_id = ''
    img_url = ''
    oppo_user = ''  #opposite user, later get the img_url
    messages = room.chats.all().order_by('created_on')[:20]
# user position
# try to get the profile pic url for opposite chat
  
    if room.prof == user:
        user_id = 'prof'
        # get the img_url of the opposite person
        oppo_user = room.fresher
        
    elif room.fresher == user:
        user_id = 'fresher'
        oppo_user = room.prof
        
    else:
        print(room.prof, room.fresher, user)
        raise Http404
    
    img_url = get_img_url(oppo_user)    # opponent image url
    self_img_url = get_img_url(user)    #Self image url
    
    return render(request, 'chat.html', context={'self_img_url':self_img_url,'user':user,'room_name': room_name,'user_id':user_id,'img_url':img_url,'messages':messages,'room':room})



def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
