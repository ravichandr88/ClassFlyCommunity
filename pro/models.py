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
    name = models.CharField(max_length=60,null=False)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,related_name='trainer_subjects')
    work =  models.CharField(max_length=20,null=False)  #Worth of the work completed
    meetings =  models.IntegerField(null=False)
    presentation = models.BooleanField(default=False)
    internship = models.BooleanField(default=False)
    price = models.IntegerField(default=500)

    def __str__(self):
        return "Name {} Trainer {} Work {} Meetings {} Presentation {} Internship {} Price {}".format(
            self.name,
            self.trainer, self.work,
            self.meetings,self.presentation,
            self.internship, self.price)

class VideoAsset(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_videos')
    asset_id = models.CharField(max_length=200,null=False)
    playback_id = models.CharField(max_length=200,null=False)

    def __str__(self):
        return "Project {} AssetID {} ".format(self.project,self.asset_id)

class RegsiteredUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='project_registered')
    # sign_key = models.CharField(max_length=3,null=False)



