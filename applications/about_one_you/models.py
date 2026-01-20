import reversion
from django.db import models


@reversion.register()
class Application(models.Model):
    """
    model used for storing applications on ABOUT ONE YOU screen
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    ios = models.URLField()
    android = models.URLField()
    icon = models.ImageField()
    list_order = models.PositiveIntegerField(default=0, help_text="Ascending ordering, 0 be first")

    class Meta:
        verbose_name = "App"
        verbose_name_plural = "Apps"
        ordering = ["list_order"]  # noqa: RUF012

    def __str__(self):
        return self.name


@reversion.register()
class AboutOneYou(models.Model):
    """
    model used for storing text on ABOUT ONE YOU screen
    """

    text = models.TextField()

    class Meta:
        verbose_name = "About Better Health"
        verbose_name_plural = "About Better Health"

    def __str__(self):
        return f"{self.text[:50]}..."
