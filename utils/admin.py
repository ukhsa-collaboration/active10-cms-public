"""Reusable admin helpers shared across content apps.

``CloneAdminMixin`` adds a per-row "Clone" button to a ``ModelAdmin`` changelist.
Clicking it duplicates that row, appends ``" clone"`` to its name field (when the
admin declares one) and, for models that have a ``published`` flag, marks the copy
unpublished. Subclasses override ``before_save_clone`` / ``after_save_clone`` to deep
-clone owned related objects (e.g. a OneToOne target or M2M through-rows).

If the clone can't be saved cleanly — most commonly because appending ``" clone"``
pushes a name past its column limit (``value too long for type character
varying(20)``) — the mixin does not 500. It saves a valid, unpublished draft and then
re-opens that object's change form pre-filled with the *attempted* name, so the
offending field shows its error inline, exactly as if you had clicked Save.
"""

from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError, models, transaction
from django.forms.models import model_to_dict
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.datastructures import MultiValueDict
from django.utils.html import format_html

# Exceptions raised when a clone can't be persisted as-is (e.g. a renamed field
# overflowing its column, or a constraint violation). Any of these routes the user
# to the pre-filled change form rather than a 500.
CLONE_SAVE_ERRORS = (ValidationError, DataError, IntegrityError)


class CloneAdminMixin:
    """Adds a per-row "Clone" button to a ``ModelAdmin``."""

    # Text field to which " clone" is appended on the copy. ``None`` = no rename.
    clone_name_field = None

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if "clone_button" not in list_display:
            list_display.append("clone_button")
        return list_display

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        custom = [
            path(
                "<path:object_id>/clone/",
                self.admin_site.admin_view(self.clone_view),
                name="%s_%s_clone" % info,
            ),
        ]
        return custom + super().get_urls()

    @admin.display(description="Clone")
    def clone_button(self, obj):
        info = self.model._meta.app_label, self.model._meta.model_name
        url = reverse("admin:%s_%s_clone" % info, args=[obj.pk])
        return format_html('<a class="button" href="{}">Clone</a>', url)

    def _url(self, view, args=None):
        info = self.model._meta.app_label, self.model._meta.model_name
        return reverse("admin:%s_%s_%s" % (info[0], info[1], view), args=args)

    def clone_view(self, request, object_id):
        if not self.has_add_permission(request):
            messages.error(request, "You do not have permission to clone this object.")
            return redirect(self._url("changelist"))

        original = get_object_or_404(self.model, pk=object_id)
        try:
            with transaction.atomic():
                clone = self.clone_object(original)
        except CLONE_SAVE_ERRORS as exc:
            return self.clone_error_response(request, original, exc)

        messages.success(request, "Cloned %s (#%s)." % (clone, clone.pk))
        return redirect(self._url("changelist"))

    def clone_object(self, original, rename=True):
        """Duplicate ``original`` and return the saved copy.

        With ``rename=False`` the copy keeps the original name — used to persist a
        valid draft when the renamed version would overflow its column.
        """
        clone = self.model.objects.get(pk=original.pk)
        clone.pk = None
        clone.id = None

        self.before_save_clone(original, clone)

        if rename:
            self.apply_clone_name(clone)

        if hasattr(clone, "published"):
            clone.published = False

        # Validate up front so an over-long rename surfaces as a field-keyed
        # ValidationError (works on any backend) instead of a backend DataError.
        # Skip uniqueness — a clone is expected to duplicate non-unique values.
        clone.full_clean(validate_unique=False)
        clone.save()
        self.after_save_clone(original, clone)
        return clone

    def apply_clone_name(self, clone):
        if self.clone_name_field:
            current = getattr(clone, self.clone_name_field, None)
            if current:
                setattr(clone, self.clone_name_field, "%s clone" % current)

    def before_save_clone(self, original, clone):
        """Hook: adjust ``clone`` before it is saved (e.g. dup a OneToOne target)."""

    def after_save_clone(self, original, clone):
        """Hook: copy related rows once ``clone`` has a pk (e.g. M2M through-rows)."""

    # --- graceful failure handling -------------------------------------------------

    def clone_error_response(self, request, original, exc):
        """Save a valid draft, then re-open its change form with the attempted name.

        The change form renders bound and invalid, so the offending field shows its
        error inline — the same UI as submitting the create/edit form with bad data.
        """
        with transaction.atomic():
            clone = self.clone_object(original, rename=False)

        # Inline formsets would need their own management-form data to replay a POST;
        # rather than risk corrupting them, fall back to a clear banner for admins
        # that declare inlines. (The realistic overflow cases have no inlines.)
        if self.get_inline_instances(request, clone):
            messages.error(request, self._clone_error_message(exc))
            return redirect(self._url("change", args=[clone.pk]))

        return self._render_change_form_with_attempted_name(request, original, clone)

    def _render_change_form_with_attempted_name(self, request, original, clone):
        post = self._clone_form_data(clone)
        if self.clone_name_field:
            current = getattr(original, self.clone_name_field, None)
            if current:
                post[self.clone_name_field] = "%s clone" % current

        # Replay the change form as a POST so it binds, validates and shows inline
        # errors. ``FILES`` is a read-only property, so set the backing attributes
        # directly. Called directly (not via the URL) it isn't CSRF-wrapped, but
        # changeform_view is — opt this synthetic request out of the CSRF check.
        request.method = "POST"
        request._post = post
        request._files = MultiValueDict()
        request._dont_enforce_csrf_checks = True
        return self.change_view(request, str(clone.pk))

    def _clone_form_data(self, clone):
        """A POST-style QueryDict of ``clone``'s values for the admin change form.

        File fields are omitted so the saved file is kept (and not re-required), and
        unchecked booleans are simply absent — matching how a browser submits a form.
        """
        file_fields = {
            f.name for f in self.model._meta.get_fields()
            if isinstance(f, models.FileField)
        }
        data = QueryDict(mutable=True)
        for name, value in model_to_dict(clone, exclude=list(file_fields)).items():
            if value is None or value == "":
                continue
            if isinstance(value, (list, tuple)):  # M2M -> list of pks
                data.setlist(name, [str(getattr(v, "pk", v)) for v in value])
            elif isinstance(value, bool):
                if value:
                    data[name] = "on"
            else:
                data[name] = str(value)
        return data

    @staticmethod
    def _clone_error_message(exc):
        if isinstance(exc, ValidationError):
            return "Could not rename the clone: %s" % "; ".join(exc.messages)
        return "Could not save the clone: %s" % exc
