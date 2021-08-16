from django.shortcuts import render,HttpResponse,Http404
from django.conf import settings
import requests
import json
from django.contrib.auth.models import User
from .forms import JobPostForm, JobApplyForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.core.mail import send_mail
from django.conf import settings


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Jobpost, Applicantion, FresherInvited
from fresher.models import ProFrehserMeeting, Meeting, MeetingActive
from interview.models import Prfessional, Fresher, HRaccount, Company
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,Http404

import json


def hraccount(function):
    # @wraps(function)
    def inner(request, *args, **kwargs):
        user = User.objects.get(username = request.user)

        if HRaccount.objects.filter(user = user).count() == 1 :
            
            if Company.objects.filter(created_by = user).count() == 1 and  Company.objects.get(created_by = user).verified :

                return function(request, **kwargs)
        
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

def video_player(request,pfmid = 3):


    if ProFrehserMeeting.objects.filter(id = pfmid).count() == 0:
        print('line 17')
        raise Http404
    
    pro_meeting = ProFrehserMeeting.objects.get(id = pfmid)

    if pro_meeting.meeting_details.vdo_id is  None:
        return HttpResponse('Not yet interviewed')

    resp = get_video_otp(pro_meeting.meeting_details.vdo_id)

    if str(resp.status_code) != '200':
        print(resp.json()) 
        raise Http404

     
    return render(request,'videoplayer_now.html', context={'otp':resp.json()['otp'],'playbackInfo':resp.json()['playbackInfo']})




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
@hraccount
def hr_dashboard(request, id = '', skill='', status = 0):
# status -> 1 -> select, 2 -> shortlist, 3 -> reject
# skill will be 'not' if user has not entered anything , but is expecting to filter based on status of the resume
    if skill == 'not':
        skill = ''
    
        


    hr = HRaccount.objects.get(user__username = request.user)
    jobs = hr.job_posted.filter(active= True)
    
    applicants = jobs[0].applicants.filter(available = True) if len(jobs) > 0 else [] 

    
    if id != '' and hr.job_posted.filter(id=id).count() != 0:
        
        
        applicants = hr.job_posted.get(id = id).applicants.filter(available = True)

    job = ''    #blank id for current job id this function is dealing with

    if len(jobs) > 0:
        if id != '':
            job = hr.job_posted.get(id = id)
        else:
            job = jobs[0]


    # Filter the applicants based on the skills
    skills =  skill.split(',')


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
            
    
    data={
        'jobs':jobs,
        'pass_applicants':pass_applicants,
        'applicants':applicants,
        'job_id':job.id,
        'job':job,
        'skills':skill 
    }

    return render(request,'hrdashboard.html',context=data)


# Code for HR to search for applicants in ClassFly Interviewed candidates Database
@login_required
@hraccount
def applicants_search(request,id=0,skill = ''):
# First get the skills and filter the freshers data for those skills for the respective job posted
#id -> is for querying from Jobpost model
    
    # If the skill is not, it means it is an empty query
    if skill == 'not':
        skill = ''

    hr = HRaccount.objects.get(user__username = request.user)

    if hr.job_posted.filter(id = id).count() == 0:
        raise Http404

    
    jobs = hr.job_posted.filter(active = True)    # this onject list is used for labeling about which wjob is being shown in the webpage
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
        'jobs':jobs,
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
def jobpost(request):
    
    form = JobPostForm()
    hr = HRaccount.objects.get(user = User.objects.get(username = request.user))


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

        
    data = {'form':form,
            'title':'Post a Job'}
    return render(request, 'formpage.html', context=data)


#  to see the posted job in detail
@login_required
def jobdetails(request,id = 0):

    if id == 0:
        raise Http404
    
    if Jobpost.objects.filter(id = id).count() == 0:
        return render(request, 'formpage.html', context={'title':'Job not Found'})
    
    job =  Jobpost.objects.get(id = id)

    company = Company.objects.get(created_by = job.hr.user)

    form = JobApplyForm(ques1=job.qu1,ques2=job.qu2,ques3=job.qu3)
    
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

    
    
    return render(request, 'formpage.html', context=data)



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
