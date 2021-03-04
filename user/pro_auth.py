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

import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.sessions.models import Session


def signup(request):
    #If user is already logged in, redirect to Dashboard

    #If method is GET, return signup Template

    
