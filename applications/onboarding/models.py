import reversion
from django.db import models


@reversion.register()
class ReadyToGetStarted(models.Model):
    intro_new_user = models.TextField()
    intro_migrating_user = models.TextField()
    motion_fitness = models.TextField()
    location = models.TextField()
    notifications = models.TextField()
    terms_link = models.TextField()

    class Meta:
        verbose_name = "Ready to get started"
        verbose_name_plural = "Ready to get started"

    def __str__(self):
        return "Ready to get started"


@reversion.register()
class Onboarding(models.Model):
    """
    Model used for storing text for some of the on boarding views the users see when starting the app.
    """  # noqa: E501

    motion_fitness = models.TextField()
    location = models.TextField()
    notifications = models.TextField()
    goals = models.TextField()
    about_you = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "On boarding"
        verbose_name_plural = "On boarding"

    def __str__(self):
        return "On boarding"
