from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Phonenumber(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,related_name='userphone')
    phone_number = models.CharField(max_length=10,blank = False,default='')

class VideoUpload(models.Model):
    title = models.CharField(max_length=200)
    video_link = models.CharField(max_length=1000)
    thumbnail_link = models.CharField(max_length=1000)
    descripion = models.TextField()
    dept_head = models.CharField(max_length=100)

    def __str__(self):
        return "Title {}  Description {} VideoLink {} description {}".format(self.title,self.video_link,self.descripion,self.thumbnail_link,self.dept_head)



class Email(models.Model):
    gmail = models.CharField(max_length=200,default='')

    def __str__(self):
        return "Email: {}".format(self.gmail)