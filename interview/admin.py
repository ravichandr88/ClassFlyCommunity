from django.contrib import admin

# Register your models here.

from .models import Fresher,HRaccount,Company,Experience,Prfessional,ProExperience,Professional_Meeting

admin.site.register(Fresher)
admin.site.register(Experience)
admin.site.register(Prfessional)
admin.site.register(ProExperience)
admin.site.register(Professional_Meeting)
admin.site.register(HRaccount)
admin.site.register(Company)