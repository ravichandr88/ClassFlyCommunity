from django.shortcuts import render,HttpResponse,Http404
from .forms import StudentForm,ProfessionalForm,HRForm,ProfessionalBankForm,ProfTimeTableForm,Experienc,ProIntervTime,CompanyForm
from django.contrib.auth.decorators import login_required
from .models import Fresher, Professinal_Interview_Time, HRaccount,Company,Experience,Professinal_Account_Details ,Prfessional,ProExperience, Professional_Meeting
from django.contrib.auth.models import User
from django.shortcuts import redirect



# Fresher Singup Page-3
# Create your views here.
@login_required
def student(request, edit = 0):
    request.session['type'] = 'student'

    
    if request.method == 'GET' and edit == 0 and Fresher.objects.filter(user__username = request.user).count() == 1:
      return HttpResponse('Please go to dashboard to edit profile information')

  # edit = 1 means loading the for editing
    if edit == 1 and Fresher.objects.filter(user__username = request.user).count() == 0:
        return HttpResponse('Please signup for Applicant Account')

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
    
    student = StudentForm()    #preparing an empty form
    fresher = Fresher() if Fresher.objects.filter(user__username = request.user).count() == 0 else Fresher.objects.get(user__username = request.user)
    skills = ''
    
        # if this is supposed to be a new form
    if request.method == 'GET' and edit == 0:

      skills = """
                    <div id="extra">
                    </div>
				<ul class=" wrap-input100 ">
					<li class="tags-new">
							<div class="wrap-input100 " >
								<h5>Skills</h5>
					  <input class="input100" type="text" placeholder="Skills"> 
					  </div>
					  <p style="color:'red'">Enter skills seperated by comma.</p>
					</li>
				  </ul>"""
      return render(request,'form.html',context={'form':student, 'skills':skills})

    # If the function called for editing
    if (Fresher.objects.filter(user__username = request.user).count() == 1 and request.method == 'GET') or edit == 1:
        
        student.initial['city_1']           = fresher.city_1 
        student.initial['city_2']           = fresher.city_2  
        student.initial['city_3']           = fresher.city_3  
        student.initial['city']             = fresher.city
        student.initial['college']          =  fresher.college    
        student.initial['branch']           =  fresher.branch    
        student.initial['passout_year']     = fresher.passout_year  
        student.initial['master_college']   = fresher.master_college 
        student.initial['master_branch']    = fresher.master_branch
        student.initial['pre_college']      = fresher.pre_college  
        student.initial['pre_branch']       = fresher.pre_branch  
        student.initial['about_yourself']   = fresher.about_yourself 
        student.initial['pre_passout']      = fresher.pre_passout 
        student.initial['master_passout']   = fresher.master_passout 
        student.initial['total_experience'] = fresher.total_experience
        student.initial['language_spoke']   =  fresher.language_spoken 
          
    
        # A special input, to get skills , we are providing extra html code.
        skills = """
                        <div id="extra">"""

        for i in fresher.skills.split(','):
        
            skills = skills + '<input name="skills" id="' + i.replace(' ','') + '" value="' + i + '" style="display:none">'

        skills = skills + '  </div><ul class=" wrap-input100 "> '

        for i in fresher.skills.split(','):
          skills = skills + '<li class="tags" id="fun"><span>' + i.replace(' ','') +'</span><i class="fa fa-times"></i></li>'


            
        skills = skills + """<li class="tags-new">
                  <div class="wrap-input100 " >
                    <h5>Skills</h5>
                <input class="input100" type="text" placeholder="Skills"> 
                </div>
                
              </li>
              </ul>"""
    



    if request.method == 'POST':

        student = StudentForm(request.POST)   
        if student.is_valid() and len(request.POST.getlist('skills')) != 0:
          

          print('City',student.cleaned_data['city'])
          fresher.user             = User.objects.get(username = request.user)
          fresher.college          = student.cleaned_data['college']
          fresher.branch           = student.cleaned_data['branch'] 
          fresher.city_1           = student.cleaned_data['city_1']
          fresher.city_2           = student.cleaned_data['city_2']
          fresher.city_3           = student.cleaned_data['city_3']
          fresher.city             = student.cleaned_data['city']
          fresher.passout_year     = student.cleaned_data['passout_year']
          fresher.master_college   = student.cleaned_data['master_college']
          fresher.master_branch    = student.cleaned_data['master_branch']
          fresher.pre_college      = student.cleaned_data['pre_college']
          fresher.pre_branch       = student.cleaned_data['pre_branch']
          fresher.about_yourself   = student.cleaned_data['about_yourself']
          fresher.pre_passout      = student.cleaned_data['pre_passout']
          fresher.master_passout   = 0000 if student.cleaned_data['master_passout'] == '' else student.cleaned_data['master_passout']
          fresher.total_experience = int(student.cleaned_data['total_experience'].split('.')[0])
          fresher.skills           = str(request.POST.getlist('skills'))[1:][:-1]
          fresher.language_spoken  = student.cleaned_data['language_spoke']
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

          if edit == 1:
            return redirect('f_dashboard')
          else:
            return redirect('resume')

        # if form is not valid
        elif len(request.POST.getlist('skills')) == 0:
          print('Not valid form, so error')
          skills = """
                    <div id="extra"></div>
				  <ul class=" wrap-input100 ">
					<li class="tags-new">
							<div class="wrap-input100 " >
								<h5>Skills</h5>
					  <input class="input100" type="text" placeholder="Skills"> 
					  </div>
					  <p style="color:red">Enter skills seperated by comma.</p>
					</li>
				  </ul>"""
        print('start',student.is_valid(),student.errors.as_data(),'end')
        print('line 157 , out of post condition')
        return render(request,'form.html',context={'form':student, 'skills':skills,'title':'Student Signup'})

    print('saved, ')
    return render(request,'form.html',context={'form':student, 'skills':skills})


# Professional Page-6
# Fresher Page-4

@login_required
def resumeview(request, edit = 0):
# edit = 1 means updating previuos resume
    next = 'notFound'
    # form = ResumeForm()
    if edit == 0:
      next = '/pro/profile'
    else:
      # know which is the user ,  professional or Fresher
      if Prfessional.objects.filter(user__username = request.user).count() != 0: 
        next = '/pro_dashboard'
      elif Fresher.objects.filter(user_username = request.user).count()  != 0:
        next = '/f_dashh'
    return render(request,'form.1.html',context={'content':"Resume", 'next' : next,'title':'Resume Upload'})



# Function to signup the professional after verifying the sms and email otp
# Professional Signup Page-3


@login_required
#function to professional signup
def prosignup(request, edit = 0):
    # edit = 1, refers to update of the curent data, edit = 0 means it is filling a new one
    request.session['type'] == 'company'

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

    prof = ProfessionalForm()
# if 
    if request.method == 'GET' and edit == 1:
          pro =  Prfessional.objects.get(user__username = request.user)

          prof.initial['company']         = pro.company
          prof.initial['designation']     = pro.designation
          prof.initial['city']            = pro.city
          prof.initial['stream']          = pro.stream
          prof.initial['college']         = pro.college
          prof.initial['language_spoke']  = pro.language_spoke
          prof.initial['about_yourself']  = pro.about_yourself 
          prof.initial['total_exp_year']  = str(pro.total_exp_year).split('.')[0]
          prof.initial['total_exp_month'] = str(pro.total_exp_year).split('.')[1]
          
          #special input field for adding skills
          skills = """
                    <div id="extra"></div>
				<ul class=" wrap-input100 "> """
        
          for i in pro.skills.replace("'",'').split(','):

            skills +=	'<li class="tags" id="fun"><span>'+ i +'</span><i class="fa fa-times"></i></li>' + '<input name="skills" id="'+i  +'" value="'+ i+'" style="display:none"></input>'
				  
          skills += """
					<li class="tags-new">
							<div class="wrap-input100 " >
								<h5>Skills</h5>
					  <input class="input100" type="text" placeholder="Skills"> 
					  </div>
					  Enter skills seperated by comma.
					</li>
				  </ul>"""


    # If the edit option is enabled , get the default values by query

    if request.method == 'POST' :
        prof = ProfessionalForm(request.POST)

        

        if prof.is_valid() and len(request.POST.getlist('skills')):
          # print(prof)
          
          #prepare experience value
          exp = float( prof.cleaned_data['total_exp_year'] + '.' + prof.cleaned_data['total_exp_month'] )
          
          # create a new one if edit = 0
          pro = Prfessional()
          
          if edit == 1:
            pro = Prfessional.objects.get(user__username = request.user)
          
           
          pro.user            = User.objects.get(username = request.user)
          pro.company         = prof.cleaned_data['company']
          pro.designation     = prof.cleaned_data['designation']
          pro.city            = prof.cleaned_data['city']
          pro.stream          = prof.cleaned_data['stream']
          pro.college         = prof.cleaned_data['college']
          pro.language_spoke  = prof.cleaned_data['language_spoke']
          pro.about_yourself  = prof.cleaned_data['about_yourself']
          pro.total_exp_year  = exp
          print(request.POST.getlist('skills'))
          pro.skills = str(request.POST.getlist('skills')).replace("'","")[1:][:-1]
          

          pro.save()

          if edit == 0:
            return redirect('/pro/exp')
          else:
            return redirect('pro_dashboard')
        
        else:
          skills = """
                    <div id="extra"></div>
				<ul class=" wrap-input100 ">
					<li class="tags-new">
							<div class="wrap-input100 " >
								<h5>Skills</h5>
					  <input class="input100" type="text" placeholder="Skills"> 
					  </div>
					<p style="color:red">  Enter skills seperated by comma.</p>
					</li>
				  </ul>"""
          # return render(request,'form.html',context={'form':prof,'skills':skills})
          
    
    
    return render(request,'form.html',context={'form':prof,'skills':skills,'title':'Professional Details'})



# Professional Signup to acquire experience details of the professional
# Professional Signup Page-5

@login_required
#function to professional signup
def proexp(request,edit=0):
    # edit = 0 is new form, edit = 1 is update of the same form

    form = Experienc()

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

    card_no = 1

    experience = [] # varibale used to store experience objects, when called for update


# if edit = 1, which means this is for update the data
    if edit == 1:
          
          prof = Prfessional.objects.get(user__username = request.user)

          experience = prof.experience.all()
          
          card_no = len(experience)

          for i in range(len(experience)):
            card += str('<cdiv class="go" id="butn" name="'+ str(i+1) +'">'
            '<br><h3>'+ experience[i].company +'</h3>'
            '<h1>'+ experience[i].designation +'</h1>'
            '<p>'+ experience[i].project +'</p>'
            '<span>'+ experience[i].cfrom +' - '+ experience[i].cto +'</span>'
            '<br></cdiv>')

          '''
          <cdiv class="go" id="butn" name="1">
          <br><h3>wipro</h3>
          <h1>great</h1>
          <p>good to go</p>
          <span>JAN 2012  -  JAN 2013</span>
          <br></cdiv>
          '''



    if request.method == 'POST':

        
        data = request.POST.dict()
        print(data)
        keys = list(data.keys())[7:]
        n = 5
        l = [keys[i * n:(i + 1) * n] for i in range((len(keys) + n - 1) // n )]
        l = l[:-1]

        print(l)
        prof = Prfessional.objects.get(user = User.objects.get(username = request.user))

        if edit == 1:
            prof.experience.all().delete()

        for i in l:
            print('Entered')
            # 'company1', 'designation1', 'project1', 'from1', 'to1'
            ProExperience(
              pro          = prof,
              company      = data[i[0]],
              designation  = data[i[1]],
              project      = data[i[2]],
              cfrom        = data[i[3]],
              cto          = data[i[4]]
            ).save() 

            # print(data[i[0]], data[i[0]], i[2], i[3], i[4])
        return redirect('/resume')



    
    return render(request,'form.html',context={'form':form,'skills':skills,'card':card,'card_no':card_no,'experienc':experience,'title':'Work Experience'})



# Professional Page-8

import datetime

@login_required
def prof_initial_meet(request):
    form = ProIntervTime()



    if request.method == 'POST':
        # print(request.POST['meet1_date'],request.POST['meet1_time'])

        # print(datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time']))
        
        user = User.objects.get(username = request.user)
        
        if Prfessional.objects.filter(user = user).count() == 0:
          return HttpResponse('Please signup as Professional First')

        prof = Prfessional.objects.get(user = user)

        pro_meet = Professional_Meeting()
        if request.POST['meet1_date'] != '' and request.POST['meet1_time'] != '':
          pro_meet.meet1 = datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time'])
        if request.POST['meet2_date'] != '' and request.POST['meet2_time'] != '':
          pro_meet.meet2 = datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time'])
        if request.POST['meet3_date'] != '' and request.POST['meet3_time'] != '':
          pro_meet.meet3 = datetime.datetime.fromisoformat(request.POST['meet1_date'] +' ' + request.POST['meet1_time'])
        pro_meet.prof = prof
        pro_meet.save()

        

        return redirect('pro_waiting')




    card = """  <h5 style="text-align: center;"> 
    Please provide your free time to connect with our 
    Experts and to be interviewed. </h5> <br><br> 
    <p style="text-align: center;"> 
    Please provide possible timings you are free, 
    and we will SMS the timings that our Experts agree on. </p> <br> """

    return render(request,'form.html',context={'form':form, 'card':card,'title':'Interview Timings'})


# Professional Signup Page-7
# Fresher Signup Page-5

@login_required
def profile_pic(request):
    
    next = ''

    # variable to point to next page
    if Prfessional.objects.filter(user__username = request.user).count() != 0:

        next = '/pro/meet'
    
    if Fresher.objects.filter(user__username = request.user).count() !=  0:
        next = '/f_dashh'

    return render(request,'pic_crop.html', context={'next' : next})


# Company Account creation by HR or employee

# HR Singup Page-3
@login_required
def company_singup(request, edit = 0):
    request.session['type'] == 'company'
    form = CompanyForm()
    
    

    if edit == 1 and request.method == 'GET':
      comp = Company(created_by__username = request.user)

      form.initial['about'] = comp.about
      form.initial['city']  = comp.city
      form.initial['state'] = comp.state
      form.initial['company_name'] = comp.company_name
      form.initial['address'] = comp.address
      form.initial['company_linkedin_url'] = comp.company_linkedin_url

    if request.method == 'POST':

        form = CompanyForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

           
            comp = Company()

            if edit == 1:
               comp = Company.objects.get(created_by__username = request.user)

            comp.created_by              = User.objects.get(username = request.user),
            comp.about                   = form.cleaned_data['about'],
            comp.company_name            = form.cleaned_data['company_name'],
            comp.address                 = form.cleaned_data['address'],
            comp.city                    = form.cleaned_data['city'],
            comp.state                   = form.cleaned_data['state'],
            comp.company_linkedin_url    = form.cleaned_data['company_linkedin_url'],
            comp.save()


            return redirect('hr_account_creation')


    return render(request,'form.html',context={'form':form,'title':'Company Details'})


# Company account creatoin done , now addding self account as HR for the company
# HR- account creatoin Page-4

@login_required
def hr_account_creation(request,edit = 0):
    
    form = HRForm()
    hr = HRaccount()
    
    if edit == 1 and request.method == 'GET':
      hr = HRaccount.objects.get(user__username = request.user)

      form.initial['designation']  = hr.designation
      form.initial['linkedin_url'] = hr.linkedin_url
      

    if request.method == 'POST':
          form = HRForm(request.POST)
          
          if form.is_valid():
              print()
              hr.user             = User.objects.get(username = request.user)
              hr.designation      = form.cleaned_data['designation']
              hr.linkedin_url     = form.cleaned_data['linkedin_url']
              hr.office_email     = User.objects.get(username = request.user).email
              hr.save()
            
              return redirect('hr_id_card')

    return render(request,'form.html',context={'form':form,'title':'HR Details'})


# HR account creation Page-5

@login_required
def hr_id_card(request):
    
    # value for the change in title of this page
    content = "ID Card"
    
    # variable to decide the next success url
    next = '/hrprofile'
    
    return render(request,'form.1.html',context = {'content':content,'next': next,'title':'HR ID Card'})


# HR account creation Page-6

@login_required
def hr_profile_pic(request):


    next ='/hr_waiting'

    return render(request,'pic_crop.html', context = {'content':'Profile Pic of HR','next':next})


# Professioinal Page-11

@login_required 
def pro_timetable(request,edit=0):
# edit = 0 is dont want to edit, 1 to edit

    form = ProfTimeTableForm()
    
    prof = Prfessional.objects.get(user__username = request.user)
    
    skills = """
    <button class="login100-form-btn" type="button" id="addd">
							Add More 
						</button>
    """

    if edit == 1 and request.method == 'GET':
      
      data = prof.prof_interview.all()
      # print(form)

      return render(request,'timetable_edit.html',context={'form':form,'skills':skills,'data':data})


    if request.method == 'POST' :

        # print(request.POST)
        
        # print(prof)
        prof.prof_interview.all().delete()

        data = dict( request.POST )
        days = data['day']
        times = data['time']

        for i in range(len(days)):

          if  times[i] != '' and days[i] != 'NULL':
              Professinal_Interview_Time(
              meet = days[i],
              time = times[i],
              prof = prof   ).save()
        if edit == 0:
          return redirect('banking')
        
        else:
          return redirect('pro_dashboard')


        # print(days,times)


    
    
    return render(request,'form.html',context={'form':form,'skills':skills,'title':'Meeting Timings'})



# Professional Page-12

@login_required
def pro_bank(request, edit = 0):
    # edit = 1 is for updating the bank details
    form = ProfessionalBankForm()
    prof = Prfessional.objects.get(user__username = request.user)

    if edit == 1 and request.method == 'GET':
      
      form.initial['ifsc']              = prof.pro_bank_account.ifsc
      form.initial['account_number']    = prof.pro_bank_account.account_number
      form.initial['name']              = prof.pro_bank_account.name
      form.initial['upi']               = prof.pro_bank_account.upi

    
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
    
    return render(request,'form.html',context={'form':form,'title':'Bank Account Details'})



# # HR account Page-7

# @login_required
# def hr_dashboard(request):
#     return render(request,'hr_dashboard.html',context={})



# Fresher Dashboard Page-6
# url = 'f_dashh'
# path('f_dashh', views.fresher_dash, name = 'f_dashboard'),
# fresher app


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


@login_required
def hr_waiting(request):

    js_code = '''
    $(document).ready(function(){
      console.log('ready');
      $('#submit_button').hide();
    })
    '''
    return render(request,'form.html',{'js_code':js_code,'message':'Will be waiting till your company is verified.'})




