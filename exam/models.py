from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Exam tables
class ExamSubject(models.Model):
    name = models.CharField(max_length=100)
    img  = models.URLField(default='https://www.classfly.in/static/4.png')
    toc  = models.URLField(default='')       #table of content for subjects
    sn   = models.URLField(default='')      #Subject notes for the subject
    count = models.IntegerField(default=0)


    def __str__(self):
        return "Name {} url {} qes_count {}".format(self.name,self.img,self.count)

#Row for user registered to the specific subject for exam
class ExamUser(models.Model):
    user      = models.ForeignKey(User,on_delete=models.CASCADE,related_name='exam_user')
    subject   = models.ForeignKey(ExamSubject,on_delete=models.CASCADE,related_name='exam_subject')
    marks     = models.IntegerField(default=0)
    exam_over = models.BooleanField(default=False)#WHETHER THE USER IS DONE WITH EXAM OR NOT
    started   = models.DateTimeField(null=True) #time the student started exam



    def __str__(self):
        return "Subject {} User {} started_time {}".format(self.subject.name,self.user.username,self.started)

class Question(models.Model):
    subject = models.ForeignKey(ExamSubject,on_delete=models.CASCADE,related_name='questions')
    question = models.CharField(max_length=500)
    answer_a = models.CharField(max_length=100)
    answer_b = models.CharField(max_length=100)
    answer_c = models.CharField(max_length=100)
    answer_d = models.CharField(max_length=100)
    correct_ans = models.CharField(max_length=1)

    def __str__(self):
        return "Subject {} Question {} a) {} b) {} c) {} d) {}".format(
            self.subject.name,
            self.question,
            self.answer_a,
            self.answer_b,
            self.answer_c,
            self.answer_d
        )

class Answer(models.Model):
    user = models.ForeignKey(ExamUser,on_delete=models.CASCADE,related_name='answers')
    ques = models.IntegerField()
    ansr = models.CharField(max_length=1)

    def __str__(self):
        return "Subject {} , ques_id {} ansr {}".format(self.user.user.username,self.ques,self.ansr)


class Certificate(models.Model):
    exam_user = models.ForeignKey(ExamUser,related_name='certfct',on_delete=models.CASCADE)
    cert_id = models.CharField(max_length=20,null=False)
    type = models.IntegerField()    # 1-> passed 2-> participated
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "subject {} cert_id {} type {} created_on {}".format(self.exam_user.subject.name,self.cert_id,self.type,self.created_on)

