from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Phonenumber(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,related_name='userphone')
    phone_number = models.CharField(max_length=10,blank = False,default='')

    def __str__(self):
        return "user {}  phone {}".format(self.user.username,self.phone_number)

class VideoUpload(models.Model):
    title = models.CharField(max_length=200)
    video_link = models.CharField(max_length=1000)
    thumbnail_link = models.CharField(max_length=1000)
    descripion = models.TextField()
    dept_head = models.CharField(max_length=100)

    def __str__(self):
        return "Title {}   VideoLink {} Description {} Thumbnail {} Departhad {}".format(self.title,self.video_link,self.descripion,self.thumbnail_link,self.dept_head)



class Email(models.Model):
    gmail = models.CharField(max_length=200,default='')

    def __str__(self):
        return "Email: {}".format(self.gmail)

class OTP(models.Model):
    user = models.OneToOneField(User,related_name='user_otp',on_delete=models.CASCADE)
    otp = models.CharField(null=False,max_length=4)
    count = models.IntegerField(default=0)

    def __str__(self):
        return "user {} count {} otp {}".format(self.user.username,self.count,self.otp)