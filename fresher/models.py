from django.db import models

# Create your models here.

from interview.models import Fresher,HRaccount,Company,Experience,Prfessional,ProExperience,Professional_Meeting,Professinal_Interview_Time


'''
Here we have tables for keeping the record for booing the the meetings


'''

class ProFrehserMeeting(models.Model):
    '''
    
    table to store the details of meeting between fresher and professional, 
    actual interview done to students.
    
    '''

    prof         = models.ForeignKey(Prfessional, on_delete = models.CASCADE, related_name = 'interviews_done', null = False)
    fresher      = models.ForeignKey(Fresher, on_delete = models.CASCADE, related_name = 'fresher_interview', null = False)
    video_url    = models.URLField(null=True)
    date_time    = models.DateTimeField(null = False)
    skills       = models.CharField(max_length = 500, null = False)
    paid         = models.BooleanField(default = False)
    created_on   = models.DateTimeField(auto_now=True)
    channel_name = models.CharField(max_length = 100,null = False)
    price        = models.FloatField(null = False)
    mode         = models.CharField(max_length = 3)
    feedback     = models.TextField(max_length = 1000, default='')   #givn by profesnl about the student
    passed       = models.BooleanField(default = False)
    approved     = models.BooleanField(default = False) #Approved by Professional for meeting


    def __str__(self):
        
        return " Professional {} Fresher {} Meeting {}".format(self.prof.user.username, self.fresher.user.username,self.date_time)








