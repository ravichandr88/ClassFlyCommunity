from django.shortcuts import render,HttpResponse,Http404, redirect
from .models import Prfessional, ProFrehserMeeting, Fresher
from .forms import ClassFlyInterviewForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from rest_framework.decorators import api_view
from rest_framework.response import Response
from chatt.models import TwoGroup
from chatt.views import chats,usertype
from intervideo.models import MeetingPurchase
from pro.sample_tasks import send_email
import math

# Create your views here.



# In this file we have built functions to support
#  professional search, 
#  professional profile
#  watching pro interview videos
#  booking meetings


# Homepage for searching professionals
# updated

@csrf_exempt
@usertype
def search_professional(request,page=1):
    

        try:
            designation = request.GET['designation']
            city        = request.GET['city']
            skill       = request.GET['skill']
            company     = request.GET['company']

        except:
            profs = Prfessional.objects.filter(approved = True,meeting_time_updated = True)
            return render(request,'searchpage.html',context={
                'profs':profs[((page-1)*10):(page*10)],
                'pages':range(1,math.ceil(len(profs)/10)+1),
                'page':page
                })
     


        
        profs = list(Prfessional.objects.filter(city__icontains = city,approved = True,meeting_time_updated = True).filter( skills__icontains = skill).filter(company__icontains = company).filter(designation__icontains = designation))
            
        return render(request,'searchpage.html',context={'profs':profs,
                'skill':skill,
                'city':city,
                'company':company,
                'designation':designation,
                'profs':profs[((page-1)*10):(page*10)],
                'pages':range(1,math.ceil(len(profs)/10)+1),
                'page':page,})

    # return render(request,'search_pro/pro_search.html',context={'profs':profs,'skill':skill,'city':city,'company':company,'designation':designation})



# updated
@login_required
@usertype
def fresher_dash(request):

    if Fresher.objects.filter(user__username = request.user).count() == 0:
        return redirect('student')
    
    # Check with the meetings that are paid , and turn the paid boolean value to True
    pending_paid_meetings = ProFrehserMeeting.objects.filter(fresher__user__username = request.user, paid = False)

    for i in pending_paid_meetings:
        try:
            if MeetingPurchase.objects.get(meeting__id=i.id).activate_meeting():
                i.paid = True
                i.save()
        except:
            continue

    # Meetings
    p = ProFrehserMeeting.objects.filter(fresher__user__username = request.user, paid = True)

    
    today = timezone.now()
    user = Fresher.objects.get(user__username = request.user)


    

    data = {'meetings':p,
            'today':today,
            'self':user,
            'chats': chats(request.user)
            }

    # return render(request,'dashboard/dist/dash_fresher.html', context={'meetings':p,'today':today,'self':user})
    return render(request,'fresher_dash.html',context=data)


@login_required
@usertype
def pro_dash(request):
# Types   of meeting states possible
# State 1 -> Booked
# State 2 -> Approved
# State 3 -> Meeting Done
# State 4 -> Rejected


    if Prfessional.objects.filter(user__username = request.user).count() == 0:
        return redirect('professional')


    if request.method == 'POST':
        data = request.POST.dict()
        print(data['meeting_id'])
        if ProFrehserMeeting.objects.filter(id=int(data['meeting_id'])).count() == 0:
            raise Http404
        
        meeting = ProFrehserMeeting.objects.get(id=int(data['meeting_id']))

        meeting.date_time =  timezone.datetime.fromisoformat(data['date'] +' '+ data['time'])
        
        # If meeting is not approved, approve it 
        if not meeting.approved:
            meeting.approved = True
            meeting.save()

            # send email for the fresher saying the meeting is approved.

            send_email(meeting.fresher.user,'ClassFly Interview', 'Your meeting is been approved, for date and time {} for {} designation . All the best'.format(meeting.date_time.strftime("%d %b %Y  %I:%M %p"),meeting.designation))

        else:
            # send email for the fresher saying the meeting is approved.

            send_email(meeting.fresher.user,'ClassFly Interview', 'Your meeting timings has been updated, for date and time {} for {} designation . Hope you are notified'.format(meeting.date_time.strftime("%d %b %Y  %I:%M %p"),meeting.designation))


    # Activate the meetings, if paid
    # Check with the meetings that are paid , and turn the paid boolean value to True
    pending_paid_meetings = ProFrehserMeeting.objects.filter(fresher__user__username = request.user, paid = False)

    # go after each meeting and chekc paid or not
    for i in pending_paid_meetings:
        try:
            if MeetingPurchase.objects.get(meeting__id=i.id).activate_meeting():
                i.paid = True
                i.save()
        except:
            continue


    # Stae 1 -> Booked
    booked_meetings     =   ProFrehserMeeting.objects.filter(prof__user__username = request.user,approved = False, rejected = False,paid= True)
    
    # State 2-> Approved
    approved_meetings   =   ProFrehserMeeting.objects.filter(prof__user__username = request.user,approved = True, rejected = False ,paid= True)
    
    # State 3 -> Meeting Done
    # need an empty query list
    done_meetings       =   ProFrehserMeeting.objects.filter(id=0)
    
    for i in ProFrehserMeeting.objects.filter(prof__user__username = request.user,approved = True, rejected = False ,paid= True):
        try:
            if i.meeting_details.record_stopped:
                done_meetings = done_meetings | i
        except:
            pass
    
    # State 4 -> Rejected
    reject_meetings     =   ProFrehserMeeting.objects.filter(prof__user__username = request.user,approved = False, rejected = True,paid= True)

    user = Prfessional.objects.get(user__username = request.user)
    today = timezone.now()
    meetings = approved_meetings | booked_meetings
    # return render(request,'dashboard/dist/dash_pro.html', context = {'meetings':meetings,'self':user,'today':today})
    return render(request,'pro_dash.html', context = {
        'meetings':meetings,
        'approved_meetings':approved_meetings,
        'pending_meetings':booked_meetings,
        'done_meetings':done_meetings,
        'reject_meetings':reject_meetings,
        'self':user,'today':today,
        'chats': chats(request.user)
        })


@login_required
@usertype
def pro_profile(request,pro):
    

    if Prfessional.objects.filter(user__id = pro).count() == 0:
        raise Http404
    
    

    prof = Prfessional.objects.get(user__id = pro)
    exps = prof.experience.all()
    pro_user  = prof.user
    
    return render(request,'professional_profile.html', context={'prof':prof,'exps':exps,'pro_user':pro_user})
   

@login_required
@usertype
def fresher_profile(request,fre):
    
    if Fresher.objects.filter(user__id = fre).count() == 0:
        raise Http404
    
    

    fres = Fresher.objects.get(user__id = fre)
    exps = fres.experience.all()
    fresher_user  = fres.user
    
    return render(request,'fresher_profile.html', context={'fresher':fres,'exps':exps,'pro_user':fresher_user})
   

@login_required
@usertype
def book_interview(request, prof = 0):  # page 22
 
    if prof == '' or Prfessional.objects.filter(user__id = prof, approved = True, meeting_time_updated = True).count() == 0:
        raise Http404

    prof = Prfessional.objects.get(user__id = prof)

    skills = prof.skills

    # lambda function to get the dates of the weekday given
    onDay = lambda date, day: date + timezone.timedelta(days=(day-date.weekday()+7)%7)
    days = {'MON':0,'TUE':1,'WED':2,'THU':3,'FRI':4,'SAT':5,'SUN':6}
    dates =[((onDay(timezone.now(),days[i.meet]).strftime('%Y-%m-%d') + ' ' +i.time.strftime('%H:%M')), str(i.meet +'  ('+onDay(timezone.now(),days[i.meet]).strftime('%m/%d/%Y')+') -> '+i.time.strftime('%H:%M %p')) ) for i in prof.prof_interview.all()]
    # 2021-07-07 03:43
    
    if request.method == 'POST':
        
        fresher = ''

        try:
            fresher = Fresher.objects.get(user__username = request.user)
        except:
            return HttpResponse('Only Fresher can book meetings')

        date_time = request.POST.get('date_time')
        # price will also be calculated on server side after this.
        
        technologies = ','.join(request.POST.getlist('technologies'))

        try:
            meeting = ProFrehserMeeting(
            prof         = prof,
            fresher      = fresher,
            designation  = request.POST.get('designation'),
            date_time    = timezone.datetime.fromisoformat(date_time),
            skills       = technologies,
            channel_name = 'car',
            price        = len(technologies.split(','))*128,
            mode         = 'PRI'   #givn by profesnl about the student #Approved by Professional for meeting
            )

            meeting.save()
                
            
            return  redirect('interview_buying',pfmid = meeting.id) 

        except:
            return HttpResponse('Sorry, meeting not registered')

    form = ClassFlyInterviewForm(skills = skills, dates = dates)
    
    

    title = "ClassFly Interview"
    text  = """
    <h5 style="text-align: center;">You can apply for jobs in our portal only if you pass in this interview,
    So, be ready before youapply to this interview.</h5>
    <br>
    <br>
    <h4 style="text-align: center;">Once you book the meeting</h4>
    <br>
    <p style="text-align: center;">You will receive message from our Professional regarding confirmation and tips for interview preparation.<p>

    """
    return render(request,'dform.html',context={'form':form,'title':title,'text':text})    #useapp templates signupcopy.html



# function to reject the interview by professional
@login_required
@usertype
@api_view(['GET'])
def reject_meeting(request,mid):
    if ProFrehserMeeting.objects.filter(id = mid).count() == 0:
        return Response(data={'message':'Not found'},status=400)

    meeting = ProFrehserMeeting.objects.get(id=mid)

    meeting.rejected = True
    meeting.save()

    return Response(data={'message':'success'})








