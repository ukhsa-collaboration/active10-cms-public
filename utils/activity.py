"""Routine-type ("activity") tagging shared across content apps.

Lets publishers tag each content piece as a Walking journey, a Wheeling journey,
or both. The API filters content by a request's ``activity_type`` query param so
the walking and wheeling versions of the app each get the right subset.

Mirrors the existing ``Article.user_group`` query-param + cascade pattern in
``applications/articles``.
"""

from django.db import models

# Query param the app passes to choose its journey, e.g. ?activity_type=wheeling
ACTIVITY_QUERY_PARAM = "activity_type"


class ActivityType(models.TextChoices):
    WALKING = "walking", "Walking journey"
    WHEELING = "wheeling", "Wheeling journey"
    BOTH = "both", "Walking and Wheeling"


class ActivityTypeModel(models.Model):
    """Abstract base adding an ``activity_type`` tag to a content model.

    Default is ``walking`` so existing rows keep showing on the current (walking)
    app, which sends no query param.
    """

    activity_type = models.CharField(
        verbose_name="Activity type",
        max_length=16,
        choices=ActivityType.choices,
        default=ActivityType.WALKING,
        help_text="Which app journey shows this content. 'Both' shows on walking and wheeling.",
    )

    class Meta:
        abstract = True


def resolve_activity(request):
    """Return the journey a request is asking for.

    Defaults to ``walking`` when the param is missing or not a concrete journey,
    so the live walking app (which sends no param) is unaffected.
    """
    value = request.query_params.get(ACTIVITY_QUERY_PARAM, ActivityType.WALKING)
    if value not in (ActivityType.WALKING, ActivityType.WHEELING, ActivityType.BOTH):
        value = ActivityType.WALKING
    return value


def filter_by_activity(queryset, activity):
    """Filter to rows for ``activity`` plus the ``both`` rows (the cascade).

    When ``activity`` is ``both``, the request wants the full catalogue, so all
    activity types (walking, wheeling and both) are returned.
    """
    if activity == ActivityType.BOTH:
        return queryset
    return queryset.filter(activity_type__in=[activity, ActivityType.BOTH])


def pick_by_activity(queryset, activity):
    """Pick the single record best matching ``activity``.

    For singleton-style content (onboarding) where exactly one record should be
    served. Prefers an exact-activity record, then a ``both`` record, then falls
    back to ``walking`` and finally any record, so the endpoint never returns
    empty just because a wheeling-specific record hasn't been authored yet.
    """
    for candidate in (activity, ActivityType.BOTH, ActivityType.WALKING):
        obj = queryset.filter(activity_type=candidate).first()
        if obj is not None:
            return obj
    return queryset.first()
