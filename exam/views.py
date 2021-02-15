from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from user.models import Phonenumber
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .validation import user_validation
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import random
import string
import requests
from django.utils import timezone
import datetime
import django.contrib.auth.password_validation as validators
from django.core import exceptions
import datetime

from .models import ExamUser,ExamSubject,Question,Answer,Certificate



#code to generate pdf
from django.http import HttpResponse
from django.views.generic import View
from django.template import Context


from django.template.loader import render_to_string
import tempfile





#function to generate random password
def get_random_string():
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(5))
    return result_str.lower()+str(random.randint(1234,9876))



@login_required
def exam_home(request):
    if ExamUser.objects.filter(user=User.objects.get(username=request.user)).count() != 0:
        subjects = ExamUser.objects.filter(user=User.objects.get(username=request.user))
    else :
        subjects = []
    return render(request, 'examhome.html', context={'subjects':subjects})

# Exam writing page 
@login_required
def exam(request,subj):
    #Condition to check whether user is registered for the exam
    if ExamUser.objects.filter(id=subj).count() == 0:
        return HttpResponse('Exam not found, Please contact support@classfly.in')
    exam = ExamUser.objects.get(user=User.objects.get(username=request.user),id=subj)
    if exam.exam_over:
        return HttpResponse('Sorry, Invalid exam id for the USER')
    
    #Gather the detials for fthe exam, PAHSE = 1
       
    subject = ExamUser.objects.get(id=subj)
    total_ques = subject.subject.questions.all()[:subject.subject.count]
    total = len(total_ques)
    time = int(total*1.5)       #variable to show the time for completing exam
    phase = 0   #the phase to keep html division active

    request.session['subj_id']=subj #store the subjectID in the request object for further user
    
    return render(request,'examstart.html',context={'subject':subject,'total':total,'time':time,'phase':phase})



@login_required
@cache_control(no_cache=True, must_revalidate=True)
def question(request,qid):
    #Check if whether the subject is present or not
    # print(not('subj_id'  in request.session.keys()))
    if not('subj_id'  in request.session.keys()):
        return HttpResponse('Sorry, Not a proper way to start exam')
    #get the siubject id and subject

    subj = request.session['subj_id']
    #Check whether this is the begning of the exam

    if ExamUser.objects.filter(user=User.objects.get(username=request.user)) == 0:
        return  HttpResponse('Sorry, You are not registered for this exam')
    elif ExamUser.objects.filter(id=subj).count() == 0:
        return  HttpResponse('Sorry, you are not registered for this subject')
    elif (qid < 1) or (qid > ExamUser.objects.get(id=subj).subject.count):  
        return  HttpResponse('Sorry, Not a valid question number')

    exam = ExamUser.objects.get(user=User.objects.get(username=request.user),id=subj)
    
    #Check if exam over or not
    if exam.exam_over:
        return redirect('result')
    
    #start the exam timer if it is not stareted
    if exam.started is None:
        exam.started = timezone.now()
        exam.save()
    
    #If exam has started, check the time remaining
    time_remaining = (exam.started + datetime.timedelta(minutes=int(exam.subject.count*1.5))) -  timezone.now()  
    # print(time_remaining)
    if timezone.now() > (exam.started + datetime.timedelta(minutes=int(exam.subject.count*1.5))):
        return HttpResponse(" Exam time is  over <a href='/result'> <button > Result </button></a> ")
    
    time_remaining = str(time_remaining).split(':')
    # print(time_remaining)
    time_remaining = int(time_remaining[0])*3600 +  int(time_remaining[1])*60 + int(float(time_remaining[2]))
    # print(time_remaining)
    
    #return the question and options
    # print(exam.subject.questions.all())
    question = exam.subject.questions.all()[qid-1:qid][0]
    prev = qid-1
    next = qid+1
    actual_qid = question.id
    question.id = qid
    context = {'question':question,'prev':prev,'next':next,'exam':exam,'time':time_remaining,'actual_qid':actual_qid}
    #Answer part, see if the user has already answered
    ans = Answer.objects.filter(user=exam,ques=actual_qid)
    if len(ans) != 0:
        ans = ans[0].ansr
    context[ans]='checked'
    return render(request,'question.html',context=context)

@login_required
def result(request,subj=0):
    if subj == 0:
        subj = request.session['subj_id']
    if ExamUser.objects.filter(id=subj).count() == 0:
        return  HttpResponse('Sorry, you are not registered for this subject')
    exam = ExamUser.objects.get(id=subj) 
    exam.exam_over = True
    exam.save()

    
    #right answers
    r_ans = len([i for i in exam.answers.all()[:exam.subject.count] if len(Question.objects.filter(subject=exam.subject,id=i.ques,correct_ans=i.ansr)) != 0])
    

    w_ans = exam.subject.count-r_ans
    context = {
        'subject_name':exam.subject.name,
        'right_answers':r_ans,
        'wrong_answers':w_ans,
        'score':round((r_ans/exam.subject.count)*100),
        'exam': exam
    }
    s = 'qwertyuiop'
    id_str = ''.join([s[int(j)] for j in str(subj) ])
    print(id_str)
    if (round((r_ans/exam.subject.count)*100) >= 50) and (Certificate.objects.filter(exam_user=exam).count() == 0):
        cert = 'CF'+ str(exam.subject.id) + '000' + str(exam.id)

        Certificate(exam_user=exam,cert_id=cert,type=1).save()
        
        # id_int = int(''.join([str(s.index(j)) for j in id]))

    context['cert_id']=id_str
    return render(request,'result.html',context=context) 

#certificate 
# @login_required
def certificate(request,id):

    s = 'qwertyuiop'
    # g = ''.join([s[int(j)] for j in i ])
    id_int = int(''.join([str(s.index(j)) for j in id]))
    subj = id_int
    if ExamUser.objects.filter(id=subj).count() == 0:
        return  HttpResponse('Sorry, User is not registered for this subject')
    exam = ExamUser.objects.get(id=subj)
    date = ''
    if (Certificate.objects.filter(exam_user=exam).count() == 0) and (exam.exam_over) :
        # cert = 'CF'+ str(exam.subject.id) + '000' + str(exam.id)

        cert = Certificate(exam_user=exam,cert_id=cert,type=1)
        cert.save()
        date = cert.created_on.date()
       
    else:
        cert = Certificate.objects.get(exam_user=exam)
        date = cert.created_on.date()
        
    
    return render(request, 'certificate.html',context={'name':exam.user.first_name,'cert_id':cert.cert_id ,'subj_name':exam.subject.name,'date':date})


@csrf_exempt
@api_view(['GET'])
def answer(request,qid,exuid,ans):
    exuser = ExamUser.objects.filter(id=exuid)[0]
    ansr = Answer.objects.filter(user=exuser,ques=qid)
    if len(ansr)==0:
        Answer(user=exuser,ques=qid,ansr=ans).save()
    else:
        ansr = ansr[0]
        ansr.ansr=ans
        ansr.save()
    return Response(data={'status':True},status=200)

#Function to accept credentials from excel sheet and post them to user database 
#Students account registering for exam
@csrf_exempt
@api_view(['POST','GET'])
def register(request):
    """
    {'phone_number':
    'email':
    'name':
    'exam_id':
    }
    """
    print(request.data)
    user_validation(request.data['phone_number'],request.data['email'])
    password = get_random_string()
    
    user = User(
        username=request.data['email'],
        first_name=request.data['name'],
        )
    try:
            validators.validate_password(password=password, user=user)
    except exceptions.ValidationError as e: 
            error = list(e.messages)[0]
            return Response(data={'message':error},status=400)
    user.set_password(password)
    user.save() 
    Phonenumber(user=user,phone_number=request.data['phone_number']).save()
    ExamUser(user=user,subject=ExamSubject.objects.get(id=request.data['exam_id'])).save()
    requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+password:{}%2CLogin+with+this+password.".format(request.data['phone_number'],password))



    return Response(data={'status':True},status=200)


#Saves the questions from the computer
@csrf_exempt
@api_view(['POST','GET'])
def save_question(request):
    '''
    {'exam_sub_id':
    'question':
    answer_a:
    answer_b:
    answer_c:
    answer_d:
    correct_ans:}
    '''
    data = request.data
    exam_sub = ExamSubject.objects.get(id=data['exam_sub_id'])
    Question(subject=exam_sub,question=data['question'],answer_a=data['answer_a'],
    answer_b=data['answer_b'],
    answer_c=data['answer_c'],
    answer_d=data['answer_d'],
    correct_ans=data['correct_ans']).save()

    return Response(data={'status':True})


def budget(request):
    return render(request,'sample.html')