from django.contrib import admin

# Register your models here.

from .models import Trainer,RegsiteredUser,VideoAsset,EmailOTP, Project, Skills, ProjectFlow

admin.site.register(EmailOTP)

admin.site.register(Trainer)

admin.site.register(RegsiteredUser)

admin.site.register(VideoAsset)

admin.site.register(Project)

admin.site.register(Skills)

admin.site.register(ProjectFlow)
