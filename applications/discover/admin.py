from django.contrib import admin
from django.forms import ModelForm, ValidationError

from applications.discover.models import Carousel, Cta, Discover, SplashScreen
from utils.admin import CloneAdminMixin


class DiscoverAdminForm(ModelForm):
    class Meta:
        model = Discover
        fields = "__all__"
        exclude = ["name_image", "name_image_url", "colour", "border_colour"]  # noqa: RUF012

    def clean_name_text(self):
        name_type = self.cleaned_data["name_type"]
        name_text = self.cleaned_data["name_text"]
        if not name_text and name_type == Discover.TEXT:
            raise ValidationError("Set name text or choose another type")
        return name_text

    def clean_name_image_url(self):
        name_type = self.cleaned_data["name_type"]
        name_image_url = self.cleaned_data["name_image_url"]
        if not name_image_url and name_type == Discover.IMAGE_URL:
            raise ValidationError("Set image url or choose another type")
        return name_image_url

    def clean_name_image(self):
        name_type = self.cleaned_data["name_type"]
        name_image = self.cleaned_data["name_image"]
        if not name_image and name_type == Discover.IMAGE:
            raise ValidationError("Set image or choose another type")
        return name_image


class DiscoverAdmin(CloneAdminMixin, admin.ModelAdmin):
    clone_name_field = 'name_text'
    form = DiscoverAdminForm
    autocomplete_fields = ["splash_screen"]  # noqa: RUF012
    search_fields = ["name_text"]  # noqa: RUF012
    list_display = ["name_text", "list_order", "published", "activity_type"]
    list_filter = ["activity_type", "published"]

    def before_save_clone(self, original, clone):
        # splash_screen is a OneToOne, so the copy needs its own SplashScreen.
        if original.splash_screen_id:
            splash_screen = original.splash_screen
            splash_screen.pk = None
            splash_screen.id = None
            splash_screen.save()
            clone.splash_screen = splash_screen


class CarouselAdmin(admin.ModelAdmin):
    fields = [  # noqa: RUF012
        "id",
        "published",
        "title",
        "message",
        "fulltext",
        "image",
        "cta",
        "list_order",
    ]
    readonly_fields = ["id"]  # noqa: RUF012
    autocomplete_fields = ["cta"]  # noqa: RUF012
    search_fields = ["title"]  # noqa: RUF012
    list_display = ["title", "list_order", "published"]  # noqa: RUF012


class SplashScreenAdmin(admin.ModelAdmin):
    search_fields = ["title"]  # noqa: RUF012


class CtaAdmin(admin.ModelAdmin):
    search_fields = ["button"]  # noqa: RUF012


admin.site.register(Discover, DiscoverAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(SplashScreen, SplashScreenAdmin)
admin.site.register(Cta, CtaAdmin)
