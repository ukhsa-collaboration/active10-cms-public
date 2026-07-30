"""Backfill ``list_order`` so admin drag-and-drop ordering can persist.

``list_order`` was added in 0002 with ``default=0`` and never populated, so every
row shares the value 0. django-admin-sortable2 works out its sort direction by
comparing the first and last row's order value; when every value is equal it
settles on *descending* and posts 0, -1, -2, ... back to the server. Those
negatives violate the ``PositiveIntegerField`` constraint, ``update_order``
swallows the error, and the changelist silently reverts on the next refresh.

Renumbering densely from 1 in the order rows are currently displayed leaves the
visible order untouched and gives the drag handler distinct values to work from.
"""

from django.db import migrations


def backfill_list_order(apps, schema_editor):
    HowItWorks = apps.get_model('how_it_works', 'HowItWorks')
    rows = list(HowItWorks.objects.order_by('list_order', 'id'))
    for order, row in enumerate(rows, start=1):
        row.list_order = order
    HowItWorks.objects.bulk_update(rows, ['list_order'])


class Migration(migrations.Migration):

    dependencies = [
        ('how_it_works', '0007_alter_howitworks_options'),
    ]

    operations = [
        # Reverse is a no-op: restoring the all-zero state would only reintroduce the bug.
        migrations.RunPython(backfill_list_order, migrations.RunPython.noop),
    ]
