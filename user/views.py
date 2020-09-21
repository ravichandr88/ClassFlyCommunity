from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import Loginform
from .models import Phonenumber
from django.contrib.auth.password_validation import validate_password
import django.contrib.auth.password_validation as validators

from django.core import exceptions


def signup(request):
    return render(request, 'signup.html', {'title': 'Sign-Up'})

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
        
        return redirect('cfhome') 

         

        




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
        return render(request,'signup.html',context={})
    # print(request.POST)
    data = request.POST
    user = User(username = data['loginName'],
    first_name = data['displayName'],
    password = data['password'] )

    


    if User.objects.filter(username = data['loginName']).count() == 0:
        user.save()
        Phonenumber(user=user,phone_number=data['phoneNumber']).save()
    else:
        User.objects.filter(username = data['loginName']).delete()
        user.save()
        Phonenumber(user=user,phone_number=data['phoneNumber']).save()
    
    login(request,user)

    return render(request,'videos.html',context={})



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
   