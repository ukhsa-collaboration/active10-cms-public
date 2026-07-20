# Populate wheelchair_text on existing My Walks / Today"s walks dynamic-text
# rows (RPE Supplementary App Content). Only updates rows that already exist
# (prod/staging); fresh databases get this content from fixtures.json instead.
from django.db import migrations

# condition -> wheeling variant. Conditions not listed are generic and keep an
# empty wheelchair_text (the app falls back to `text`).
MY_WALK_WHEELCHAIR_TEXT = {
    "weeks_days_2_3": (
        "You hit your target on %d days this week. Try to increase more of "
        "your wheeling to brisk in order to stay on track."
    ),
    "weeks_days_1": (
        "You hit your target on 1 day this week. Try to increase more of "
        "your wheeling to brisk in order to stay on track."
    ),
    "days_no_brisk_walking": (
        "Struggling to fit in brisk wheeling? Check our tips for some helpful guidance"
    ),
    "days_target_no_hit": (
        "You didn"t quite hit your target but you"ve still clocked up %d mins "
        "of brisk wheeling!"
    ),
}

TARGET_WHEELCHAIR_TEXT = {
    "0_a10s_0_mins": "Let's get brisk wheeling to achieve an Active 10",
}


def set_wheelchair_text(apps, schema_editor):
    MyWalk = apps.get_model("my_walks", "MyWalk")
    Target = apps.get_model("my_walks", "Target")

    for condition, text in MY_WALK_WHEELCHAIR_TEXT.items():
        MyWalk.objects.filter(condition=condition).update(wheelchair_text=text)

    for condition, text in TARGET_WHEELCHAIR_TEXT.items():
        Target.objects.filter(condition=condition).update(wheelchair_text=text)


class Migration(migrations.Migration):

    dependencies = [
        ("my_walks", "0005_mywalk_wheelchair_text_target_wheelchair_text"),
    ]

    operations = [
        migrations.RunPython(set_wheelchair_text, reverse_code=migrations.RunPython.noop),
    ]
