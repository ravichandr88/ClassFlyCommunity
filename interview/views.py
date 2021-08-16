from django.shortcuts import render,HttpResponse
from .forms import StudentForm,ProfessionalForm,HRForm,ProfessionalBankForm,ProfTimeTableForm,Experienc,ProIntervTime,CompanyForm
from django.contrib.auth.decorators import login_required
from .models import Fresher, Professinal_Interview_Time, HRaccount,Company,Experience,Professinal_Account_Details ,Prfessional,ProExperience, Professional_Meeting
from django.contrib.auth.models import User
from django.shortcuts import redirect



# Fresher Singup Page-3
# Create your views here.
@login_required
def student(request):
    """
    form values 
    college 
    branch 
    passout_year 
    skills
     exp_company_1 
    exp_work_1 
    exp_period_1 
    """
    
    form = StudentForm()    #preparing an empty form


    if request.method == 'POST':
        student = StudentForm(request.POST)
        

        if student.is_valid():
          fresher = Fresher(
            user             = User.objects.get(username = request.user),
            college          = student.cleaned_data['college'],
            branch           = student.cleaned_data['branch'],
            passout_year     = student.cleaned_data['passout_year'],
            about_yourself   = student.cleaned_data['about_yourself'],
            total_experience = int(student.cleaned_data['total_experience']),
            skills           = str(request.POST.getlist('skills')))
          fresher.save() 

          exp1 = student.exp(1)
          if exp1 != 0:
             exp1.applicant = fresher
             exp1.save()
            
          exp2 = student.exp(2)
          if exp2 != 0:
             exp2.applicant = fresher
             exp2.save()

          exp3 = student.exp(3)
          if exp3 != 0:
            exp3.applicant = fresher
            exp3.save()
        
# A special input, to get skills , we are providing extra html code.
    skills = """
                    <div id="extra"></div>
				<ul class=" wrap-input100 ">
					<li class="tags-new">
							<div class="wrap-input100 " >
								<h5>Skills</h5>
					  <input class="input100" type="text" placeholder="Skills"> 
					  </div>
					  Enter skills seperated by comma.
					</li>
				  </ul>"""
    return render(request,'form.html',context={'form':form, 'skills':skills})


# Professional Page-6
# Fresher Page-4

@login_required
def resumeview(request):

    # form = ResumeForm()
  
    next = '/pro/profile'

    return render(request,'form.1.html',context={'content':"Resume", 'next' : next})



# Function to signup the professional after verifying the sms and email otp
# Professional Signup Page-3


@login_required
#function to professional signup
def prosignup(request):
    
    #special input field for adding skills
    skills = """
                    <div id="extra"></div>
				<ul class=" wrap-input100 ">
					<li class="tags-new">
							<div class="wrap-input100 " >
								<h5>Skills</h5>
					  <input class="input100" type="text" placeholder="Skills"> 
					  </div>
					  Enter skills seperated by comma.
					</li>
				  </ul>"""
    form = ProfessionalForm()
    

    if request.method == 'POST':
        prof = ProfessionalForm(request.POST)

        if prof.is_valid():
          # print(prof)
          
          #prepare experience value
          exp = float( prof.cleaned_data['total_exp_year'] + '.' + prof.cleaned_data['total_exp_month'] )
          
          
          pro = Prfessional(
          user            = User.objects.get(username = request.user),
          company         = prof.cleaned_data['company'],
          designation     = prof.cleaned_data['designation'],
          city            = prof.cleaned_data['city'],
          stream          = prof.cleaned_data['stream'],
          college         = prof.cleaned_data['college'],
          language_spoke  = prof.cleaned_data['language_spoke'],
          about_yourself  = prof.cleaned_data['about_yourself'],
          total_exp_year  = exp,
          skills = str(request.POST.getlist('skills'))
          )

          pro.save()

          return redirect('/pro/exp')
        
        else:
  
          return render(request,'form.html',context={'form':prof,'skills':skills})
          
    form = ProfessionalForm()
    
    return render(request,'form.html',context={'form':form,'skills':skills})



# Professional Signup to acquire experience details of the professional
# Professional Signup Page-5

@login_required
#function to professional signup
def proexp(request):
    
    form = Experienc()


    if request.method == 'POST':
        data = request.POST.dict()
        keys = list(data.keys())[7:]
        n = 5
        l = [keys[i * n:(i + 1) * n] for i in range((len(keys) + n - 1) // n )]
        l = l[:-1]

        print(l)

        for i in l:
          # 'company1', 'designation1', 'project1', 'from1', 'to1'
          ProExperience(
            pro          = Prfessional.objects.get(user = User.objects.get(username = request.user)),
            company      = data[i[0]],
            designation  = data[i[1]],
            project      = data[i[2]],
            cfrom        = data[i[3]],
            cto          = data[i[4]]
          ).save() 

          # print(data[i[0]], data[i[0]], i[2], i[3], i[4])
          return redirect('/resume')



    
    card = """
    <cdiv class="go" id="butn">
						<h3>Company</h3>
						<h2>Designation</h2>
						<br>
						<p>Technologies and work done</p>
						<span>From - Till</span>
						<br>
						<br>
						</cdiv>
				"""


    skills = """
    <button class="login100-form-btn" type="button" id='add'>
							Add More 
						</button>
    """
    return render(request,'form.html',context={'form':form,'skills':skills,'card':card})



# Professional Page-8

import datetime

@login_required
def prof_initial_meet(request):
    form = ProIntervTime()

    if request.method == 'POST':
        print(request.POST['meet1_date'],request.POST['meet1_time'])

        # print(datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time']))
        
        
        Professional_Meeting(
          meet1 = datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time']),
          meet2 = datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time']),
          meet3 = datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time']),
          prof = Prfessional.objects.get(id=5)
        ).save()

        return redirect('pro_waiting')




    card = """  <h5 style="text-align: center;"> 
    Please provide your free time to connect with our 
    Experts and to be interviewed. </h5> <br><br> 
    <p style="text-align: center;"> 
    Please provide possible timings you are free, 
    and we will SMS the timings that our Experts agree on. </p> <br> """

    return render(request,'form.html',context={'form':form, 'card':card})


# Professional Signup Page-7
# Fresher Signup Page-5

@login_required
def profile_pic(request):
    
    next = ''

    # variable to point to next page
    if Prfessional.objects.filter(user__username = request.user).count() != 0:

        next = '/pro/meet'
    
    if Fresher.objects.filter(user__username = request.user).count() !=  0:
        next = '/applicant/dashboard'

    return render(request,'pic_crop.html', context={'next' : next})


# Company Account creation by HR or employee

# HR Singup Page-3
@login_required
def company_singup(request):
    
    form = CompanyForm()

    if request.method == 'POST':

        form = CompanyForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            Company(
              created_by              = User.objects.get(username = request.user),
              about                   = form.cleaned_data['about'],
              company_name            = form.cleaned_data['company_name'],
              address                 = form.cleaned_data['address'],
              city                    = form.cleaned_data['city'],
              state                   = form.cleaned_data['state'],
              company_linkedin_url    = form.cleaned_data['company_linkedin_url'],
              ).save()


            return redirect('hr_account_creation')


    return render(request,'form.html',context={'form':form})


# Company account creatoin done , now addding self account as HR for the company
# HR- account creatoin Page-4

@login_required
def hr_account_creation(request):
    
    form = HRForm()

    if request.method == 'POST':
          form = HRForm(request.POST)

          if form.is_valid():
            HRaccount(
              user             = User.objects.get(username = request.user),
              designation      = form.cleaned_data['designation'],
              linkedin_url     = form.cleaned_data['linkedin_url'],
              office_email     = User.objects.get(username = request.user).email
            ).save()
            
            return redirect('hr_id_card')

    return render(request,'form.html',context={'form':form})


# HR account creation Page-5

@login_required
def hr_id_card(request):
    
    # value for the change in title of this page
    content = "ID Card"
    
    # variable to decide the next success url
    next = '/hrprofile'
    
    return render(request,'form.1.html',context = {'content':content,'next': next})


# HR account creation Page-6

@login_required
def hr_profile_pic(request):


    next ='/hr/dashboard'

    return render(request,'pic_crop.html', context = {'content':'Profile Pic of HR'})



# Professional Page-12

@login_required 
def pro_timetable(request):
    if request.method == 'POST':

        # print(request.POST)
        prof = Prfessional.objects.get(user__username = request.user)

        print(prof)
        prof.save()

        data = dict( request.POST )
        days = data['day']
        times = data['time']

        for i in range(len(days)):

          if  times[i] != '':
              Professinal_Interview_Time(
              meet = days[i],
              time = times[i],
              prof = prof   ).save()

        return redirect('banking')


        # print(days,times)


    form = ProfTimeTableForm()


    skills = """
    <button class="login100-form-btn" type="button" id="addd">
							Add More 
						</button>
    """
    
    return render(request,'form.html',context={'form':form,'skills':skills})


# Professioinal Page-11

@login_required
def pro_bank(request):
    
    form = ProfessionalBankForm()

    
    if request.method == 'POST':
        form = ProfessionalBankForm(request.POST)
        if form.is_valid():
          if Prfessional.objects.filter(user__username = request.user).count == 0:
              return HttpResponse('Sorry you are not signed up for porfessional person')

          pro = Professinal_Account_Details()

          if Professinal_Account_Details.objects.filter(pro = Prfessional.objects.get(user__username = request.user)).count() != 0:
              pro = Professinal_Account_Details.objects.get(pro = Prfessional.objects.get(user__username = request.user))
          

              
          pro.pro  = Prfessional.objects.get(user__username = request.user)
          pro.ifsc =           form.cleaned_data['ifsc']
          pro.account_number = form.cleaned_data['account_number']
          pro.name =           form.cleaned_data['name']
          pro.upi  =           form.cleaned_data['upi']
          
          pro.save()

          return redirect('pro_dashboard')
    
    return render(request,'form.html',context={'form':form})


# HR account Page-7

@login_required
def hr_dashboard(request):
    return render(request,'hr_dashboard.html',context={})



# Fresher Dashboard Page-6

@login_required
def applicant_dashboard(request):
    return HttpResponse('Fresher Dashbaord')


# professional Page-13

@login_required
def prof_dashboard(request):
  return HttpResponse('Professional Dashboard')



# Professional Page-9

@login_required
def pro_waiting(request):

    js_code = '''
    $(document).ready(function(){
      console.log('ready');
      $('#submit_button').hide();
    })
    '''
    return render(request,'form.html',{'js_code':js_code,'message':'Will be waiting till your interview with Expert is done.'})






