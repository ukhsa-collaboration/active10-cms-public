"""Backfill ``list_order`` so admin drag-and-drop ordering can persist.

Same defect as ``how_it_works.0008_backfill_list_order``: ``list_order`` was added
in 0002 with ``default=0`` and never populated, so every row shares the value 0.
With no distinct values to compare, django-admin-sortable2 sorts descending and
posts 0, -1, -2, ... back, which the ``PositiveIntegerField`` rejects — the error
is swallowed and the changelist reverts on refresh.

Renumbering densely from 1 in the order rows are currently displayed leaves the
visible order untouched and gives the drag handler distinct values to work from.
"""

from django.db import migrations


def backfill_list_order(apps, schema_editor):
    MainTip = apps.get_model('tips', 'MainTip')
    rows = list(MainTip.objects.order_by('list_order', 'id'))
    for order, row in enumerate(rows, start=1):
        row.list_order = order
    MainTip.objects.bulk_update(rows, ['list_order'])


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0008_alter_maintip_options'),
    ]

    operations = [
        # Reverse is a no-op: restoring the all-zero state would only reintroduce the bug.
        migrations.RunPython(backfill_list_order, migrations.RunPython.noop),
    ]
