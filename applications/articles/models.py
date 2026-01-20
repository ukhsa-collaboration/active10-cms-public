import os

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.html import format_html, mark_safe

from applications.views.models import View

from .utils import SubjectOptimizedImageField, path_and_rename_image


class Image(models.Model):
    name = models.CharField(max_length=128, blank=True, default="")
    image = SubjectOptimizedImageField(
        subject_location_field="subject_location",
        upload_to=path_and_rename_image,
        optimized_image_resize_method="width",
        optimized_image_output_size=(1000, 1000),
        help_text="Max 50MB",
    )
    subject_location = models.CharField("subject coords", max_length=8, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        path = "#" if not self.image else os.path.join(self.image.url)
        if path == "#":
            return
        return mark_safe(f'<img src="{path}" style="max-width:120px; max-height: 200px;"/>')

    class Meta:
        ordering = ["name"]  # noqa: RUF012


class ArticleCategory(models.Model):
    name = models.CharField(max_length=256, default="", blank=True)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Article Categories"


class Article(models.Model):
    class Platform(models.TextChoices):
        ALL = "all"
        IOS = "ios"
        ANDROID = "android"

    class ArticleType(models.TextChoices):
        CONTENT = "content"
        CONTAINER = "container"
        LINK = "link"

    # Common part
    published = models.BooleanField(default=False)
    slug = models.CharField(blank=True, max_length=128, help_text="Max 128 characters")
    title = models.CharField(max_length=128, help_text="Max 128 characters")
    description = models.CharField(max_length=512, help_text="Max 512 characters")
    type = models.CharField(max_length=16, default=ArticleType.CONTENT, choices=ArticleType.choices)
    destination_ios = models.CharField(
        blank=True,
        default="",
        max_length=128,
        help_text="Max 128 characters, LINK: url for external website, CONTAINER: view's slug",
    )
    destination_android = models.CharField(
        blank=True,
        default="",
        max_length=128,
        help_text="Max 128 characters, LINK: url for external website, CONTAINER: view's slug",
    )
    content = RichTextField(blank=True, default="")
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, null=True)
    analytics_tag = models.CharField(
        max_length=64, default="", blank=True, help_text="Max 64 characters"
    )
    platform = models.CharField(max_length=7, default=Platform.ALL, choices=Platform.choices)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    button_title = models.CharField(
        max_length=32, default="", blank=True, help_text="Max 32 characters"
    )
    button_analytics_tag = models.CharField(
        max_length=64, default="", blank=True, help_text="Max 64 characters"
    )
    button_url = models.CharField(
        max_length=128, default="", blank=True, help_text="Max 128 characters"
    )
    button_accessibility_label = models.CharField(
        max_length=64, default="", blank=True, help_text="Max 64 characters"
    )

    views = models.ManyToManyField(View, through="ArticleView")

    related_section_title = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        help_text="Max 128 characters",
    )
    related_section_description = models.CharField(
        max_length=256,
        default="",
        blank=True,
        null=True,
        help_text="Max 256 characters",
    )
    related = models.ManyToManyField("self", through="ArticleRelated", symmetrical=False)

    user_group = models.CharField(
        verbose_name="Filter for content to be published for the following user groups",
        max_length=64,
        choices=(
            ("all_users", "All users"),
            ("nhs_users", "NHS users"),
            ("users", "User without NHS account"),
        ),
        default="all_users",
    )

    def __str__(self):
        return self.title

    def get_parent_views(self):
        result = "<br/>".join(
            ("<b>" + v.title + "</b> - " + v.slug + " - " + v.type + "") for v in self.views.all()
        )
        return format_html(result)

    def image_tag(self):
        path = "#" if not self.image else os.path.join(self.image.Image)
        if path == "#":
            return
        return mark_safe(f'<img src="{path}" width="120px"/>')

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
        ordering = ["title"]  # noqa: RUF012


class ArticleRelated(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, related_name="parent_article"
    )
    related_article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, related_name="related_article"
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ""

    class Meta:
        unique_together = ("article", "related_article")
        ordering = ("-order",)
        verbose_name = "Related articles"
        verbose_name_plural = "Related articles"


class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    view = models.ForeignKey(View, on_delete=models.CASCADE, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ""

    class Meta:
        unique_together = ("article", "view")
        ordering = ("-order",)


class ContentView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    view = models.ForeignKey(View, on_delete=models.CASCADE, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.view.title

    class Meta:
        verbose_name = "content view"
        verbose_name_plural = "content views"
        ordering = ["order"]  # noqa: RUF012
