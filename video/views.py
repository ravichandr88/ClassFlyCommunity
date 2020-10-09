
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import FileResponse
import os
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import DeptHead,Playlist,Subject,VideoId,Subject,EducationDomain,Department
from rest_framework.response import Response
import json



# Create your views here.
def about(request):
    return render(request, 'about.html',{'title':'About Us'})
def home(request):
    return render(request, 'home.html',{'title':'Home'})

def community(request,sub,chp=1):

    if Subject.objects.filter(id=sub).count() == 0:
        return HttpResponse('Stop Playing')
    
    subjct_chptrs = Subject.objects.get(id=sub).subject_playlist.all().order_by('chapter')
    if (chp < 1) or (chp > len(subjct_chptrs)):
        return HttpResponse('Stop Playing')
    
    chptrs = list(range(1,len(subjct_chptrs)+1))
    chptrs.remove(chp)
    print(subjct_chptrs)
    
    chptrs_name = [i.name for i in Subject.objects.get(id=sub).subject_playlist.all().order_by('chapter')]
    chptrs_name = dict(zip(range(1,len(chptrs_name)+1),chptrs_name))



    chptrs_name.pop(chp)
    print(chptrs_name) 
    chptr_one = subjct_chptrs[chp-1]
    video_list = []  # the list of related videos
    first_video = ''    #The id of the first video
    
    if subjct_chptrs[chp-1].cf:
        video_list = [ i.video_id for i in chptr_one.playlist_videos.all()]
        first_video = video_list[0]
    else:
        
        video_list = [i.video_id for i in chptr_one.playlist_videos.all()]
        title_list = [i.title for i in chptr_one.playlist_videos.all()]
        first_video = []
        first_video.append(video_list[0] if (len(video_list)> 0) else None)
        first_video.append(title_list[0] if (len(title_list)> 0) else None)

        video_list = dict(zip(video_list,title_list))

    chptrs_vcount = {}
    for i in chptrs:
        chptrs_vcount[i] = len(subjct_chptrs[i-1].playlist_videos.all())
    


    
    return render(request, 'community.html',{'title':'Community','video_list':video_list,'cf':subjct_chptrs[chp-1].cf,'chapters':chptrs,'chptrs_videos':chptrs_vcount,'vcount':len(video_list),'first_video':first_video,'cchpt':chp})


def communityn(request):
    return render(request, 'community.html',{'title':'Community'})


def lib(request):
    domains = EducationDomain.objects.all()

    depts = { i.name:list(i.departments.all()) for i in domains}
    for i in depts.keys():
        #{'VTU': {'Mech' : [Subject Lists]}}
       depts[i] = {j.name: list(j.domain_subjects.all().values('name','imgurl','descp','id')) for j in depts[i]}

    print(depts)



    return render(request, 'lib.html',{'title':'Video Library','domain':depts})

def default(request):
	return render(request, 'default.html',{'title':'error'})


def generate_PDF(request):
    return FileResponse(open('ClassFlyTraining.pdf', 'rb'), content_type='application/pdf')


def generate_detailsPDF(request):
    return FileResponse(open('ClassFlyTrainingCollege.pdf', 'rb'), content_type='application/pdf')



from django.urls import reverse_lazy

@csrf_exempt
@login_required
def playlist(request):
    print(request.user)
    if DeptHead.objects.filter(user=request.user).count() == 0:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == 'GET':
        subject = Subject.objects.all().values('name')
    
        return render(request,'upload.html',{'title':'Community','subject':subject})
    
    subject = Subject.objects.get(name=request.POST['subject'])

    id_list = eval(request.POST['id_list'])
   
    print(request.POST)
    if len(id_list) == 0:
        # return render(request,'videosuploaded.html',{'title':'Community'})

        return HttpResponse(json.dumps({'code':'No youtube id found'}),status=400, content_type="application/json")

    playlist_name = request.POST['playlist']
    dept_head = DeptHead.objects.get(user__username=request.user)
    
    playlist = Playlist(name=playlist_name,subject=subject,uploaded_by=dept_head)
    playlist.save()
    print(id_list)
    for i in id_list:
        print(i)
        VideoId(video_id=i,playlist=playlist).save()

    return HttpResponse(json.dumps({'code':'Videos Playlist Saved'}), content_type="application/json")
     
@login_required
def videos_list(request):
    dept_head = DeptHead.objects.get(user__username=request.user)
    all_playlist = dept_head.depthead_playlist.all().values('id','name','subject','uploaded_by')
    
    print(all_playlist)

    for i in all_playlist:
        print(Playlist.objects.get(id=i['id']).playlist_videos.all().values('video_id'))
        i['videos'] = Playlist.objects.get(id=i['id']).playlist_videos.all().values('video_id')
        i['subject'] = Subject.objects.get(id=i['subject']).name
    return render(request,'videosuploaded.html',{'title':'Community','playlist':all_playlist})
       