from django.urls import path, include
from . import views
from .validation import user_validation



urlpatterns = [
path('exam/<int:subj>',views.exam),
path('pathway',views.register),                #to register the user for exam  
path('pathques',views.save_question),        #to upload the question to DB
path('examhome',views.exam_home),            #exam homepage 
path('result',views.result),                 #result page after the exam
path('question/<int:qid>',views.question),  #question to answer
path('answer/<int:qid>/<int:exuid>/<slug:ans>',views.answer),
path('certificate',views.certificate), 
path('budget',views.budget)
]