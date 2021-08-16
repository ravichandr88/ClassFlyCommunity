from django.contrib import admin

# Register your models here.

from .models import Jobpost, Applicantion

admin.site.register(Jobpost)
admin.site.register(Applicantion)