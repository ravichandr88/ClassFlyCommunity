from django.shortcuts import render
from django import forms
from django.http.request import QueryDict, MultiValueDict
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from django.forms.utils import ErrorList
import re
# Create your views here.

from .forms import SignupForm
from .sample_tasks import create_task

from rest_framework.decorators import api_view

#Function to validate Phone Number



def signup(request):
    if request.method == 'POST':
        data = request.POST.dict()
        form = SignupForm(request.POST)
        #Validate Phone Number

        if form.is_valid():
            return render(request,'signupcopy.html', context={'form':form})
        else: 
            errors = form._errors.setdefault("username", ErrorList())
            error_message = str(errors.as_text())
            errors.clear()
            error_message = error_message.replace('username','phone number',1)
            errors.append(u"" + error_message)
            return render(request,'signupcopy.html', context={'form':form})
    return render(request, "signupcopy.html", context={'form':SignupForm()})

def searchpage(request):
    # working model   
    return render(request,'search_page.html')

def login(request):
    return render(request,'prologin.html')

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
    task = create_task.delay(int(task_type))
    return Response(data={"task_id": task.id}, status=202)
    # return Response(data={'caught':'No'})