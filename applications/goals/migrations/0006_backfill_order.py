"""Backfill ``order`` so admin drag-and-drop ordering can persist.

Same defect as ``how_it_works.0008_backfill_list_order``, on ``Goal.order``: every
row shares the default value 0, so django-admin-sortable2 has no distinct values to
derive a sort direction from, settles on descending, and posts 0, -1, -2, ... back.
The ``PositiveIntegerField`` rejects the negatives, ``update_order`` swallows the
error, and the changelist reverts on refresh.

Renumbering densely from 1 in the order rows are currently displayed leaves the
visible order untouched and gives the drag handler distinct values to work from.
"""

from django.db import migrations


def backfill_order(apps, schema_editor):
    Goal = apps.get_model('goals', 'Goal')
    rows = list(Goal.objects.order_by('order', 'id'))
    for order, row in enumerate(rows, start=1):
        row.order = order
    Goal.objects.bulk_update(rows, ['order'])


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_goal_activity_type'),
    ]

    operations = [
        # Reverse is a no-op: restoring the all-zero state would only reintroduce the bug.
        migrations.RunPython(backfill_order, migrations.RunPython.noop),
    ]
