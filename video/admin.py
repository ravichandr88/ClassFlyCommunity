from django.contrib import admin
from .models import DeptHead,Subject,Playlist,Department,VideoId,EducationDomain
from .models import VideoDeptHead,VideoMaker,VideosMade,Notes

admin.site.register(DeptHead)
admin.site.register(Subject)
admin.site.register(Playlist)
admin.site.register(Department)
admin.site.register(VideoId)
admin.site.register(EducationDomain)
admin.site.register(VideoDeptHead)
admin.site.register(VideoMaker)
admin.site.register(VideosMade)
admin.site.register(Notes)




# Register your models here.
