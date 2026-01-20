import reversion
from django.db import models
from reversion.models import Revision


class VersionsSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    revision = models.OneToOneField(Revision, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Version"
        verbose_name_plural = "Versions"

    def __str__(self):
        return self.name

    def revert(self):
        """
        method used for reverting data
        :return:
        """
        # delete all objects
        self._delete_old_objects()
        # restore saved objects
        self.revision.revert(delete=False)

    @staticmethod
    def _get_objects(model):
        return model.objects.iterator()

    @staticmethod
    def _delete_old_objects():
        for model in reversion.get_registered_models():
            model.objects.all().delete()

    def _create_revisions(self):
        with reversion.create_revision(atomic=True):
            reversion.set_comment(self.name)
            for model in reversion.get_registered_models():
                for obj in self._get_objects(model):
                    reversion.add_to_revision(obj, model_db=None)

    def _get_revision(self):
        return Revision.objects.get(comment=self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.revision:
            self._create_revisions()
            self.revision = self._get_revision()
        return super(VersionsSet, self).save(  # noqa: UP008
            force_insert=False, force_update=False, using=None, update_fields=None
        )
