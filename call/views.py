from django.shortcuts import render
from django.utils import timezone
import requests 
import json
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import RecordingUid
from chatt.models import MeetingChat, MeetingMessages
# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,Http404
from django.http import FileResponse
import os
from rest_framework.decorators import api_view
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from video.models import DeptHead,Book,Playlist,Subject,VideoMaker,VideosMade,VideoId,VideoDeptHead,Subject,EducationDomain,Department
from rest_framework.response import Response
import json
import boto3
from botocore.client import Config

from fresher.models import ProFrehserMeeting, Meeting, MeetingActive
from interview.models import Prfessional, Fresher
from .forms import MeetingFeedbackForm
# from .models import 

# Contains one SMS call REST API
# line no. 338, 278
from agora.src.RtcTokenBuilder import *
import time
import random

DEBUG = True

#  connect_to_call_fresh -> have External RESt API

'''
To connect to meeting,
Professional has to connect from waiting room by clicking the "join" button.
Fresher Meeting room will be chekcing server every 20 sec, to check whether professional has joined the meeting or not.
Fresher will recieve SMS when professional joins the meeting.
And if the fresher has been in waiting room, the page will automatically forward to the meeting room.


Recording steps:
When professional joins the meeting, the server will trigger the get resourceID api.
When Professional call, the "Meeting" object will be updated for 'pro_joined'.

When Fresher join the meeting room , the "Meeting" objects 'fre_joined' will be updated.
When Fresher connect to call, recording api will be called and then join the call.

Step 1: def video_prepare(request,id=''): -> called by both Fre, Pro.
Step 2: def videocall(request): -> Pro will connect directly by button.
Step 3: def pro_joined(request,mid,fid): -> called by Fresher from waiting room, and get recording resource id.
Step 4: def videocall(request): -> Fresher will connect to this meeting room automatically
Step 5: def connect_to_call_pro(request,pid,mid): -> Pro connecting to . Created MeetingActive object
Step 6: def connect_to_call_fresh(request, fid, mid): -> Fresher to connect to call and start recording.
Step 7: Disconnect Pro,
Step 8: Disconnect Fresher.
Step 9: Wait till the meeting recorded is saved  to s3
Step 10: Upload s3 videos to vdocipher
Step 11: Show the video once for the Fresher.


'''

# Waiting room
def video_prepare(request,id=''):

    # The first part of id will be the category fresher 'f' or professional 'p'
    categ = id.split('_')[0]

    id = id.split('_')[1]

    if categ == 'p':
        print('line 79 It is not time yet')
        request.session['category'] = 'p'
        waiting_room = False        #Professional should not wait unitll it is time
    else:
        print('Fresher has to wait till time')
        request.session['category'] = 'f'
        waiting_room = True         #Fresher has to wait untill the Professional joines the meeting

    # print(categ)

    request.session['meeting'] = id

    
    # Check if the given id is present in the meeting table or not
    if ProFrehserMeeting.objects.filter(id=id).count() != 1:
        raise Http404

    meeting = ProFrehserMeeting.objects.get(id=id)

    if Meeting.objects.filter(meeting__id = meeting.id).count() == 0:
        print('Meetig  details ')
        Meeting( meeting  = meeting).save()


    remain = meeting.date_time

    now    = timezone.now()

    
    return render(request,'waitingroom.html',context={'remain':remain,'now':now,'waiting':waiting_room,'mid':meeting.id,'fid':meeting.fresher.id})


#final video call work
def videocall(request):    

    # If the request is from professional , he can join
    # If the request is from fresher, he can join after the professional has joined

    print(request.session.keys())    
    user = ''
    uid = ''

    if ProFrehserMeeting.objects.filter(id=request.session['meeting']).count() == 0:
        raise Http404

    # print(request.session.get('meeting'))

    meeting = ProFrehserMeeting.objects.get(id=request.session['meeting'])


    
    if Prfessional.objects.filter(id =  meeting.prof.id).count() == 1 and request.session['category'] == 'p':
        user = 'prof'
        print(user)

    elif Fresher.objects.filter(user__username = request.user).count() == 1 and request.session['category'] == 'f':
        user = 'fresher'

    

    else:
        raise Http404
    
    meet_details = Meeting.objects.get(meeting_id = meeting.id)


# Code to estimate the time with respect to skills
    
    
    g = meeting.date_time
    g = g + timedelta( minutes = 20 ) 

    
    
    # If the current time is greater than meeting start time and 
    # less than 2 hours of meeting start time, you can join
    # print(timezone.now() > meeting.date_time   , timezone.now() > g , not meeting.meeting_details.record_stopped)
    if not(timezone.now() > meeting.date_time   and not(timezone.now() > g) and not meeting.meeting_details.record_stopped) :
    
        if request.session['category'] == 'f':
            print('line 159 f_dashboard redirect')
            return redirect('f_dashboard')
           
        else:
            print('line 162from video call views')
            return redirect('pro_dashboard')
          


    # If the user oif fresher , check whether the professional has joined or not.
    if request.session['category'] == 'f' and not(meet_details.pro_joined) :
        # default varibel to pass the html page
        # if professional has not joined, then redirect to waiting room
        remain = timezone.now()
        now    = timezone.now()

        waiting_room = 'True' # Which supoorts te decision to make sure we call server evry 30 seconds to know whether the professional have joined the meeting or not.
       
        return render(request,'waitingroom.html',context={'title':'Please wait for Professional to Join','remain':remain,'now':now,'waiting':waiting_room,'mid':meeting.id,'fid':meeting.fresher.id})




    # print(meeting.channel_name)

    appID = "e73019d92f714c95b9bc47ea63de404c"
    appCertificate = "ed36762fba3f4e42acaf99c6265ec4c3"
    channelName = meeting.channel_name
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds
    uid = random.randrange(22222222,99999999)

    record_uid = RecordingUid.objects.get(meeting = meeting) if RecordingUid.objects.filter(meeting = meeting).count() == 1 else RecordingUid(pro_uid = int(str(uid) + str(meeting.prof.id))%10000000,fresh_uid = int(str(uid) + str(meeting.fresher.id))%10000000,meeting = meeting)
    record_uid.save()

    if user == 'prof':

        uid = record_uid.pro_uid
        
        # Create MeetingActive table object
        if MeetingActive.objects.filter(meeting = meeting).count() == 0:
            MeetingActive(meeting = meeting).save()

    else: 
        uid =   record_uid.fresh_uid

    token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, Role_Attendee, privilegeExpiredTs)

# check meetingchat , and create chat if does not exists , or get the one
    meetchat    = MeetingChat.objects.get_or_create(meeting = meeting, channel_name = str(meeting.prof.id) + '_' + str(meeting.fresher.id))[0] 
    chats       = meetchat.meeting_chats.all()

    data = {
    'token'         : token,
    'appid'         : appID,
    'channel'       : channelName,
    'meeting_uid'   : int(uid),
    'uid'           : meeting.prof.id if user == 'prof' else meeting.fresher.id,
    'meet'          : meeting,
    'status'        : meet_details,
    'user'          : user,
    'pro'           : True if user == 'prof' else False,    
    'aid'           : 'p' if user == 'prof' else 'f',
    'mid'           : meeting.meeting_status.id,
    'pfmid'         : meeting.id,
    #Code the auto connect the user, if disconnected for any reason 
    'auto_connect'  : False ,
    # attributes related to chatting
    'room_name'     : meetchat.channel_name,
    'user_id'       : meeting.prof.user.id if user == 'prof' else meeting.fresher.user.id,
    'user_name'     : meeting.prof.user.first_name if user == 'prof' else meeting.fresher.user.first_name,
    'oppo_user_name' : meeting.prof.user.first_name if user == 'fresher' else meeting.fresher.user.first_name, 
    'oppo_user_id'  : meeting.prof.user.id if user == 'fresher' else meeting.fresher.user.id,
    'user_pic'      : meeting.prof.profile_pic if user == 'prof' else meeting.fresher.profile_pic,
    'oppo_user_pic' : meeting.prof.profile_pic if user != 'fresher' else meeting.fresher.profile_pic,
    'chats'   : chats
    }

    print('line 218===',data['auto_connect'])

    # return render(request,'videocall/call.html',context = data)

    return render(request,'videocall.html',context = data)


# API call for professional to inform about  joining  the meeting
@csrf_exempt
@api_view(['GET'])
def connect_to_call_pro(request,pid,mid):

    if Prfessional.objects.filter(id = pid).count() == 0:
        return Response(data={'message':'Not valid Professional'}, status=404)

    pro = Prfessional.objects.get(id = pid)

    profremeeting = ProFrehserMeeting.objects.get(id = mid, prof__id = pid)

    
    if ProFrehserMeeting.objects.filter(id = mid, prof__id = pid).count() == 0:
        return Response(data={'message':'Not valid Meeting'}, status=404)

    meeting = ProFrehserMeeting.objects.get(id = mid, prof__id = pid).meeting_details
    fresher = profremeeting.fresher
    # print(meeting) 

    meeting.pro_joined = True
    meeting.save()

    
    # code to send SMS for the Fresher to inform Professional have joined the meeting
    # please uncomment sms here
    # requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=26&type=text&contacts={}&senderid=SOFTEC&msg=ClassFly+Interview+Meeting+has+been+started,+please+login+and+connect+to+meeting.".format(fresher.user.userphone.phone_number))
    

    return Response(data={'message':'joined'})



# function called by fresher to know whether the professional has joinde the meeting or not
@csrf_exempt
@api_view(['GET'])
def pro_joined(request,mid,fid):
    
    if ProFrehserMeeting.objects.filter(id = mid,fresher__id = fid).count() == 0:
        return Response(data={'message':'Not valid meeting '}, status = 400)

    meeting = ProFrehserMeeting.objects.get(id = mid, fresher__id = fid).meeting_details
    print('Line 274', meeting.pro_joined, not meeting.record_stopped)
    if meeting.pro_joined and not meeting.record_stopped :
        # Code to get agora record resource ID
        pro_meeting = ProFrehserMeeting.objects.get(id=mid, fresher__id = fid)

        # REST API for calling the resouceID for the recording

        resp = record_resource_id(pro_meeting)
        print('line 274==','got resource id',resp)

        if str(resp.status_code) != '200':
            print(resp.content, resp)
            return Response(data={'message':resp.json()['reason']})

        return Response(data={'message':'joined'})

    else:
        return Response(data={'message':'Not yet'})


# Function to connect Fresher for video call, 
# to record about their joining to the meeting
# And get the resource id for connecting to video call
@csrf_exempt
@api_view(['GET'])
def connect_to_call_fresh(request, fid, mid, host=''):
    print("line 291 ==, Start record")
       
    if ProFrehserMeeting.objects.filter(id=mid).count() == 0:
        return Response(data={'message':'Not valid registration'}, status= 400)
    pro_meeting = ProFrehserMeeting.objects.get(id=mid, fresher__id = fid)
    meeting = pro_meeting.meeting_details


    # End of code for the REST API resourceID code
    
    if meeting.pro_joined and not meeting.record_stopped:
        
        pro_meeting.meeting_details.record_start_time = timezone.now() 
        pro_meeting.meeting_details.save()

        if host == 'classfly':       #varible to activate and deactivate the code while testing
            resp = start_record_api(pro_meeting)

            if str(resp.status_code) != '200':
                meeting_error_email(pro_meeting,resp)
                return Response(data={'message':resp.json()['reason']})
            
            # Before we start the meeting, save the record start time and fix the end time too.
            
            meeting.sid = resp.json()['sid']
            meeting.record_started = True
            meeting.fre_joined = True
            meeting.save()
            print('meeting record started and saved to db')
            # Returning time in seconds for the js to count down
            # print((g - meeting.date_time ).total_seconds())

        skills_time = len(pro_meeting.skills.split(',')) + 1 #The last + 1 is for interaction apart from the topics
        # record end time is addition of 10 * skills minutes and + 1 for other discussion.

        pro_meeting.meeting_details.record_stop_time = pro_meeting.meeting_details.record_start_time + timedelta( minutes = skills_time*10) # Each skill has given equal 10 minutes time for interview
        pro_meeting.meeting_details.save()

        time = int(((pro_meeting.meeting_details.record_start_time + timedelta( minutes = skills_time*10 ) ) - timezone.now()).total_seconds())
        # print(skills_time, time) 
        
        return Response(data={'message':'joined','time':time}) 
    
    else:

        return Response(data={'message':'Not right time'}, status= 400)


# @csrf_exempt
# @api_view(['GET'])
# def start_record(request,fid,mid):


#     if ProFrehserMeeting.objects.filter(id = mid, fresher__id = fid).count() == 0 :
#         return Response(data={'message':'Not a Meeting and Fresher'}, status= 400)
        
#     # Start recording 
#     meeting = meeting.objects.get(id = mid, fresher__id = fid)
    


#     if str(res.status_code) != '200':
#         print(res.json())    
#         meeting_error_email(meeting,res)
        
#         return Response(data={'message':'Sorry, There was an error. We have contacted Admin'}, status= 400)

#     return Response(data={'message':'Recording Started'})






# function to provide html page for recording
# mid -> meeting ID(ProFrehserMeeting), fid -> Fresher id
def record(request,fid=0,mid=0):
    
    if ProFrehserMeeting.objects.filter(id=mid,fresher__id = fid).count() == 0:
        # print(fid,mid)
        raise Http404

    meeting = ProFrehserMeeting.objects.get(id=mid)
    # recording uid details for prfesional and fresher
    if RecordingUid.objects.filter(meeting = meeting).count() == 0:
        raise Http404

    record_uid = RecordingUid.objects.get(meeting = meeting)

    

    appID = "e73019d92f714c95b9bc47ea63de404c"
    appCertificate = "ed36762fba3f4e42acaf99c6265ec4c3"
    channelName = meeting.channel_name
    uid = random.randrange(10000000,20000000)
    # userAccount = str(uid)
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds


    token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, Role_Attendee, privilegeExpiredTs)

    data = {
            'token' : token,
            'appid': appID,
            'channel': channelName,
            'uid': uid,
            'aid':  'r',
            'mid':  meeting.meeting_status.id,  #MeetingActive table id
            'pfmid': meeting.id, #ProFreshMeeting id ,
            'pro_uid': record_uid.pro_uid,
            'fresh_uid':record_uid.fresh_uid,
            'skills':meeting.skills.replace("'",'').split(',')
            }
    
    # return render(request, 'videocall/record.html', context= data)
    return render(request,'recording_update.html', context = data)



# check whether the meeting is going on 
@csrf_exempt
@api_view(['GET'])
def meeting_status(request,aid, mid, pfmid,t = 0): # aid (account id) -> Professional 'p', Fresher 'f' or recorder 'r' id, mid ->  MeetingActive id
    
    if MeetingActive.objects.filter(id = mid).count() == 0 or ProFrehserMeeting.objects.filter(id = pfmid).count() == 0:
        
        meeting_error_email( '' , '' , 'Recording Error Function No MeetingStatus Object found aid {} mid {} pfmid {}'.format(aid,mid,pfmid) )

        return Response(data={'message':'Not available'}, status= 400)
    
    # First check whether the meeting was supposed to be stopped or not


    meeting = MeetingActive.objects.get(id = mid)

    if aid == 'p':      # aid -> professional page is calling
        meeting.prof = meeting.prof + 1

    elif aid == 'f':    #aid ->  fresher page is calling
        meeting.fres = meeting.fres + 1

    elif aid == 'r':    #rid -> recording page is calling
        meeting.record = meeting.record + 1

    else:
        meeting_error_email( '' , '' , 'Not related to any team ,aid->{} '.format(aid) )

        return Response( data={'message':'Not related to anything team '}, status = 400 )
    
    try:
        # Code to check whether the time is over for the meeting
        if  timezone.now() > meeting.record_stop_time:
            return Response(data={'message':'stop'})
    except:
        pass
    meeting.save() 

    data={
        'message':'success',
        'pro':meeting.prof, 
        'fres': meeting.fres, 
        'record':meeting.record }

    # For professional , time is sent from here. After fresher is joined to meeting
    
    pro_meeting = ProFrehserMeeting.objects.get(id = pfmid)
    
    if t != 0 and pro_meeting.meeting_details.fre_joined:
        

        # skills_time = len(pro_meeting.skills.split(',')) + 1 #The last + 1 is for interaction apart from the topics
        # # record end time is addition of 10 * skills minutes and + 1 for other discussion.

        # pro_meeting.meeting_details.record_stop_time = pro_meeting.meeting_details.record_start_time + timedelta( minutes = skills_time*10) # Each skill has given equal 10 minutes time for interview
        # pro_meeting.meeting_details.save()

        

        time = int((pro_meeting.meeting_details.record_stop_time - timezone.now()).total_seconds())

        data['time'] = time
    
        

    return Response(data = data )


# to test the audio recording for aws s3 agora recording
def audio_testing(request):
    return render(request,'audio.html',context={})


# to test the video playing from dacast
def video_play(request):
    return render(request,'dacast.html',context={})



# Complete REST API codes


# Call to get resource ID for Recording Meeting
# Called when fresher pinged to know the status of Professional joined the meeting or not
# 
def record_resource_id(pro_meeting):
    
    url = "https://api.agora.io/v1/apps/e73019d92f714c95b9bc47ea63de404c/cloud_recording/acquire"

    data = { 
    "cname": pro_meeting.channel_name,
    "uid": '39690211',
    "clientRequest":{
    "resourceExpiredHour": 24,
    "scene": 1
    }
    }

        

    headers = {'Content-type': 'application/json;charset=utf-8',
            'Authorization': 'Basic NWYzZWZhMTM4MTY4NDM3MThkMDc0OTI1ZWI3MzBlM2M6YWQ1NTVjODIzYTA3NGZmMGE4NDhiZjY3NjdmMDgwNDY='          
    }

    resp = requests.post(url=url,data=json.dumps(data),headers=headers)

    meeting = pro_meeting.meeting_details
    
    # For live working production mode uncomment the below line
    meeting.resource_id = resp.json()['resourceId']
    # meeting.resource_id = 'testingnow'

    meeting.save()
    return resp


# Function to send email if any error before the meeting
def meeting_error_email(meeting,resp,message=''):
    # print(meeting,resp,message)
    if resp != '' :
        subject = 'Error From ClassFly meeting'
        message = f'Could not record the meeting .' + str(meeting.dict()) + str(resp.json())
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['ravichandrareddy88@gmail.com', ]
        send_mail( subject, message, email_from, recipient_list )
    else:
        subject = 'Error From ClassFly recording'
        message = f'Could not record the meeting .' + str(meeting.dict()) + message
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['ravichandrareddy88@gmail.com', ]
        send_mail( subject, message, email_from, recipient_list )


def start_record_api(pro_meeting):
        
    # return 
    


    url = 'https://api.agora.io/v1/apps/e73019d92f714c95b9bc47ea63de404c/cloud_recording/resourceid/' + pro_meeting.meeting_details.resource_id + '/mode/web/start'
    

    
    data = {
    "cname":pro_meeting.channel_name,
    "uid":'39690211',
    "clientRequest":{
        "token": "006e73019d92f714c95b9bc47ea63de404cIADVMPOGFws086UlSkWOq1HVa79tc6nmik3Gi15gOgZDVJ3mPXeby/NFIgCCVCMBAGbdYAQAAQCQItxgAgCQItxgAwCQItxgBACQItxg",
        "extensionServiceConfig": {
            "errorHandlePolicy": "error_abort",
            "extensionServices":[{ 
                    "serviceName":"web_recorder_service",
                    "errorHandlePolicy": "error_abort",
                    "serviceParam": {  
                        "url": "https://www.classfly.in/record/" + str( pro_meeting.fresher.id ) + '/' + str( pro_meeting.id ),
                        # "url": "https://www.classfly.in/record",
                        "audioProfile":0,
                        "videoWidth":1280,
                        "videoHeight":720,
                        "maxRecordingHour":2,
                        "readyTimeout": 60
                }
            }]
        },
        "recordingFileConfig":{
            "avFileType":[
                "hls",
                "mp4"
            ]
        },
        "storageConfig":{
            "vendor":1,
            "region":14,
            "bucket":"classfly",
            "accessKey":"AKIAS6UIIOP5B476WEOF",
            "secretKey":"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",
            "fileNamePrefix":[
                "directory1",
                "directory7"
            ]
        }
    }
    }



    headers = {'Content-type': 'application/json;charset=utf-8',
            'Authorization': 'Basic NWYzZWZhMTM4MTY4NDM3MThkMDc0OTI1ZWI3MzBlM2M6YWQ1NTVjODIzYTA3NGZmMGE4NDhiZjY3NjdmMDgwNDY='
            
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)

    print('line 560 == ',res)

    return res



def record_file_exists(key = ''):


    s3 = boto3.resource("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))
    bucket = s3.Bucket('classfly')

    if key =='' or key == '.mp4':
        return 'Wrong key'

    

    objs = list(bucket.objects.filter(Prefix=key))
    if len(objs) > 0 and objs[0].key == key:
        print('line 617 ==',"Exists!")
        return 'Found'

    else:
        print('line 581==',"Doesn't exist")
        return 'Not Found'



# Code to start to upload video from s3 to VDO
def upload_s3video(file):

        
    url = "https://dev.vdocipher.com/api/videos/importUrl"

    payload = json.dumps({"url":"https://classfly.s3.ap-south-1.amazonaws.com/" + file })
    
    headers = {    
        'Authorization': "Apisecret " + settings.VDO_API,  
        'Accept': "application/json",    
        'Content-Type': "application/json"    
        }

    response = requests.request("PUT", url, data=payload, headers=headers)

    return response



def upload_vdo_status(vdo_id):
    
    url = "https://dev.vdocipher.com/api/videos/" + vdo_id

    headers = {    'Authorization': "Apisecret " + settings.VDO_API,
            'Content-Type': "application/json", 
            'Accept': "application/json"    }

    resp = requests.request("GET", url, headers=headers)

    return resp 


# Code to work after video calling is done, Mainly fresher work.
'''
Step1: We have to check whether the recording has stopped and .mp4 is available in S3.
Step2: When .mp4 is ready in S3, call VDO to get meeting video uploaded.
Step3: Code to show the upload status.
'''



# Step1: We have to check whether the recording has stopped and .mp4 is available in S3.
@csrf_exempt
@api_view(['GET'])
def record_complete(request,pfmid):

    if ProFrehserMeeting.objects.filter(id = pfmid).count() == 0:
        return Response(data = {'message':'Not a valid meeting'})

    pro_meeting = ProFrehserMeeting.objects.get(id = pfmid)
    file = 'directory1/directory7/' + pro_meeting.meeting_details.sid + '_' + pro_meeting.channel_name + '_0.mp4'

    status = record_file_exists(file)

    if status == 'Wrong key': # Some key error from meeting , email to admin
        meeting_error_email(pro_meeting,'','There is no SID for given  meeting')
        return Response(data={'message':'Server Error, We have sent report for Admin. We will get back to you soon'}, status=400)

    elif status == 'Found':
        if not DEBUG:
            file_name  = 'directory1/directory7/' + pro_meeting.meeting_details.sid + '_' + pro_meeting.channel_name + '_0.mp4' 
            
            resp = upload_s3video(file_name)

            if str(resp.status_code) != '200':
                meeting_error_email(pro_meeting,resp,'Uploading to VDO error')
                return Response(data={'message':'We have reported the problem for admin, We will get back to you soon'},status= 400)
            
            # If upload video initiating is success, store the vdo_id in DB

            pro_meeting.meeting_details.vdo_id = resp.json()['id']
            pro_meeting.meeting_details.save()


        return Response(data={'message':'success'}) #File found so check with uploading as next step
    
    else:
        return Response(data={'message':'Waiting'}) #We have to wait for some more time for the file to appear here

    


# Render the template after the meeting is complete
def after_record(request,pfmid):

    if ProFrehserMeeting.objects.filter(id = pfmid).count() == 0:
        raise Http404

    pro_meeting = ProFrehserMeeting.objects.get(id = pfmid)

    if MeetingChat.objects.filter(meeting = pro_meeting).count() == 0:
        raise Http404
    
    meetingchat = MeetingChat.objects.get(meeting = pro_meeting)
    meetingchat.locked = True
    meetingchat.save()
    
    
    return render(request,'after_record.html',context={'form':{},'pfmid':pfmid})


def meeting_feedback(request,mid=0):

    form = MeetingFeedbackForm()

    # check for meeting id
    if ProFrehserMeeting.objects.filter(id = mid).count() == 0 :
         raise Http404
    
    meeting = ProFrehserMeeting.objects.get(id = mid)

    if len(meeting.feedback) > 3:
        form.initial['result'] = ('Passed','pass') if meeting.passed else ('Failed','fail')
        form.initial['skills'] = meeting.fresher.skills
        form.initial['feedback'] = meeting.feedback

    
    try:
        if meeting.meeting_details.record_stop_time > timezone.now() + timezone.timedelta(minutes = 40):
            return HttpResponse('You have already submitted the feedback')
    except:
            raise Http404

    if request.method == 'POST':
        form = MeetingFeedbackForm(request.POST)


        if form.is_valid():

            meeting.feedback = form.cleaned_data['feedback']
            meeting.passed =True if form.cleaned_data['result'] == 'pass' else False
            meeting.fresher.skills = form.cleaned_data['skills']

            meeting.save()

            return redirect('pro_dashboard')
    print(form.errors.as_text)
    title = 'Feedback'
    return render(request,'dform.html',context={'form':form,'title':title})    #useapp templates signupcopy.html






