from ckeditor.fields import RichTextField
from django.db import models


class Legal(models.Model):
    page_type = models.CharField(
        choices=[
            ("terms_and_conditions", "Terms and Conditions"),
            ("accessibility", "Accessibility"),
            ("privacy_policy", "Privacy Policy"),
        ],
        max_length=32,
        null=True,
    )
    title = models.CharField(max_length=128, blank=True, default="")
    content = RichTextField(blank=True, default="")
    should_accept = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
