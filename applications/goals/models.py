import reversion
from django.db import models


@reversion.register()
class Goal(models.Model):
    text = models.TextField()
    user = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = "User goal"
        verbose_name_plural = "User goals"
        ordering = ["order"]  # noqa: RUF012

    def __str__(self):
        return f"{self.text[:60]}-{self.user}" if self.user else f"{self.text[:60]}"
