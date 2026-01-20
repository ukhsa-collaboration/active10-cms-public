import reversion
from ckeditor.fields import RichTextField
from django.db import models


@reversion.register()
class Link(models.Model):
    url = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.link}"


@reversion.register()
class TermsConditions(models.Model):
    latest_version = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    button = models.CharField(max_length=200)
    agree = models.CharField(max_length=200)
    links = models.ManyToManyField(Link, blank=True)

    class Meta:
        verbose_name = "Terms & Conditions"
        verbose_name_plural = "Terms & Conditions"

    def __str__(self):
        return f"{self.latest_version} - {self.title}"


@reversion.register()
class MissingData(models.Model):
    title_android = models.CharField(max_length=200, default="")
    title_ios = models.CharField(max_length=200, default="")
    text_android = models.TextField()
    text_ios = models.TextField()

    class Meta:
        verbose_name = "Missing Data"
        verbose_name_plural = "Missing Data"

    def __str__(self):
        return f"{self.title_android} / {self.title_ios}"


@reversion.register()
class App(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Operating System"
        verbose_name_plural = "Operating Systems"

    def __str__(self):
        return f"{self.name}"


@reversion.register()
class AppVersion(models.Model):
    app = models.OneToOneField(
        App,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    latest_version = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    button = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Mobile App Version"
        verbose_name_plural = "Mobile App Versions"

    def __str__(self):
        return f"{self.app.name} - {self.latest_version}"


class Accessibility(models.Model):
    device_choices = (("ios", "iOS"), ("android", "Android"))
    device = models.CharField(max_length=200, choices=device_choices)
    text = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = "Accessibility Statement"
        verbose_name_plural = "Accessibility Statement"

        constraints = [models.UniqueConstraint(fields=["device"], name="unique device")]  # noqa: RUF012

    def __str__(self):
        return f"{self.device} - {self.text[:50]}"
