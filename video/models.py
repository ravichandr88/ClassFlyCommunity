from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class College(models.Model):
#     name = models.CharField(max_length=200,null=False)
#     place = models.CharField(max_length=100,null=False)



class DeptHead(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_depthead')
    college = models.CharField(max_length=200,null=False)
    dept = models.CharField(max_length=100)

    def __str__(self):
        return "User {} College {} Branch {}".format(self.user.username,self.college,self.dept)




class EducationDomain(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return "Domain name : {}".format(self.name)



class Department(models.Model):
    name = models.CharField(max_length=200,null=False)
    domain = models.ForeignKey(EducationDomain,on_delete=models.CASCADE,related_name='departments')

    def __str__(self):
        return "Name {} Domain {}".format(self.name,self.domain.name)

class Subject(models.Model):

    name = models.CharField(max_length=200,null=False)
    domain = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='domain_subjects')
    descp = models.CharField(max_length=200,default='')
    imgurl = models.URLField(default='https://www.classfly.in/static/assets/img/comm.jpg')
    def __str__(self):
        return "Subject name:  {} , Domain : {} Description: {}".format(self.name,self.domain.name,self.descp)

class Playlist(models.Model):
    name = models.CharField(max_length = 200,null=False)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subject_playlist')
    chapter = models.IntegerField(null=False,default=1)
    uploaded_by = models.ForeignKey(DeptHead,on_delete=models.CASCADE,related_name='depthead_playlist')
    cf = models.BooleanField(default = False)

    def __str__(self):
        return " Playlist Name: {} Subject: {}  Chapter : {} UploadedBy: {}".format(self.name,self.subject.name,self.chapter,self.uploaded_by.user.username)

 
class VideoId(models.Model):
    video_id = models.CharField(max_length=20,null=False)
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE,related_name='playlist_videos')
    title = models.CharField(max_length=200,default='')

    def __str__(self):
        return "Video ID: {} Playlist : {}  Title {}".format(self.video_id,self.playlist.name,self.title)
    
    def list(self):
        return self.video_id



#the following tables are made for video uploading and analytics for depthead and videoamker

DEFAULTUSER = 1
class VideoDeptHead(models.Model):
    user = models.OneToOneField(User,related_name='dept_head',on_delete=models.CASCADE,default=DEFAULTUSER)
    name        = models.CharField(max_length=100)
    usn         = models.CharField(max_length=20)
    report_to   = models.ForeignKey(User,related_name='dept_head_report_to',on_delete=models.CASCADE)

    def __str__(self):
        return "name {}, usn {}, report_to {}".format(self.name,self.usn,self.report_to)


class VideoMaker(models.Model):
    user = models.OneToOneField(User,related_name='video_maker',on_delete=models.CASCADE,default=DEFAULTUSER)
    name = models.CharField(max_length=40)
    usn = models.CharField(max_length=20)
    dept_head = models.ForeignKey(VideoDeptHead,on_delete=models.CASCADE,related_name='report_to_dept_head')

    def __str__(self):
        return "Name {} USN {} Report_to {}".format(self.name,self.usn,self.dept_head.name)


class VideosMade(models.Model):
    video_link = models.CharField(max_length=600)
    title = models.CharField(max_length=100)
    thumbnail_link = models.CharField(max_length=600)
    video_maker = models.ForeignKey(VideoMaker,on_delete=models.CASCADE,related_name='videos_made')
    datetime = models.DateTimeField(auto_now=True)
    report = models.TextField(max_length=1000,default='')
    status = models.BooleanField(null=True)

    def __str__(self):
        return "Name {} Title {} report {} status {}".format(self.video_maker.name,self.title,self.report,self.status)
#this is the end for tables including work for video uploader and depthead


#table for notes
class Notes(models.Model):
    name = models.CharField(max_length = 200,null=False)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subject_noteslist')
    chapter = models.IntegerField(null=False,default=1)
    uploaded_by = models.ForeignKey(VideoMaker,on_delete=models.CASCADE,related_name='notes_uploaded')
    note_link = models.CharField(max_length=300)

    def __str__(self):
        return "Created_By {} Subject {} Chapter {} Uploaded_By {} note_link {}".format(self.name,self.subject,self.chapter,self.uploaded_by.name,self.note_link)



