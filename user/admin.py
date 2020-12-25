from django.contrib import admin
from .models import Email,Phonenumber,OTP

admin.site.register(Email)
# Register your models here.

admin.site.register(Phonenumber)

admin.site.register(OTP)