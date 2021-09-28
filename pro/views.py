from django.shortcuts import render,redirect,HttpResponse
from django import forms
from django.http.request import QueryDict, MultiValueDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from interview.models import Fresher,Prfessional, HRaccount

from .models import  EmailOTP



from exam.models import Certificate
from .sample_tasks import send_student_otp,send_email_otp


from django.http.response import JsonResponse

from rest_framework.response import Response
from django.forms.utils import ErrorList
import re
from random import randint
# Create your views here.
from django.contrib.auth.models import User
from .forms import SignupForm, SMSotpForm, LoginForm,EmailOTPForm,EmailForm, ResetPasswordForm, PasswordResetForm
from .sample_tasks import get_call, send_otp
from django.core.exceptions import ValidationError 

from rest_framework.decorators import api_view

#models for sending otp
from user.models import Phonenumber,OTP

# function header to check whether username stored in request object or not
def session(function):
    # @wraps(function)
    def inner(request, *args, **kwargs):
            # print(request.session.keys())
            if 'username' in request.session.keys(): 
                # print(request.session)
                return function(request, *args,  **kwargs)
            elif request.user:
                return redirect('pro_home')
            else:
                return redirect('login_new')

    return inner

def start(request):
    return redirect('start')

def startpage(request):
    return render(request,'startpage.html',context={})



def signup(request,type="student"):
    title = 'Welcome To ClassFly'

    # print(request.user)
    #IF the user is already logged in 
    if request.user is  not 'AnonymousUser':
        # print(request.user)
        if Fresher.objects.filter(user__username = request.user).count() == 1:
            return redirect('f_dashboard')
         
        elif Prfessional.objects.filter(user__username = request.user).count() == 1:
            return redirect('pro_dashboard')
        
        elif HRaccount.objects.filter(user__username = request.user).count() == 1:
            return redirect('hrdashboard')
        

        

    # Signup candidate type of registration, -> student,proessional,company
    request.session['type'] = type

    
    if request.method == 'POST':
# check if the username exists and not activated, dele the user account
        

        form = SignupForm(request.POST)

        if User.objects.filter(username = form.data['username'], is_active = False).count() == 1:
            User.objects.get(username = form.data['username']).delete()
        

        #Validate Phone Number

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            
            #save username in request object
            request.session['username'] = user.username
            request.session['reason'] = 'signup'

            #prepare otp for the user confirmation
            otp = str(randint(1234,9876)) 
            otp = OTP(user=user,otp=otp)
            otp.save()
            send_otp(user.username,otp.otp)

            return redirect('otp_verify')
        else: 
            #IF error contains 'username' message, replace it with 'phone number'
            errors = form._errors.setdefault("username", ErrorList())
            error_message = str(errors.as_text())
            errors.clear() 
            error_message = error_message.replace('username','phone number',1)
            errors.append(u"" + error_message)
            return render(request,'signupcopy.html', context={'form':form,'title':title})
    return render(request, "signupcopy.html", context={'form':SignupForm(), 'title':title})


@session
def otp_verify_view(request):
    title = 'Phone OTP Verification'

    print(request.session['username'])

    if request.method == 'POST':
        form = SMSotpForm(request.POST)
        # print(request.session['username'])
        if form.is_valid():
            #Code to activate normal user account activation
            user = User.objects.get(username=request.session['username'])
                
            

            try:
                otp = form.cleaned_data['otp']
                print(form.cleaned_data['otp'])
                otp = OTP.objects.get(user=user,otp=otp)
                user.is_active = True
                user.save()
                print(request.session.keys())
                #Check the reason for OTP
                if request.session['reason'] == 'signup':
                    
                    return redirect('emailpage')
                    # code that will redirect the users with respect to account type

                   
                elif request.session['reason'] == 'reset_password':
                    return redirect('password_reset_pro') 
                
            except:
                errors = form._errors.setdefault("otp", ErrorList())
                errors.clear()
                error_message = str('OTP did not match')
                errors.append(u"" + error_message)
                return render(request,'signupcopy.html', context={'form':form, 'title' : title})

           
                
    otp_form = SMSotpForm()
    return render(request,'signupcopy.html', context={'form':otp_form, 'title': title})



# Function to accept  Email from User
@session
def email_function(request):
    title = 'Email is Required'
    print(request.session.keys())
    
    form = EmailForm()
    
    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            # Createa otp for email and save it into DB
        
            # Send otp for this email
            
            #  otp generated will be saved into  odel and only then sent through email
            otp = randint(111111,999999)

            # User object for reference, and update the email
            user = User.objects.get(username = request.session['username'])
            user.email = form.cleaned_data['email']
            user.save()

            

            email_otp = EmailOTP(
                user = user,
                otp = otp
            )


            # If the user has already created email otp oject just override it
            if EmailOTP.objects.filter(user__username = request.session['username']).count() != 0:
                email_otp = EmailOTP.objects.get(user__username = request.session['username'])

            
            
            email_otp.save()

            send_email_otp(user, email_otp.otp)
            return redirect('email_otp_verify')

    return render(request,'signupcopy.html', context={'form':form,'title':title})


# Function to recive the email otp from user
@session
def email_otp(request):
    print(request.session.keys())
    title = 'Email OTP please..'

    # First check whether the user have requedsted for email otp
    form  = EmailOTPForm()

    
    if request.method == 'POST':
        form = EmailOTPForm(request.POST)

        if form.is_valid():
            otp = form.cleaned_data['email_otp']
            if EmailOTP.objects.filter(user__username = request.session['username'],otp = otp).count() == 1:
                # disbale the otp "requested" varibale in "EmailOTP" table 
                    
                    emailotp = EmailOTP.objects.get(user__username = request.session['username'])

                    emailotp.requested = False

                    user = User.objects.get(username = request.session['username'])

                    #After Successfull OTP validation Login the user
                    user.is_active = True   #activate user account
                    user.save()
                    login(request,user)
                    #after successful signup, redirect user based on type from request, -> student,professional,company
                    if 'type' in request.session.keys():
                        if request.session['type'] == 'student':
                            return redirect('student')
                        
                        elif request.session['type'] == 'professional':
                            return redirect('professional')

                        elif request.session['type'] == 'company': 
                            return redirect('company')
                        else:
                            return redirect('selection')
                    else:
                        return redirect('selection')

    return render(request,'signupcopy.html', context={'form':form,'title':title})

# Selection Function, if they have signed up for the account and not selected any account type
#  Fresher, Professional, HRaccount
def selection(request):

    return render(request,'selection.html')


# function to resend email otp through REST api
@session
def resend_email_otp(request,):

    user = User.objects.get(username = request.session['username'])

    # First check whether email otp has been requested or not
    if EmailOTP.objects.filter(user__username = user.username).count() == 0:

        return  JsonResponse({'message':'user has not found'},status=400)
    
    # Check whether user has approved for email otp request
    email_otp = EmailOTP.objects.get(user__username = user.username)
    
    if email_otp.requested:
        send_email_otp(User.objects.get(username = user.username),email_otp.otp)

    return  JsonResponse({'message':'Successfully sent'},status=200)



@session
def resend_otp(request):
    
    user = User.objects.get(username = request.session['username'])
    if OTP.objects.filter(user = user).count() != 0:
        otp = OTP.objects.get(user = user)
    else:
        otp = str(randint(1234,9876)) 
        otp = OTP(user=user,otp=otp)
        otp.save()
    
    otp.count+=1
    otp.save()

    #check if the user has remianing otps
    if otp.count > 25:
        return JsonResponse({'message':'Sorry'},status=500)
        
    send_otp(user.username,otp.otp)
    return JsonResponse({'message':'Sent Successfully'},status=200)



def login_view(request): 
    #IF the user is already logged in 
    title = 'Please Login'
    
    form = LoginForm()

    if str(request.user) != 'AnonymousUser':
        return redirect('pro_home')
 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            user = authenticate(request, username=form.user.username, password=form.cleaned_data['password'])
            
            print(user == None)
            
            if user == None:
                form.add_error('password','Incorrect password')
                return render(request,'signupcopy.html',context={'form':form,'title':title})
            
            #Login the User
            login(request,user)

            if Fresher.objects.filter(user = user).count() == 1:
                return redirect('f_dashboard')
            elif Prfessional.objects.filter(user = user).count() == 1:
                return redirect('pro_dashboard')
            elif HRaccount.objects.filter(user = user).count() == 1:
                return redirect('hrdashboard')
            

            return redirect('pro_home')  
        
        else:
            # variables for working with phone and email otp
            request.session['username'] = request.POST['phone_number']
            request.session['reason'] = 'signup'
            # If user account is not activated, reirect to OTP page
            if form.phone_redirect:
                return redirect('otp_verify')
            elif form.email_redirect:
                return redirect('emailpage')
            

        
    return render(request,'signupcopy.html',context={'form':form,'title':title})


@login_required
def logout_view(request):
    logout(request)
    return redirect('pro_home')

import requests
def forgot_password(request):

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = form.cleaned_data['phone_number'])

            if OTP.objects.filter(user = user).count() != 0:
                otp = OTP.objects.get(user = user)
                otp.delete()
            otp = str(randint(1234,9876)) 
            otp = OTP(user=user,otp=otp)
            otp.save()
            send_otp(form.cleaned_data['phone_number'],otp.otp)
            # requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(form.cleaned_data['phone_number'],otp.otp))
   

            #remind our app that he is aloowed to access OTP page
            request.session['username'] = form.cleaned_data['phone_number']
            request.session['reason'] = 'reset_password'
            return redirect('otp_verify')
        else:
            return render(request, 'signupcopy.html',context={'form':form})

    form = ResetPasswordForm()
    return render(request, 'signupcopy.html',context={'form':form})
    

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username = request.session['username'])
                validators.validate_password(password=form.cleaned_data['password'], user=user)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('login_new')
            except exceptions.ValidationError as e:
                error = list(e.messages)[0]
                form.add_error('password',error)
                return render(request, 'signupcopy.html',context={'form':form})
        else:
            return render(request, 'signupcopy.html',context={'form':form})

    form = PasswordResetForm()
    return render(request, 'signupcopy.html',context={'form':form})


def searchpage(request):
    # working model   
    return render(request,'search_page.html')


def homepage(request):
    return render(request,'homepage.html')

def profile_card(request):
    return render(request,'profile_card.html')

def project_detail(request):
    return render(request,'project_page.html')


@csrf_exempt
@api_view(['GET','POST'])
def run_task(request):
    print(request.POST)
    task_type = 1
    task = get_call(int(task_type))
    return Response(data={'task_id':task.id}, status=202)
    # return Response(data={'caught':'No'})


@api_view(['GET'])
def temp_otp(request,phone,otp):
    obj = Certificate.objects.get(id=1)
    obj.type = obj.type + 1
    obj.save()
    if obj.type > 20:
        return Response(data={'message':'You have exceeded you OTP limit'},status=500)

    send_student_otp(phone,otp)
    # requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(phone,otp))
    
    return Response(data={'message':'OTP sent'},status=200)
