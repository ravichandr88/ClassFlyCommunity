
from django.shortcuts import render,redirect,HttpResponse
from django.http import FileResponse

# Create your views here.
def about(request):
    return render(request, 'about.html',{'title':'About Us'})
def home(request):
    return render(request, 'home.html',{'title':'Home'})

def community(request):
    return render(request, 'community.html',{'title':'Community'})
def lib(request):
    return render(request, 'lib.html',{'title':'Video Library'})
def default(request):
	return render(request, 'default.html',{'title':'error'})

def upload(request):
    return render(request,'upload.html',{'title':'Community'})

import os

def generate_PDF(request):
    return FileResponse(open('ClassFlyTraining.pdf', 'rb'), content_type='application/pdf')


def generate_detailsPDF(request):
    return FileResponse(open('ClassFlyTrainingCollege.pdf', 'rb'), content_type='application/pdf')