from django.contrib import admin


# Register your models here.

from .models import TwoGroup,Messages,OnlineStatus

admin.site.register(TwoGroup)
admin.site.register(Messages)
admin.site.register(OnlineStatus)