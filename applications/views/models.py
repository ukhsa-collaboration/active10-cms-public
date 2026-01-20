from tempfile import NamedTemporaryFile

from django.core import files
from django.db import models
from django.utils.html import format_html
from requests import codes, get

from utils import path_and_rename_image, validate_image_extension

VIEW_TYPE = [
    "root_page",
    "carousel_small_items",
    "carousel_double_items",
    "carousel_large_items",
    "carousel_goals",
    "hero_item",
    "article_list",
    "article_list_small_items",
    "popup",
]


class View(models.Model):
    type = models.CharField(
        choices=[(item, item) for item in VIEW_TYPE],
        max_length=100,
        default=VIEW_TYPE[0],
    )
    slug = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True, default="")
    analytics_tag = models.CharField(blank=True, null=True, default="", max_length=128)
    version = models.IntegerField(default=0)

    articles = models.ManyToManyField("articles.Article", through="articles.ArticleView")
    views = models.ManyToManyField("View", through="ViewsRelation")

    def get_child_articles(self):
        result = "<br/>".join(
            ("<b>" + v.title + "</b> - " + v.slug + " - " + v.type + "")
            for v in self.articles.all()
        )
        return format_html(result)

    def get_child_views(self):
        result = "<br/>".join(
            ("<b>" + v.title + "</b> - " + v.slug + " - " + v.type + "") for v in self.views.all()
        )
        return format_html(result)

    def __str__(self):
        return "%s - (%s)" % (self.title, self.slug)  # noqa: UP031

    class Meta:
        ordering = ["title"]  # noqa: RUF012


class ViewsRelation(models.Model):
    parent = models.ForeignKey(View, on_delete=models.CASCADE, null=True, related_name="parents")
    child = models.ForeignKey(View, on_delete=models.CASCADE, null=True, related_name="children")
    order = models.PositiveIntegerField(default=0)
    alternative_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ""

    class Meta:
        unique_together = ("parent", "child")
        ordering = ("-order",)


class ViewMedia(models.Model):
    type = models.CharField(max_length=256)
    tag = models.CharField(max_length=256)
    url = models.FileField(
        upload_to=path_and_rename_image,
        validators=[validate_image_extension],
        blank=True,
    )
    resource_id = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    view = models.ForeignKey(View, related_name="view_media", on_delete=models.CASCADE)

    @staticmethod
    def import_from_json(item, view):
        response = get(item["url"], stream=True)

        if response.status_code != codes.ok:
            return

        file_name = item["url"].split("/")[-1]

        lf = NamedTemporaryFile()  # noqa: SIM115

        for block in response.iter_content(1024 * 8):
            if not block:
                break

            lf.write(block)

        view_media = ViewMedia()

        view_media.type = item["type"]
        view_media.tag = item["tag"]
        view_media.resource_id = item["resourceId"]
        view_media.label = item["label"]
        view_media.view_id = view.id
        view_media.url.save(file_name, files.File(lf))

        return view_media


class ViewProperty(models.Model):
    key = models.CharField(max_length=256)
    value = models.TextField(blank=True)
    view = models.ForeignKey(View, related_name="view_property", on_delete=models.CASCADE)
