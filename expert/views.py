from django.shortcuts import render, HttpResponse

# Create your views here.


def expert_signup_1(request):
    return HttpResponse('expert signup 1')


def expert_signup_2(request):
    return HttpResponse('Expert signup 2')


def professional_applications(request):
    return HttpResponse('Expert Dahboard')

def professional_video_player(request):
    return HttpResponse('Profesional interview video player')

def professional_interview_room(request):
    return HttpResponse('Interview room for expert and professional')