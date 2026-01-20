from django.contrib import admin

from .models import Lapsed, LocalNotification, Onboarding, Reminder, UserInfo

admin.site.register(UserInfo)
admin.site.register(Onboarding)
admin.site.register(Lapsed)
admin.site.register(Reminder)
admin.site.register(LocalNotification)
