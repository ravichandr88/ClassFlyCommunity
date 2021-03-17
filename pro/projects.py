from django.shortcuts import render,redirect,HttpResponse
from django import forms
from django.http.request import QueryDict, MultiValueDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.core import exceptions

from rest_framework.decorators import api_view

from .models import Project,Trainer,Skills

def slice_list(x):
    n = 3
    l=[]
    while n < len(x):
        l.append(x[n-3:n])
        n+=3
    l.append(x[n-3:])
    return l


def search(request):
    id = 1
    project = Project.objects.get(id=1)
    projects = [project,project,project]
    l = []
    for project in projects:
        data = {
        'project_title': project.title,
        'trainer_name' : project.trainer.name,
        'exp'          : project.trainer.exp,
        'skills'       : slice_list(project.skills.all().values('title')),
        'description'  : project.description,
        'work_period'  : project.work,
        'exp'          : project.trainer.exp          
        }
        l.append(data)
    return render(request,'search.html',context={'data': l})


def project_review(request):
    project = Project.objects.get(id=1)

    skills = project.skills.all()
    n = len(skills)
    skills_percent = [skills[:int(n/2)],skills[int(n/2):]]

    project_flow = project.flow.all()[0]
    flow = str(project_flow.description).split("<>")
    project_flow = {}
    for i in flow:
        head = i.split("<*>")[0]
        flow_list = i.split("<*>")[1:]

        project_flow[head] = flow_list
    
    print(project.presentation)

    data={
        'skills'        : str([i.title for i in skills]).replace('[','').replace(']','').replace("'",'',40),
        'skills_percent': skills_percent,
        'skills_count'  : len(skills),
        'work'          : int(project.work[:2]),
        'project_flow'  : project_flow
    }

    return render(request,'project.html',context={'project':project,'data':data})
