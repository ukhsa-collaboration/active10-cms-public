from django.contrib import admin

from applications.rewards.models import *  # noqa: F403

admin.site.register(Reward)  # noqa: F405
