from django.db import models

from fresher.models import HRaccount,Company, Fresher
from django.utils import timezone
from django.contrib.auth.models import User
from fresher.models import ProFrehserMeeting
from interview.models import Prfessional

# Create your models here.

# default time value for deleted column JobPost Table
def now():
    return timezone.now()


# Table to store Job Post

class Jobpost(models.Model):

    hr = models.ForeignKey(HRaccount, on_delete = models.CASCADE, related_name = 'job_posted' )
    designation     = models.CharField(max_length = 60)
    role            = models.CharField(max_length = 60, default = '')
    industry_type   = models.CharField(max_length = 60, default = '')
    employment_type = models.CharField(max_length = 60, default = '')
    edu_ug          = models.CharField(max_length = 60, default = '')
    edu_pg          = models.CharField(max_length = 60, default = '')
    edu_doc         = models.CharField(max_length = 60, default = '')
    skills          = models.CharField(max_length = 150)
    description     = models.TextField(max_length = 800)
    requirement     = models.TextField(max_length = 800)
    created_on      = models.DateTimeField(auto_now = True)
    min_salary      = models.FloatField()
    max_salary      = models.FloatField() 
    min_exp         = models.FloatField()
    max_exp         = models.FloatField()
    qu1             = models.CharField(max_length = 400)
    qu2             = models.CharField(max_length = 400) 
    qu3             = models.CharField(max_length = 400)
    city            = models.CharField(max_length = 100, default = '')
    active          = models.BooleanField(default = False )
    deleted         = models.BooleanField(default = False)
    deleted_date    = models.DateTimeField(default = now)


    def __str__(self):
        return "{} HR, designation {} skills {}  Active {}".format(self.hr,self.designation, self.skills, self.active)

    def skills_split(self):
        return self.skills.split(',')

# Table to store the application sub ited byt the fresher

class Applicantion(models.Model): 
    job = models.ForeignKey(Jobpost, on_delete = models.CASCADE, related_name = 'applicants')
    fresher = models.ForeignKey(Fresher, on_delete = models.CASCADE, related_name = 'jobs_applied')
    created_on = models.DateTimeField(auto_now = True)
    ans1       = models.TextField(max_length = 800)
    ans2       = models.TextField(max_length = 800)
    ans3       = models.TextField(max_length = 800)
    status     = models.CharField(max_length = 10, default = '')
    available  = models.BooleanField(default = True)   #He is not hired yet by any other company
    

    def __str__(self):
        return "Job {} Fresher {} created_on {}".format(self.job, self.fresher, self.created_on)


class FresherInvited(models.Model):
    job         = models.ForeignKey(Jobpost, on_delete = models.CASCADE, related_name='invited')
    fresher     = models.ForeignKey(Fresher, on_delete = models.CASCADE, related_name='invited_to')
    created_on  = models.DateTimeField(auto_now = True)
    accepted    = models.BooleanField(default = False)
    seen        = models.BooleanField(default = False) 

    def __str__(self):
        return "Job {} Fresher {} created_on {}".format(self.job,self.fresher,self.created_on)


# Table to store the queries done by different people for interview videos
class InterviewSearch(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'interview_queries')
    pro_name        = models.CharField(max_length = 50,default = '')
    pro_designation = models.CharField(max_length = 50,default = '')
    skills          = models.CharField(max_length = 200, default = '')
    created_on      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "user {} Name {} Designation {}".format(self.user.first_name, self.pro_name, self.pro_designation)


# function to get default user for User column in Interviewvdeio
def defaultUser():
    return User.objects.get(username='bunny').id

class InterviewVideo(models.Model):
    # Had given bunny account as default because of too many editing of the table column details
    user    = models.ForeignKey(User,related_name= 'user_views', on_delete=models.CASCADE, default = defaultUser)
    video   = models.ForeignKey(ProFrehserMeeting, on_delete = models.CASCADE, related_name= 'video_views')
    like    = models.CharField(max_length=1,default = 'N') # N is none, D is dislike, L is like (small or big)
    comment = models.CharField(max_length = 200, default = '')
    created_on = models.DateTimeField(auto_now= True)

    def __str__(self):
        return "User {} Video {}".format(self.user.first_name,self.video.designation)


class Payment(models.Model):
    user                    = models.ForeignKey(User, related_name='user_pay', on_delete=models.CASCADE)
    receipt                 = models.CharField(max_length=10,default='')
    service                 = models.CharField(max_length = 80, default = '')
    amount                  = models.FloatField(default = 0)
    tax                     = models.FloatField(default = 0)
    total_amount            = models.FloatField(default = 0)
    service_type            = models.CharField(max_length=20,default='')  #VDO->VideoInterview, RES->Resume, INT->InterviewBooking, PRO->ProfessionalResume
    razor_order_id          = models.CharField(max_length=30, default='')
    razorpay_payment_id     = models.CharField(max_length = 20, default='')
    razorpay_signature      = models.CharField(max_length=70,default = '')
    created_on              = models.DateTimeField(auto_now = True)


    def __str__(self):
        return "Service Type {} User {}  total amount {}".format(self.service_type,self.user.first_name, self.total_amount)


    def razorpay_amount(self):
        return self.total_amount * 100

    def expiry(self):
        if self.service_type == 'RES':
            if  self.resume_payment_done.download_count < 31:
                return "Resume downloads with Skill_count of {} before {}".format(self.resume_payment_done.skills_count,str(timezone.timedelta(days=30)+self.created_on)[:-16] )
            else:
                return "Service Expired, Thank You"

        elif self.service_type == 'VDO':
            if self.created_on + timezone.timedelta(days = 5) < timezone.now():
                return "Video will be available till {}".format( str(self.created_on + timezone.timedelta(days = 5))[:-16])
            else:
                return "Video service is Expired"

        elif self.service_type == 'INT':
            return "Sucessfully Booked"


class VideoPurchase(models.Model):
    video = models.ForeignKey(InterviewVideo, on_delete = models.CASCADE, related_name= 'video_purchase' )
    payment = models.OneToOneField(Payment, on_delete = models.CASCADE, related_name = 'payment_done')


    def valid(self):
        # Function to return whether the user can watch the video or not
        # Video cannot be played when user has paid and ist been 5 days
        # check with payment created_on date and return true or false based on number of days pased
        
        if self.payment.created_on > (self.payment.created_on + timezone.timedelta(days = 5)):
            return False
        
        return True


class ResumePurchase(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'resume_purchase')
    payment         = models.OneToOneField(Payment, on_delete = models.CASCADE, related_name = 'resume_payment_done')
    download_count  = models.IntegerField(default = 0)
    skills_count    = models.IntegerField(default = 0)     #accoridng to the pricing plan, there 2 levels of skills 6 & 16
    

    def __str__(self):
        return "user {} payment  {} count {}".format(self.user.first_name, self.payment.amount, self.skills_count)

    def download(self, prof):

        self.download_count += 1
        self.save()

        if  self.skills_count >= len(prof.skills.split(',')) and self.download_count < 31 and timezone.now() < (self.payment.created_on + timezone.timedelta(days = 30) ) :    
            return prof.resume_url
        
        return False
    
    def expiry(self):

        return self.payment.created_on + timezone.timedelta(days = 30)




class MeetingPurchase(models.Model):
    meeting = models.OneToOneField(ProFrehserMeeting, on_delete = models.CASCADE, related_name = 'meeting_purchase')
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name = 'payment_meeting')
    repaid  = models.BooleanField(default = False) #to check whether we have repaid them or not, when meeting is rejected

    def __str__(self):
        return " meeting {} payment {}".format(self.meeting, self.payment.amount)





