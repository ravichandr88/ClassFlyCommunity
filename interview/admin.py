from django.contrib import admin

# Register your models here.

from .models import Fresher,HRaccount,Company,Experience,Expert,ProfessionalInterview,Prfessional,ProExperience,Professional_Meeting, Professinal_Interview_Time

admin.site.register(Fresher)
admin.site.register(Experience)
admin.site.register(Prfessional)
admin.site.register(ProExperience)
admin.site.register(Professional_Meeting)
admin.site.register(HRaccount)
admin.site.register(Company)
admin.site.register(Professinal_Interview_Time)
admin.site.register(ProfessionalInterview)
admin.site.register(Expert)