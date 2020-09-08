from django.shortcuts import render
from django.shortcuts import render,redirect

# Create your views here.
def about(request):
    return render(request, 'about.html',{'title':'About Us'})
def home(request):
    return render(request, 'home.html',{'title':'Home'})

def community(request):
    return render(request, 'community.html',{'title':'Community'})
def lib(request):
    return render(request, 'lib.html')
def default(request):
	return render(request, 'default.html',{'title':'error'})