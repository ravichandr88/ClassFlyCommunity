
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import FileResponse
import os
from rest_framework.decorators import api_view
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import DeptHead,Book,Playlist,Subject,VideoMaker,VideosMade,VideoId,VideoDeptHead,Subject,EducationDomain,Department
from rest_framework.response import Response
import json

#header for dept head

def depthead_required(function):
    # @wraps(function)
    def inner(request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        if VideoDeptHead.objects.filter(user=user).count() == 1:
            return function(request,  **kwargs)
        else:
            return HttpResponse('Sorry, you are not signedup as Department Head')

    return inner

# video maker header
def videomaker_required(function):
    # @wraps(function)
    def inner(request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        if VideoMaker.objects.filter(user=user).count() == 1:
            return function(request,  **kwargs)
        else:
            return HttpResponse('Sorry, you are not signedup as Video Maker')

    return inner


# Create your views here.
def about(request):
    return render(request, 'about.html',{'title':'About Us'})
def home(request):
    return render(request, 'home.html',{'title':'Home'})

def community(request,sub,chp=1):

    if Subject.objects.filter(id=sub).count() == 0:
        return HttpResponse('Stop Playing')
    subjct = Subject.objects.get(id=sub)
    subjct_chptrs = subjct.subject_playlist.all().order_by('chapter')
    if (chp < 1) or (chp > len(subjct_chptrs)):
        return HttpResponse('Stop Playing')

    chptrs = list(range(1,len(subjct_chptrs)+1))
    chptrs.remove(chp)
    # print(Subject.objects.get(id=sub).subject_noteslist.all().filter(chapter=1))
    
    chptrs_name = [i.name for i in Subject.objects.get(id=sub).subject_playlist.all().order_by('chapter')]
    chptrs_name = dict(zip(range(1,len(chptrs_name)+1),chptrs_name))



    chptrs_name.pop(chp)
    # print(chptrs_name) 
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

    #chapter numbers to display playlist, if present
    chptrs_vcount = {}
    for i in chptrs:
        chptrs_vcount[i] = len(subjct_chptrs[i-1].playlist_videos.all())
    fristChptrNotes = Subject.objects.get(id=sub).subject_bookslist.all().filter(chapter=chp,active=True)
    
    allChptrNts = {}
    #Prepare notes buttons
    for i in range(1,11):
        if (i != chp ) :
            notes = Subject.objects.get(id=sub).subject_bookslist.all().filter(chapter=i,active=True)
            if len(notes) > 0:
                allChptrNts[i] = notes
    # print(fristChptrNotes)
    engg = Department.objects.get(id=subjct.domain.id)
    subj = engg.domain_subjects.all().values('name','imgurl','id')
    print(subj)
    return render(request, 'civil.html',{'title':'Community',
                                        'video_list':video_list,
                                        'cf':subjct_chptrs[chp-1].cf,
                                        'chapters':chptrs,
                                        'chptrs_videos':chptrs_vcount,
                                        'vcount':len(video_list),
                                        'first_video':first_video,
                                        'cchpt':chp,
                                        'fristChptrNotes':fristChptrNotes,
                                        'allChptrNts':allChptrNts,
                                        'subject':subjct.name,
                                        'subjects':subj
                                        })

'''

'''
def communityn(request):
    return render(request, 'community.html',{'title':'Community'})


def lib(request):
    # domains = EducationDomain.objects.all()

    # depts = { i.name:list(i.departments.all()) for i in domains}
    # for i in depts.keys():
    #     #{'VTU': {'Mech' : [Subject Lists]}}
    #    depts[i] = {j.name: list(j.domain_subjects.all().values('name','imgurl','descp','id')) for j in depts[i]}
       
    engg = Department.objects.get(id=1)
    subj = engg.domain_subjects.all().values('name','imgurl','id')
    if request.method == 'POST':
        subj = Subject.objects.filter(name__icontains=request.POST['search']).values('name','imgurl','id')
        return render(request, 'community1.html',{'title':'Video Library','subjects':subj,'subject_title':'Results for "'+request.POST['search']+'"', 'pic':False})
    # print(depts)

    return render(request, 'community1.html',{'title':'Video Library','subjects':subj,'subject_title':'Engineering First Year', 'pic':True})

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
    # print(request.user)
    if DeptHead.objects.filter(user=request.user).count() == 0:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == 'GET':
        subject = Subject.objects.all().values('name')
    
        return render(request,'upload.html',{'title':'Community','subject':subject})
    
    subject = Subject.objects.get(name=request.POST['subject'])

    id_list = eval(request.POST['id_list'])
   
    # print(request.POST)
    if len(id_list) == 0:
        # return render(request,'videosuploaded.html',{'title':'Community'})

        return HttpResponse(json.dumps({'code':'No youtube id found'}),status=400, content_type="application/json")

    playlist_name = request.POST['playlist']
    dept_head = DeptHead.objects.get(user__username=request.user)
    
    playlist = Playlist(name=playlist_name,subject=subject,uploaded_by=dept_head)
    playlist.save()
    # print(id_list)
    for i in id_list:
        # print(i)
        VideoId(video_id=i,playlist=playlist).save()

    return HttpResponse(json.dumps({'code':'Videos Playlist Saved'}), content_type="application/json")
     
@login_required
def videos_list(request):
    dept_head = DeptHead.objects.get(user__username=request.user)
    all_playlist = dept_head.depthead_playlist.all().values('id','name','subject','uploaded_by')
    
    # print(all_playlist)

    for i in all_playlist:
        print(Playlist.objects.get(id=i['id']).playlist_videos.all().values('video_id'))
        i['videos'] = Playlist.objects.get(id=i['id']).playlist_videos.all().values('video_id')
        i['subject'] = Subject.objects.get(id=i['subject']).name
    return render(request,'videosuploaded.html',{'title':'Community','playlist':all_playlist})



#videoDeptHead Dashboard
@login_required
@depthead_required
def depthead_dashboard(request,page='p'):
    
    user = request.user
    #videomakers under this depthead
    video_makers = VideoDeptHead.objects.get(user__username=user)
    videos_made = []
    if page == 'r':
        #Iterate over the video_makers
        for i in video_makers.report_to_dept_head.all():
            videos_made.append(i.videos_made.filter(status=False))
    elif page == 'a':
        for i in video_makers.report_to_dept_head.all():
            videos_made.append(i.videos_made.filter(status=True))
    else:
        for i in video_makers.report_to_dept_head.all():
            videos_made.append(i.videos_made.filter(status=None))
    # print(videos_made)
    return render(request,'depthead_dashboard.html',context={'videos':videos_made,'mode':page})



#API to reject or approve Videos , this is for dept head
@login_required
@depthead_required
@api_view(['POST','GET'])
def approve_reject_video(request):
    if request.method == 'POST':
        video = VideosMade.objects.get(id=request.data['id'][0])
        video.report = request.data['report']
        video.status = False
        video.save()
        return Response(data={'code':200})
    if request.method == 'GET':
        video = VideosMade.objects.get(id= request.GET['id'][0])
        video.status = True
        video.save()
        return Response(data={'code':200})

#function for video makers to submit the video.
@login_required
@videomaker_required
def video_uploader(request):
    if request.method == 'POST':
        # print(request.POST['title'])
        VideosMade(
            title=request.POST['title'],
            video_link=request.POST['video_link'],
            thumbnail_link=request.POST['thumbnail_link'],
            video_maker=VideoMaker.objects.get(user__username=request.user)).save()
        return HttpResponseRedirect(reverse('videom_dashboard'))

    dept_head = VideoMaker.objects.get(user__username=request.user)
    return render(request,'video_submit.html',context={'dept_head':dept_head.dept_head.name})


#function for video_makers dashboard
@login_required
@videomaker_required
def videos_uploaded_list(request):
    vmaker = VideoMaker.objects.get(user__username=request.user)
    vlist = vmaker.videos_made.all()
    vlist = vlist[::-1]
    # print(vlist)

    return render(request,'videos_list.html',context={'videos':vlist})


#PDF viewer page
def reader(request,id):
    if Book.objects.filter(id=id).count() == 0:
        return HttpResponse('Stop playing the notes ID')
    link = Book.objects.get(id=id).note_link
    return render(request,'reader.html',context={'link':link})


#uploading notes by a student/video maker
@login_required
@videomaker_required
def notes_upload(request):
    if request.method == 'POST':
        print(request.POST)
        Book(
            name=request.POST['name'], #book written author name
            note_link=str(request.POST['notes_link']).split('/d/')[1].split('/')[0],
            subject = Subject.objects.get(id=request.POST['subject_id']),
            chapter = request.POST['chapter'],
            uploaded_by=VideoMaker.objects.get(user__username=request.user)).save()
        return HttpResponseRedirect(reverse('videom_dashboard'))

    dept_head = VideoMaker.objects.get(user__username=request.user)
    subjects = Subject.objects.all().values('id','name')
    print(subjects)
    return render(request,'notes_upload.html',context={'dept_head':dept_head.dept_head.name,'subjects':subjects})



#function for video_makers dashboard to see Book
@login_required
@videomaker_required
def notes_uploaded_list(request):
    vmaker = VideoMaker.objects.get(user__username=request.user)
    vlist = vmaker.books_uploaded.all().values('id','name','subject__name','chapter','datetime','active')
    vlist = vlist[::-1]
    # print(vlist)

    return render(request,'notes_list.html',context={'videos':vlist})



#videoDeptHead Book Dashboard
@login_required
@depthead_required
def depthead_notes_dashboard(request,page='p'):
    
    user = request.user
    #videomakers under this depthead
    video_makers = VideoDeptHead.objects.get(user__username=user)
    notes_made = []
    if page == 'r':
        #Iterate over the video_makers
        for i in video_makers.report_to_dept_head.all():
            notes_made.append(i.books_uploaded.filter(active=False))
            print(i.books_uploaded.filter(active=False))
    elif page == 'a':
        for i in video_makers.report_to_dept_head.all():
            notes_made.append(i.books_uploaded.filter(active=True))
    else:
        for i in video_makers.report_to_dept_head.all():
            notes_made.append(i.books_uploaded.filter(active=None))
    # print(videos_made)
    return render(request,'depthead_notes_dashboard.html',context={'notes':notes_made,'mode':page})


#API to approve or Reject the Book, Dept Head
@login_required
@depthead_required
@api_view(['POST','GET'])
def approve_reject_notes(request):
    if request.method == 'POST':
        notes = Book.objects.get(id=request.data['id'][0])
        notes.report = request.data['report']
        notes.active = False
        notes.save()
        # print(notes.active)
        return Response(data={'code':200})
    if request.method == 'GET':
        notes = Book.objects.get(id= request.GET['id'][0])
        notes.active = True
        notes.save()
        return Response(data={'code':200})
