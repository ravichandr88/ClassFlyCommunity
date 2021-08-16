from django.db import models

from fresher.models import HRaccount,Company, Fresher

# Create your models here.


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