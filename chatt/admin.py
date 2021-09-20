from django.contrib import admin


# Register your models here.

from .models import TwoGroup,Messages,OnlineStatus,MeetingChat,MeetingMessages

admin.site.register(TwoGroup)
admin.site.register(Messages)
admin.site.register(OnlineStatus)
admin.site.register(MeetingChat)
admin.site.register(MeetingMessages)