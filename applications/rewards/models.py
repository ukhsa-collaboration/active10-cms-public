import reversion
from django.core.validators import MaxLengthValidator
from django.db import models


@reversion.register()
class Reward(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=250, help_text="Max: 250 symbols")
    category = models.CharField(max_length=250, help_text="Max: 250 symbols")
    slug = models.CharField(max_length=250, help_text="Max: 250 symbols")
    text = models.TextField(
        help_text="Text (2000 chars max)", validators=[MaxLengthValidator(2000)]
    )
    on_image = models.ImageField()
    off_image = models.ImageField()
    animation = models.FileField()
    how_to = models.TextField(
        help_text="Text (2000 chars max)", validators=[MaxLengthValidator(2000)]
    )
    share = models.TextField(
        blank=True,
        default=None,
        null=True,
        help_text="Text (2000 chars max)",
        validators=[MaxLengthValidator(2000)],
    )
    position = models.IntegerField(blank=True, default=1)

    class Meta:
        verbose_name = "Reward"
        verbose_name_plural = "Rewards"

        constraints = [models.UniqueConstraint(fields=["slug"], name="unique slug")]  # noqa: RUF012

    def __str__(self):
        return f"{self.title}"
