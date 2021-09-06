from django.contrib import admin


# Register your models here.

from .models import TwoGroup,Messages

admin.site.register(TwoGroup)
admin.site.register(Messages)