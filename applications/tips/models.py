import reversion
from django.core.validators import MaxLengthValidator
from django.db import models


@reversion.register()
class MainTip(models.Model):
    published = models.BooleanField(default=True)
    title = models.CharField(max_length=20, help_text="Max: 20 symbols")
    description = models.TextField(
        help_text="Max: 250 symbols", validators=[MaxLengthValidator(250)]
    )
    image = models.ImageField()
    list_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Tip"
        verbose_name_plural = "Tips"

    def __str__(self):
        return self.title
