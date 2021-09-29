from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, Http404
from django.contrib.auth.models import User
from django.db.models import Q
from interview.models import Prfessional, Fresher, HRaccount
from django.utils import timezone
from fresher.models import ProFrehserMeeting
from intervideo.models import MeetingPurchase


# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TwoGroup, Messages


# class ChatView(TemplateView):
#     template_name = 'chat/chat.html'

@login_required
def index(request):
    user = User.objects.get(username = request.user)
    # Check wether the user is have an Chat group , If not redirect user for professional search page

    if TwoGroup.objects.filter(Q(prof__username = user.username) | Q(fresher__username = user.username)).count() == 0:
        # Check if 
        return HttpResponse('No chatting account found')

    groups = TwoGroup.objects.filter(prof__id = user.id) | TwoGroup.objects.filter(fresher__id = user.id)

    return render(request, 'chat/index.html', {'groups':groups})



def get_img_url(user):
    img_url = ''
    print(user.id,user)
    # get the img_url for the opposite user
    if Prfessional.objects.filter(user = user).count() == 1:
        print('pro')
        img_url = Prfessional.objects.get(user = user).profile_pic

    elif Fresher.objects.filter(user = user).count()  == 1:
        print('fresher')
        img_url = Fresher.objects.get(user = user).profile_pic

    elif HRaccount.objects.filter(user = user).count() == 1:
        print('HRaccount')
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
        # If chat room has not been created, check the profid and fresher_id 
        # Get the meeting booked, check if paid
        #  and create the room.
        found_meet = False
    #Step 1
        profid      = int(room_name.split('_')[0])
        fresherid   = int(room_name.split('_')[1])
        print(profid, fresherid)
    #Step 2
        for i in ProFrehserMeeting.objects.filter(prof__user__id = profid, fresher__user__id = fresherid,paid=True):
            print('loop',i)
            try:
                if i.paid:
                    TwoGroup(prof = i.prof.user, fresher = i.fresher.user,channel_name = room_name).save()
                    found_meet = True
                    break
            except:
                continue

        if not found_meet:
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
        room.prof_lastseen = timezone.now()
        room.save()

        # get the img_url of the opposite person
        oppo_user = room.fresher
        
    elif room.fresher == user:
        user_id = 'fresher'
        room.fresher_lastseen = timezone.now()
        room.save()

        # get the img_url of the opposite person
        oppo_user = room.prof
        
    else:
        print(room.prof, room.fresher, user)
        raise Http404
    
    img_url = get_img_url(oppo_user)    # opponent image url
    
    return render(request, 'chat.html', context={'user':user,'oppo_user':oppo_user,'room_name': room_name,'user_id':user_id,'img_url':img_url,'messages':messages,'room':room})



def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })




def chats(username):
    p_chats = TwoGroup.objects.filter(prof__username = username) 
    f_chats = TwoGroup.objects.filter(fresher__username = username)
    
    # An empty list of Twogroups models
    chats = []

    for i in p_chats:
        print(i.id,i.prof_lastseen)

        try:
            last_chat = i.chats.filter(sender = i.fresher).latest("created_on")
            print(last_chat.id,last_chat.created_on)
            if i.prof_lastseen < last_chat.created_on:
                chats.append({
                    'first_name'    : last_chat.sender.first_name,
                    'message'       : last_chat.message[:40],
                    'time'          : last_chat.created_on,
                    'channel_name'  : last_chat.chatgroup.channel_name
                })
        except:
            continue

# messages sent by opposite person(Professional) when you are Fresher, 
# check whether fresher_lastseen is less than any message sent by professional
    for i in f_chats:
        try:
            print(i)
            print(i.fresher_lastseen, 'two group lastseen')

            last_chat = i.chats.filter(sender = i.prof).latest("created_on")
            
            print(last_chat.created_on,'last_chat.created_on')

            if i.fresher_lastseen < last_chat.created_on:
                    chats.append({
                    'first_name'    : last_chat.sender.first_name,
                    'message'       : last_chat.message[:40],
                    'time'          : last_chat.created_on,
                    'channel_name'  : last_chat.chatgroup.channel_name
                    })
        except:
            continue

    return chats



# function header to check whether username belongs to fresher , profesional and hr for respective navbar options
def usertype(function):
    # @wraps(function)
    def inner(request, *args, **kwargs):
            try:
                # fre,  pro, hra, frepro, prohra, frehra, freprohra

                u_type = ''

                if Fresher.objects.filter(user__username = request.user).count() == 1:
                    u_type = 'fre'

                if Prfessional.objects.filter(user__username = request.user).count() == 1:
                    u_type+='pro'

                if HRaccount.objects.filter(user__username = request.user).count() == 1:
                    u_type+='hra'
                
                request.session['usertype'] = u_type

            except:
                print('Not logged in')

            return function(request, *args,  **kwargs)
            

    return inner
