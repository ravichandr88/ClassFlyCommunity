from django.shortcuts import render,HttpResponse,Http404, redirect
from .models import Prfessional, ProFrehserMeeting, Fresher
from .forms import ClassFlyInterviewForm
import datetime
# Create your views here.



# In this file we have built functions to support
#  professional search, 
#  professional profile
#  watching pro interview videos
#  booking meetings


# Homepage for searching professionals

def search_professional(request,query=''):
    
    profs = set()


    if request.method == 'GET':
        profs = Prfessional.objects.all()[:10]

        return render(request,'search_pro/pro_search.html',context={'profs':profs})

    else:
        designation = request.POST['designation']
        city        = request.POST['city']
        skill       = request.POST['skill']
        company     = request.POST['company']


        
        profs = list(Prfessional.objects.filter(city__icontains = city).filter( skills__icontains = skill).filter(company__icontains = company).filter(designation__icontains = designation))
            
    
    

    return render(request,'search_pro/pro_search.html',context={'profs':profs,'skill':skill,'city':city,'company':company,'designation':designation})


def fresher_dash(request):
    p = ProFrehserMeeting.objects.all()

    today = datetime.datetime.now()
    user = Fresher.objects.get(user__username = request.user)
    return render(request,'dashboard/dist/index.html', context={'meetings':p,'today':today,'self':user})




def pro_dash(request):
    
    return render(request,'dashboard/dist/index.html')



def pro_profile(request,pro):
    pro = pro.split('_')[1]

    # print(pro)
    if Prfessional.objects.filter(user__username = pro).count() == 0:
        raise Http404

    prof = Prfessional.objects.get(user__username = pro)
    exps = prof.experience.all()

    pro_user  = prof.user
    return render(request,'pro_profile/pro_profile.html', context={'prof':pro,'exps':exps,'pro_user':pro_user})



def book_interview(request, prof):  # page 22
    
    prof = prof.split('_')[1]

    if prof == '' or Prfessional.objects.filter(user__username = prof).count() == 0:
        raise Http404


    prof = Prfessional.objects.get(user__username = prof)

    skills = prof.skills

    # lambda function to get the dates of the weekday given
    onDay = lambda date, day: date + datetime.timedelta(days=(day-date.weekday()+7)%7)
    days = {'MON':0,'TUE':1,'WED':2,'THU':3,'FRI':4,'SAT':5,'SUN':6}
    dates =[((onDay(datetime.datetime.now(),days[i.meet]).strftime('%Y-%m-%d') + ' ' +i.time.strftime('%H:%M')), str(i.meet +'  ('+onDay(datetime.datetime.now(),days[i.meet]).strftime('%m/%d/%Y')+') -> '+i.time.strftime('%H:%M %p')) ) for i in prof.prof_interview.all()]
    # 2021-07-07 03:43
    print(dates[0][0])
    
    if request.method == 'POST':
        

        date_time = request.POST.get('date_time')
        # price will also be calculated on server side after this.
        
        price = request.POST.get('price')
        technologies = ','.join(request.POST.getlist('technologies'))

        print(date_time, price, technologies)

        ProFrehserMeeting(
        prof         = prof,
        fresher      = Fresher.objects.get(user__username = request.user),
        date_time    = datetime.datetime.fromisoformat(date_time),
        skills       = technologies,
        channel_name = 'car',
        price        = 100,
        mode         = 'PRI'   #givn by profesnl about the student #Approved by Professional for meeting
        ).save()
               
        return  redirect('f_dashboard') 


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














