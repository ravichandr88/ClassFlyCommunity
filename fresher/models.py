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
    designation  = models.CharField(max_length = 50,default='')
    video_url    = models.URLField(null=True)
    date_time    = models.DateTimeField(null = False)
    skills       = models.CharField(max_length = 500, null = False)
    paid         = models.BooleanField(default = False)
    created_on   = models.DateTimeField(auto_now=True)
    channel_name = models.CharField(max_length = 100,null = False)
    price        = models.FloatField(null = False)
    mode         = models.CharField(max_length = 3)           #givn by profesnl about the student #Approved by Professional for meeting
    feedback     = models.TextField(max_length = 1000, default='')   #givn by profesnl about the student
    passed       = models.BooleanField(default = False)  #Whether student has passed the exams or not
    approved     = models.BooleanField(default = False) #Approved by Professional for meeting
    rejected     = models.BooleanField(default = False)

    def __str__(self):
        
        return " Professional {} Fresher {} Meeting {}".format(self.prof.user.username, self.fresher.user.username,self.date_time)

    def dict(self):
        return {
            'id'            : self.id,
            'prof'          : self.prof.user.username,
            'fresher'       : self.fresher.user.username,   
            'video_url'     : self.video_url,
            'date_time'     : self.date_time,
            'skills'        : self.skills,
            'paid'          : self.paid,
            'channel_name'  : self.channel_name
        }
    
    def skills_count(self):
        return len(self.skills.split(','))    

 
# video calling detailas table

class Meeting(models.Model):   
    meeting         = models.OneToOneField(ProFrehserMeeting, on_delete = models.CASCADE, related_name = 'meeting_details')
    pro_joined      = models.BooleanField(default = False)
    fre_joined      = models.BooleanField(default = False)
    record_started  = models.BooleanField(default = False)
    record_stopped  = models.BooleanField(default = False)
    uploaded_vdo    = models.BooleanField(default = False)
    resource_id     = models.CharField(max_length = 600,null = True)
    sid             = models.CharField(max_length = 600,null = True)
    vdo_id          = models.CharField(max_length = 200, null = True)
    created_on      = models.DateTimeField(auto_now = True)
    record_start_time = models.DateTimeField(null = True)
    record_stop_time = models.DateTimeField(null=True)
    


    def __str__(self):
        return "Record Started {} Record Stopped {} "


class MeetingActive(models.Model):
    meeting = models.OneToOneField( ProFrehserMeeting, on_delete = models.CASCADE, related_name = 'meeting_status' )
    prof    = models.IntegerField(default = 0)
    fres    = models.IntegerField(default = 0)
    record  = models.IntegerField(default = 0)
    created_on = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return "Created On {} ".format(self.created_on)








