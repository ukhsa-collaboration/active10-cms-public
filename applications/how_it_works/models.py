import reversion
from django.core.validators import MaxLengthValidator
from django.db import models

from utils.activity import ActivityTypeModel


@reversion.register()
class HowItWorks(ActivityTypeModel):
    title = models.CharField(max_length=20, help_text="Max: 20 symbols")
    description = models.TextField(
        help_text="Max: 200 symbols", validators=[MaxLengthValidator(200)]
    )
    image = models.ImageField()
    list_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "How It Works"
        verbose_name_plural = "How It Works"
        ordering = ["list_order", "id"]

    def __str__(self):
        return self.title
