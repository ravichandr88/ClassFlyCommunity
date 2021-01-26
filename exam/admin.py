from django.contrib import admin
from .models import ExamUser,ExamSubject,Answer,Question
# Register your models here.
admin.site.register(ExamSubject)

admin.site.register(ExamUser)

admin.site.register(Answer)

admin.site.register(Question)
