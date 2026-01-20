from django.contrib import admin

from .models import Accessibility, App, AppVersion, Link, MissingData, TermsConditions

admin.site.register(Link)
admin.site.register(App)
admin.site.register(AppVersion)
admin.site.register(TermsConditions)
admin.site.register(MissingData)
admin.site.register(Accessibility)
