from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import Loginform
import requests
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse

from .models import Phonenumber,OTP
from django.contrib.auth.password_validation import validate_password
import django.contrib.auth.password_validation as validators
from django.urls import resolve, Resolver404
from django.http import HttpResponseRedirect 
from django.shortcuts import redirect
from random import randint
from django.core import exceptions

from .models import Email


@csrf_exempt
def loginview(request):
    if request.method == 'GET':
        return render(request,'login.html',{})
    else:
        data = dict(request.POST)
        data['username'] = data['username'][0]
        data['password'] = data['password'][0]
        #check if username exists

        user = None
        if User.objects.filter(username=data['username']).count() == 0:
            print(User.objects.filter(username=str(data['username'])),data)
            if Phonenumber.objects.filter(phone_number = data['username']).count() == 0:
                return HttpResponse('Username or Phone number not found')
            user = Phonenumber.objects.get(phone_number=data['username']).user
        else:
            user = User.objects.get(username=data['username'])
         
        user = authenticate(request, username=user.username, password=data['password'])
    
        if user == None:
            print(user)
            return HttpResponse('Incorrect Paaword , please try again<br><a href="/login" >Go Back</a>')

        #if everything is good
        login(request,user)
        url = request.POST.get("next")
        # print(request.POST)
        try:
            resolve(url)
            return HttpResponseRedirect(url)
        except Resolver404: # Make sure the url comes from your project
            return redirect("cfhome") # A default view
         

        




def home(request):
    return render(request,'ClassFlyStatic/home.html',{})

def php(request):
    return render(request,'ClassFlyStatic/php.html',{})

def python(request):
    return render(request,'ClassFlyStatic/python.html',{})


def angular(request):
    return render(request,'ClassFlyStatic/angular.html',{})


def ds(request):
    return render(request,'ClassFlyStatic/ds.html',{})

def ml(request):
    return render(request,'ClassFlyStatic/ml.html',{})


def web(request):
    return render(request,'ClassFlyStatic/web.html',{})


def java(request):
    return render(request,'ClassFlyStatic/java.html',{})


def sql(request):
    return render(request,'ClassFlyStatic/sql.html',{})


def eh(request):
    return render(request,'ClassFlyStatic/eh.html',{})

def privacy(request):
    return render(request,'privacy.htm',{})

from .forms import VideoUploadForm
def videoupload(request):
    if request.method == 'GET':
        return render(request, 'videouploader.html')
    
    form = VideoUploadForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        print(form.cleaned_data)
    else:
       print( form.errors.as_data)
    return HttpResponse(request.POST) 


@csrf_exempt
def subsignup(request):
    if request.method == 'GET':
        if 'username' in request.session.keys():
            request.session.pop('username') 
        return render(request,'signupnew.html',context={})
    # print(request.POST)
    #if the user has given etails and not verified number
    # print(request.session.keys())
    data={}
    if 'loginName' in request.POST.keys():    #when user submit his details
        data = request.POST.dict()
        #validation for user details
        print(len(data['phoneNumber']))
        if User.objects.filter(username=data['loginName']).count() != 0:
            data['error'] = 'Username already exists'
            return render(request,'signupnew.html',context = data)
        elif   not str(data['phoneNumber']).isdecimal() :
            data['error'] = 'Phone Number should be numbers only'
            return render(request,'signupnew.html',context = data)
        elif len(data['phoneNumber']) != 10:
            data['error'] = 'Phone Number should length of 10 digits'
            return render(request,'signupnew.html',context = data)
        elif (Phonenumber.objects.filter(phone_number=data['phoneNumber']).count() != 0) and (User.objects.get):
            if Phonenumber.objects.filter(phone_number=data['phoneNumber'])[0].user.is_active:
                data['error'] = 'Phone Number already exists'
                return render(request,'signupnew.html',context = data)
            else:
                Phonenumber.objects.get(phone_number=data['phoneNumber']).delete()
            
        user = User(username = data['loginName'],
        first_name = data['displayName'],
        password = data['password'] )
        request.session['username'] = data['loginName'] #to remember the user has given details
        user.is_active = False
        user.save()  
        Phonenumber(user=user,phone_number=data['phoneNumber']).save()
        otp = str(randint(1234,9876))
        OTP(user=user,otp=otp).save()
        print("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(data['phoneNumber'],otp))
        resp = requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(data['phoneNumber'],otp))
          #generate otp for the user
        # print(resp.text)
        return render(request,'signupnew.html',context={'otp':True,'phoneNumber':data['phoneNumber']})
    
    elif 'otp' in request.POST.keys():   # when otp is submittted
        print(request.POST)
        otp = request.POST['otp']   #otp entered by user
        # otp frm the table
        t_otp = OTP.objects.get(user__username = request.session['username'])
        if otp is t_otp:
            user = User.objects.get(username = request.session['username'])
        # if otp matches to the table ,success
            login(request,user)

            return render(request,'lib.html',context={})

        # if otp does not match the otp entered by the user
        #if failed otp
        return render(request,'signupnew.html',context={'otp':True,'error' : 'OTP did not match'})

    elif 'phoneNumber' in request.POST.keys():

        data = request.POST
        if Phonenumber.objects.filter(phone_number=data['phoneNumber']).count() > 0:
            return render(request,'signupnew.html',context={'phone':True,'error':'Phone Number Already exists'})
        elif   not str(data['phoneNumber']).isdecimal() : 
            return render(request,'signupnew.html',context={'phone':True,'error': 'Phone Number should be numbers only'})
        elif len(data['phoneNumber']) == 10:
            return render(request,'signupnew.html',context ={'phone':True,'error': 'Phone Number should length of 10 digits'})
        
        phone = Phonenumber.objects.get(user__username = request.session['username'])
        phone.phone_number = data['phoneNumber']
        otp = OTP.objects.get(user__username = request.session['username'])
        otp.count+=1
        otp.save()
        phone.save()

        #IF user have used too many sms, max is 25 otp sms per user
        if otp.count > 25:
           return HttpResponse("You have used too many otp sms, Due to security reasons we are deactivating your account. Please contact +91 8972233124")
        
        requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(phone_number.phone_number,otp.otp))
    
        return render(request,'signupnew.html',context={'otp':True})
        #change the phone number in the phone number table


   # view function to resend otp
@csrf_exempt
@api_view(['GET'])
def resend_otp(request):
    #check if user otp

    user = User.objects.get(username = request.GET['username'])
    phone_number = Phonenumber.objects.get(user = user)
    otp = OTP.objects.get(user = user)
    #check if the user has remianing otps
    if otp.count > 25:
        return HttpResponse("You have used too many otp sms, Due to security reasons we are deactivating your account. Please contact +91 8972233124")
        
    requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(phone_number.phone_number,otp.otp))
    return Response(data={'sucess':True})

   



@csrf_exempt
@api_view(["POST","GET"])
def password_reset(request):
    print('good')
    if request.method == 'POST':
        data = dict(request.data)
        new_password = data['new_password'][0]
        phoneNumber = data['phoneNumber'][0]
        country = data['countryCode'][0]
        otp_code = data['otpcode'][0]

        user = Phonenumber.objects.get(phone_number=phoneNumber)

        try:
            validators.validate_password(password=new_password, user=user)
        except exceptions.ValidationError as e:
            error = list(e.messages)[0]
            return Response(data={'message':error},status=400)
                


        #Using username and oldpassword, try to login,If user is genuine, we will get access toke,
        #Change the password to  new password
        import requests 
        import json

        # api-endpoint 
        URL = "https://api-jp.kii.com/api/apps/kmjufxhuj911/users/PHONE:"+ country + phoneNumber +"/password/complete-reset"

        
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {
                "pinCode": otp_code,
                "newPassword": new_password
            }
            
        HEADERS= {
               "Authorization" : "Basic a21qdWZ4aHVqOTExOjY4MjY3ZWQ5NmVmOTQ4M2VhYjE1OWVkMjdlN2U0ODgz",
                "Content-Type": "application/vnd.kii.CompletePasswordResetRequest+json"
                 }			


        # sending get request and saving the response as response object 
        r = requests.post(url = URL,headers=HEADERS, data = json.dumps(PARAMS))
        # print(r.content)
        print(r.status_code)
        
        # extracting data in json format 
        if str(r.status_code) != '204':   #if YES, change the password,
            return Response(data={'code':'failed','message':r.json()['message']},status=500)
            #get the new password and add it as current password for the user
        else:   
            user =  Phonenumber.objects.get(phone_number=phoneNumber).user
            user.set_password(new_password)
            user.save()
            return Response(data={'code':'success','message':'Password Changed Successfully'},status=200)
       
            
        return Response(data={'code':'good'})
    
    return render(request,'password.html',{})
    



@csrf_exempt
@api_view(['POST','GET'])
def example(request):
    print(request.data)
    return Response(data={})
   

def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("cfhome")

def webinar(request):
    return render(request,'register.html')

@csrf_exempt
@api_view(['GET'])
def save_email(request):
    Email(gmail=request.GET['gmail']).save()
    return Response(data={'code':'success'})

def redirect_event(request):
    return redirect('register')