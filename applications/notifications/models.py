import reversion
from django.db import models


@reversion.register()
class UserInfo(models.Model):
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name = "User Info"
        verbose_name_plural = "User Info's"

    def __str__(self):
        return f"{self.label} - {self.value}"


@reversion.register()
class Onboarding(models.Model):
    day = models.IntegerField(default=0)
    copy = models.TextField()
    userinfo = models.ManyToManyField(UserInfo, blank=True)

    class Meta:
        verbose_name = "Onboarding"
        verbose_name_plural = "Onboarding"

    def __str__(self):
        return f"{self.day} - {self.copy[:60]}"


@reversion.register()
class Lapsed(models.Model):
    ident = models.CharField(max_length=200)
    copy = models.TextField()
    userinfo = models.ManyToManyField(UserInfo, blank=True)
    days = models.IntegerField(default=5)

    class Meta:
        verbose_name = "Lapsed"
        verbose_name_plural = "Lapsed"

    def __str__(self):
        return f"{self.ident} - {self.copy[:60]}"


@reversion.register()
class Reminder(models.Model):
    copy = models.TextField()

    def __str__(self):
        return f"{self.copy[:60]}"


@reversion.register()
class LocalNotification(models.Model):
    slug = models.CharField(max_length=64)
    title = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField()
    destination = models.CharField(max_length=64, default="", blank=True)
    isLapsed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
