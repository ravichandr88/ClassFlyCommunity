from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trainer(models.Model):
    name        =  models.CharField(max_length=60,null=False)
    exp         =  models.CharField(max_length=10,null=False)
    designation =  models.CharField(max_length=60,null=False)

    def __str__(self):
        return " Name {} Exp {} Design {}".format(self.name,self.exp,self.designation)


class Project(models.Model):
    title = models.CharField(max_length=60,null=False)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,related_name='trainer_subjects')
    description = models.TextField(max_length=5000)     #search page description
    work =  models.CharField(max_length=20,null=False)  #Worth of the work completed
    meetings =  models.IntegerField(null=False)
    presentation = models.BooleanField(default=False)       
    internship = models.BooleanField(default=False)
    price = models.IntegerField(default=500)
    program_flow_dscp = models.TextField(max_length=3000)   #Project Flow description
    video_length = models.CharField(max_length=10,default="10")


    def __str__(self):
        return "Name {} Trainer {} Work {} Meetings {} Presentation {} Internship {} Price {}".format(
            self.title,
            self.trainer, self.work,
            self.meetings,self.presentation,
            self.internship, self.price)


class Skills(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='skills')
    title = models.CharField(max_length=100,null=False)
    percent = models.IntegerField(default=0)

    def __str__(self):
        return "Project {} Title {} Percent {}".format(self.project,self.title,self.percent)

class ProjectFlow(models.Model):
    description = models.TextField(max_length=3000) #" Title <*> line1 <*> line2 <*> line3"
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='flow')
 
    def __str__(self):
        return "project {}".format(self.project)

class VideoAsset(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_videos')
    asset_id = models.CharField(max_length=200,null=False)
    playback_id = models.CharField(max_length=200,null=False)

    def __str__(self):
        return "Project {} AssetID {} ".format(self.project,self.asset_id)


class RegsiteredUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='project_registered')
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='registered_users')
    sign_key = models.CharField(max_length=300,null=False)
    private_key = models.TextField(max_length=3000,null=False)
    created_on = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    feedback = models.TextField(max_length=3000,null=True)


    def __str__(self):
        return "User {} created_on {} Project {} Rating {}".format(self.user.username, self.created_on, self.project.name, self.rating)





