from django.shortcuts import render
from django.shortcuts import render,redirect

# Create your views here.
def about(request):
    return render(request, 'about.html',{'title':'About Us'})
def home(request):
    return render(request, 'home.html',{'title':'Home'})

def community(request):
    return render(request, 'community.html',{'title':'Community'})
def library(request):
    return render(request, 'library.html',{'title':'Video Library'})