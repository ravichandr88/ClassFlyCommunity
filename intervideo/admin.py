from django.contrib import admin

# Register your models here.

from .models import Jobpost, Applicantion, InterviewSearch, ResumePurchase, InterviewVideo, Payment, VideoPurchase

admin.site.register(Jobpost)
admin.site.register(Applicantion)
admin.site.register(InterviewSearch)
admin.site.register(InterviewVideo)
admin.site.register(Payment)
admin.site.register(VideoPurchase)
admin.site.register(ResumePurchase)

