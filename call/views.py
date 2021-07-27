from django.shortcuts import render
from django.utils import timezone
import requests
import json
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail

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

from fresher.models import ProFrehserMeeting, Meeting
from interview.models import Prfessional, Fresher
# from .models import 

# Contains one SMS call REST API
# line no. 338, 278
from agora.src.RtcTokenBuilder import *
import time
import random


#  connect_to_call_fresh -> have External RESt API




def video_prepare(request,id=''):
    # The first part of id will be the category fresher 'f' or professional 'p'
    categ = id.split('_')[0]

    id = id.split('_')[1]

    if categ == 'p':
        request.session['category'] = 'p'
        waiting_room = False        #Professional should wait unitll it is time
    else:
        request.session['category'] = 'f'
        waiting_room = True         #Fresher has to wait untill the Professional joines the meeting

    # print(categ)

    request.session['meeting'] = id

    
    # Check if the given id is present in the meeting table or not
    if ProFrehserMeeting.objects.filter(id=id).count() != 1:
        raise Http404

    meeting = ProFrehserMeeting.objects.get(id=id)

    if Meeting.objects.filter(meeting__id = meeting.id).count() == 0:
        Meeting( meeting  = meeting).save()


    remain = meeting.date_time

    now    = timezone.now()

    
    return render(request,'waitingroom.html',context={'remain':remain,'now':now,'waiting':waiting_room,'mid':meeting.id,'fid':meeting.fresher.id})


#final video call work
def videocall(request):    

    # If the request is from professional , he can join
    # If the request is from fresher, he can join after the professional has joined

    
    user = ''
    uid = ''

    if ProFrehserMeeting.objects.filter(id=request.session['meeting']).count() == 0:
        raise Http404


    meeting = ProFrehserMeeting.objects.get(id=request.session['meeting'])

    
    if Prfessional.objects.filter(id =  meeting.prof.id).count() == 1:
        user = 'prof'


    elif Fresher.objects.filter(user__username = request.user).count() == 1:
        user = 'fresher'


    else:
        raise Http404
    
    meet_details = meeting.meeting_details

    # print(meeting.date_time - datetime.datetime.now())
    g = meeting.date_time
    g = g + timedelta( hours=2) 
    print(g)

    # If the current time is greater than meeting start time and 
    # less than 2 hours of meeting start time, you can join
    if timezone.now() > meeting.date_time   and timezone.now() < g and not meeting.meeting_details.record_stopped:
        print(timezone.now(), meeting.date_time )
        
    # Else move to dashboard
    else:
        if request.session['category'] == 'f':
           return redirect('f_dashboard')
           
        else:
           return redirect('pro_dashboard')
          


    # If the user oif fresher , check whether the professional has joined or not.
    if request.session['category'] == 'f' and not(meet_details.pro_joined) :
        # default varibel to pass the html page
        # if professional has not joined, then redirect to waiting room
        remain = datetime.datetime.now()
        now    = datetime.datetime.now()

        waiting_room = 'True' # Which supoorts te decision to make sure we call server evry 30 seconds to know whether the professional have joined the meeting or not.
       
        return render(request,'waitingroom.html',context={'title':'Please wait for Professional to Join','remain':remain,'now':now,'waiting':waiting_room,'mid':meeting.id,'fid':meeting.fresher.id})




    # print(meeting.channel_name)

    appID = "e73019d92f714c95b9bc47ea63de404c"
    appCertificate = "ed36762fba3f4e42acaf99c6265ec4c3"
    channelName = meeting.channel_name
    uid = random.randrange(11111111,99999999)
    userAccount = str(uid)
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    if user == 'prof':
        uid = meeting.prof.id
    else: 
        uid = meeting.fresher.id

    token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, Role_Attendee, privilegeExpiredTs)

    data = {'token' : token,
    'appid': appID,
    'channel': channelName,
    'uid': uid,
    'uid' : meeting.prof.id,
    'meet': meeting,
    'status': meet_details,
    'user':user,
    'pro' : True if user == 'prof' else False
    }



    return render(request,'videocall/call.html',context = data)



# API call for professional to inform about  joining  the meeting
@csrf_exempt
@api_view(['GET'])
def connect_to_call_pro(request,pid,mid):

    if Prfessional.objects.filter(id = pid).count() == 0:
        return Response(data={'message':'Not valid Professional'}, status=404)

    pro = Prfessional.objects.get(id = pid)

    

    
    if ProFrehserMeeting.objects.filter(id = mid, prof__id = pid).count() == 0:
        return Response(data={'message':'Not valid Meeting'}, status=404)

    meeting = ProFrehserMeeting.objects.get(id = mid, prof__id = pid).meeting_details
    fresher = ProFrehserMeeting.objects.get(id = mid, prof__id = pid).fresher
    # print(meeting) 

    meeting.pro_joined = True
    meeting.save()

    
    # code to send SMS for the Fresher to inform Professional have joined the meeting
    
    requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=26&type=text&contacts={}&senderid=SOFTEC&msg=ClassFly+Interview+Meeting+has+been+started,+please+login+and+connect+to+meeting.".format(fresher.user.userphone.phone_number))
    

    return Response(data={'message':'joined'})



# function called by fresher to know whether the professional has joinde the meeting or not
@csrf_exempt
@api_view(['GET'])
def pro_joined(request,mid,fid):
    
    if ProFrehserMeeting.objects.filter(id = mid,fresher__id = fid).count() == 0:
        return Response(data={'message':'Not valid meeting '}, status = 400)

    meeting = ProFrehserMeeting.objects.get(id = mid, fresher__id = fid).meeting_details
    
    if meeting.pro_joined and not meeting.record_stopped :
        # Code to get agora record resource ID
        pro_meeting = ProFrehserMeeting.objects.get(id=mid, fresher__id = id)

        # REST API for calling the resouceID for the recording

        resp = record_resource_id(pro_meeting)

        if str(resp.status_code) != '200':
            return Response(data={'message':resp.json()['reason']})

        return Response(data={'message':'joined'})

    else:
        return Response(data={'message':'Not yet'})


# Function to connect Fresher for video call, 
# to record about their joining to the meeting
# And get the resource id for connecting to video call
@csrf_exempt
@api_view(['GET'])
def connect_to_call_fresh(request, fid, mid):
    
       
    if ProFrehserMeeting.objects.filter(id=mid, fresher__id = id).count() == 0:
        return Response(data={'message':'Not valid registration'}, status= 400)
    pro_meeting = ProFrehserMeeting.objects.get(id=mid, fresher__id = id)
    meeting = pro_meeting.meeting_details


    # End of code for the REST API resourceID code
    
    if meeting.pro_joined and not meeting.record_stopped:

        meeting.fre_joined = True
        meeting.save()

        resp = start_record_api(pro_meeting)

        if str(resp.status_code) != '200':
            meeting_error_email(meeting)
            return Response(data={'message':resp.json()['reason']})

        meeting.sid = resp.json()['sid']
        meeting.save()

        return Response(data={'message':'joined'})
    
    else:

        return Response(data={'message':'Not right time'}, status= 400)


@csrf_exempt
@api_view(['GET'])
def start_record(request,fid,mid):


    if ProFrehserMeeting.objects.filter(id = mid, fresher__id = fid).count() == 0 :
        return Response(data={'message':'Not a Meeting and Fresher'}, status= 400)
        
    # Start recording 
    meeting = meeting.objects.get(id = mid, fresher__id = fid)
    


    if str(res.status_code) != '200':

        meeting_error_email(meeting,res)
        
        return Response(data={'message':'Sorry, There was an error. We have contacted Admin'}, status= 400)

    return Response(data={'message':'Recording Started'})






# function to provide html page for recording
# mid -> meeting ID(ProFrehserMeeting), fid -> Fresher id
def record(request,fid=0,mid=0):
    
    if ProFrehserMeeting.objects.filter(id=mid,fresher__id = fid).count() != 0:
        
        raise Http404

    

    appID = "e73019d92f714c95b9bc47ea63de404c"
    appCertificate = "ed36762fba3f4e42acaf99c6265ec4c3"
    channelName = "car"
    uid = random.randrange(11111111,99999999)
    userAccount = str(uid)
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds


    token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, Role_Attendee, privilegeExpiredTs)

    data = {
            'token' : token,
            'appid': appID,
            'channel': channelName,
            'uid': uid
            }
    
    return render(request, 'videocall/record.html', context= data)


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
    "uid": "39690211",
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

    meeting.resource_id = resp.json()['resourceId']

    meeting.save()

    return resp


# Function to send email if any error before the meeting
def meeting_error_email(meeting,message):
        subject = 'welcome to GFG world'
        message = f'Could not record the meeting .' + meeting.dict() + str(message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['ravichandrareddy88@gmail.com', ]
        send_mail( subject, message, email_from, recipient_list )


def start_record_api(pro_meeting):
        
    return 

    url = 'https://api.agora.io/v1/apps/e73019d92f714c95b9bc47ea63de404c/cloud_recording/resourceid/' + pro_meeting.meeting_details.resource_id + '/mode/web/start'
    
    data = {
    "cname":"car",
    "uid":"39690211",
    "clientRequest":{
        "token": "006e73019d92f714c95b9bc47ea63de404cIADVMPOGFws086UlSkWOq1HVa79tc6nmik3Gi15gOgZDVJ3mPXeby/NFIgCCVCMBAGbdYAQAAQCQItxgAgCQItxgAwCQItxgBACQItxg",
        "extensionServiceConfig": {
            "errorHandlePolicy": "error_abort",
            "extensionServices":[{ 
                    "serviceName":"web_recorder_service",
                    "errorHandlePolicy": "error_abort",
                    "serviceParam": {  
                        "url": "https://www.classfly.in/record/" + pro_meeting.fresher.id + '/' + pro_meeting.id,
                        "audioProfile":0,
                        "videoWidth":1280,
                        "videoHeight":720,
                        "maxRecordingHour":2,
                        "readyTimeout": 100
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

    return res

