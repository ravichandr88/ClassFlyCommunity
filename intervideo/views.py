from django.shortcuts import render,HttpResponse,Http404
from django.conf import settings
import requests
import json
from django.contrib.auth.models import User
from .forms import JobPostForm, JobApplyForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from itertools import chain

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import requests
from requests.auth import HTTPBasicAuth


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Jobpost, Applicantion, Payment ,ResumePurchase ,MeetingPurchase , FresherInvited, VideoPurchase, InterviewSearch, InterviewVideo
from fresher.models import ProFrehserMeeting, Meeting, MeetingActive
from interview.models import Prfessional, Fresher, HRaccount, Company, ProfessionalInterview
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,Http404

import json

from chatt.views import usertype



# REST API at 566

def hraccount(function):
    # @wraps(function)
    def inner(request, *args, **kwargs):
        
        user = User.objects.get(username = request.user)
        
        if HRaccount.objects.filter(user = user).count() == 1 :
            
            if Company.objects.filter(created_by = user).count() == 1 and  Company.objects.get(created_by = user).verified :

                return function(request, **kwargs)

            elif not Company.objects.get(created_by = user).verified:

                return HttpResponse('HR account not activated, Still verifying under process.')
        
        return HttpResponse('Not a HR account ')

    return inner




# Function to check whether the skills are 90% similar or not
def skillsmatch(job,fresher):
    j_list = job.split(',')         #skills in job
    a_list = fresher.split(',')     #skills in applicant
    a_in_j = 0                      # applicant skills found in job post
                       
    for i in a_list:
        if i in j_list:
            a_in_j += 1
    
    if a_in_j >= len(j_list) - 3:
        return True
    
    return False


# Create your views here.
# REST API
@login_required
@usertype
def video_player(request,pfmid = 0, prof=False):
# pfmid = ProFresherMeeting ID, prof
# user type -> pro,fre,hra
    user_type = 'none'

    if request.method == 'GET' and pfmid == 0:
        meetings = ProFrehserMeeting.objects.filter(~Q(feedback = ''),approved = True)[:10]
        message = 'New Interview Videos'
        if len(meetings) == 0:
            message = 'Sorry, No interviews found'

        return render(request,'videoplayer_now.html', context={'message':message,'video':False,'meetings':meetings,'user_type':user_type})


    

    if request.method == 'POST':

        data = request.POST.dict()

        # Table InterviewSearch, keep record for all the queries done by user
        InterviewSearch(
            user =              User.objects.get(username = request.user), 
            pro_name =          data['pro_name'],
            pro_designation =   data['pro_designation'],
            skills =            data['skills']       
            ).save()
        
        
        meetings  =   ProFrehserMeeting.objects.filter(~Q(feedback = ''), approved = True, prof__user__first_name__icontains = data['pro_name'])
        
        meetings  =   meetings.filter(prof__designation__icontains = data['pro_designation'])
        message = 'New Interview Videos'

        for i in data['skills'].split(','):
            meetings = meetings.filter(skills__icontains = i)
        
        if len(meetings) == 0:
            message = 'No matching videos found, Will SMS you when these topics interviews are done. Thank You'
        # variable video is for activating the video player
        #message is message given based on the videos quer, ex: no videos found
        return render(request,'videoplayer_now.html', context={'message':message,'video':False,'meetings':meetings})


    resp = ''
    pro_meeting = ''

    meetings = ProFrehserMeeting.objects.filter(~Q(feedback = ''), approved = True).filter(~Q(id=pfmid)).order_by('-id')[:10]


# Code for watching the video
    if pfmid != 0:

        if ProFrehserMeeting.objects.filter(id = pfmid).count() == 0:
                raise Http404 
        
        pro_meeting = ProFrehserMeeting.objects.get(id = pfmid)

        # Code to record the video viewing count for the user and meeting
        
        video = InterviewVideo.objects.get_or_create(
                video = pro_meeting,
                user = User.objects.get(username = request.user)
            )[0]
        

        try:
            resp = get_video_otp(pro_meeting.meeting_details.vdo_id)
            print(resp)
            if str(resp.status_code) != '200':
                raise Http404
        except:        
            meetings = ProFrehserMeeting.objects.filter(~Q(feedback = ''),approved = True)[:10]
            print(resp,'00000000000000000000')
            return render(request,'videoplayer_now.html', context={'message':'Sorry, Video not loaded','video':False,'meetings':meetings})


        
        
    else:
        meetings = ProFrehserMeeting.objects.filter(~Q(feedback = ''),approved = True)[:10]

        return render(request,'videoplayer_now.html', context={'message':'Candidate not yet interviewed','video':False,'meetings':meetings})


    return render(request,'videoplayer_now.html', context={'video':True,'otp':resp.json()['otp'],'playbackInfo':resp.json()['playbackInfo'],'meeting':pro_meeting,'meetings':meetings})



# Code to get the otp for the video to play from VDO
def get_video_otp(id):
        
    url = "https://dev.vdocipher.com/api/videos/" + id+ "/otp"

    headers = {
            'Authorization': "Apisecret " + settings.VDO_API ,
            'Content-Type': "application/json",  
            'Accept': "application/json"
            }

    data = {
        # "ttl": 300,
    }

    resp = requests.post(url,headers = headers, data = data)

    return resp


@login_required
@usertype
@hraccount
def hr_dashboard(request, id = '', skill='', status = 0):
# status -> 1 -> select, 2 -> shortlist, 3 -> reject
# skill will be 'not' if user has not entered anything , but is expecting to filter based on status of the resume
    if skill == 'not':
        skill = ''
    
        

    hr = HRaccount.objects.get(user__username = request.user)
    jobs = hr.job_posted.filter(active= True,deleted = False)
    
  
    applicants = jobs[0].applicants.filter(available = True) if len(jobs) > 0 else [] 
    
    
    if id != '' and hr.job_posted.filter(id=id,deleted = False).count() != 0:
        
        
        applicants = hr.job_posted.get(id = id).applicants.filter(available = True)

    job = ''    #blank id for current job id this function is dealing with

    if len(jobs) > 0:
        if id != '':
            job = hr.job_posted.get(id = id)
        else:
            job = jobs[0]


    # Filter the applicants based on the skills
    skills =  skill.split(',')

    if len(applicants) > 0:
        applicants = applicants.filter(fresher__skills__icontains = skills[0]) #filter to get required skills

    
        for i in skills[1:]:
            applicants = applicants | applicants.filter(fresher__skills__icontains = i) 


    # status -> 1 -> select, 2 -> short, 3 -> reject
    options = {1:'select',2:'short',3:'reject'}


    if status in options.keys():
        applicants =  applicants.filter(status = options[status])
    
    pass_applicants = []    #This is dummy empty query Model List to start adding the actual data
    
# Code to filter all the interview passed candidates to show in the begining,
# Second the 'appllicants' will be showed in the dashboard
    for i in applicants:
        for j in i.fresher.fresher_interview.all():
            if j.passed:
                pass_applicants   = applicants.filter(id=i.id)  if len(pass_applicants) == 0 else pass_applicants | i
                applicants = applicants.filter(~Q(id=i.id))
                break
            
    print(job)
    data={
        'jobs':jobs,
        'pass_applicants':pass_applicants,
        'applicants':applicants,
        'job_id':'' if job == '' else job.id,
        'job':job,
        'skills':skill 
    }

    return render(request,'hrdashboard.html',context=data)


# Code for HR to search for applicants in ClassFly Interviewed candidates Database
@login_required
@hraccount
@usertype
def applicants_search(request,id=0,skill = ''):
# First get the skills and filter the freshers data for those skills for the respective job posted
#id -> is for querying from Jobpost model
    
    # If the skill is not, it means it is an empty query
    if skill == 'not':
        skill = ''

    hr = HRaccount.objects.get(user__username = request.user)

    if hr.job_posted.filter(id = id).count() == 0:
        raise Http404

    
    jobs = hr.job_posted.filter(active = True, deleted = False)    # this onject list is used for labeling about which wjob is being shown in the webpage
    job = jobs.get(id = id)

    #Instead of applicants for the job posted, we will be showing the candidates list for
    # Filter based on skills presented for JobPost


    skills =[i  for i in job.skills.split(',') if  not len(i) < 2 ]
    applicants = Fresher.objects.filter(skills__icontains = skills[0])
    
    for i in skills[1:]:
        applicants = applicants | Fresher.objects.filter(skills__icontains = i)
    
    if skill != '':
        skills = skill.split(',')
        for i in skills[1:]:
            applicants = applicants | applicants.filter(skills__icontains = i)
    
# skills of all the applicants available
    applicant_skills = [j for i in applicants for j in i.skills.split(',')]
    applicant_skills = set([i.replace(" ",'') for i in applicant_skills])
    
# streams of all the applicants
    applicant_branch = set([i.branch for i in applicants])

# cities of all applicants
    applicant_city = set([i.city for i in applicants]) 

    data={
        'jobs_posted':jobs,
        'applicant_skills':applicant_skills,
        'applicant_branch':applicant_branch,
        'applicant_city': applicant_city,
        'applicants':applicants[:30],
        'job':job,
        'skills':skill 
    }

    return render(request, 'applicant_search.html', context=data)



# Page to post a new job

@login_required
@hraccount
@usertype
def jobpost(request,job_id = 0,edit = 0):
    
    form = JobPostForm()
    hr = HRaccount.objects.get(user = User.objects.get(username = request.user))

    if request.method == 'GET' and edit == 1:
        
        if Jobpost.objects.filter(id = job_id).count() == 0:
            return HttpResponse('Job with that ID not found')

        jobpost = Jobpost.objects.get(id = job_id)

        form.initial['designation'] = jobpost.designation 
        form.initial['role'] = jobpost.role            
        form.initial['industry_type'] = jobpost.industry_type 
        form.initial['employment_type'] = jobpost.employment_type  
        form.initial['edu_ug'] = jobpost.edu_ug    
        form.initial['edu_pg'] = jobpost.edu_pg        
        form.initial['edu_doc'] = jobpost.edu_doc      
        form.initial['skills'] = jobpost.skills
        form.initial['city'] = jobpost.city   
        form.initial['description'] = jobpost.description    
        form.initial['requirement'] = jobpost.requirement     
        form.initial['min_salary'] = jobpost.min_salary 
        form.initial['max_salary'] = jobpost.max_salary   
        form.initial['min_experience'] = jobpost.min_exp   
        form.initial['max_experience'] = jobpost.max_exp       
        form.initial['question1'] = jobpost.qu1   
        form.initial['question2'] = jobpost.qu2   
        form.initial['question3'] = jobpost.qu3   

        data = {'form':form,
            'title':'Post a Job'}
        return render(request, 'formpage.html', context=data)
        


    if request.method == 'POST':
        form = JobPostForm(request.POST)
        
        if form.is_valid():
            # 'designation', 'skills', 'description', 'requirement', 'min_experience','max_experience','min_salary','max_salary','question1','question2','question3'
            Jobpost(
                hr              =  hr,
                designation     =  form.cleaned_data['designation'],
                role            =  form.cleaned_data['role'],
                industry_type   =  form.cleaned_data['industry_type'],
                employment_type =  form.cleaned_data['employment_type'],
                edu_ug          =  form.cleaned_data['edu_ug'],
                edu_pg          =  form.cleaned_data['edu_pg'],
                edu_doc         =  form.cleaned_data['edu_doc'],
                skills          =  form.cleaned_data['skills'],
                city            =  form.cleaned_data['city'],
                description     =  form.cleaned_data['description'],
                requirement     =  form.cleaned_data['requirement'],
                min_salary      =  form.cleaned_data['min_salary'],
                max_salary      =  form.cleaned_data['max_salary'],
                min_exp         =  form.cleaned_data['min_experience'],
                max_exp         =  form.cleaned_data['max_experience'],
                qu1             =  form.cleaned_data['question1'],
                qu2             =  form.cleaned_data['question2'],
                qu3             =  form.cleaned_data['question3']
            ).save()
            return redirect('hrdashboard')
        
    data = {'form':form,
            'title':'Post a Job'}
    return render(request, 'formpage.html', context=data)

@login_required
@hraccount
@api_view(['GET'])
def delete_jobpost(request,id):
    if Jobpost.objects.filter(id = id).count() == 0:
        return Response(data={'message':'Job post not found '}, status=400)
    
    job = Jobpost.objects.get(id=id)

    job.deleted = True
    job.deleted_date = timezone.now()
    job.save()

    return Response(data={'message':'success'})

#  to see the posted job in detail
@login_required
@usertype
def jobdetails(request,id = 0):

    if id == 0:
        raise Http404
    
    if Jobpost.objects.filter(id = id).count() == 0:
        return render(request, 'formpage.html', context={'title':'Job not Found','submit':False})   #'submit' is for showing go back button title
    
    
    job =  Jobpost.objects.get(id = id)

    company = Company.objects.get(created_by = job.hr.user)

    form = JobApplyForm(ques1=job.qu1,ques2=job.qu2,ques3=job.qu3)
    
    if job.applicants.filter(fresher__user__username = 'bunny').count() == 1:
        form = None
        # return render(request, 'formpage.html', context={'title':'You already applied','submit':False})
    
    data={
        'title':job.designation,
        'details':True, # boolean to save 
        'job' : job,
        'company':company,
        'form':form
        }
        

    if request.method == 'POST':
        
        form = JobApplyForm(request.POST)
 
        #Now validate whether the fresher is interviewed or not,
        #  and if skills are matching or not 
        if Fresher.objects.filter(user__username = request.user).count() == 0:
            data['error'] = 'Not Signed Up'

            return render(request, 'formpage.html', context=data)
        
        fresher = Fresher.objects.get(user__username = request.user)

        if fresher.fresher_interview.filter(passed = True).count() == 0:
            data['error'] = 'Not Yet Passed Interview'

            return render(request, 'formpage.html', context=data)
        
        if not skillsmatch(job.skills,fresher.skills):
            data['error'] = 'Not Enough Skills'
            
            return render(request, 'formpage.html', context=data) 

        form = JobApplyForm(request.POST)

        

            
        Applicantion(
                job         = job,
                fresher     = fresher,
                ans1        = request.POST['question1'],
                ans2        = request.POST['question2'],
                ans3        = request.POST['question3']
            ).save()

        if FresherInvited.objects.filter(job = job, fresher = fresher).count() != 0:
            freshinvite = FresherInvited.objects.get(job = job, fresher = fresher)
            freshinvite.accepted = True
            freshinvite.save()
        
        return redirect('jobsearh')

    return render(request, 'formpage.html', context=data)


@usertype
def job_search(request,desig = '',city = '',salary = ''):

    jobs = []

    if city == '' and desig == '' and salary == '':
        jobs =    Jobpost.objects.all()
    else:
        ''' we have added '-' symbols to catch the url parameters when empty,
        remove the, before query  '''
        desig=desig[:-1]
        city=city[:-1]
        salary=salary[:-1]

        designation = desig.split(',')

        jobs = Jobpost.objects.filter(designation__icontains = designation[0])
        jobs = jobs | Jobpost.objects.filter(skills__icontains = designation[0])

        for i in designation[1:]:
        
            jobs = jobs | Jobpost.objects.filter(designation__icontains=i)
            print(jobs)
            jobs = jobs | Jobpost.objects.filter(skills__icontains=i)

        jobs = jobs.filter(city__icontains = city)

            
    return render(request, 'new_job_search.html', context={'jobs':jobs,'designation':desig,'city':city})



@usertype
def old_job_search(request,desig = '',city = '',salary = ''):

    jobs = []

    if city == '' and desig == '' and salary == '':
        jobs =    Jobpost.objects.all()
    else:
        ''' we have added '-' symbols to catch the url parameters when empty,
        remove the, before query  '''
        desig=desig[:-1]
        city=city[:-1]
        salary=salary[:-1]

        designation = desig.split(',')

        jobs = Jobpost.objects.filter(designation__icontains = designation[0])
        jobs = jobs | Jobpost.objects.filter(skills__icontains = designation[0])

        for i in designation[1:]:
        
            jobs = jobs | Jobpost.objects.filter(designation__icontains=i)
            print(jobs)
            jobs = jobs | Jobpost.objects.filter(skills__icontains=i)

        jobs = jobs.filter(city__icontains = city)

            
    return render(request, 'job_search.html', context={'jobs':jobs,'designation':desig,'city':city})







# jobs input auto complete REST API
@api_view(['GET'])
def autocompleteModel(request,key=''):
    
    if key=='':
        return Response(data={'data':[]})

    search_qs = Jobpost.objects.filter(designation__startswith=key)
    results = [] 
    for r in search_qs:
        results.append(r.designation)
    print(results)
    return Response(data={'data':results})


# Function to chage the status of the applications
# Done by HR looking at applicants
@login_required
@hraccount
@api_view(['GET'])
def change_status(request, id='', status = ''):
    # status should be -> short, reject, select. else error

    if Applicantion.objects.filter(id = id).count() == 0 or id == '' or status == '' or not (status =='short' or status == 'reject' or status == 'select' ):
        return Response(data={'message':'error'})
    
    applicant = Applicantion.objects.get(id = id)
    applicant.status = status
    applicant.save()

    return Response(data={'message':'success'})


@login_required
@hraccount
@api_view(['GET'])
def invite_fresher(request, fid = 0, jobid = 0):

    if Fresher.objects.filter(id = fid).count() == 0 or Jobpost.objects.filter(id = jobid).count() == 0:
        return Response(data={'message':'error'}, status= 400)

    fresher = Fresher.objects.get(id = fid)
    job = Jobpost.objects.get(id=jobid)
    
    job_link = str(request.get_host()) + '/job/' + str(jobid)

    invite_email(job_link, fresher.user.email)

    if FresherInvited.objects.filter(job = job,fresher = fresher).count() == 0:
        FresherInvited(
        job     = job,
        fresher = fresher
        ).save()

    return Response(data={'message':'success'})


def videocall(request):
   
    return render(request,'videocall.html',context={}) 


def invite_email(job_url,to_email):
    
    return
    subject = 'Invitaion for Job'
    message = f'You are been invited by the HR to apply this Job. <a href="' + job_url +'" >Job Link </a>'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email, ]
    send_mail( subject, message, email_from, recipient_list )


def error_email(error):
    
    return
    subject = 'Error'
    message = f'Error while paying: ' + error +'.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ravichandrareddy88@gmail.com', ]
    send_mail( subject, message, email_from, recipient_list )



@login_required
@usertype
def jobs_applied(request):
    
    if Fresher.objects.filter(user__username = request.user).count() == 0:
        raise Http404
    fresher  = Fresher.objects.get(user__username = request.user)
    applicants =[i for i in fresher.jobs_applied.all()]
    invited_jobs = fresher.invited_to.filter(accepted = False)

    data={
        'jobs':applicants,
        'invitations':invited_jobs,
        'applicants':applicants,
        'job_id':'',
        'job':None,
        'skills':[] 
    }

    return render(request, 'jobs_applied.html', context = data)


@login_required
@usertype
def video_buying(request, vdo_id = 0):
    #1 check whether vdo exists
    if vdo_id == 0 or ProFrehserMeeting.objects.filter(id = vdo_id).count() == 0:
        raise Http404
    
    #2 Check if the meeting is done or not
    meeting = ProFrehserMeeting.objects.get(id = vdo_id)
    
    try:
        if not meeting.meeting_details.record_stopped:
            return HttpResponse('Meeting not yet done')
    except:
        return HttpResponse('Meeting not yet done')
    
    #3 If User has not watched video, then create InterviewVideo row and add user
    intervideo = InterviewVideo.objects.get_or_create(
            user    = User.objects.get(username = request.user),
            video   = meeting
        )[0]
        
    #4 Now create payment object for transaction
    
    # 4a We need current Payment id for recipt, so if there are no rows in tbale, get the id = 1
    reciept_id = 0  # receipt is formed by that row id and ProFreMeeting id and service type
    
    try:
        reciept_id = Payment.objects.latest('id').id + 1
    except:
        reciept_id = 1
    

    payment = Payment(
        receipt                 = 'VDO000' + str(reciept_id) + '_0' + str(meeting.id) ,
        user                    = User.objects.get(username = request.user),
        service                 = meeting.prof.designation + '| interview |' + meeting.designation,
        amount                  = (len(meeting.skills.split(','))*20),
        service_type            = 'VDO',
        )
    payment.tax             = round((payment.amount)*0.18,2)

    payment.total_amount    =  round(payment.tax + payment.amount )
    payment.save()

    # 4b Get the order_id from the razorpay by getting 
    
    data =    {
        "amount": payment.total_amount * 100,
        "currency": "INR",
        "receipt": payment.receipt
        } 

    resp = requests.post('https://api.razorpay.com/v1/orders',
            headers = {'content-type': 'application/json'},data = json.dumps(data),
            auth = HTTPBasicAuth(settings.KEY_ID, settings.KEY_SECRET))

    if resp.status_code != 200:
        message = str(resp.json()) + 'User: '+ request.user 
        error_email(message)

        return HttpResponse('Sorry, Payment not done, Situation is reported. Please start again. Message {}'.format(resp.json()['error']['description']))
    print(resp.json())
# 4c prepare receipt id
    payment.razor_order_id = resp.json()['id']

    payment.save()

    video = VideoPurchase(
        video = intervideo,
        payment = payment
    )

    video.save()

    
    return render(request,'payment.html', context={'video':video,'payment':payment})


# function for booking the meetings
@login_required
@usertype
def purchase_interview(request, pfmid = 0):

    meeting = '' #ProFreshermeeting object

    try:
        meeting = ProFrehserMeeting.objects.get(id = pfmid)
    except:
        raise Http404

    # Check if the payment is already done or not
    if MeetingPurchase.objects.filter(meeting__id = meeting.id).count() != 0:
        if MeetingPurchase.objects.get(meeting__id = meeting.id).payment.razorpay_signature != '':
            return HttpResponse('Payment is already done ')

    # Create a payment object, and get razorpayid
    try:
        reciept_id = Payment.objects.latest('id').id + 1
    except:
        reciept_id = 1

    payment = Payment(
        receipt                 = 'INT000' + str(reciept_id) + '_0' + str(meeting.id) ,
        user                    = User.objects.get(username = request.user),
        service                 = meeting.prof.designation + '| interview for |' + meeting.designation +' | position.',
        amount                  = (len(meeting.skills.split(','))*128),
        service_type            = 'INT',
        )
    payment.tax             = round((payment.amount)*0.18,2)
    payment.total_amount    =  round(payment.tax + payment.amount )
    payment.save()

    # 4b Get the order_id from the razorpay by getting 
    
    data =    {
        "amount": payment.total_amount * 100,
        "currency": "INR",
        "receipt": payment.receipt
        } 

    resp = requests.post('https://api.razorpay.com/v1/orders',
            headers = {'content-type': 'application/json'},data = json.dumps(data),
            auth = HTTPBasicAuth(settings.KEY_ID, settings.KEY_SECRET))

    if resp.status_code != 200:
        message = str(resp.json()) + 'User: '+ request.user 
        error_email(message)

        return HttpResponse('Sorry, Payment not done, Situation is reported. Please start again. Message {}'.format(resp.json()['error']['description']))

# 4c prepare receipt id
    payment.razor_order_id = resp.json()['id']
    payment.save()

    meeting_payed = ''
    try:
        print('inisede try')
        meeting_payed = MeetingPurchase(
        meeting  = meeting,
        payment  = payment
        )

        meeting_payed.save()
    except:
        print('inside exception')
        meeting_payed = MeetingPurchase.objects.get(meeting__id = meeting.id)
        meeting_payed.payment = payment
        
        meeting_payed.save()

    print(meeting_payed,payment) 
    return render(request, 'payment.html',context={'meeting':meeting_payed,'payment':payment})


# Function to buy resume subscription
@login_required
def resume_purchase(request,skills = 0):

    if skills == 0 and skills != 6 and skills != 16 and skills != 25:
        raise Http404

    user = User.objects.get(username = request.user)

    # Create a payment object, and get razorpayid
    try:
        reciept_id = Payment.objects.latest('id').id + 1
    except:
        reciept_id = 1

    payment = Payment(
        receipt                 = 'RES000' + str(reciept_id) + '_0' + str(user.id) ,
        user                    =  User.objects.get(username = request.user),
        service                 = '30 Downloads of ' + str(skills) + ':Skills Resumes',
        amount                  =  39 if skills == 6 else 99 if skills == 16 else 149,
        service_type            = 'RES',
        )

    payment.tax             = round((payment.amount)*0.18,2)
    payment.total_amount    = round(payment.tax + payment.amount )

    payment.save()

    # 4b Get the order_id from the razorpay by getting 
    
    data =    {
        "amount": payment.total_amount * 100,
        "currency": "INR",
        "receipt": payment.receipt
        } 

    resp = requests.post('https://api.razorpay.com/v1/orders',
            headers = {'content-type': 'application/json'},data = json.dumps(data),
            auth = HTTPBasicAuth(settings.KEY_ID, settings.KEY_SECRET))

    if resp.status_code != 200:
        message = str(resp.json()) + 'User: '+ request.user 
        error_email(message)

        return HttpResponse('Sorry, Payment not done, Situation is reported. Please start again. Message {}'.format(resp.json()['error']['description']))

# 4c prepare receipt id
    payment.razor_order_id = resp.json()['id']
    payment.save()


    

    resume = ResumePurchase(
        user = User.objects.get(username = request.user),
        payment = payment,
        skills_count = skills
    )
    resume.save()


    return render(request, 'payment.html', context={'resume':resume, 'payment': payment})



# Function for payment
@login_required
@csrf_exempt
def payment(request):

    data = request.POST.dict()
    print(data)
    try:
        # Check if order id is present int the table
        if Payment.objects.filter(razor_order_id = data['razorpay_order_id']).count() == 0:
            return HttpResponse('Payment was not placed, ')
    except:
        raise Http404

    payment = Payment.objects.get(razor_order_id = data['razorpay_order_id'])
    payment.razorpay_signature = data['razorpay_signature']
    payment.razorpay_payment_id = data['razorpay_payment_id']
    payment.save()

    return redirect('pro_search')
    # return render(request,'payment.html', context={})


# Complete bought services by anyone.
@login_required
@usertype
def paid_services(request):

    payments = Payment.objects.filter(~Q(razorpay_signature = ''),user__username = request.user)
    
    return render(request, 'paid_services.html',context={'payments':payments})

# All purchasing options
@login_required
@usertype
def pricing(request):

    return render(request,'pricing.html')




@login_required
@usertype
def purchased_videos(request, pfmid = 0, prof=False):
    # pfmid = ProFresherMeeting ID, prof
    # user type -> pro,fre,hra
    user_type = 'none'

    # if request.method == 'GET' and pfmid == 0:
    #     meetings = ProFrehserMeeting.objects.filter(~Q(feedback = ''),approved = True)[:10]
    #     message = 'New Interview Videos'
    #     if len(meetings) == 0:
    #         message = 'Sorry, No interviews found'

    #     return render(request,'purchased_videos.html', context={'message':message,'video':False,'meetings':meetings,'user_type':user_type})


    

  
    resp = ''
    pro_meeting = ''

    meetings_available = set()

    meetings_expired   = set()
    print(request.user)
    meetings = InterviewVideo.objects.filter(user__username = request.user)

    for i in meetings:

        if i.watch():
            meetings_available.add(i.video)

        else:
            meetings_expired.add(i.video)
        

# Code for watching the video
    if pfmid != 0:

        if ProFrehserMeeting.objects.filter(id = pfmid).count() == 0:
                raise Http404 
        
        pro_meeting = ProFrehserMeeting.objects.get(id = pfmid)

        # Code to record the video viewing count for the user and meeting
        
        video = InterviewVideo.objects.get_or_create(
                video = pro_meeting,
                user = User.objects.get(username = request.user)
        )[0]

        #Check wehther user has purchased the video and valid or not 
        for i in video.video_purchase.all():
            if i.valid():
                try:
                    resp = get_video_otp(pro_meeting.meeting_details.vdo_id)
                    print(resp)
                    if str(resp.status_code) != '200':
                        raise Http404
                    
                except:        
                    # Dummy meeting object queryset
                    meetings = []

                    for i in InterviewVideo.objects.filter(user__username = request.user):
                        for j in  i.video_purchase.all():
                            if j.valid():
                                meetings.append(i.video)
        
                    print(meetings)
                    return render(request,'purchased_videos.html', context={'message':'Sorry, Video not loaded','video':False,'meetings_available':meetings_available,'meetings_expired':meetings_expired})

        #If the user has not permission to watch the video, return , not allowed
        if resp == '':
            print(meetings_available,meetings_expired)

            return render(request,'purchased_videos.html', context={'message':'Sorry,Validity might have expired','video':False,'meetings_available':meetings_available,'meetings_expired':meetings_expired})


        
        
    else:
        meetings = ProFrehserMeeting.objects.filter(~Q(feedback = ''),approved = True)[:10]

        return render(request,'purchased_videos.html', context={'message':'Candidate not yet interviewed','video':False,'meetings_available':meetings_available,'meetings_expired':meetings_expired})


    return render(request,'purchased_videos.html', context={'video':True,'otp':resp.json()['otp'],'playbackInfo':resp.json()['playbackInfo'],'meeting':pro_meeting,'meetings_available':meetings_available,'meetings_expired':meetings_expired})

