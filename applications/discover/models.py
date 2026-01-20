import reversion
from colorful.fields import RGBColorField
from django.core.validators import MaxLengthValidator
from django.db import models


@reversion.register()
class SplashScreen(models.Model):
    """
    model used for storing text on splash screen on Discover view
    """

    title = models.CharField(
        max_length=20,
        help_text="Max: 20 symbols",
    )
    text = models.TextField()
    button = models.CharField(max_length=25, help_text="Max: 25 symbols")
    link = models.URLField(null=True, blank=True)

    is_app = models.BooleanField(default=False)
    android_link = models.URLField(null=True, blank=True)
    ios_link = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Splash Screen"
        verbose_name_plural = "Splash Screen"

    def __str__(self):
        return self.title


@reversion.register()
class Discover(models.Model):
    IMAGE = "image"
    IMAGE_URL = "image_url"
    TEXT = "text"

    NAME_TYPE = ((IMAGE, "Image"), (IMAGE_URL, "Image url"), (TEXT, "Text"))
    published = models.BooleanField(default=True)
    header_image = models.ImageField(blank=True, null=True)
    name_type = models.CharField(max_length=25, choices=NAME_TYPE, default=TEXT)

    name_text = models.CharField(max_length=20, help_text="Max: 20 symbols", blank=True, null=True)
    name_image_url = models.URLField(blank=True, null=True)
    name_image = models.ImageField(blank=True, null=True)
    alt_text = models.CharField(
        max_length=255, help_text="alt text for image", blank=True, null=True
    )

    description = models.TextField(
        help_text="Max: 250 symbols", validators=[MaxLengthValidator(250)]
    )
    action = models.CharField(max_length=20, help_text="Max: 20 symbols")
    colour = RGBColorField(default="#32B678")
    border_colour = RGBColorField(default="#32B678")
    splash_screen = models.OneToOneField(
        SplashScreen, on_delete=models.CASCADE, blank=True, null=True
    )
    list_order = models.PositiveIntegerField(default=0, help_text="Ascending ordering, 0 be first")

    class Meta:
        verbose_name = "Discover"
        verbose_name_plural = "Discover"
        ordering = ["list_order"]  # noqa: RUF012

    def __str__(self):
        if self.name_text:
            return self.name_text

        return self.description


@reversion.register()
class Cta(models.Model):
    button = models.CharField(max_length=25, help_text="Max: 25 symbols")
    link = models.URLField()

    class Meta:
        verbose_name = "CTA"
        verbose_name_plural = "CTA"

    def __str__(self):
        return f"{self.button} {self.link}"


@reversion.register()
class Carousel(models.Model):
    published = models.BooleanField(default=True)
    title = models.CharField(max_length=50, help_text="Max: 50 symbols")
    message = models.CharField(max_length=255)
    fulltext = models.TextField()
    image = models.ImageField()
    cta = models.OneToOneField(Cta, on_delete=models.SET_NULL, blank=True, null=True)
    list_order = models.PositiveIntegerField(default=0, help_text="Ascending ordering, 0 be first")

    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = "Carousels"

    def __str__(self):
        return self.title
