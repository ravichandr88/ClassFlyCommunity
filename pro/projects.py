from django.shortcuts import render,redirect,HttpResponse
from django import forms
from django.http.request import QueryDict, MultiValueDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
import base64
import time
import jwt

from django.core import exceptions

from rest_framework.decorators import api_view

from .models import Project,Trainer,Skills,VideoAsset, RegsiteredUser



headers = {'Content-Type':'application/json'}
auth = ('24484635-ee3e-4633-977a-88679bbb0551','jqDGptsyBdyh3bQa6NuqnWgEgwFkadLNQm6lJ6ryF1t59GfRcFBy3ZvY6NzuBBgI+fGhBJsolBM')


def slice_list(x):
    n = 3
    l=[]
    while n < len(x):
        l.append(x[n-3:n])
        n+=3
    l.append(x[n-3:])
    return l


def search(request):
    id = 1
    project = Project.objects.get(id=1)
    projects = [project,project,project]
    l = []
    for project in projects:
        data = {
        'project_title': project.title,
        'trainer_name' : project.trainer.name,
        'exp'          : project.trainer.exp,
        'skills'       : slice_list(project.skills.all().values('title')),
        'description'  : project.description,
        'work_period'  : project.work,
        'exp'          : project.trainer.exp          
        }
        l.append(data)
    return render(request,'search.html',context={'data': l})


def project_review(request):
    project = Project.objects.get(id=1)

    skills = project.skills.all()
    n = len(skills)
    skills_percent = [skills[:int(n/2)],skills[int(n/2):]]

    project_flow = project.flow.all()[0]
    flow = str(project_flow.description).split("<>")
    project_flow = {}
    for i in flow:
        head = i.split("<*>")[0]
        flow_list = i.split("<*>")[1:]

        project_flow[head] = flow_list
    
    # print(project.presentation)

    data={
        'skills'        : str([i.title for i in skills]).replace('[','').replace(']','').replace("'",'',40),
        'skills_percent': skills_percent,
        'skills_count'  : len(skills),
        'work'          : int(project.work[:2]),
        'project_flow'  : project_flow
    }

    return render(request,'project.html',context={'project':project,'data':data})


@login_required
def videoplayer(request,video_id):
    
    headers = {'Content-Type':'application/json'}
    auth = ('24484635-ee3e-4633-977a-88679bbb0551','jqDGptsyBdyh3bQa6NuqnWgEgwFkadLNQm6lJ6ryF1t59GfRcFBy3ZvY6NzuBBgI+fGhBJsolBM')

    #create a signed url for the video ID and store the keys to user registered project
    
    video = VideoAsset.objects.get(id=video_id)
    project = video.project
    register_user = RegsiteredUser.objects.filter(user__username = request.user, project = project)
    
    if len(register_user) == 0:
        return HttpResponse("User is Not registered to this Subject")
    register_user = register_user[0]
    print(register_user.sign_key)
    if register_user.sign_key == 'null':
        url = 'https://api.mux.com/video/v1/signing-keys'
        response = requests.post(url,headers=headers,auth=auth)
        data = response.json()['data']

        register_user.sign_key = data['id']
        register_user.private_key =  data['private_key']
        register_user.save()
    #create JWT token for the video, every time a user request a video
    playback_id     =   video.playback_id
    signing_key_id  =   register_user.sign_key
    private_key_base64= register_user.private_key

    # playback_id     =   "o6NfTUyXvdbIoZcDXvgKom02RIcEIU5MB01jjKEnv6OSM"
    # signing_key_id  =   "gDnnyCAeuFFCxjk929pHv8qIUF5uvMp00Uo4VjQ01VK00U"
    # private_key_base64 = "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBdkl2ckpsY090ZGZpUEpNbWZMb0swaHZxOENGaGtQb2lSeU1ReVBYcWJsVTRBZTFNCjFLdktpSy9MeHBtOXIvTXBpN0tVTThDU3IvQy81RWlMWVl5dnp6NE95SU9VUVUremtLWE5VUEdiVW4vMUthZUkKempGWDFqZkJiaGk0dnJST1RqMys4OFdienozalFVa0krejdPZUw0L2cyTzYvK1J0QUM0MXNldGladzNoVWltNgpUcXlTa1JDdG5MMFlubFArNUVsK0xXVmdERFBxeFB6L3lMU24yOHhZbU5pSy80cHU1dG1vMTZyMUVyS2h1ZnlFClh5bGRHc0drUVM4cG03dVFBQ0haS2FjQVJxeldyMW1UNkJSdmNxTEYwTWovK1Q2bHRzL0h3VEtYeDNWWHZ4SzUKalo1SFQzdTY5RzVPYk1MSGs1SkErUEc0ZnlNL2VQLzJxYm1ldFFJREFRQUJBb0lCQVFDOEw5c3dsVXYxYTlnLwpKWkFRaFpBdlRmWWNYdlVHd3VKYnBrQW1sR3k4V3dwZndmNGhkcVhiNzdxd0t0c05OdUtNc0YwRG1uM09aYmpoCm5SYWc4czYzUnZWeVpRSWdmZkIzdTBWR09TQVNJKzBLK2xDdG5NcFM0YXVLdTlvSlhlV2FhbjZCeVFaT3Z6S0kKQXVHWUE0UUpON29rNWZITFhxNzhzeUtjeHBlY3lxSHU3aWxOc3YzRmVKdWtDNFpmL0h4TkZ5OTJmd29RVzlYNgozQzNmUHh3Q25Ya1BMbHpSZXQ3OE1GaDBYR1Rmd2RkMFlMeXA4M0kvNjJYdVllSlRXZlVyUk1Ybmh0RlRQeExzCm1jeDVjSThwZWVLblY1bjN3d1BBWTMrbE00aThpeVlxN3hNMm1VTHJ3Z3FMR3g2d0ZzS3oxZzQ3WlRQMGtyMDEKWWFaQzcrV3hBb0dCQU8xUW1MdVlHZHBhZFRodlhYYUdNVVFVZ1lFL0tkMkhYaWhlTFQwS0p0Ui9QWXZTZXdUSQp0ZzVxRzRSSld1S1NtY3FDUlBxbXk2THp1Mml3Y3FkSUdVZ245M1VCa0dxQitZOWV3VDBzR2dMZ1VHQ291TUo1CkxtWXh2TUtKbXVNY0pFTjU5aHdlZUhNazhoeXp2NWtON1FXdGpqaUYzVStGbUl5bE55eTRMY0xmQW9HQkFNdGsKVkwxTEJsUzk5cVE3ZzFEMVV3SG9wSXMxZDRNRnJrVHZWN3ZmelBLdUFNUk5tNXhKcmRGWVdTOENxNVdYY1c3cQoraXowdnQwQWlmR0RGaFVCY2pBSFoxU0FOSXR0b0xRbG9zNjYzTm1sSG5QZDloZUdUa29PeG5nYWluUlFFUDZFCmZoSitMS0h4TU9EMzJjUnU3Qm51RHl2R3ZYK0dzRjlMTThZZkc4VHJBb0dBSXBwaDZ0aWV6R3ZzTTdKcFdtTHUKeEJLSlg2TXFJNWNkYjUxcjB6NnJzc2hxM1B4djI1NjRqUm1Ec2FKUWtrRDJFOFV5OGFsb2YvWXlHVzNCQ2d0RgpSSFF2Yk93eGRwWkZJVmFicnFQRGx5L0dDSklSZnFuVXppbnFjQ05JWmwwd0hIYW9JQ21CUHFqZ2RMYnc5UXhHCngxRXJMNnExUG1jb2V6bUw5Z1ZWQnRrQ2dZQVpoUkk0MmhRR1IvdU5hY1kxUDBMV0IzbTEyZFNRQlFOenROQSsKUzN0c3E3Wis2dm51WnpRL0F5WFZoekUrU00wN3pKSHRXQndtb0sydU52TnJXVTRaaHFSSmJ2aW8wZTJMRFBuYgpsSWluYWxkaTFHUFBXZE95NlIydjdpeVhJWUN3WHJGdTRwUDVFY2svUVBuNjhxdi9LT2FRYUpSWVR1OE1WZVErCkpLTVlWd0tCZ0ZpNXdjbG55L1krYTBtK3JoT3JaM3grTmF6MHIwVHZ1NmMxSU4rS09QRElZWFAzTGlhYlBYOHUKeVJiWUJiNXArZ255dlFFRTFxSlBUc1JtK0phQlRHL2lLMHNzUGwxUU0rV25qN1BFdUdrR0pIMktoc0F2dDQyYgp2TTFXRXdSd2ZLek02ZjhOM2JOdXc4dlZ2V1c1c0p0TXNIU0JQbXVRa2tlaGlPVUpFSkE3Ci0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg=="


    private_key = base64.b64decode(private_key_base64)


    token = {
        'sub': playback_id,
        'exp': int(time.time()) + 3600, # 1 hour
        'aud': 'v'
    }
    headers = {
        'kid': signing_key_id
    }
    json_web_token = jwt.encode(token, private_key, algorithm="RS256", headers=headers)

    try:
        json_web_token = json_web_token.decode("utf-8") 
    except:
        json_web_token 
    
    url = "https://stream.mux.com/{}.m3u8?token={}".format(playback_id,json_web_token)

    # user = User.objects.get(username = request.user)


    
    return render(request,'video.html',context={'url': url})



@login_required
def dashboard(request):
    user = User.objects.get(username=request.user)
    projects = slice_list(user.project_registered.all())
    
    return render(request,'dashboard.html', context={'user':user,'projects':projects})