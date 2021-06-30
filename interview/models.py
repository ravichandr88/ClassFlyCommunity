from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Fresher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='applicant')
    college = models.CharField(max_length=40)
    branch = models.CharField(max_length = 50) 
    passout_year = models.IntegerField()
    about_yourself = models.CharField(max_length=500,null=True)
    total_experience = models.FloatField()
    resume_url = models.URLField(null=True)
    skills = models.CharField(max_length=500,default='')    


    def __str__(self):
        return "User {} College {} Branch {} Exp {} url {}".format(self.user,self.college,self.branch,self.total_experience,self.resume_url)

class Experience(models.Model):
    applicant = models.ForeignKey(Fresher,on_delete=models.CASCADE,related_name='experience')
    exp_company = models.CharField(max_length=80)
    exp_work = models.CharField(max_length=500)
    exp_period = models.CharField(max_length=40)

    def __str__(self):
        return "Applicant {} Exp_Comp {} Exp_Work {} Exp_Period {}".format(self.applicant,self.exp_company,self.exp_work,self.exp_period)
    


class Prfessional(models.Model):
    user            = models.OneToOneField(User,on_delete=models.CASCADE, related_name = 'proaccount')
    company         = models.CharField(max_length=70, null=False)
    designation     = models.CharField(max_length=60, null=False)
    city            = models.CharField(max_length=60, null=False)
    stream          = models.CharField(max_length = 60,null=False)
    college         = models.CharField(max_length=80, null=False)
    language_spoke  = models.CharField(max_length = 150, null=False)
    about_yourself  = models.TextField(max_length = 500)
    total_exp_year  = models.FloatField()
    resume_url      = models.URLField()
    profile_pic     = models.URLField()
    skills          = models.CharField(max_length = 500)
     

    def __str__(self):
        return "Company {} City {} Designation {}".format(self.company,self.city,self.designation)

class ProExperience(models.Model):
    pro = models.ForeignKey(Prfessional, on_delete = models.CASCADE, related_name='experience')
    company = models.CharField(max_length = 80)
    designation = models.CharField(max_length = 80)
    project = models.CharField(max_length = 60)
    cfrom = models.CharField(max_length = 20)
    cto = models.CharField(max_length = 20)

    def __str__(self):
        return "Professional {} Company {} Designation {} cfrom {} cto {}".format(self.pro,self.company,self.designation,self.cfrom,self.cto)
 

#Table to have the interview timings between expert and profesiionals
class Professional_Meeting(models.Model):
    meet1 = models.DateTimeField()
    meet2 = models.DateTimeField()
    meet3 = models.DateTimeField()
    prof  = models.ForeignKey(Prfessional, on_delete = models.CASCADE, related_name="meeting")
    
    def __str__(self):
        return "Meet 1 {}  Meet 2 {}  Meet 3 {} prof {}".format(self.meet1,self.meet2,self.meet3,self.prof)

#Table to store the timings between fresher and professionals
class Professinal_Interview_Time(models.Model):
    meet = models.CharField(max_length = 3)
    time = models.TimeField()
    prof = models.ForeignKey(Prfessional, on_delete = models.CASCADE, related_name="prof_interview")
    
    def __str__(self):
        return "Meet {} Professional {}".format(self.meet, self.prof.user.username)


class Company(models.Model):
    created_by              = models.OneToOneField(User,  related_name='company', on_delete=models.CASCADE)
    company_name            = models.CharField(max_length = 100,null=False)
    address                 = models.TextField(max_length = 500, null=False)    
    city                    = models.CharField(max_length=50,null=False)
    company_linkedin_url    = models.URLField()
    created_on              = models.DateTimeField(auto_now=True)
    state                   = models.CharField(max_length = 100, null =False)
    verified                = models.BooleanField(default = False)

    def __str__(self):
        return "Company Name {} Address {} City {} LinkedinUrl {}".format(self.company_name,self.address,self.city,self.company_linkedin_url)


class HRaccount(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='hraccount')
    designation      = models.CharField(max_length = 50,null=False)
    linkedin_url     = models.URLField() 
    created_on       = models.DateTimeField(auto_now=True)
    idcard           = models.URLField(default='')
    profilepic       = models.URLField(default='')
    office_email     = models.EmailField(null=True)



    def __str__(self):
        return "user {} designation {} linkedinurl {} idcard {} profile_pic {}".format(self.user.username,self.designation,self.linkedin_url, self.idcard, self.profilepic)


class Expert(models.Model):
    user           = models.OneToOneField(User, related_name = 'expert', on_delete = models.CASCADE)
    interviewed_by = models.ForeignKey(User, related_name='expert_interviewed', on_delete = models.CASCADE)
    skills         = models.CharField(max_length = 200)
    # the link for video interview url
    resume  = models.URLField()
    company        = models.CharField(max_length = 100)
    designation    = models.CharField(max_length = 100)
    experience     = models.FloatField()
    created_on     = models.DateTimeField(auto_now=True)
    profile_pic    = models.URLField()

    def __str__(self):
        return "User {} Interviewed By {} company {} Experience {}".format(self.user.username,self.interviewed_by.username,self.company,self.experience)


# table to work on professoinal and Expert meeting details and result
 
class ProfessionalInterview(models.Model):
    expert = models.ForeignKey(Expert, on_delete = models.CASCADE, related_name='interviewed')
    pro   = models.OneToOneField(Prfessional, on_delete = models.CASCADE, related_name ='pro_interview')
    interview_on = models.DateTimeField()
    interview_url = models.URLField()
    topics = models.CharField(max_length = 300)
    comments = models.CharField(max_length = 200)



    def __str__(self):
        return "Expert {} Pro {} InterviewURL {} Interview On {}  Topics {} Comments {}".format(self.expert.user.username, self.pro.user.username,self.interview_url,self.interview_on,self.topics,self.comments)



class ProfessionalTimeTable(models.Model):
    day = models.CharField(max_length = 10)
    time= models.TimeField()
    prof= models.ForeignKey(Prfessional, on_delete=models.CASCADE, related_name='prof_timings')

    def __str__(self):
        return "Day {} Time {} Prof {}".format(self.day, self.time, self.prof.user.username)


    
class Professinal_Account_Details(models.Model):
    pro  = models.OneToOneField(Prfessional, on_delete = models.CASCADE, related_name='pro_bank_account')
    ifsc = models.CharField(max_length=11, null = False)
    account_number = models.CharField(max_length=18, null = False)
    name = models.CharField(max_length = 40, null = False)
    upi  = models.CharField(max_length = 40)

    def __str__(self):
        return " Professional {} IFSC {} Account Number {} Name {} UPI {}".format(self.pro.user.username,self.ifsc,self.account_number,self.name,self.upi)


