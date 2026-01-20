import reversion
from django.db import models


@reversion.register()
class MyWalk(models.Model):
    condition = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        verbose_name = "My walks dynamic text"
        verbose_name_plural = "My walks dynamic text"

    def __str__(self):
        return self.condition


@reversion.register()
class TodayWalk(models.Model):
    target_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Today's walks dynamic text"
        verbose_name_plural = "Today's walks dynamic text"

    def __str__(self):
        return self.target_name


@reversion.register()
class Target(models.Model):
    condition = models.CharField(max_length=255)
    text = models.TextField()
    target = models.ForeignKey(TodayWalk, on_delete=models.CASCADE)

    def __str__(self):
        return self.condition
