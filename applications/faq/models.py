import reversion
from django.db import models


@reversion.register()
class Faq(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    list_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.title
