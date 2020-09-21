
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

def generate_PDF(request):
    # file = open('PHPClassFly.pdf', "w+b")
    # file.seek(0)
    # pdf = file.read()
    # file.close()
    # return HttpResponse(open('PHPClassFly.pdf', "w+b"), 'application/pdf')
    
    # return FileResponse(open('PHPClassFly.pdf', 'rb'), content_type='application/pdf')
   
    return FileResponse(open('PHPClassFly.pdf', 'r'), content_type='application/pdf')
    # with open('PHPClassFly.pdf', 'rb') as pdf:
    #     response = HttpResponse(pdf.read(), content_type='application/pdf')
    #     response['Content-Disposition'] = 'inline;filename=some_file.pdf'
    #     return response